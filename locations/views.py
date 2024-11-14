import json
import urllib
import wikipediaapi
import folium
from folium.plugins import MarkerCluster

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.db.models import Q

from notes.models import Reference
from mainmenu.views import pagination

# from ukheritage.views import map_points

from .forms import *
from .models import *
from .utils import *


def index(request):
    return render(request, "locations/index.html")


def routes_southern(request):
    return render(request, "locations/routes_southern.html")


def locations(request):
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, fallback to form data otherwise
    if request.method == "POST":
        selection_criteria = LocationSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty
        form_data = request.session.get("selection_criteria", None)
        selection_criteria = LocationSelectionForm(form_data)

    # Default to all records if no valid selection criteria
    queryset = Location.objects.order_by("name")

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors
    else:
        query = Q()
        name_query = selection_criteria.cleaned_data.get("name", "")
        categories_query = selection_criteria.cleaned_data.get("categories", "")

        if name_query:
            query &= Q(name__icontains=name_query)

        if categories_query:
            query &= Q(categories__category__icontains=categories_query.category)

        queryset = Location.objects.filter(query).distinct().order_by("name")

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "locations/locations.html", context)


def location(request, location_id):
    location = Location.objects.get(id=location_id)
    categories = location.categories.all()
    posts = location.posts.all()
    references = location.references.all()

    sql = """ 
    SELECT ST_Y(ST_CENTROID(a.geometry)) AS st_y, 
           ST_X(ST_CENTROID(a.geometry)) AS st_x, 
           a.name
    FROM 
    public."locations_location" AS a
    WHERE a.id = %s;
    """
    coords = execute_sql(sql, [location_id])
    y_coord = coords[0].get("st_y")
    x_coord = coords[0].get("st_x")
    location_name = coords[0].get("name")
    if y_coord and x_coord:
        map_html = folium_map_location(y_coord, x_coord, None)
    else:
        map_html = None

    nls_url = f"https://maps.nls.uk/geo/explore/print/#zoom=17&lat={y_coord}&lon={x_coord}&layers=168&b=5"
    nls_url_1944_1973 = f"https://maps.nls.uk/geo/explore/print/#zoom=17&lat={y_coord}&lon={x_coord}&layers=173&b=5"

    context = {
        "posts": posts,
        "location": location,
        "categories": categories,
        "map": map_html,
        "title": location_name,
        "nls_url": nls_url,
        "nls_url_1944_1973": nls_url_1944_1973,
        "references": references,
    }
    return render(request, "locations/location.html", context)


def location_map(request, location_id):
    sql = """ 
    SELECT ST_Y(ST_CENTROID(a.geometry)) AS st_y, 
           ST_X(ST_CENTROID(a.geometry)) AS st_x, 
           a.name
    FROM 
    public."locations_location" AS a
    WHERE a.id = %s;
    """
    coords = execute_sql(sql, [location_id])

    y_coord = coords[0].get("st_y")
    x_coord = coords[0].get("st_x")
    map_html = folium_map_location(y_coord, x_coord, None)
    # map_html = map._repr_html_()
    location_name = coords[0].get("name")

    nls_url = f"https://maps.nls.uk/geo/explore/print/#zoom=16&lat={y_coord}&lon={x_coord}&layers=168&b=5"

    if coords:
        context = {
            "map": map_html,
            "title": location_name,
            "nls_url": nls_url,
        }
    else:
        context = {"map": None, "title": f"{location_name} Location not found"}

    return render(request, "locations/folium_map.html", context)


