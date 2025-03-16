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

            wikislug = location.get("wikislug", "")
            wiki_wiki = wikipediaapi.Wikipedia(
                user_agent="github/prpfr3 TPAM",
                language="en",
                extract_format=wikipediaapi.ExtractFormat.HTML,
            )

            html_string = markdown.markdown(f"https://en.wikipedia.org/wiki/{wikislug}")
            page = wiki_wiki.page(wikislug)

            if wikislug and page.exists:
                text_array = page.text.split("<h2>References</h2>")
                text = text_array[0]
            else:
                text = html_string

            location_slide["text"] = {
                "text": text.replace('"', "'"),
                "headline": location.get("name", ""),
            }

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
            # "map_type": "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
            # "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
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


def fetch_route_locations(route):
    routemaps = route.wikipedia_routemaps.all()

    if not routemaps:
        return None  # No routemaps found, return None

    sql = """
    SELECT DISTINCT ON (a."id") 
        a."id", a."wikiname", a."wikislug", a."opened", a."closed", a."name",
        ST_Y(ST_CENTROID(a.geometry)),
        ST_X(ST_CENTROID(a.geometry)),
        a."media_url"
    FROM "locations_location" AS a
    INNER JOIN "locations_routelocation" AS b
        ON (a."id" = b."location_fk_id")
    WHERE a."geometry" IS NOT NULL AND b."routemap_id" = %s
    ORDER BY a."id";  -- Ensure consistent ordering for DISTINCT ON"""

    results = []
    for routemap in routemaps:
        results.extend(
            execute_sql(sql, [routemap.id])
        )  # Execute SQL for each routemap and collect results

    return (
        results if results else None
    )  # Return all collected results or None if no results


def routes_mapdata_extract(routes):
    elr_geojsons = []
    route_locations = []

    for route in routes:
        route_locations.extend(fetch_route_locations(route) or [])
        elr_geojsons.extend(
            elr.geojson
            for elr in route.elrs.all()
            if elr.geojson and elr.geojson.get("features")
        )

    return elr_geojsons or None, route_locations or None


def folium_map_geojson(elr_geojsons, locations, height=650, width=1100):
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

    # See Overlay tab of NLS Maps for map county options
    folium.TileLayer(
        "https://mapseries-tilesets.s3.amazonaws.com/25_inch/sussex/{z}/{x}/{y}.png",
        attr='<a href="https://maps.nls.uk/"> \
            OS 25 1892-1914 maps Reproduced with the permission of the National Library of Scotland</a>',
        name="NLS 25inch (Sussex only)",
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

    if elr_geojsons:
        for elr_geojson in elr_geojsons:
            # Iterate through features and collapse tags to properties
            for feature in elr_geojson["features"]:
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
                style="""
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 3px;
                    box-shadow: 3px;
                    font-size: 20px;
                    padding: 5px;
                """,
            ),
            popup=folium.GeoJsonPopup(fields=["name"], aliases=[""], localize=True),
            name="Route",
            style_function=lambda x: {
                "color": (
                    "#78491c" if x["properties"].get("ref") == "NSM" else "#c94f1a"
                ),
                **(
                    {"dashArray": "30 15"}
                    if x["properties"].get("ref") == "NSM"
                    else {}
                ),
            },
            highlight_function=lambda x: {"weight": 6},
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
                    url = reverse("locations:location", args=[location["id"]])
                    name = f'<a href="{url}" target="_blank">{location["wikiname"]}</a>'
                elif location["name"] != None:
                    name = f'{location["name"]}'
                else:
                    name = f'{str(location["st_y"])," ",str(location["st_x"])}'

                label_html = folium.Html(f"{name}{opened}{closed}", script=True)

                if location["media_url"]:  # i.e. if there is a media_url
                    img_html = (
                        f'<img src="{location["media_url"]}" width="230" height="172"><br/>'
                        or None
                    )
                else:
                    img_html = ""

                popup = f"""
                    <div style='font-size: 20px;'>{img_html}<span>{name}{opened}{closed}</span></div>
                    """

                popup = folium.Popup(popup, max_width=2650)
                coords_tuple = (location["st_y"], location["st_x"])
                folium.Marker(
                    location=coords_tuple, popup=popup, tooltip=str(name)
                ).add_to(marker_cluster)

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


