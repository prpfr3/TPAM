import datetime
import json
import urllib
import wikipediaapi

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from notes.models import Reference
from mainmenu.views import pagination

from .forms import *
from .models import *
from .utils import *


def home(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'locations/index.html', {'title': 'Home Page', 'year': datetime.now().year, })


def index(request):
    return render(request, 'locations/index.html')


def locations(request):

    if request.method == 'POST':
        selection_criteria = LocationSelectionForm(request.POST)
        if selection_criteria.is_valid() and selection_criteria.cleaned_data['wikiname'] != None:
            queryset = Location.objects.filter(
                wikiname__icontains=selection_criteria.cleaned_data['wikiname']).order_by('wikiname', 'stationname')
            errors = None
        elif selection_criteria.is_valid() and str(selection_criteria.cleaned_data['type']) != None:
            queryset = Location.objects.filter(
                type__icontains=selection_criteria.cleaned_data['type']).order_by('wikiname', 'stationname')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Location.objects.order_by('wikiname', 'stationname')
    else:
        selection_criteria = LocationSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Location.objects.order_by('wikiname', 'stationname')

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria': selection_criteria,
               'errors': errors, 'locations': queryset}
    return render(request, 'locations/locations.html', context)


def location(request, location_id):

    location = Location.objects.get(id=location_id)

    sql = """ 
    SELECT ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry))
    FROM 
    public."locations_location" AS a
    WHERE a.id = %s;
    """
    coords = execute_sql(sql, [location_id])
    y_coord = coords[0][0]
    x_coord = coords[0][1]
    #  = f'https://maps.nls.uk/geo/explore/print/#zoom=15&lat={location.geometry.y}&lon={location.geometry.x}&layers=168&b=5'
    nls_url = f'https://maps.nls.uk/geo/explore/print/#zoom=15&lat={y_coord}&lon={x_coord}&layers=168&b=5'

    # Get text describing the location either from a custom post, else Wikipedia, else none
    if location.post_fk:
        description = location.post_fk.body
        description_type = "Notes"
    elif location.wikislug:
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
        slug = location.wikislug.replace('/wiki/', '')
        slug = urllib.parse.unquote(slug, encoding='utf-8', errors='replace')
        description = wiki_wiki.page(slug).text
        description_type = "From Wikipedia:-"
    else:
        description = None
        description_type = None

    context = {'location': location, 'description_type': description_type,
               'description': description, 'nls_url': nls_url}
    return render(request, 'locations/location.html', context)


