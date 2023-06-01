def osm_elr_fetch(elr):

    import osm2geojson
    import requests

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
        way(area)["ref"="{elr}"]->.elr;
        node(around.elr:50)["railway"];
        way(around.elr:50)["railway"];
        out geom;
        """

    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Convert OSM json to Geojson. Warning ! The osm2geojson utility is still under development
    return osm2geojson.json2geojson(data)


def generate_storymap(headline, text, locations):

    import json
    import markdown
    import wikipediaapi

    # Add the first slide to a dictionary list from the SlideHeader Object
    header_slide = \
        {"location_line": "true",
         "type": "overview",
         "media":
            {"caption": "",
             "credit": "",
             "url": ""},
         "text":
            {"headline": headline,
             "text": text}
         }

    slide_list = [header_slide]

    for location in locations:
        try:
            location_slide = \
                {"background":
                    {"url": ""},
                 "location":
                    {"lat": location[5],  # location.geometry.y, # when using ORM rather than SQL
                     # location.geometry.x, # when using ORM rather than SQL
                     "lon": location[6],
                     "zoom": "12"},
                 "media":
                    {"caption": location[7],
                     "credit": location[8],
                     "url": location[9]},
                 "text":
                    # location.wikiname # when using ORM rather than SQL
                    {"headline": location[0]}
                 }

            # location.wikislug # when using ORM rather than SQL
            html_string = markdown.markdown(
                f'https://en.wikipedia.org/wiki/{location[1]}')
            location_slide['text']['text'] = html_string.replace('"', '\'')

            # location.wikislug # when using ORM rather than SQL
            wikislug = location[1].replace('/wiki/', '')
            pagename = wikislug.replace('_', ' ')
            wiki_wiki = wikipediaapi.Wikipedia(
                language='en', extract_format=wikipediaapi.ExtractFormat.HTML)

            if wikislug and wiki_wiki.page(wikislug).exists:
                text_array = wiki_wiki.page(
                    wikislug).text.split('<h2>References</h2>')
                location_slide['text'] = {
                    'text': text_array[0], 'headline': pagename}
            else:
                location_slide['text'] = {
                    'text': html_string, 'headline': pagename}

            slide_list.append(location_slide)
        except Exception as e:
            print(e)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    routemap_dict = \
        {"storymap":
            {"attribution": "Wikipedia / OpenStreetMaps",
             "call_to_action": True,
             "call_to_action_text": "A Routemap",
             "map_as_image": False,
             "map_subdomains": "",
             # OSM Railway Map Type alternative shows all ELRs but not the OSM basemap. Also some zooming issues.
             # "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
             "map_type": "osm:standard",
             "slides": slide_list,
             "zoomify": False
             }
         }

    return (json.dumps(routemap_dict))


def execute_sql(sql, parameters):
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameters)
            result = cursor.fetchall()

    except Exception as e:
        print(e)

    return result


"""
Function for use when using ORM & GeoDjango which required GDAL
An alternative to  function generate_folium_map sql
"""
# def generate_folium_map(geojson, title, locations ):

#     import folium
#     from django.contrib.gis.db.models import Extent
#     from folium.plugins import MarkerCluster

#     # By default folium will use OpenStreetMap as the baselayer. 'tiles=None' switches the default off
#     m = folium.Map(zoom_start= 13, prefer_canvas=True, height=500)

#     """
#     Use OpenRailwayMap as the baselayer to give a better rendering of the line
#     Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
#     """
#     folium.TileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
#         attr='<a href="https://www.openstreetmap.org/copyright"> \
#             © OpenStreetMap contributors</a>, \
#             Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
#             CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap', \
#         name = "OpenRailwayMap", \
#         min_zoom = 2, max_zoom = 19).add_to(m)

