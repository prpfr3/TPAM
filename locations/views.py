import json
from sqlalchemy import null
import wikipediaapi
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpRequest, HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.db.models import Q, F, ExpressionWrapper, fields
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.core.exceptions import ObjectDoesNotExist

from itertools import chain

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
        routes = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        # Get the county record to calculate the centre of the map
        sql = text('SELECT * FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = :county')
        df_county = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

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
            print(f"{selection_criteria=}\n{selection_criteria.cleaned_data['wikiname']=}\n{selection_criteria.cleaned_data['type']=}")
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

def routemap(request, route_id):
  
    import wikipediaapi
    import urllib
    import folium
    from folium.plugins import MarkerCluster

    figure = None
    route = Route.objects.get(id=route_id)

    # Get the Wikipedia Page
    wiki_wiki = wikipediaapi.Wikipedia(language='en',extract_format=wikipediaapi.ExtractFormat.HTML)
    slug = route.wikipedia_slug.replace('/wiki/', '')
    slug = urllib.parse.unquote(slug, encoding='utf-8', errors='replace')
    route_page = wiki_wiki.page(slug).text

    # Wikipedia usually only has one routemap for a railway route page...but there could be more than one
    routemaps = route.wikipedia_routemaps.all()

    for routemap in routemaps:

        routelocations = RouteLocation.objects.filter(routemap=routemap.id)
        from django.contrib.gis.db.models import Extent
        boundbox = routelocations.exclude(location_fk=None).aggregate(Extent('location_fk__geometry'))
        if boundbox['location_fk__geometry__extent'] is not None:

            figure = folium.Figure()
            m = folium.Map(zoom_start= 13, prefer_canvas=True, height=500)
            folium.FitBounds([[boundbox['location_fk__geometry__extent'][1], 
                              boundbox['location_fk__geometry__extent'][0]], 
                              [boundbox['location_fk__geometry__extent'][3], 
                              boundbox['location_fk__geometry__extent'][2]]]).add_to(m)
            folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(m)
            folium.TileLayer('http://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
            attr='<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
            # Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
            min_zoom = 12, max_zoom = 19).add_to(m)

            # For each of the locations on the routemap, see if has a relationship with a location (i.e. a location is normally in the Routes table if it has a wikipedia page, normally for a railway station). Only if it has will there be geometry available which would allow us to add it to the map.
            for routelocation in routelocations:
              if routelocation.location_fk != None:
                  folium.Marker(location=[routelocation.location_fk.geometry.y, routelocation.location_fk.geometry.x], 
                    tooltip=str(routelocation.location_fk.wikiname), 
                    popup=folium.Popup(str(routelocation.location_fk.wikiname), parse_html=True)).add_to(m)

            marker_cluster = MarkerCluster().add_to(m)

            for point in range(len(routelocations)):

              if routelocations[point].location_fk:
                if str(routelocations[point].location_fk.opened) != 'None':
                  opened = f'<br>Opened {str(routelocations[point].location_fk.opened)}'
                else:
                  opened = '<br>Opened: Not Recorded'

                if str(routelocations[point].location_fk.closed) != 'None':
                  closed = f'<br>Closed {str(routelocations[point].location_fk.closed)}'
                else:
                  closed = '<br>Closed: Not Recorded'
                
                label = '<a href="https://en.wikipedia.org/' \
                + str(routelocations[point].location_fk.wikislug) \
                + '"target="_blank"> ' \
                + str(routelocations[point].location_fk.wikiname) \
                + '</a>' \
                + opened \
                + closed 

                label_html = folium.Html(label, script=True)
                label = folium.Popup(label_html, max_width=2650)
                coords_tuple = (routelocations[point].location_fk.geometry.y, routelocations[point].location_fk.geometry.x)
                folium.Marker(location = coords_tuple, popup= label, tooltip=str(routelocations[point].location_fk.wikiname)).add_to(marker_cluster)

            figure = folium.Figure()
            m.add_to(figure)     
            figure.render()

    context =  {"map": figure, "route": route.name, "wikipage": route_page }
    return render(request, 'locations/routemap_folium.html', context)

