from .forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
from django.views import View


class RegionSelectView(View):
    template_name = "locations/region_select.html"
    redirect_view_name = None

    def get_redirect_view_name(self):
        if self.redirect_view_name is None:
            raise NotImplementedError("Subclasses must provide a redirect_view_name.")
        return self.redirect_view_name

    def get(self, request):
        region_form = RegionChoiceForm()
        context = {"region_form": region_form}
        return render(request, self.template_name, context)

    def post(self, request):
        region_form = RegionChoiceForm(request.POST)
        if region_form.is_valid():
            geo_area = region_form.cleaned_data["regions"]
            redirect_view_name = self.get_redirect_view_name()
            redirect_url = reverse(redirect_view_name, args=[geo_area])

            # This class can be called by a function or a class, either of which
            # provides a redirect view. If called by a CBV then kwargs needs to be returned
            # Check if the redirect_view is a class-based view
            if callable(redirect_view_name):
                view_name = redirect_view_name.__name__
                view_args = ()
                view_kwargs = {}
                url = reverse(view_name, args=view_args, kwargs=view_kwargs)
                redirect_view_name = resolve(url).url_name

            return HttpResponseRedirect(redirect_url)
        else:
            context = {"region_form": region_form}
            return render(request, self.template_name, context)


def osm_elr_fetch(elr, bbox):
    import osm2geojson
    import requests

    overpass_url = "http://overpass-api.de/api/interpreter"

    # Use this query to get nearby features as well as the ELR Geojson itself

    overpass_query = f"""
        [out:json];
        area["ISO3166-1"="GB"][admin_level=2]->.a;
        way(area.a)[ref="{elr}"]->.w;
        node(around.w:50)["railway"];
        (._; .w;);
        out geom;
        """

    # If a bounding box has been pre-specified restrict the overpass ELR query to that bounding box. Otherwise get the whole of the ELR but restricting it to Great Britain so as not to pick up none British ELRs
    if bbox:
        overpass_query = f"""
            [out:json];
            (way["ref"="{elr}"]["railway"]{bbox};
            );
            out geom;
            """
    else:
        overpass_query = f"""
            [out:json];    
            area["ISO3166-1"="GB"][admin_level=2]->.a;
            way(area.a)["ref"="{elr}"]["railway"];
            out geom;
            """
    response = requests.get(overpass_url, params={"data": overpass_query})
    data = response.json()

    # Convert OSM json to Geojson. Warning ! The osm2geojson utility is still under development
    return osm2geojson.json2geojson(data)


def generate_storymap(headline, text, locations):
    import json
    import markdown
    import wikipediaapi

    # Add the first slide to a dictionary list from the SlideHeader Object
    header_slide = {
        "location_line": "true",
        "type": "overview",
        "media": {"caption": "", "credit": "", "url": ""},
        "text": {"headline": headline, "text": text},
    }

    slide_list = [header_slide]

    for location in locations:
        try:
            location_slide = {
                "background": {"url": ""},
                "location": {
                    "lat": location.get("st_y"),
                    "lon": location.get("st_x"),
                    "zoom": "12",
                },
                "media": {
                    "caption": location.get("media_caption"),
                    "credit": location.get("media_credit"),
                    "url": location.get("media_url"),
                },
                "text": {"headline": location.get("wikiname")},
            }

            html_string = markdown.markdown(
                f"https://en.wikipedia.org/wiki/{location.get('wikislug')}"
            )
            location_slide["text"]["text"] = html_string.replace('"', "'")

            wikislug = location.get("wikislug").replace("/wiki/", "")
            pagename = wikislug.replace("_", " ")
            wiki_wiki = wikipediaapi.Wikipedia(
                user_agent="github/prpfr3 TPAM",
                language="en",
                extract_format=wikipediaapi.ExtractFormat.HTML,
            )

            if wikislug and wiki_wiki.page(wikislug).exists:
                text_array = wiki_wiki.page(wikislug).text.split("<h2>References</h2>")
                location_slide["text"] = {"text": text_array[0], "headline": pagename}
            else:
                location_slide["text"] = {"text": html_string, "headline": pagename}

            slide_list.append(location_slide)
        except Exception as e:
            print(e)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    routemap_dict = {
        "storymap": {
            "attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "View Route Locations",
            "map_as_image": False,
            "map_subdomains": "",
            # OSM Railway Map Type alternative shows all ELRs but not the OSM basemap. Also some zooming issues.
            #  "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    return json.dumps(routemap_dict)


def execute_sql_nofieldnames(sql, parameters):
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameters)
            result = cursor.fetchall()

    except Exception as e:
        print(e)

    return result


def execute_sql(sql, parameters):
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameters)

            # Get the column names from the description attribute
            columns = [col[0] for col in cursor.description]

            # Fetch all rows from the result
            rows = cursor.fetchall()
            # Create a list of dictionaries where each dictionary represents a row
            result = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(e)

    return result