def routes(request):
    map_html = None
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, fallback to form data otherwise
    if request.method == "POST":
        selection_criteria = RouteSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["route_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty
        form_data = request.session.get("route_selection_criteria", None)
        selection_criteria = RouteSelectionForm(form_data)

    # Default to all routes if no valid selection criteria
    queryset = Route.objects.all().order_by("name")

    if selection_criteria.is_valid():
        cleandata = selection_criteria.cleaned_data
        query = Q()

        if "name" in cleandata and cleandata["name"]:
            query &= Q(name__icontains=cleandata["name"])
        if "owner_operators" in cleandata and cleandata["owner_operators"]:
            query &= Q(owneroperators=cleandata["owner_operators"].pk)
        if "categories" in cleandata and cleandata["categories"]:
            query &= Q(categories=cleandata["categories"])

        # Filter the queryset only if query conditions are set
        if query:
            queryset = Route.objects.filter(query).distinct().order_by("name")
    else:
        errors = selection_criteria.errors

    # Check for "map" action if requested
    if "action" in request.GET and request.GET.get("action") == "map":
        elr_geojsons, locations = routes_mapdata_extract(queryset)
        if locations or elr_geojsons:
            map_html = folium_map_geojson(elr_geojsons, locations)

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "map": map_html,
    }
    return render(request, "locations/routes.html", context)


def route(request, slug):

    route = Route.objects.get(slug=slug)
    references = route.references.all
    elrs = route.elrs.all
    posts = route.posts.all

    events_json = None
    if route_events := LocationEvent.objects.filter(route_fk_id=route.id):
        events_json = events_timeline(route_events)

    context = {
        "route": route,
        "elrs": elrs,
        "posts": posts,
        "references": references,
        "timeline_json": events_json,
    }
    return render(request, "locations/route.html", context)


def route_map(request, slug):

    route = Route.objects.get(slug=slug)
    elrs = route.elrs.all
    routes = [route]

    elr_geojsons, locations = routes_mapdata_extract(routes)
    map_html = None
    if locations or elr_geojsons:
        map_html = folium_map_geojson(elr_geojsons, locations)

    context = {
        "map": map_html,
        "route": route,
        "elrs": elrs,
        "title": route.name,
    }
    return render(request, "locations/folium_map.html", context)


def route_timeline(request, slug):

    route = Route.objects.get(slug=slug)
    elrs = route.elrs.all
    routes = [route]

    elr_geojsons, locations = routes_mapdata_extract(routes)
    map_html = None
    if locations or elr_geojsons:
        map_html = folium_map_timeline(elr_geojsons, locations)

    context = {
        "map": map_html,
        "route": route,
        "elrs": elrs,
        "title": route.name,
    }
    return render(request, "locations/folium_map.html", context)


def events_timeline(events_in):
    events_out = []
    count = 0

    for event in events_in:
        if event.datefield:
            count += 1
            # https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {
                "id": count,
                "content": event.description,
                "start": event.datefield.strftime("%Y/%m/%d"),
                "event.type": "point",
            }
            events_out.append(event)

    return json.dumps(events_out)


