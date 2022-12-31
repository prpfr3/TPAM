import json
import datetime

from django.http import (HttpRequest, HttpResponseRedirect)
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import *
from .models import *
from locos.views import pagination

def home(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'locations/index.html',{'title':'Home Page', 'year':datetime.now().year,})

def index(request):
  return render(request, 'locations/index.html')

def map_closed_lines_select(request):

    if request.method == 'POST':
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            county=str(selected_location)
            return HttpResponseRedirect(reverse('locations:map_closed_lines', args=[county]))
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {'location_list':location_list, 'errors': errors,}
        return render(request, 'locations/map_closed_lines_select.html', context)

class MapClosedLines(TemplateView):

    template_name = "locations/map_closed_lines.html"

    def get_context_data(self, **kwargs):
        import os
        import folium
        import geopandas as gpd
        from sqlalchemy import create_engine, text
        from django.conf import settings

        county = self.kwargs['county_name']
        db_connection_url = os.environ.get('DATABASE_URL') or settings.DATABASE_URL
        con = create_engine(db_connection_url)

        # Note that locations_UK_admin_boundaries should have been loaded with crs of 4326 in this database (originally data is CRS 27700)
        sql = text('SELECT a.* FROM public."locations_routes_geo_closed" as a JOIN public."locations_UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        routes = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county}, crs="EPSG:4326")

        # Get the county record to calculate the centre of the map
        sql = text('SELECT * FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = :county')
        df_county = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county}, crs="EPSG:4326")
        df_bounds = df_county.bounds

        south = df_bounds.miny[0]
        west = df_bounds['minx'][0]
        north = df_bounds['maxy'][0]
        east = df_bounds['maxx'][0]

        figure = folium.Figure()
        m = folium.Map([df_county.geometry.centroid.y[0], df_county.geometry.centroid.x[0]], zoom_start= 9, height=500, tiles='cartodbpositron', prefer_canvas=True)
        m.add_to(figure)
        folium.GeoJson(data=routes["geometry"], popup=routes["name"]).add_to(m)
        figure.render()
        return {"map": figure, "county": county}

def routes(request):

    if request.method == 'POST':
        selection_criteria = RouteSelectionForm(request.POST)

        if selection_criteria.is_valid() and str(selection_criteria.cleaned_data['name']):
            queryset = Route.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        elif selection_criteria.is_valid() and str(selection_criteria.cleaned_data['wikipedia_route_categories']) != 'None':
            queryset = Route.objects.filter(wikipedia_route_categories__in=selection_criteria.cleaned_data['wikipedia_route_categories']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Route.objects.order_by('name')
    else:
        selection_criteria = RouteSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Route.objects.order_by('name')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'routes': queryset}
    return render(request, 'locations/routes.html', context)

def locations(request):

    if request.method == 'POST':
        selection_criteria = LocationSelectionForm(request.POST)
        if selection_criteria.is_valid() and selection_criteria.cleaned_data['wikiname'] != None:
            queryset = Location.objects.filter(wikiname__icontains=selection_criteria.cleaned_data['wikiname']).order_by('wikiname')
            errors = None
        elif selection_criteria.is_valid() and str(selection_criteria.cleaned_data['type']) != 'None':
            queryset = Location.objects.filter(type__icontains=selection_criteria.cleaned_data['type']).order_by('wikiname')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Location.objects.order_by('wikiname')
    else:
        selection_criteria = LocationSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Location.objects.order_by('wikiname')

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'locations': queryset}
    return render(request, 'locations/locations.html', context)

def location(request, location_id):

    location = Location.objects.get(id=location_id)

    nls_url = f'https://maps.nls.uk/geo/explore/print/#zoom=15&lat={location.geometry.y}&lon={location.geometry.x}&layers=168&b=5'
    context = {'location': location, 'nls_url': nls_url}
    return render(request, 'locations/location.html', context)