def folium_map_timeline(elr_geojsons, locations, height=650, width=1100):
    import folium
    from folium.plugins import MarkerCluster, MiniMap

    from folium.plugins import Timeline, TimelineSlider
    from folium.features import GeoJsonPopup, GeoJsonTooltip
    from datetime import datetime

    # Get the current date in ISO 8601 format
    current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

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

    # See Overlay tab of NLS Maps for map county options
    folium.TileLayer(
        "https://mapseries-tilesets.s3.amazonaws.com/25_inch/kent/{z}/{x}/{y}.png",
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

    if elr_geojsons:
        for elr_geojson in elr_geojsons:
            # Iterate through features and collapse tags to properties
            for feature in elr_geojson["features"]:
                properties = feature["properties"]
                tags = properties.pop("tags", {})  # Remove 'tags' key and get its value
                properties.pop("nodes", {})
                properties.update(tags)  # Add tags to properties

                # Ensure "times" is setup for the Timelineslider in ISO format and convert if necessary
                if "opened" in properties and isinstance(properties["opened"], str):
                    try:
                        properties["start"] = (
                            f'{properties["opened"][:10]}T00:00:00Z'  # Ensure it's in YYYY-MM-DD format
                        )
                    except Exception as e:
                        print(f"Error processing 'opened' date: {e}")
                        properties["start"] = None

                if "closed" in properties and isinstance(properties["closed"], str):
                    try:
                        properties["end"] = (
                            f'{properties["closed"][:10]}T00:00:00Z'  # Ensure it's in YYYY-MM-DD format
                        )
                    except Exception as e:
                        print(f"Error processing 'closed' date: {e}")
                        properties["closed"] = None
                else:
                    properties["end"] = f"{current_date}"

                if properties.get("name") is not None:
                    properties["tooltip"] = properties["name"]
                else:
                    properties["tooltip"] = "No Name"

                # ADDED TO SOLVE THE 'NO POPUP' ISSUE. DOESN'T ADD ANY EXTRA INFO OVER THE TOOLTIP
                if properties.get("name") is not None:
                    properties["popup"] = properties["name"]
                else:
                    properties["popup"] = "No Name"

                # Accumulate features
                # Only include features with a valid "opened" date
                if properties.get("opened") is not None:
                    all_features.append(feature)

    if locations:
        marker_cluster = MarkerCluster(name="All Locations", show=False).add_to(m)

        for location in locations:

            if not location.get("st_x") or not location.get("st_y"):
                continue  # Skip this iteration if either 'st_x' or 'st_y' is missing

            if location["name"] != None:
                name = f'{location["name"]}'
            else:
                name = f'{str(location["st_y"])," ",str(location["st_x"])}'

            if location["wikislug"] != None:
                try:
                    url = reverse("locations:location", args=[location["id"]])
                    popup_name = (
                        f'<a href="{url}" target="_blank">{location["wikiname"]}</a>'
                    )
                except Exception as e:
                    # print(location["wikislug"], location["id"], e)
                    pass
            else:
                popup_name = name

            if location["media_url"]:
                img_html = (
                    f'<img src="{location["media_url"]}" width="230" height="172"><br/>'
                    or None
                )
            else:
                img_html = ""

            opened = (
                f'<br>Opened {str(location["opened"])}' if location["opened"] else ""
            )
            closed = (
                f'<br>Closed {str(location["closed"])}' if location["closed"] else ""
            )

            popup = f"""<div style='font-size: 20px;'>{img_html}<span>{popup_name}{opened}{closed}</span></div>"""

            all_locations_popup = folium.Popup(popup, max_width=2650)
            coords_tuple = (location["st_y"], location["st_x"])

            folium.Marker(
                location=coords_tuple,
                popup=all_locations_popup,
                tooltip=popup,
            ).add_to(marker_cluster)

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
            else:
                # For first time calculation
                bounding_box = [coords_tuple, coords_tuple]

            if (
                location["st_y"]
                and location["st_x"]
                and (location["opened"] is not None and len(location["opened"]) == 10)
            ):
                # Ensure dates for timeline are in YYYY-MM-DD format
                try:
                    timeline_date_start = f'{location["opened"]}T00:00:00Z'
                except Exception as e:
                    print(f"Error processing 'opened' date: {e}")
                    timeline_date_start = None

                if location["closed"] is not None and len(location["closed"]) == 10:
                    try:
                        timeline_date_end = f'{location["closed"]}T00:00:00Z'
                    except Exception as e:
                        print(f"Error processing 'closed' date: {e}")
                        timeline_date_end = f"{current_date}"
                else:
                    timeline_date_end = f"{current_date}"

                timeline_point_feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            location["st_x"],
                            location["st_y"],
                        ],
                    },
                    "properties": {
                        "name": name,
                        "wikislug": location["wikislug"],
                        "opened": location["opened"],
                        "closed": location["closed"],
                        "start": timeline_date_start,
                        "end": timeline_date_end,
                        "popup": popup,
                        # "icon": DivIcon(html=icon_html), # Does not work as DivIcon is not serializable
                    },
                }

                all_features.append(timeline_point_feature)

    # Set "name" property to "No Name" for features without a name
    for feature in all_features:
        properties = feature.get("properties", {})
    if "name" not in properties:
        properties["name"] = "No Name"

    # Turn all_features back into GeoJSON data
    locations_geojson = {"type": "FeatureCollection", "features": all_features}
    geojson_layer = folium.GeoJson(
        locations_geojson,
    )
    bounding_box = geojson_layer.get_bounds()

    # Add the Timeline plugin layer
    timeline = Timeline(
        locations_geojson,
        period="P1Y",  # (i.e. 1 Year Period)
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options="YYYY-MM-DD",
        time_slider_drag_update=True,
        duration="P1M",  # Duration for playback (if auto-play is enabled)
        name="Timeline Layer",
    )

    GeoJsonPopup(
        fields=["popup"],
        aliases=[""],
        localize=True,
        style="""
        background-color: white;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        font-size: 20px;
        padding: 5px;
        """,
    ).add_to(timeline)

    GeoJsonTooltip(
        fields=["name"],
        aliases=[""],
        labels=True,
        localize=True,
        sticky=False,
        style="""
                background-color: white;
                border: 1px solid black;
                border-radius: 3px;
                box-shadow: 3px;
                font-size: 20px;
                padding: 5px;
            """,
    ).add_to(timeline)

    # Wrap the timeline in a GeoJson layer to give it a name
    timeline_layer = folium.FeatureGroup(name="Timeline Layer", show=True).add_to(m)
    timeline.add_to(timeline_layer)

    # Add the TimelineSlider to the map
    TimelineSlider(
        auto_play=False,
        show_ticks=True,
        date_options="YYYY",
        enable_keyboard_controls=True,
        playback_duration=30000,
        show=False,
    ).add_timelines(timeline).add_to(m)

    # Add custom JavaScript to hide the slider initially - not working
    slider_init_js = """
        <script>
        // Hide the timeline slider on page load
        document.querySelector('.range-control').style.display = 'none';

        // Function to toggle slider visibility based on layer control
        function toggleSliderVisibility() {
            var layerControl = document.querySelectorAll('input.leaflet-control-layers-selector');
            layerControl.forEach(function(input) {
                input.addEventListener('change', function() {
                    if (input.checked) {
                        document.querySelector('.range-control').style.display = 'block';
                    } else {
                        document.querySelector('.range-control').style.display = 'none';
                    }
                });
            });
        }

        // Call the function on map load
        toggleSliderVisibility();
        </script>
    """

    # Add the custom script to the map
    m.get_root().html.add_child(folium.Element(slider_init_js))

    # Adjust formatting on timeline slider (Not working - see Chatgpt for suggestions ?)

    custom_css = """
    <style>
        /* Targeting the specific elements for the timeline dates */
        .leaflet-timeline-control .time-text {
            font-size: 200px !important;  /* Adjust font size */
            font-weight: bold !important;  /* Make it bold */
            color: black !important;  /* Change color */
        }

        .leaflet-timeline-control .time-slider {
            background-color: yellow !important;  /* Adjust the background color of the slider */
        }

        .leaflet-timeline-control .leaflet-bar {
            background-color: yellow !important;  /* Customize the background of the control bar */
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    m.fit_bounds(bounding_box)
    folium.LayerControl().add_to(m)
    minimap = MiniMap(position="topright")
    m.add_child(minimap)
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()
    map_html = figure._repr_html_()
    return map_html


def folium_map_location(latitude, longitude, tooltip_text, height=600, width=1000):
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

    # See Overlay tab of NLS Maps for map county options
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