# Function to format tags as an HTML list
def format_tags_as_list(tags_dict):
    formatted_tags = "<ul>"
    for key, value in tags_dict.items():
        formatted_tags += f"<li>{key}: {value}</li>"
    formatted_tags += "</ul>"
    return formatted_tags


def fetch_locations(route):
    routemaps = route.wikipedia_routemaps.all()

    if len(routemaps) == 0:
        return None  # No routemaps found, return None

    sql = """
        SELECT a."wikiname", a."wikislug", a."opened", a."closed", a."name",
            ST_Y(ST_CENTROID(a.geometry)),
            ST_X(ST_CENTROID(a.geometry)),
            a."media_url"
        FROM "locations_location" AS a
        INNER JOIN "locations_routelocation" AS b
            ON (a."id" = b."location_fk_id")
        WHERE a."geometry" IS NOT NULL AND b."routemap_id" = %s;
    """

    return execute_sql(sql, [routemaps[0].id])


def routes_mapdata_extract(routes):
    elr_geojsons = None
    locations = None
    figure = None
    for route in routes:
        route_locations = fetch_locations(route)
        if route_locations and locations is None:
            locations = []
        if route_locations:
            locations.extend(route_locations)

        if elrs := route.elrs.all():
            for elr in elrs:
                if elr.geodata and len(elr.geodata["features"]) > 0:
                    if elr_geojsons is None:
                        elr_geojsons = []
                    elr_geojsons.append(elr.geodata)

    return elr_geojsons, locations


def route_section_locations_extract(route):
    locations = None
    figure = None

    route_locations = fetch_locations(route)
    if route_locations:
        for route_location in route_locations:
            if locations is None:
                locations = []
            locations.append(route_location)

    return locations


