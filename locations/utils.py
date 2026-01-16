from .forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
from django.views import View

from datetime import datetime


def is_valid_yyyy_mm_dd(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except Exception:
        return False


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
    from storymaps.views import get_wikipedia_summary

    # Add the first slide to a dictionary list from the SlideHeader Object
    header_slide = {
        "location_line": "true",
        "type": "overview",
        "media": {"caption": "", "credit": "", "url": ""},
        "text": {"headline": headline, "text": text},
    }

    slide_list = [header_slide]

    for location in locations:

        slide_dict = {
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
        }

        wikislug = location.get("wikislug", "")
        slide_dict["text"] = {}
        slide_dict["text"]["headline"] = location.get("name", "") or None
        slide_dict["text"]["text"] = location.get("notes") or None

        if wikislug:
            url = f"https://en.wikipedia.org/wiki/{wikislug}"
            slide_dict["text"]["text"] = get_wikipedia_summary(url)
        else:
            slide_dict["text"]["text"] = ""

        slide_list.append(slide_dict)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    storymap_dict = {
        "storymap": {
            "attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "Up and Down the Line",
            "map_as_image": False,
            "map_subdomains": "",
            # "map_type": "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    return json.dumps(storymap_dict)


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

    return results or None  # Return all collected results or None if no results


def routes_mapdata_extract(routes):
    elrs = []
    route_locations = []

    for route in routes:
        route_locations.extend(fetch_route_locations(route) or [])
        elrs.extend(
            elr.geojson
            for elr in route.elrs.all()
            if elr.geojson and elr.geojson.get("features")
        )

    return elrs or None, route_locations or None


def folium_map_location(latitude, longitude, tooltip_text, height=600, width=1100):
    import folium
    from folium.plugins import MiniMap

    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=17,
        prefer_canvas=True,
        height=height,
        width=width,
        tiles="OpenStreetMap",  # base layer
    )

    # Create the NLS layer but don’t activate it yet
    nls_layer = folium.TileLayer(
        tiles="https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
        attr='<a href="https://maps.nls.uk/">OS 25 1892–1914 maps – National Library of Scotland</a>',
        name="NLS 25-inch (1892–1914)",
        min_zoom=2,
        max_zoom=19,
        show=False,
        overlay=True,
        control=True,
        opacity=0.7,
    )

    nls_layer.add_to(m)  # must come before LayerControl()

    # Marker
    folium.Marker([latitude, longitude], tooltip=tooltip_text).add_to(m)

    # LayerControl must be added after *all* layers are defined
    folium.LayerControl(collapsed=False).add_to(m)

    # Optional: MiniMap
    minimap = MiniMap()
    m.add_child(minimap)

    # Render
    figure = folium.Figure()
    m.add_to(figure)
    figure.render()
    return figure._repr_html_()


def create_folium_map(elrs, locations, height=650, width=1100, timeline=False):
    """
    Create a Folium map with optional timeline support.

    Args:
        elrs: list of GeoJSONs for ELR lines.
        locations: list of locations with st_x, st_y, name, media_url, opened, closed, wikislug.
        height, width: map size.
        timeline: bool, if True, create a timeline map.

    Returns:
        HTML string of the map.
    """
    import folium
    from datetime import datetime
    from folium.plugins import Timeline, TimelineSlider, MarkerCluster, MiniMap
    from django.urls import reverse
    from django.utils import timezone

    current_date = f"{timezone.now().date().isoformat()}T00:00:00Z"
    bounding_box = None
    timeline_features = []

    # -------------------------------
    # Helper functions
    # -------------------------------
    def format_date(date_str, fmt="%d-%m-%Y"):
        if not date_str:
            return ""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime(fmt)
        except Exception:
            return ""

    def timeline_dates(opened, closed, current_date=current_date):
        start = f"{opened}T00:00:00Z" if opened else None
        end = f"{closed}T00:00:00Z" if closed else current_date
        return start, end

    def build_location_popup(loc):
        st_x, st_y = loc.get("st_x"), loc.get("st_y")
        display_name = loc.get("name") or loc.get("wikiname") or f"({st_y}, {st_x})"

        if loc.get("wikislug"):
            try:
                url = reverse("locations:location", args=[loc["id"]])
                popup_name = f'<a href="{url}" target="_blank">{display_name}</a>'
            except Exception:
                popup_name = display_name
        else:
            popup_name = display_name

        img_html = (
            f'<img src="{loc["media_url"]}" width="230" height="172"><br/>'
            if loc.get("media_url")
            else ""
        )
        opened_html = (
            f"<br>Opened {format_date(loc.get('opened'))}" if loc.get("opened") else ""
        )
        closed_html = (
            f"<br>Closed {format_date(loc.get('closed'))}" if loc.get("closed") else ""
        )
        popup_html = f"<div style='font-size:20px'>{img_html}<span>{popup_name}{opened_html}{closed_html}</span></div>"

        # Return popup HTML, tooltip text, and timeline ISO dates
        start_date, end_date = timeline_dates(loc.get("opened"), loc.get("closed"))
        return popup_html, display_name, start_date, end_date

    def add_timeline(m, features):
        locations_geojson = {"type": "FeatureCollection", "features": features}
        style = """
            background-color: white;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
            font-size: 20px;
            padding: 5px;
        """
        tl = Timeline(
            locations_geojson,
            period="P1Y",
            add_last_point=True,
            auto_play=False,
            loop=False,
            max_speed=1,
            loop_button=True,
            date_options="YYYY-MM-DD",
            time_slider_drag_update=True,
            duration="P1M",
            name="Timeline Layer",
        )

        folium.GeoJsonPopup(
            fields=["popup"], aliases=[""], localize=True, style=style
        ).add_to(tl)

        folium.GeoJsonTooltip(
            fields=["name"],
            aliases=[""],
            labels=True,
            localize=True,
            sticky=False,
            style=style,
        ).add_to(tl)

        timeline_layer = folium.FeatureGroup(name="Timeline Layer", show=True)
        tl.add_to(timeline_layer)
        timeline_layer.add_to(m)
        
        TimelineSlider(
            auto_play=False,
            show_ticks=True,
            date_options="YYYY",
            enable_keyboard_controls=True,
            playback_duration=30000,
            show=False,
        ).add_timelines(tl).add_to(m)

    def extend_bounding_box(bbox, coords):
        if bbox is None:
            return [coords, coords]
        (min_lat, min_lon), (max_lat, max_lon) = bbox
        lat, lon = coords
        return [
            (min(min_lat, lat), min(min_lon, lon)),
            (max(max_lat, lat), max(max_lon, lon)),
        ]

    # -------------------------------
    # Base map and tiles
    # -------------------------------
    m = folium.Map(
        zoom_start=13,
        location=[51.5072, -0.1276],
        prefer_canvas=True,
        height=height,
        width=width,
        tiles=None,
    )

    folium.TileLayer("OpenStreetMap", name="OpenStreetMap", overlay=True).add_to(m)
    folium.TileLayer(
        "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
        attr='<a href="https://maps.nls.uk/">OS 25 1892-1914 maps Reproduced with the permission of the National Library of Scotland</a>',
        name="NLS 25inch",
        min_zoom=2,
        max_zoom=19,
        overlay=True,
        show=False,
    ).add_to(m)

    # -------------------------------
    # Process ELRs
    # -------------------------------
    if elrs:
        for elr in elrs:
            for feature in elr.get("features", []):
                props = feature.get("properties", {})
                props.update(props.pop("tags", {}))
                props.pop("nodes", None)
                opened = props.get("opened")
                closed = props.get("closed")
                props["start"], props["end"] = timeline_dates(opened, closed)
                props["name"] = props.get("name") or props.get("ref") or "No Name"

            folium.GeoJson(
                elr,
                tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False),
                popup=folium.GeoJsonPopup(fields=["name"], labels=False),
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
                name="Route",
                smooth_factor=2,
                show=True,
            ).add_to(m)

    # -------------------------------
    # Process locations
    # -------------------------------
    if locations:
        marker_cluster = (
            None
            if timeline
            else MarkerCluster(name="Locations", show=True).add_to(m)
        )
        for loc in locations:
            st_x, st_y = loc.get("st_x"), loc.get("st_y")
            if st_x is None or st_y is None:
                continue

            coords = (st_y, st_x)
            bounding_box = extend_bounding_box(bounding_box, coords)

            popup_html, tooltip_name, start_date, end_date = build_location_popup(loc)

            if not timeline:
                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_html, max_width=2650),
                    tooltip=folium.Tooltip(tooltip_name),
                ).add_to(marker_cluster)

            if (
                timeline
                and is_valid_yyyy_mm_dd(loc.get("opened"))
                and is_valid_yyyy_mm_dd(loc.get("closed"))
            ):
                timeline_features.append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [st_x, st_y]},
                        "properties": {
                            "name": tooltip_name,
                            "wikislug": loc.get("wikislug"),
                            "opened": loc.get("opened"),
                            "closed": loc.get("closed"),
                            "start": start_date,
                            "end": end_date,
                            "popup": popup_html,
                        },
                    }
                )

    # -------------------------------
    # Fit map and finalize
    # -------------------------------
    if bounding_box:
        m.fit_bounds(bounding_box)

    if timeline:
        add_timeline(m, timeline_features)

    folium.LayerControl().add_to(m)
    MiniMap(position="topright").add_to(m)
    return m._repr_html_()
