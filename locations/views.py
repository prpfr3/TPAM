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
    letter = request.GET.get(
        "letter", "A"
    ).upper()  # Get the selected letter, default to 'A'
    selection_criteria = LocationSelectionForm(request.GET or None)

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    # Base queryset filtered by the letter
    queryset = Location.objects.filter(name__istartswith=letter).order_by("name")
    # queryset = Location.objects.order_by("name")

    query = Q()

    if selection_criteria.is_valid():
        name_query = selection_criteria.cleaned_data.get("name", "")
        categories_query = selection_criteria.cleaned_data.get("categories", "")

        if name_query:
            query &= Q(name__icontains=name_query)

        if categories_query:
            query &= Q(
                categories__name__icontains=categories_query
            )  # Assuming categories have a 'name' field

        # Apply the letter filter only if no specific name or category is provided
        if not name_query and not categories_query:
            query &= Q(name__istartswith=letter)
    else:
        query &= Q(name__istartswith=letter)

    queryset = Location.objects.filter(query).order_by("name")
    queryset, page = pagination(request, queryset, 36)

    query_params = QueryDict(mutable=True)
    for key, value in request.GET.items():
        if (
            key != "page" and key != "letter"
        ):  # Exclude page number and letter to reset it correctly
            query_params[key] = value

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "page": page,
        "query_params": query_params.urlencode(),
        "letter": letter,  # Pass the current letter to the context
    }
    return render(request, "locations/locations_by_letter_prototype.html", context)


def location(request, location_id):
    location = Location.objects.get(id=location_id)
    categories = location.categories.all()
    posts = location.posts.all()

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
    map = folium_map_latlong(y_coord, x_coord, None)
    map_html = map._repr_html_()
    location_name = coords[0].get("name")

    nls_url = f"https://maps.nls.uk/geo/explore/print/#zoom=16&lat={y_coord}&lon={x_coord}&layers=168&b=5"

    context = {
        "posts": posts,
        "location": location,
        "categories": categories,
        "map": map_html,
        "title": location_name,
        "nls_url": nls_url,
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
    map = folium_map_latlong(y_coord, x_coord, None)
    map_html = map._repr_html_()
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
    queryset = Route.objects.order_by("name")
    selection_criteria = RouteSelectionForm(request.GET or None)

    if request.method == "POST":
        # Use GET method for form submission
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if selection_criteria.is_valid():
        query = Q()
        cleandata = selection_criteria.cleaned_data

        if "name" in cleandata and cleandata["name"]:
            query &= Q(name__icontains=cleandata["name"])

        if "owner_operators" in cleandata and cleandata["owner_operators"]:
            fk = cleandata[
                "owner_operators"
            ].pk  # Get the primary key of the selected owner operator
            query &= Q(owneroperators=fk)

        if "categories" in cleandata and cleandata["categories"]:
            fk = cleandata["categories"]
            query &= Q(categories=fk)

        queryset = Route.objects.filter(query).order_by("name")

        # Check the value of the "action" parameter

        if "action" in request.GET:
            action = request.GET["action"]

            if action == "map":  # Defaults to "list" if not map
                elr_geojsons, locations = routes_mapdata_extract(queryset)
                if locations or elr_geojsons:
                    map_html = folium_map_geojson(elr_geojsons, locations)

    queryset, page = pagination(request, queryset, 36)

    # Retain existing query parameters for pagination links
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "query_params": query_params.urlencode(),  # Pass query_params to the template
        "map": map_html,
    }
    return render(request, "locations/routes.html", context)


def route(request, slug):

    route = Route.objects.get(slug=slug)
    references = route.references.all
    elrs = route.elrs.all

    events_json = None
    if route_events := LocationEvent.objects.filter(route_fk_id=route.id):
        events_json = events_timeline(route_events)

    routes = [route]
    elr_geojsons, locations = routes_mapdata_extract(routes)
    if locations or elr_geojsons:
        map_html = folium_map_geojson(elr_geojsons, locations)

    context = {
        "map": map_html,
        "route": route,
        "elrs": elrs,
        "references": references,
        "timeline_json": events_json,
    }
    return render(request, "locations/route.html", context)


def route_map(request, slug):

    route = Route.objects.get(slug=slug)
    elrs = route.elrs.all
    routes = [route]

    elr_geojsons, locations = routes_mapdata_extract(routes)
    if locations or elr_geojsons:
        map_html = folium_map_geojson(elr_geojsons, locations)

    context = {
        "map": map_html,
        "route": route,
        "elrs": elrs,
        "title": route.name,
    }
    print(elrs)
    return render(request, "locations/folium_map.html", context)