def routes(request):

    errors = None

    if request.method == 'POST':
        selection_criteria = RouteSelectionForm(request.POST)
        if not selection_criteria.is_valid():
            errors = selection_criteria.errors
            queryset = Route.objects.order_by('name')
        elif str(selection_criteria.cleaned_data['name']):
            queryset = Route.objects.filter(
                name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
        elif len(selection_criteria.cleaned_data['wikipedia_route_categories']) != 0:
            queryset = Route.objects.filter(
                wikipedia_route_categories__in=selection_criteria.cleaned_data['wikipedia_route_categories']).order_by('name')
        elif str(selection_criteria.cleaned_data['source']) != 'None':
            queryset = Route.objects.filter(
                source=selection_criteria.cleaned_data['source']).order_by('name')
    else:
        selection_criteria = RouteSelectionForm()
        errors = selection_criteria.errors
        queryset = Route.objects.order_by('name')

    context = {'selection_criteria': selection_criteria,
               'errors': errors, 'routes': queryset}
    return render(request, 'locations/routes.html', context)


def route(request, route_id):

    import urllib
    import wikipediaapi

    route = Route.objects.get(id=route_id)
    references = route.references.all()

    # # Get either a customised post or otherwise a wikipedia page
    if route.post_fk:
        description = route.post_fk.body
        description_type = "Notes"
    elif route.wikipedia_slug:
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
        slug = route.wikipedia_slug.replace('/wiki/', '')
        slug = urllib.parse.unquote(slug, encoding='utf-8', errors='replace')
        description = wiki_wiki.page(slug).text
        description_type = "From Wikipedia:-"
    else:
        description = None
        description_type = None

    figure = None
    events_json = None

    if routemaps := route.wikipedia_routemaps.all():  # i.e. If the route has any wikipedia routemaps

        """ THIS IS DJANGO ORM CODE SUPERSEDED BY NATIVE SQL CODE BELOW TO REMOVE GDAL DEPENDENCIES
        if locations := Location.objects.filter(
            routelocation__routemap=routemaps[0].id):
            figure = generate_folium_map(None, route.name, locations)
        """

        sql = """
            SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."stationname",
                ST_Y(ST_CENTROID(a.geometry)),
                ST_X(ST_CENTROID(a.geometry)),
                a."media_url"
            FROM "locations_location" AS a
            INNER JOIN "locations_routelocation" AS b
                ON (a."id" = b."location_fk_id")
            WHERE a."geometry" IS NOT NULL AND b."routemap_id" = %s;
        """

        if locations := execute_sql(sql, [routemaps[0].id]):

            # Calculate the Boundary Box from the Locations
            sql = """ 
            SELECT max(ST_Ymax(geometry)), max(ST_Xmax(geometry)), min(ST_Ymin(geometry)), min(ST_Xmin(geometry))
            FROM "locations_location"
            INNER JOIN "locations_routelocation"
                ON ("locations_location"."id" = "locations_routelocation"."location_fk_id")
            WHERE "locations_routelocation"."routemap_id" = %s;
            """
            bounds = execute_sql(sql, [routemaps[0].id])
            west = bounds[0][3]
            south = bounds[0][2]
            east = bounds[0][1]
            north = bounds[0][0]
            bound_box_sql = [[south, west], [north, west],
                             [north, east], [south, east]]

            figure = generate_folium_map_sql(
                None, route.name, locations, bound_box_sql)

    if route_events := LocationEvent.objects.filter(route_fk_id=route_id):
        events_json = events_timeline(route_events)

    context = {"map": figure, "route": route.name, "references": references,
               "description_type": description_type, "description": description, 'timeline_json': events_json}
    return render(request, 'locations/route.html', context)


def events_timeline(events_in):

    events_out = []
    count = 0

    for event in events_in:
        if event.datefield:
            count += 1
            # https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {"id": count,
                     "content": event.description,
                     "start": event.datefield.strftime("%Y/%m/%d"),
                     "event.type": 'point'}
            events_out.append(event)

    return json.dumps(events_out)