def route_map(request, route_id):
  
    import wikipediaapi
    import urllib

    route = Route.objects.get(id=route_id)

    # Get the Wikipedia Page
    wiki_wiki = wikipediaapi.Wikipedia(language='en',extract_format=wikipediaapi.ExtractFormat.HTML)
    slug = route.wikipedia_slug.replace('/wiki/', '')
    slug = urllib.parse.unquote(slug, encoding='utf-8', errors='replace')
    route_page = wiki_wiki.page(slug).text

    # Wikipedia usually only has one routemap for a railway route page...but there could be more than one
    routemaps = route.wikipedia_routemaps.all()
    routemap = routemaps[0]

    if locations := Location.objects.filter(
        routelocation__routemap=routemap.id):
        figure = generate_folium_map(None, route.name, locations)
    else:
        figure = None

    context =  {"map": figure, "route": route.name, "wikipage": route_page }
    return render(request, 'locations/routemap_folium.html', context)

def route_storymap(request, route_id):

    import markdown
    import wikipediaapi
    import urllib
    
    storymap_json = None
    route = Route.objects.get(id=route_id)
    
    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict = \
        {"location_line":"true",
        "type":"overview",
        "media":
            {"caption":"",
            "credit":"",
            "url":""},
        "text":
            {"headline":route.name,
            "text":""}
        }

    wikislug = route.wikipedia_slug.replace('/wiki/', '')
    pagename = wikislug.replace('_', ' ')
    pagename = urllib.parse.unquote(pagename, encoding='utf-8', errors='replace')
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    
    if wikislug and wiki_wiki.page(wikislug).exists:
        text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
        slide_dict['text']['text'] = text_array[0]

    slide_list = [slide_dict]

    routemaps = route.wikipedia_routemaps.all()
    for routemap in routemaps:
      routelocations = RouteLocation.objects.filter(routemap=routemap.id)
      for routelocation in routelocations:
        if routelocation.location_fk != None:
          try:
            slide_dict = \
                {"background":
                    {"url": ""},
                "location":
                    {"lat": routelocation.location_fk.geometry.y,
                    "lon": routelocation.location_fk.geometry.x,
                    "zoom": "12"},
                "media":
                    {"caption":"",
                    "credit":"",
                    "url":""},
                "text":
                    {"headline":routelocation.location_fk.wikiname}
                }

            html_string = markdown.markdown(routelocation.label.replace('/wiki/', 'https://en.wikipedia.org/wiki/'))
            slide_dict['text']['text'] = html_string.replace('"', '\'')

            wikislug = routelocation.location_fk.wikislug.replace('/wiki/', '')
            pagename= wikislug.replace('_', ' ')
            wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
            
            if wikislug and wiki_wiki.page(wikislug).exists:
                text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
                slide_dict['text'] = {'text': text_array[0], 'headline': pagename}
            else:
                slide_dict['text'] = {'text': html_string, 'headline': pagename}

            slide_list.append(slide_dict)
          except Exception as e:
            print(e)

      #Create a dictionary in the required JSON format, including the dictionary list of slides
        routemap_dict = \
            {"storymap":
                {"attribution": "Wikipedia / OpenStreetMaps",
                "call_to_action": True,
                "call_to_action_text": "A Routemap",
                "map_as_image": False,
                "map_subdomains": "",
                "map_type": "osm:standard",
                "slides": slide_list,
                "zoomify": False
                }
            }

      storymap_json = json.dumps(routemap_dict)

    return render(request, 'locations/storymap.html', {'storymap_json':storymap_json})

def osm_railmap_county_select(request):

    if request.method == 'POST':
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            county=str(selected_location)
            return HttpResponseRedirect(reverse('locations:osm_railmap_county', args=[county]))
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {'location_list':location_list, 'errors': errors,}
        # Uses the same county selection form as map_closed_lines
        return render(request, 'locations/map_closed_lines_select.html', context)

def osm_railmap_county(request, county):

    import os
    import requests
    import osm2geojson
    import geopandas as gpd
    from sqlalchemy import create_engine, text
    from django.conf import settings

    # Get the county record to calculate the centre of the map
    db_connection_url = os.environ.get('DATABASE_URL') or settings.DATABASE_URL
    con = create_engine(db_connection_url)
    sql = text('SELECT * FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = :county')
    df_county = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county}, crs="EPSG:4326")
    df_bounds = df_county.bounds

    south = df_bounds.miny[0]
    west = df_bounds['minx'][0]
    north = df_bounds['maxy'][0]
    east = df_bounds['maxx'][0]

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
    figure = None

    # Get all the locations within the county
    county_record = UkAdminBoundaries.objects.filter(ctyua19nm=county)
    locations = Location.objects.filter(geometry__within=county_record[0].geometry)

    title = county
    if len(geojson['features']) != 0:
        figure = generate_folium_map(geojson, title, locations)
    context =  {"map": figure, "title": title}
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

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'elrs': elrs}
    return render(request, 'locations/elrs.html', context)