def routemap_storymap(request, route_id):
    import markdown
    import wikipediaapi
    slide_list = []
    storymap_json = None
    route = Route.objects.get(id=route_id)
    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict={}
    slide_dict['location_line'] = "true"
    slide_dict['media'] = {}
    slide_dict['media']['caption'] = ""
    slide_dict['media']['credit'] = ""
    slide_dict['media']['url'] = ""
    slide_dict['text'] = {}
    slide_dict['text']['headline'] = route.name
    slide_dict['text']['text'] = ""

    wikislug = route.wikipedia_slug.replace('/wiki/', '')
    pagename= wikislug.replace('_', ' ')
    import urllib
    pagename = urllib.parse.unquote(pagename, encoding='utf-8', errors='replace')
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    
    if wikislug and wiki_wiki.page(wikislug).exists:
        text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
        slide_dict['text'] = {'text': text_array[0], 'headline': route.name}
    else:
        slide_dict['text'] = {'headline': route.name, 'text': ""}


    slide_dict['type'] = "overview"
    slide_list.append(slide_dict)


    routemaps = route.wikipedia_routemaps.all()
    for routemap in routemaps:
      routelocations = RouteLocation.objects.filter(routemap=routemap.id)
      for routelocation in routelocations:
        if routelocation.location_fk != None:
          try:
            slide_dict={}
            slide_dict['background'] = {}
            slide_dict['background']['url'] = ""
            slide_dict['location'] = {}
            slide_dict['location']['lat'] = routelocation.location_fk.geometry.y
            slide_dict['location']['lon'] = routelocation.location_fk.geometry.x
            slide_dict['location']['zoom'] = "12"
            slide_dict['media'] = {}
            slide_dict['media']['caption'] = ""
            slide_dict['media']['credit'] = ""
            slide_dict['media']['url'] = ""
            slide_dict['text'] = {}
            slide_dict['text']['headline'] = routelocation.location_fk.wikiname

            html_string = markdown.markdown(routelocation.label.replace('/wiki/', 'https://en.wikipedia.org/wiki/'))
            slide_dict['text']['text'] = html_string.replace('"', '\'')

            wikislug = routelocation.location_fk.wikislug.replace('/wiki/', '')
            pagename= wikislug.replace('_', ' ')
            wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
            
            if wikislug and wiki_wiki.page(wikislug).exists:
                text_array = wiki_wiki.page(wikislug).text.split('<h2>References</h2>')
                slide_dict['text'] = {'text': text_array[0], 'headline': pagename}
            else:
                slide_dict['text'] = {'headline': pagename, 'text': html_string}

            slide_list.append(slide_dict)
          except Exception as e:
            print(e)

      #Create a dictionary in the required JSON format, including the dictionary list of slides
      routemap_dict = {"storymap":
        {"attribution": "Paul Frost",
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

      # Routemaps uses the same template as storymaps
    print(storymap_json)
    return render(request, 'locations/storymap.html', {'storymap_json':storymap_json})

def osm_rail_map_select(request):

    if request.method == 'POST':
        selection_criteria = OSMRailMapSelectForm(request.POST)

        if selection_criteria.is_valid():
            if str(selection_criteria.cleaned_data['itemAltLabel']):
                elrs = ELR.objects.filter(itemAltLabel__icontains=selection_criteria.cleaned_data['itemAltLabel']).order_by('itemAltLabel')
                errors = None
            elif str(selection_criteria.cleaned_data['itemLabel']) != 'None':
                elrs = ELR.objects.filter(itemLabel__icontains=selection_criteria.cleaned_data['itemLabel']).order_by('itemAltLabel')
                errors = None
        else:
            errors = selection_criteria.errors or None
            elrs = ELR.objects.order_by('itemAltLabel')

    else:
        selection_criteria = OSMRailMapSelectForm()
        errors = selection_criteria.errors or None
        elrs = ELR.objects.order_by('itemAltLabel')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'elrs': elrs}
    return render(request, 'locations/map_osm_lines_select.html', context)

def geojson_boundbox(features):

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

def osm_rail_map(request, elr_id):
    
    import folium
    import requests
    import osm2geojson

    elr = ELR.objects.get(id=elr_id)

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    area["ISO3166-1"="GB"][admin_level=2];
    (
      way(area)["ref"="{elr.itemAltLabel}"];
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Convert OSM json to Geojson. Warning ! The osm2geojson utility is still under development
    geojson = osm2geojson.json2geojson(data)

    figure = None

    if len(geojson['features']) != 0:
        figure = generate_folium_map(folium, geojson, elr)
    context =  {"map": figure, "route": f'{elr.itemAltLabel}: {elr.itemLabel}' }
    return render(request, 'locations/map_osm_lines.html', context)

def generate_folium_map(folium, geojson, elr):
    m = folium.Map(zoom_start= 13, prefer_canvas=True, height=500)
    folium.FitBounds(geojson_boundbox(geojson['features'])).add_to(m)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(m)
    folium.TileLayer('http://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
    attr='<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
    # Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
    min_zoom = 12, max_zoom = 19).add_to(m)
    # folium.GeoJson(geojson, name=elr.itemAltLabel).add_to(m)
    result = folium.Figure()
    m.add_to(result)
    result.render()

    return result

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
        attr='<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
        # Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
        min_zoom = 12, max_zoom = 19).add_to(m)
        folium.GeoJson(data=track_details["geometry"], popup=track_details["id"]).add_to(m)
 
        # folium.Icon(icon="cloud").add_to(m)
        # folium.Marker(track_details["geometry"][0], popup=track_details["id"][0], tooltip=tooltip,).add_to(m)

        m.add_to(figure)
        figure.render()
        return {"map": figure}

def location_timeline(request):
  location_events = LocationEvent.objects.order_by('datefield')

  events = []
  forlooplimiter = 0
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
  depots = Depot.objects.order_by('depot', 'datefield_start')
  events = []
  forlooplimiter = 0

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