def route_storymap(request, slug):

    from storymaps.views import get_wikipage_html

    storymap_json = None
    route = Route.objects.get(slug=slug)

    if (
        routemaps := route.wikipedia_routemaps.all()
    ):  # i.e. If the route has any wikipedia routemaps
        sql = """
            SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."name",
                ST_Y(ST_CENTROID(a.geometry)),
                ST_X(ST_CENTROID(a.geometry)),
                a."media_caption",
                a."media_credit",
                a."media_url"
            FROM "locations_location" AS a
            INNER JOIN "locations_routelocation" AS b
                ON (a."id" = b."location_fk_id")
            WHERE a."geometry" IS NOT NULL AND b."routemap_id" = %s
            ORDER BY b."loc_no";
        """

        if slide_locations := execute_sql(sql, [routemaps[0].id]):
            header_title = route.name or None
            wikislug = route.wikipedia_slug or None

            # If the route has notes, show these on the first page, otherwise show the wikipage
            if route.notes:
                header_text = route.notes
            else:
                pagename = route.wikipedia_slug.replace("_", " ")
                wikipage = urllib.parse.unquote(
                    pagename, encoding="utf-8", errors="replace"
                )

                wiki_wiki = wikipediaapi.Wikipedia(
                    language="en",
                    user_agent="prpfr3/Github TPAM",
                    extract_format=wikipediaapi.ExtractFormat.HTML,
                )

                # VARIANTS FOR THE TEXT TO APPEAR ON THE STORYMAP FRONT PAGE
                # This variant gets only the text up to the Notes or References section
                if wiki_wiki.page(wikipage).exists:
                    text_array = wiki_wiki.page(wikipage).text.split("<h2>Notes</h2>")
                    header_text = text_array[0].split("<h2>References</h2>")

                # This variant gets only the summary text
                if wiki_wiki.page(wikipage).exists:
                    header_text = wiki_wiki.page(wikipage).summary

                # This variant gets the routemap template page rather than the route page
                routemaps = route.wikipedia_routemaps.all()
                url = f"https://en.wikipedia.org/wiki/Template:{str(routemaps[0])}"
                header_text = get_wikipage_html(url)

                # This variant gets all the html
                url = f"https://en.wikipedia.org/wiki/{wikipage}"
                header_text = get_wikipage_html(url)

            storymap_json = generate_storymap(
                header_title, header_text, slide_locations
            )

            # Specify the file path where you want to save the JSON file
            output_file_path = (
                "D:\OneDrive\Source\FE Projects\BRMTimeline\\bluebell_storymap.json"
            )

            # Write the storymap_json to the JSON file
            # with open(output_file_path, "w") as json_file:
            #     json_file.write(json.dumps(storymap_json, indent=2))

    return render(request, "locations/storymap.html", {"storymap_json": storymap_json})


class ClosedLinesRegionSelectView(RegionSelectView):
    redirect_view_name = "locations:map_closed_lines"


class RegionalMapSelectView(RegionSelectView):
    redirect_view_name = "locations:regional_map"


def regional_map(request, geo_area):

    # Calculate the boundary box from the Region Geometry
    sql = """SELECT ST_XMin(geometry), ST_YMin(geometry), ST_XMax(geometry), ST_YMax(geometry),
    ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry))
    FROM public."locations_ukarea" WHERE "ITL121NM" = %s;"""
    ukarea_bounds = execute_sql(sql, [geo_area])
    west = ukarea_bounds[0]["st_xmin"]
    south = ukarea_bounds[0]["st_ymin"]
    east = ukarea_bounds[0]["st_xmax"]
    north = ukarea_bounds[0]["st_ymax"]

    sql = """
    SELECT 
        *
    FROM
        public."locations_elr" AS a 
    JOIN
        (SELECT ST_MakeEnvelope(%s, %s, %s, %s, 4326) AS geometry) AS b
    ON
        ST_Within(a.geometry, b.geometry);
    """

    sql = """
    SELECT 
        *
    FROM
        public."locations_elr" AS a 
    JOIN
        (SELECT ST_MakeEnvelope(%s, %s, %s, %s, 4326) AS geometry) AS b
    ON
        ST_Within(ST_GeomFromGeoJSON(a.geojson), b.geometry);
    
    """

    # elrs = execute_sql(sql, [west, south, east, north])

    elr_geojsons = None

    # for elr in elrs:
    #     try:
    #         if elr["geojson"]:
    #             if elr_geojsons is None:
    #                 elr_geojsons = []
    #             geojson = json.loads(elr["geojson"])
    #             elr_geojsons.append(geojson)
    #     except Exception as e:
    #         print(f"Error {e}")

    locations = None

    sql = """
    SELECT 
        a."wikiname", a."wikislug", a."opened", a."closed", a."name",
        ST_Y(ST_CENTROID(a.geometry)),
        ST_X(ST_CENTROID(a.geometry)),
        a."media_url"
    FROM
        public."locations_location" AS a 
    JOIN
        (SELECT ST_MakeEnvelope(%s, %s, %s, %s, 4326) AS geometry) AS b
    ON
        ST_Intersects(a.geometry, b.geometry);
    """

    # FOR THE WHOLE COUNTRY
    # sql = """
    # SELECT
    #     a."wikiname", a."wikislug", a."opened", a."closed", a."name",
    #     ST_Y(ST_CENTROID(a.geometry)),
    #     ST_X(ST_CENTROID(a.geometry)),
    #     a."media_url"
    # FROM
    #     public."locations_location" AS a
    # """

    locations = execute_sql(sql, [west, south, east, north])

    if locations or elr_geojsons:
        map_html = folium_map_timeline(elr_geojsons, locations)

    title = f"UK {geo_area} Region"
    context = {"map": map_html, "title": title}
    return render(request, "locations/folium_map.html", context)