def geojson_boundbox(features):

    #  Calculates the boundary box
    #  the following may provide a simpler method 
    #  https://gis.stackexchange.com/questions/166863/how-to-calculate-the-bounding-box-of-a-geojson-object-using-python-or-javascript

    xcoords = []
    ycoords = []

    for f in features:
        geom = f['geometry']
        for coord in geom['coordinates']:
            if type(coord) == float:  # then its a point feature
                xcoords.append(geom['coordinates'][0])
                ycoords.append(geom['coordinates'][1])
            elif type(coord) == list:
                for c in coord:
                    if type(c) == float:  # then its a linestring feature
                        xcoords.append(coord[0])
                        ycoords.append(coord[1])
                    elif type(c) == list:  # then its a polygon feature
                        xcoords.append(c[0])
                        ycoords.append(c[1])

    return([[min(ycoords), min(xcoords)],
        [max(ycoords), min(xcoords)],
        [max(ycoords), max(xcoords)],
        [min(ycoords), max(xcoords)]])

def elr_map(request, elr_id):
    
    import requests
    import osm2geojson

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

    locations = Location.objects.filter(elr_fk__itemAltLabel=elr.itemAltLabel)

    title = f'{elr.itemAltLabel}: {elr.itemLabel}'
    if len(geojson['features']) != 0:
        figure = generate_folium_map(geojson, title, locations)
    else:
        figure = None

    context =  {"map": figure, "title": title}
    return render(request, 'locations/folium_map.html', context)

def generate_folium_map(geojson, title, locations ):

    import folium
    from folium.plugins import MarkerCluster
    from django.contrib.gis.db.models import Extent

    # By default folium will use OpenStreetMap as the baselayer. 'tiles=None' switches the default off
    m = folium.Map(zoom_start= 13, prefer_canvas=True, height=500)

    """
    Use OpenRailwayMap as the baselayer to give a better rendering of the line
    Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
    """
    folium.TileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
        attr='<a href="https://www.openstreetmap.org/copyright"> \
            © OpenStreetMap contributors</a>, \
            Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
            CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap', \
        name = "OpenRailwayMap", \
        min_zoom = 2, max_zoom = 19).add_to(m)

    # If there is geojson (i.e. OSM) input then use it to calculate the boundary box.
    # If not calculate the boundary box from the locations co-ordinates
    if geojson:
        folium.GeoJson(geojson, name=title).add_to(m)
        bound_box = geojson_boundbox(geojson['features'])
    else:
        extent = locations.aggregate(Extent('geometry'))
        bound_box = [[extent['geometry__extent'][1], 
            extent['geometry__extent'][0]], 
            [extent['geometry__extent'][3], 
            extent['geometry__extent'][2]]]

    folium.FitBounds(bound_box).add_to(m)

    marker_cluster = MarkerCluster(name="Locations").add_to(m)

    for location in locations:
        if location.geometry:

            if str(location.opened) != 'None':
                opened = f'<br>Opened {str(location.opened)}'
            else:
                opened = ''

            if str(location.closed) != 'None':
                closed = f'<br>Closed {str(location.closed)}'
            else:
                closed = ''

            if str(location.wikislug) != 'None':
                name = f'<a href="https://en.wikipedia.org//wiki/{str(location.wikislug)}"target="_blank"> \
                {str(location.wikiname)}</a>'
            else:
                name = f'{str(location.stationname)}'

            label_html = folium.Html(f'{name}{opened}{closed}', script=True)
            label = folium.Popup(label_html, max_width=2650)
            coords_tuple = (location.geometry.y, location.geometry.x)
            folium.Marker(location = coords_tuple, popup= label, tooltip=str(name)).add_to(marker_cluster)

    folium.LayerControl().add_to(m)
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()

    return figure