def folium_map_geojson(geojsons, locations, height=600, width=1000):
    import folium
    from folium.plugins import MarkerCluster, MiniMap

    # By default folium will use OpenStreetMap as the baselayer. 'tiles=None' switches the default off
    m = folium.Map(
        zoom_start=13,  # Initial zoom level (will be overridden by fit_bounds)
        location=[
            51.5072,
            -0.1276,
        ],  # Initial location of London (will be overridden by fit_bounds)
        prefer_canvas=True,
        height=height,
        width=width,
        tiles=None,
    )

    # Add OpenStreetMap as a tile layer with a name
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="OpenStreetMap",
        overlay=True,
    ).add_to(m)

    folium.TileLayer(
        "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
        attr='<a href="https://maps.nls.uk/"> \
            OS 25 1892-1914 maps Reproduced with the permission of the National Library of Scotland</a>',
        name="NLS 25inch (Yorkshire only)",
        min_zoom=2,
        max_zoom=19,
        overlay=True,
        show=False,
    ).add_to(m)

    """
    Use OpenRailwayMap as the baselayer to give a better rendering of the line
    Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
    """
    folium.TileLayer(
        "https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
        attr='<a href="https://www.openstreetmap.org/copyright"> \
            © OpenStreetMap contributors</a>, \
            Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
            CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
        name="OpenRailwayMap",
        min_zoom=2,
        max_zoom=19,
        overlay=True,
        show=False,
    ).add_to(m)

    all_features = []
    bounding_box = None

    if geojsons:
        for geojson in geojsons:
            # Iterate through features and collapse tags to properties
            for feature in geojson["features"]:
                properties = feature["properties"]
                tags = properties.pop("tags", {})  # Remove 'tags' key and get its value
                properties.pop("nodes", {})
                properties.update(tags)  # Add tags to properties

                # Accumulate features
                all_features.append(feature)

        # Set "name" property to "No Name" for features without a name
        # Without this the folium tooltip feature throws an error
        for feature in all_features:
            properties = feature.get("properties", {})
            if "name" not in properties:
                properties["name"] = "No Name"

        # filename = "SRR.geojson"
        # # Write the GeoJSON to a file
        # all_features = {"type": "FeatureCollection", "features": all_features}
        # with open(filename, "w") as f:
        #     # json.dumps(all_features)
        #     json.dump(all_features, f, indent=4)
        #     print("GeoJSON saved to", filename)

        geojson_layer = folium.GeoJson(
            {"type": "FeatureCollection", "features": all_features},
            tooltip=folium.GeoJsonTooltip(
                fields=["name"],
                aliases=[""],
                labels=True,
                localize=True,
                sticky=False,
            ),
            popup=folium.GeoJsonPopup(fields=["name"], aliases=[""], localize=True),
            name="Route",
            # style_function=lambda x: {
            #     "color": "#78491c"
            #     if x["properties"].get("ref") == "NHB"
            #     else "#c94f1a"
            # },
            # Weight determines the width of lines, fillColor has no effect on ways
            highlight_function=lambda x: {"weight": 6, "fillColor": "yellow"},
            smooth_factor=2,
            show=True,  # Show the route on the map initially
        ).add_to(m)

        # Calculate the bounding box of the GeoJSON data
        bounding_box = geojson_layer.get_bounds()

    if locations:
        marker_cluster = MarkerCluster(name="Route Locations", show=False).add_to(m)

        for location in locations:
            # i.e. if a y-coordinate is present (if not then it can't be mapped)
            if location["st_y"]:
                opened = (
                    f'<br>Opened {str(location["opened"])}'
                    if str(location["opened"]) != "None"
                    else ""
                )
                closed = (
                    f'<br>Closed {str(location["closed"])}'
                    if str(location["closed"]) != "None"
                    else ""
                )

                if location["wikislug"] != None:
                    name = f'<a href="https://en.wikipedia.org//wiki/{str(location["wikislug"])}"target="_blank"> \
                    {str(location["wikiname"])}</a>'
                elif location["name"] != None:
                    name = f'{location["name"]}'
                else:
                    name = f'{str(location["st_y"])," ",str(location["st_x"])}'

                label_html = folium.Html(f"{name}{opened}{closed}", script=True)

                if location["media_url"]:  # i.e. if there is a media_url
                    img_html = (
                        f'<img src="{location["media_url"]}" width="230" height="172">'
                        or None
                    )
                else:
                    img_html = ""

                label_html = f"""
                    <div>{img_html}<br/><span>{name}{opened}{closed}</span></div>
                    """

                label = folium.Popup(label_html, max_width=2650)
                coords_tuple = (location["st_y"], location["st_x"])
                # Note that tooltip does not accept images, only text
                folium.Marker(
                    location=coords_tuple, popup=label, tooltip=str(name)
                ).add_to(marker_cluster)

                coords_tuple = (location["st_y"], location["st_x"])

                if bounding_box:
                    min_lat, min_lon = bounding_box[0]
                    max_lat, max_lon = bounding_box[1]

                    min_lat, min_lon = min(coords_tuple[0], min_lat), min(
                        coords_tuple[1], min_lon
                    )
                    max_lat, max_lon = max(coords_tuple[0], max_lat), max(
                        coords_tuple[1], max_lon
                    )

                    bounding_box = [
                        (min_lat, min_lon),
                        (max_lat, max_lon),
                    ]
                else:  # For first set of location co-ordinates where there is no ELR Geojson data
                    bounding_box = [coords_tuple, coords_tuple]

    # format of bound_box is [(minimum latitude, minimum longitude]), [(maximum latitude, maximum longitude)]) i.e. south west, north east
    m.fit_bounds(bounding_box)

    folium.LayerControl().add_to(m)

    minimap = MiniMap()
    m.add_child(minimap)
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()
    map_html = figure._repr_html_()
    return map_html