def elrs(request):
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, or use empty data on first load
    if request.method == "POST":
        selection_criteria = ELRSelectForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["elr_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("elr_selection_criteria", None)
        selection_criteria = ELRSelectForm(form_data)

    # Default queryset for all ELRs
    queryset = ELR.objects.only("itemLabel", "itemAltLabel")

    if selection_criteria.is_valid():
        # Build the queryset based on valid selection criteria
        queryset = elrs_query_build(selection_criteria.cleaned_data)
    else:
        errors = selection_criteria.errors

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "locations/elrs.html", context)


def elrs_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "itemAltLabel" in cleandata and cleandata["itemAltLabel"]:
        conditions &= Q(itemAltLabel__icontains=cleandata["itemAltLabel"])

    if "itemLabel" in cleandata and cleandata["itemLabel"]:
        conditions &= Q(itemLabel__icontains=cleandata["itemLabel"])

    queryset = ELR.objects.filter(conditions).only("itemLabel", "itemAltLabel")

    return queryset


def elr_map(request, elr_id):
    elr = ELR.objects.get(id=elr_id)

    if elr.geojson and len(elr.geojson["features"]) > 0:
        elr_geojsons = []
        elr_geojsons.append(elr.geojson)

        sql = """
        SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."name",
        ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), a."media_url", b."itemAltLabel", b."itemLabel"
        FROM "locations_location" AS a
        INNER JOIN "locations_elrlocation" AS c ON a."id" = c."location_fk_id"
        INNER JOIN "locations_elr" AS b ON c."elr_fk_id" = b."id"
        WHERE b."id" = %s;
        """
        locations = execute_sql(sql, [elr_id])

        title = f"{elr.itemAltLabel}: {elr.itemLabel}"
        map_html = folium_map_geojson(elr_geojsons, locations)
    else:
        map_html = None
        title = None

    context = {"map": map_html, "title": title}
    return render(request, "locations/folium_map.html", context)


def elr_storymap(request, elr_id):
    elr = ELR.objects.get(id=elr_id)

    sql = """ 
    SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."name",
        ST_Y(ST_CENTROID(a.geometry)), 
        ST_X(ST_CENTROID(a.geometry)),
        a."media_caption",
        a."media_credit",
        a."media_url",
        c."distance"
    FROM "locations_location" AS a 
    INNER JOIN "locations_elrlocation" AS c ON a."id" = c."location_fk_id"
    INNER JOIN "locations_elr" AS b ON c."elr_fk_id" = b."id"
    WHERE b."id" = %s
    ORDER BY c."distance";
    """
    storymap_json = None

    if slide_locations := execute_sql(sql, [elr_id]):
        header_title = f"{elr.itemAltLabel}: {elr.itemLabel}"

        # If the elr has some notes
        header_text = ""
        storymap_json = generate_storymap(header_title, header_text, slide_locations)
    return render(request, "locations/storymap.html", {"storymap_json": storymap_json})