#     # If there is geojson (i.e. OSM) input then use it to calculate the boundary box.
#     # If not calculate the boundary box from the locations co-ordinates
#     if geojson:
#         folium.GeoJson(geojson, name=title).add_to(m)
#         bound_box = geojson_boundbox(geojson['features'])
#     else:
#         extent = locations.aggregate(Extent('geometry'))
#         bound_box = [[extent['geometry__extent'][1],
#             extent['geometry__extent'][0]],
#             [extent['geometry__extent'][3],
#             extent['geometry__extent'][2]]]

#     folium.FitBounds(bound_box).add_to(m)

#     marker_cluster = MarkerCluster(name="Locations").add_to(m)

#     for location in locations:
#         if location.geometry:

#             if str(location.opened) != 'None':
#                 opened = f'<br>Opened {str(location.opened)}'
#             else:
#                 opened = ''

#             if str(location.closed) != 'None':
#                 closed = f'<br>Closed {str(location.closed)}'
#             else:
#                 closed = ''

#             if str(location.wikislug) != 'None':
#                 name = f'<a href="https://en.wikipedia.org//wiki/{str(location.wikislug)}"target="_blank"> \
#                 {str(location.wikiname)}</a>'
#             else:
#                 name = f'{str(location.name)}'

#             label_html = folium.Html(f'{name}{opened}{closed}', script=True)
#             label = folium.Popup(label_html, max_width=2650)
#             coords_tuple = (location.geometry.y, location.geometry.x)
#             folium.Marker(location = coords_tuple, popup= label, tooltip=str(name)).add_to(marker_cluster)

#     folium.LayerControl().add_to(m)
#     figure = folium.Figure()
#     m.add_to(figure)
#     figure.render()

#     return figure


def generate_folium_map_sql(geojsons, title, locations, bound_box):

    import folium
    from folium.plugins import MarkerCluster

    # By default folium will use OpenStreetMap as the baselayer. 'tiles=None' switches the default off
    m = folium.Map(zoom_start=13, prefer_canvas=True, height=500)

    """
    Use OpenRailwayMap as the baselayer to give a better rendering of the line
    Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
    """
    folium.TileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png',
                     attr='<a href="https://www.openstreetmap.org/copyright"> \
            © OpenStreetMap contributors</a>, \
            Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
            CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
                     name="OpenRailwayMap",
                     min_zoom=2, max_zoom=19).add_to(m)

    if geojsons:
        for geojson in geojsons:
            folium.GeoJson(geojson, name=title).add_to(m)

    folium.FitBounds(bound_box).add_to(m)

    marker_cluster = MarkerCluster(name="Locations").add_to(m)

    for location in locations:
        # i.e. if a y-coordinate is present (if not then it can't be mapped)
        if location[5]:

            if str(location[2]) != 'None':
                opened = f'<br>Opened {str(location[2])}'
            else:
                opened = ''

            if str(location[3]) != 'None':
                closed = f'<br>Closed {str(location[3])}'
            else:
                closed = ''

            if str(location[1]) != 'None':
                name = f'<a href="https://en.wikipedia.org//wiki/{str(location[1])}"target="_blank"> \
                {str(location[0])}</a>'
            elif str(location[4]) != 'None':
                name = f'{str(location[4])}'
            else:
                name = f'{str(location[5])}'

            label_html = folium.Html(f'{name}{opened}{closed}', script=True)

            if location[7]:  # i.e. if there is a media_url
                img_html = f'<img src="{location[7]}" width="230" height="172">' or None
            else:
                img_html = ''

            label_html = f"""
            <div>{img_html}<br/><span>{name}{opened}{closed}</span></div>"""

            label = folium.Popup(label_html, max_width=2650)
            coords_tuple = (location[5], location[6])
            folium.Marker(location=coords_tuple, popup=label,
                          tooltip=str(name)).add_to(marker_cluster)

    folium.LayerControl().add_to(m)
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()
    return figure


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

    return ([[min(ycoords), min(xcoords)],
            [max(ycoords), min(xcoords)],
             [max(ycoords), max(xcoords)],
             [min(ycoords), max(xcoords)]])