def folium_map_latlong(latitude, longitude, tooltip_text, height=600, width=1000):
    import folium
    from folium.plugins import MiniMap

    # By default folium will use OpenStreetMap as the baselayer. 'tiles=None' switches the default off
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=17,
        prefer_canvas=True,
        height=height,
        width=width,
    )

    folium.TileLayer(
        "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
        attr='<a href="https://maps.nls.uk/"> \
            OS 25 1892-1914 maps Reproduced with the permission of the National Library of Scotland</a>',
        name="NLS 25inch",
        min_zoom=2,
        max_zoom=19,
    ).add_to(m)

    """
    Use OpenRailwayMap as the baselayer to give a better rendering of the line
    Minimum zoom setting of 12 gives about 40 miles/60 kms across the screen
    """
    folium.TileLayer(
        "https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
        attr='<a href="https://www.openstreetmap.org/copyright"> \
            © OpenStreetMap contributors</a>, \
            Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
            CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a> and OpenStreetMap',
        name="OpenRailwayMap",
        min_zoom=2,
        max_zoom=19,
    ).add_to(m)

    folium.Marker([latitude, longitude], tooltip=tooltip_text).add_to(m)

    folium.LayerControl().add_to(m)
    minimap = MiniMap()
    m.add_child(minimap)
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()
    map_html = figure._repr_html_()
    return map_html


# def merge_geojson_features():
#         # THIS FUNCTION NOT YET WORKING - DOES NOT ORDER CO-ORDINATES IN THE RIGHT SEQUENCE
#         import json

#         # Define the filename
#         # Group features based on "name" and "ref" properties
#         grouped_features = {}
#         for feature in all_features:
#             key = (feature["properties"]["name"], feature["properties"]["ref"])
#             if key not in grouped_features:
#                 grouped_features[key] = {
#                     "properties": feature["properties"],
#                     "geometries": [],
#                 }
#             grouped_features[key]["geometries"].append(feature["geometry"])

#         # Merge geometries and properties for features with the same "name" and "ref"
#         from shapely.geometry import Point, LineString
#         import numpy as np
#         import math

#         # Merge geometries and properties for features with the same "name" and "ref"
#         merged_features = []
#         for key, group in grouped_features.items():
#             merged_geometry = {
#                 "type": group["geometries"][0]["type"],
#                 "coordinates": [],
#             }
#             prev_coordinate = None
#             for geometry in group["geometries"]:
#                 points = geometry["coordinates"]
#                 if prev_coordinate is None:
#                     # If it's the first geometry, add the coordinates directly
#                     merged_geometry["coordinates"].extend(geometry["coordinates"])
#                     prev_coordinate = points[
#                         -1
#                     ]  # Set the last point as the previous coordinate
#                 else:
#                     distances = [math.dist(prev_coordinate, point) for point in points]
#                     min_distance_index = distances.index(min(distances))
#                     # Add the next closest coordinate and the subsequent coordinates
#                     merged_geometry["coordinates"].extend(
#                         points[min_distance_index:] + points[:min_distance_index]
#                     )
#                     prev_coordinate = points[
#                         -1
#                     ]  # Set the last point as the previous coordinate
#             merged_feature = {
#                 "type": "Feature",
#                 "geometry": merged_geometry,
#                 "properties": {"name": key[0], "ref": key[1]},
#             }
#             merged_features.append(merged_feature)

#         # Create a new GeoJSON FeatureCollection
#         # merged_geojson = {"type": "FeatureCollection", "features": merged_features}

#         # Save the merged GeoJSON to a file
#         filename = "SRR_optimised.geojson"
#         with open(filename, "w") as f:
#             json.dump(merged_features, f, indent=4)