def elr_display_osmdata(request, elr_id):
    # This function was intended to strip out all the coordinates on an ELR from the geojson linestrings and sort them into order to form a single linestring. However, this tends not to work as an ELR may have a branch, making it impossible for the maths functions to know which is the next coordinate to the current one (as there are two). Also an ELR may have an error in the Geodata such as the WCML from Euston which has a linestring around Oxford.

    import math

    elr = ELR.objects.get(id=elr_id)

    elr_geojsons = [osm_elr_fetch(elr.itemAltLabel, None)]
    elr_geojson = elr_geojsons[0]

    # Extracting line geometries from the GeoJSON features
    extracted_coords_list = []
    for feature in elr_geojson["features"]:
        for coordinate_pair in feature["geometry"]["coordinates"]:
            # for coordinate_pair in geojson_coordinate_list:
            extracted_coords_list.append(coordinate_pair)

    # print(extracted_coords_list)

    # Haversine distance calculation function
    def distance(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371  # Radius of Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # Function to calculate the distance range in km for latitudes and longitudes
    def get_coordinate_ranges(coords):
        longitudes = [coord[0] for coord in coords]
        latitudes = [coord[1] for coord in coords]

        lon_range_deg = max(longitudes) - min(longitudes)
        lat_range_deg = max(latitudes) - min(latitudes)

        # Convert latitude range to kilometers (1 degree latitude ≈ 111 km)
        lat_range_km = lat_range_deg * 111

        # Find average latitude to compute distance of 1 degree longitude in kilometers
        avg_latitude = sum(latitudes) / len(latitudes)
        lon_range_km = lon_range_deg * 111 * math.cos(math.radians(avg_latitude))

        return lon_range_km, lat_range_km

    # Rough sorting by the axis with the largest range in km
    def rough_sort(coords):
        lon_range, lat_range = get_coordinate_ranges(coords)

        if lon_range > lat_range:
            # Sort by longitude if its distance range is greater
            return sorted(coords, key=lambda x: x[0])
        else:
            # Otherwise, sort by latitude
            return sorted(coords, key=lambda x: x[1])

    # Nearest-neighbor sorting with a rough sort first
    def sort_by_proximity(coords):
        # Step 1: Rough sort by the axis with the largest range in distance (km)
        coords = rough_sort(coords)

        # Step 2: Nearest-neighbor sorting
        sorted_coords = [coords.pop(0)]  # Start from the first coordinate
        while coords:
            last_point = sorted_coords[-1]
            next_point = min(coords, key=lambda x: distance(last_point, x))
            sorted_coords.append(next_point)
            coords.remove(next_point)

        return sorted_coords

    # Sort the coordinates by proximity
    sorted_coords = sort_by_proximity(extracted_coords_list)

    geojson_feature = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": sorted_coords},
        "properties": {},
    }

    output_file = "modified_geojson.txt"
    with open(output_file, "w") as file:
        json.dump(geojson_feature, file, separators=(",", ":"))

    title = f"{elr.itemAltLabel}: {elr.itemLabel}"

    features = [
        geojson_feature
    ]  # The webpage expects a list of features whereas we have just one here which we put in a list

    context = {"elr_geojson": features, "title": title}
    return render(request, "locations/elr_display_osmdata.html", context)


def elr_history(request, elr_id):
    # Function under development. Aims to show route sections over time
    elr = ELR.objects.get(id=elr_id)

    route_sections = RouteSection.objects.filter(routesectionelr__elr_fk=elr)

    if elr.geojson and len(elr.geojson["features"]) > 0:
        elr_geojsons = []
        elr_geojsons.append(elr.geojson)

        sql = """
        SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."name",
        ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), a."media_url", b."itemAltLabel", b."itemLabel"
        FROM "locations_location" AS a
        INNER JOIN "locations_elrlocation" AS c ON a."id" = c."location_fk_id"
        INNER JOIN "locations_elr" AS b ON c."elr_fk_id" = b."id"
        WHERE b."id" = %s;
        """
        locations = execute_sql(sql, [elr_id])

        title = f"{elr.itemAltLabel}: {elr.itemLabel}"
        map_html = folium_map_geojson(elr_geojsons, locations)
    else:
        map_html = None
        title = None

    context = {"map": map_html, "title": title}
    return render(request, "locations/folium_historymap.html", context)