def elr_storymap(request, elr_id):
    import markdown
    import wikipediaapi
    import urllib
    
    storymap_json = None
    elr = ELR.objects.get(id=elr_id)
    
    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict = \
        {"location_line":"true",
        "type":"overview",
        "media":
            {"caption":"",
            "credit":"",
            "url":""},
        "text":
            {"headline":f'{elr.itemAltLabel}: {elr.itemLabel}',
            "text":""}
        }

    # wikislug = route.wikipedia_slug.replace('/wiki/', '')
    # pagename = wikislug.replace('_', ' ')
    # pagename = urllib.parse.unquote(pagename, encoding='utf-8', errors='replace')
    # wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    
    # if wikislug and wiki_wiki.page(wikislug).exists:
    #     text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
    #     slide_dict['text']['text'] = text_array[0]

    slide_list = [slide_dict]

    locations = Location.objects.filter(elr_fk__itemAltLabel=elr.itemAltLabel)

    for location in locations:
        if location.elr_fk != None:
            try:
                slide_dict = \
                    {"background":
                        {"url": ""},
                    "location":
                        {"lat": location.geometry.y,
                        "lon": location.geometry.x,
                        "zoom": "12"},
                    "media":
                        {"caption":"",
                        "credit":"",
                        "url":""},
                    "text":
                        {"headline":location.wikiname}
                    }

                html_string = markdown.markdown(f'https://en.wikipedia.org/wiki/{location.wikislug}')
                slide_dict['text']['text'] = html_string.replace('"', '\'')

                wikislug = location.wikislug.replace('/wiki/', '')
                pagename= wikislug.replace('_', ' ')
                wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
                
                if wikislug and wiki_wiki.page(wikislug).exists:
                    text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
                    slide_dict['text'] = {'text': text_array[0], 'headline': pagename}
                else:
                    slide_dict['text'] = {'text': html_string, 'headline': pagename}

                slide_list.append(slide_dict)
            except Exception as e:
                print(e)

    #Create a dictionary in the required JSON format, including the dictionary list of slides
    routemap_dict = \
        {"storymap":
            {"attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "A Routemap",
            "map_as_image": False,
            "map_subdomains": "",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False
            }
        }

    storymap_json = json.dumps(routemap_dict)

    return render(request, 'locations/storymap.html', {'storymap_json':storymap_json})

class Trackmap(TemplateView):
    template_name = "locations/trackmap.html"

    def get_context_data(self, **kwargs):
        import geopandas as gpd
        import folium
        file = "D:\Data\QGIS\ElhamValleyRailway.geojson"
        track_details = gpd.read_file(file)

        figure = folium.Figure()
        m = folium.Map([track_details.geometry.centroid.y[0], track_details.geometry.centroid.x[0]], height=500, zoom_start= 12, 
        prefer_canvas=True)

        folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(m)
        folium.TileLayer('http://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
            attr='<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, \
                 Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> \
                 <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
            min_zoom = 12, max_zoom = 19).add_to(m)
        folium.GeoJson(data=track_details["geometry"], popup=track_details["id"]).add_to(m)
 
        # folium.Icon(icon="cloud").add_to(m)
        # folium.Marker(track_details["geometry"][0], popup=track_details["id"][0], tooltip=tooltip,).add_to(m)

        m.add_to(figure)
        figure.render()
        return {"map": figure}

def location_timeline(request):

    events = []
    forlooplimiter = 0
    location_events = LocationEvent.objects.order_by('datefield')

    for location_event in location_events:
        if location_event.datefield:
            forlooplimiter += 1
            ## https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {"id": forlooplimiter,
                    "content": location_event.description,
                    "start": location_event.datefield.strftime("%Y/%m/%d"),
                    "event.type": 'point'}
            events.append(event)

    return render(request, 'locations/location_timeline.html', {'timeline_json':json.dumps(events)})

def depot_vis_timeline(request):

    events = []
    forlooplimiter = 0
    depots = Depot.objects.order_by('depot', 'datefield_start')

    for depot in depots:
        if depot.datefield_start and depot.datefield_end:
            forlooplimiter += 1
            ## For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {"id": forlooplimiter,
                    "content": f'{depot.depot} {depot.code}',
                    "start": depot.date_start.replace("??", "01"),
                    "end": depot.date_end.replace("??", "01"),
                    "event.type": 'point'}
            events.append(event)

    return render(request, 'locations/depots_vis_timeline.html', {'timeline_json':json.dumps(events)})