def route_sections(request):
    if request.method == "POST":
        selection_criteria = RouteSectionSelectionForm(request.POST)

        if selection_criteria.is_valid():
            if str(selection_criteria.cleaned_data["name"]):
                queryset = RouteSection.objects.filter(
                    name__icontains=selection_criteria.cleaned_data["name"]
                ).order_by("name")
                errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = RouteSection.objects.order_by("name")

    else:
        selection_criteria = RouteSectionSelectionForm()
        errors = selection_criteria.errors or None
        queryset = RouteSection.objects.order_by("name")

    queryset, page = pagination(request, queryset)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "locations/route_sections.html", context)


def route_section(request, route_section_id):

    # Temporarily built to generate a route page rather than route_section

    route_section = RouteSection.objects.get(id=route_section_id)
    route = Route.objects.get(id=route_section.route_fk.id)
    locations = route_section_locations_extract(route)
    if locations or route_section.geodata:
        map_html = folium_map_geojson(route_section.geodata, locations)

    # events_json = None
    # if route_events := LocationEvent.objects.filter(route_fk_id=route.id):
    #     events_json = events_timeline(route_events)

    context = {
        "map": map_html,
        "route_section": route_section,
        "elrs": None,
        "references": None,
        "timeline_json": None,
    }
    return render(request, "locations/route_section.html", context)


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

            # If the route has a post recorded for it, it should be used in preference to the wikipedia page for the route description
            if route.post_fk:
                header_title = route.post_fk.title
                header_text = route.post_fk.body
            else:
                pagename = route.wikipedia_slug.replace("_", " ")
                wikipage = urllib.parse.unquote(
                    pagename, encoding="utf-8", errors="replace"
                )
                header_title = wikipage
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

    # elrs = execute_sql(sql, [west, south, east, north])

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

    locations = execute_sql(sql, [west, south, east, north])

    elr_geojsons = None

    # for elr in elrs:
    #     try:
    #         if elr["geodata"]:
    #             if elr_geojsons is None:
    #                 elr_geojsons = []
    #             geojson = json.loads(elr["geodata"])
    #             elr_geojsons.append(geojson)
    #     except Exception as e:
    #         print(f"Error {e}")

    figure = None
    if locations or elr_geojsons:
        map_html = folium_map_geojson(elr_geojsons, locations)

    title = f"UK {geo_area} Region"
    context = {"map": map_html, "title": title}
    return render(request, "locations/folium_map.html", context)


def elrs(request):
    errors = None
    queryset = ELR.objects.order_by("itemAltLabel")
    selection_criteria = ELRSelectForm(request.GET or None)

    if request.method == "POST":
        # Use GET method for form submission
        return redirect(request.path_info + "?" + request.POST.urlencode())

    if not selection_criteria.is_valid():
        errors = selection_criteria.errors

    if selection_criteria.is_valid():
        queryset = elrs_query_build(selection_criteria.cleaned_data)

    queryset, page = pagination(request, queryset, 36)

    # Retain existing query parameters for pagination
    query_params = QueryDict("", mutable=True)
    query_params.update(request.GET)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
        "query_params": query_params.urlencode(),
    }

    return render(request, "locations/elrs.html", context)


def elrs_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "itemAltLabel" in cleandata and cleandata["itemAltLabel"]:
        conditions &= Q(itemAltLabel__icontains=cleandata["itemAltLabel"])

    if "itemLabel" in cleandata and cleandata["itemLabel"]:
        conditions &= Q(itemLabel__icontains=cleandata["itemLabel"])

    queryset = ELR.objects.filter(conditions).order_by("itemAltLabel")

    return queryset


def elr_map(request, elr_id):
    elr = ELR.objects.get(id=elr_id)

    if elr.geodata and len(elr.geodata["features"]) > 0:
        elr_geojsons = []
        elr_geojsons.append(elr.geodata)

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
        header_text = elr.post_fk.body if elr.post_fk else ""
        storymap_json = generate_storymap(header_title, header_text, slide_locations)
    return render(request, "locations/storymap.html", {"storymap_json": storymap_json})


def elr_display_osmdata(request, elr_id):
    elr = ELR.objects.get(id=elr_id)

    elr_geojson = [osm_elr_fetch(elr.itemAltLabel, None)]

    if elr_geojson:  # i.e. If OSM has some geodata relating to the ELR then display it
        title = f"{elr.itemAltLabel}: {elr.itemLabel}"
    else:
        figure = None

    context = {"elr_geojson": elr_geojson[0]["features"], "title": title}
    return render(request, "locations/elr_display_osmdata.html", context)


def elr_history(request, elr_id):
    # Function under development. Aims to show route sections over time
    elr = ELR.objects.get(id=elr_id)

    route_sections = RouteSection.objects.filter(routesectionelr__elr_fk=elr)
    print(route_sections)

    if elr.geodata and len(elr.geodata["features"]) > 0:
        elr_geojsons = []
        elr_geojsons.append(elr.geodata)

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

    context = {"visit": visit, "page": page, "images": images}
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