class HeritageSiteListView(ListView):
    model = HeritageSite
    queryset = HeritageSite.objects.order_by("country", "type", "name").exclude(
        name="N/A"
    )


def heritage_site(request, heritage_site_id):
    heritage_site = HeritageSite.objects.get(id=heritage_site_id)
    context = {"heritage_site": heritage_site}
    return render(request, "locations/heritage_site.html", context)


class VisitListView(ListView):
    model = Visit


@login_required
def visit(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    images = Reference.objects.filter(visit=visit_id).order_by("id")
    paginator = Paginator(images, 20)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)

    context = {"visit": visit, "images": images}
    return render(request, "maps/visit.html", context)


# class MapClosedLines(TemplateView):

#     template_name = "locations/folium_map.html"

#     def get_context_data(self, **kwargs):
#         geo_area = self.kwargs["geo_area"]

#         sql = """SELECT ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry)) FROM public."locations_ukarea" WHERE "ITL121NM" = %s;"""
#         centroid = execute_sql_nofieldnames(sql, [geo_area])

#         basemap = folium.Map(
#             centroid[0],
#             zoom_start=10,
#             tiles="cartodb positron",
#             prefer_canvas=True,
#             height=500,
#         )
#         marker_cluster = MarkerCluster().add_to(basemap)

#         sql = """
#         SELECT a."name", NULL, ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."locations_routes_geo_closed" AS a JOIN public."locations_ukarea" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b."ITL121NM" = %s ;
#         """
#         results = execute_sql_nofieldnames(sql, [geo_area])

#         map_points(results, marker_cluster, basemap)

#         figure = folium.Figure()
#         basemap.add_to(figure)
#         figure.render()
#         return {"map": figure, "title": geo_area}


# def calculate_centroid(coordinates):
#     total_x = total_y = 0
#     num_points = len(coordinates)

#     # Calculate the centroid using the mean of x and y coordinates
#     for point in coordinates:
#         total_x += point[0]
#         total_y += point[1]

#     centroid_x = total_x / num_points
#     centroid_y = total_y / num_points

#     return centroid_x, centroid_y


class Trackmap(TemplateView):
    template_name = "locations/folium_map.html"

    def get_context_data(self, **kwargs):

        file = "D:\Data\TPAM\ElhamValleyRailway.geojson"

        try:
            with open(file, "r") as f:
                geojson_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
        except Exception as e:
            print("An error occurred while loading the GeoJSON file:", e)

        # Accumulate LineString coordinates
        line_coordinates = []

        # Iterate over features
        for feature in geojson_data["features"]:
            if feature["geometry"]["type"] == "LineString":
                line_coordinates.extend(feature["geometry"]["coordinates"])

        # Calculate centroid for all LineString features combined
        centroid_x, centroid_y = calculate_centroid(line_coordinates)

        m = folium.Map(
            [centroid_y, centroid_x],
            height=500,
            zoom_start=12,
            prefer_canvas=True,
        )

        folium.TileLayer("openstreetmap", name="OpenStreet Map").add_to(m)

        folium.TileLayer(
            "http://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
            attr='<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, \
            Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> \
            <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
            min_zoom=12,
            max_zoom=19,
        ).add_to(m)

        # Iterate over features
        for feature in geojson_data["features"]:
            geometry = feature.get("geometry")
            properties = feature.get("properties")

            # Check if geometry and properties are not None
            if geometry and properties:
                feature_name = properties.get("name") or None

            # Add GeoJson with popup if feature_id is not None
            if geometry:
                folium.GeoJson(data=geometry, tooltip=feature_name).add_to(m)

        figure = folium.Figure()
        m.add_to(figure)
        figure.render()
        return {"map": figure, "title": f"Map of file {file}"}