def route_storymap(request, route_id):

    import urllib
    import wikipediaapi

    storymap_json = None
    route = Route.objects.get(id=route_id)

    if routemaps := route.wikipedia_routemaps.all():  # i.e. If the route has any wikipedia routemaps

        sql = """
            SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."stationname",
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

            # If the route has some notes these should be used in preference to the wikipedia page for the route description
            if route.post_fk:
                header_text = route.post_fk.body
            else:
                wikislug = wikislug.replace('/wiki/', '')
                pagename = wikislug.replace('_', ' ')
                pagename = urllib.parse.unquote(
                    pagename, encoding='utf-8', errors='replace')
                wiki_wiki = wikipediaapi.Wikipedia(
                    language='en', extract_format=wikipediaapi.ExtractFormat.HTML)

                if wikislug and wiki_wiki.page(wikislug).exists:
                    text_array = wiki_wiki.page(
                        wikislug).text.split('<h2>References</h2>')
                    header_text = text_array[0]

            storymap_json = generate_storymap(
                header_title, header_text, slide_locations)

    return render(request, 'locations/storymap.html', {'storymap_json': storymap_json})


def osm_railmap_county_select(request):

    if request.method == 'POST':
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            county = str(selected_location)
            return HttpResponseRedirect(reverse('locations:osm_railmap_county', args=[county]))
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {'location_list': location_list, 'errors': errors, }
        return render(request, 'locations/county_select.html', context)


def osm_railmap_county(request, county):

    import osm2geojson
    import requests

    # Get the county record to calculate the centre of the map
    """ THIS IS GEOPANDAS CODE SUPERSEDED BY NATIVE SQL CODE BELOW TO REMOVE GDAL DEPENDENCIES

    import os
    import geopandas as gpd
    from django.conf import settings
    from sqlalchemy import create_engine, text
    
    db_connection_url = os.environ.get('DATABASE_URL') or settings.DATABASE_URL
    con = create_engine(db_connection_url)
    sql = text('SELECT * FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = :county')
    df_county = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county}, crs="EPSG:4326")
    df_bounds = df_county.bounds

    south = df_bounds.miny[0]
    west = df_bounds['minx'][0]
    north = df_bounds['maxy'][0]
    east = df_bounds['maxx'][0]
    """

    # Calculate the boundary box from the County Geometry
    sql = """SELECT ST_XMin(geometry), ST_YMin(geometry), ST_XMax(geometry), ST_YMax(geometry),
    ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry))
    FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = %s;"""
    bounds = execute_sql(sql, [county])
    west = bounds[0][0]
    south = bounds[0][1]
    east = bounds[0][2]
    north = bounds[0][3]
    bound_box_sql = [[south, west], [north, west], [north, east], [south, east]]

    # Calculate the Boundary Box from the Locations
    sql = """ 
    SELECT max(ST_Ymax(a.geometry)), max(ST_Xmax(a.geometry)), min(ST_Ymin(a.geometry)), min(ST_Xmin(a.geometry))
    FROM 
    public."locations_location" AS a JOIN public."locations_UK_admin_boundaries" as b 
    ON ST_WITHIN(a.geometry, b.geometry) 
    WHERE b.ctyua19nm = %s;
    """
    bounds = execute_sql(sql, [county])
    west = bounds[0][3]
    south = bounds[0][2]
    east = bounds[0][1]
    north = bounds[0][0]
    bound_box_sql = [[south, west], [north, west], [north, east], [south, east]]

    # Get all the OSM data within the county
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        node({south}, {west}, {north}, {east})["railway"];
        way({south}, {west}, {north}, {east})["railway"];
        out geom;
        """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    # Convert OSM json to Geojson. Warning ! The osm2geojson utility is still under development
    geojson = osm2geojson.json2geojson(data)

    # Get all the locations within the county
    """ THIS IS DJANGO ORM CODE SUPERSEDED BY NATIVE SQL CODE BELOW TO REMOVE GDAL DEPENDENCIES
    county_record = UkAdminBoundaries.objects.filter(ctyua19nm=county)
    locations_orm = Location.objects.filter(geometry__within=county_record[0].geometry)
    """

    sql = """ 
    SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."stationname",
    ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)),
    a."media_url"
    FROM 
    public."locations_location" AS a JOIN public."locations_UK_admin_boundaries" as b 
    ON ST_WITHIN(a.geometry, b.geometry) 
    WHERE a."geometry" IS NOT NULL AND b.ctyua19nm = %s;
    """
    locations = execute_sql(sql, [county])

    if geojson:
        figure = generate_folium_map_sql(
            geojson, county, locations, bound_box_sql)
    else:
        figure = None
    context = {"map": figure, "title": county}
    return render(request, 'locations/folium_map.html', context)


def elrs(request):

    if request.method == 'POST':
        selection_criteria = OSMRailMapSelectForm(request.POST)

        if selection_criteria.is_valid():
            if str(selection_criteria.cleaned_data['itemAltLabel']):
                elrs = ELR.objects.filter(itemAltLabel__icontains=selection_criteria.cleaned_data['itemAltLabel']) \
                    .order_by('itemAltLabel')
                errors = None
            elif str(selection_criteria.cleaned_data['itemLabel']) != 'None':
                elrs = ELR.objects.filter(itemLabel__icontains=selection_criteria.cleaned_data['itemLabel']) \
                    .order_by('itemAltLabel')
                errors = None
        else:
            errors = selection_criteria.errors or None
            elrs = ELR.objects.order_by('itemAltLabel')

    else:
        selection_criteria = OSMRailMapSelectForm()
        errors = selection_criteria.errors or None
        elrs = ELR.objects.order_by('itemAltLabel')

    context = {'selection_criteria': selection_criteria,
               'errors': errors, 'elrs': elrs}

    return render(request, 'locations/elrs.html', context)


def elr_map(request, elr_id):

    import osm2geojson
    import requests

    elr = ELR.objects.get(id=elr_id)

    """
    Overpass Turbo query gets the Way relating to the Engineer's Line Reference
    and then uses the "around" statement to get nodes such as stations and ways
    not labelled as the Engineer's Line Reference within x (e.g. 500) metres of the
    ELR way
    """

    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = f"""
        [out:json];
        area["ISO3166-1"="GB"][admin_level=2];
        way(area)["ref"="{elr.itemAltLabel}"]->.elr;
        node(around.elr:50)["railway"];
        way(around.elr:50)["railway"];
        out geom;
        """

    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Convert OSM json to Geojson. Warning ! The osm2geojson utility is still under development
    geojson = osm2geojson.json2geojson(data)

    """ THIS IS DJANGO ORM CODE SUPERSEDED BY NATIVE SQL CODE BELOW TO REMOVE GDAL DEPENDENCIES
    locations_orm = Location.objects.filter(elr_fk__itemAltLabel=elr.itemAltLabel)

    if len(geojson['features']) != 0:
        figure = generate_folium_map(geojson, title, locations_orm)
    else:
        figure = None
    """

    sql = """ 
    SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."stationname",
    ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), b."itemAltLabel", b."itemLabel"
    FROM "locations_location" AS a INNER JOIN "locations_elr" AS b
    ON (a."elr_fk_id" = b."id" ) 
    WHERE b."id" = %s;
    """

    locations_sql = execute_sql(sql, [elr_id])

    if geojson:  # i.e. If OSM has some geodata relating to the ELR then generate the map
        title = f'{elr.itemAltLabel}: {elr.itemLabel}'
        bound_box = geojson_boundbox(geojson['features'])
        figure = generate_folium_map_sql(
            geojson, title, locations_sql, bound_box)
    else:
        figure = None

    context = {"map": figure, "title": title}
    return render(request, 'locations/folium_map.html', context)


def elr_storymap(request, elr_id):
    import urllib
    import wikipediaapi

    storymap_json = None
    route = ELR.objects.get(id=elr_id)

    sql = """ 
    SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."stationname",
        ST_Y(ST_CENTROID(a.geometry)), 
        ST_X(ST_CENTROID(a.geometry)),
        a."media_caption",
        a."media_credit",
        a."media_url"
    FROM "locations_location" AS a 
    INNER JOIN "locations_elr" AS b
        ON (a."elr_fk_id" = b."id" ) 
    WHERE b."id" = %s;
    """

    if slide_locations := execute_sql(sql, [elr_id]):

        header_title = f'{route.itemAltLabel}: {route.itemLabel}'

        # If the elr has some notes
        header_text = route.post_fk.body if route.post_fk else ''
        storymap_json = generate_storymap(
            header_title, header_text, slide_locations)
    return render(request, 'locations/storymap.html', {'storymap_json': storymap_json})


class HeritageSiteListView(ListView):
    model = HeritageSite
    queryset = HeritageSite.objects.order_by(
        'country', 'type', 'name').exclude(name='N/A')


def heritage_site(request, heritage_site_id):
    heritage_site = HeritageSite.objects.get(id=heritage_site_id)
    context = {'heritage_site': heritage_site}
    return render(request, 'locations/heritage_site.html', context)


class VisitListView(ListView):
    model = Visit


@login_required
def visit(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    images = Reference.objects.filter(visit=visit_id).order_by('id')
    paginator = Paginator(images, 20)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)

    context = {'visit': visit, 'page': page, 'images': images}
    return render(request, 'maps/visit.html', context)
