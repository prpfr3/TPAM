import folium
import json
import logging
import osm2geojson
import requests

import concurrent.futures
from django.utils import timezone

from folium.plugins import FastMarkerCluster, MiniMap
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
from django.views import View
from django.db import connection
from django.conf import settings
from datetime import datetime
from typing import Any, Dict, List, Optional
from storymaps.views import get_wikipedia_summary
from shapely.geometry import shape, mapping

from .forms import *

logger = logging.getLogger(__name__)

# locations/converters.py

class WikipediaSlugConverter:
    # Accept:
    # - ASCII letters, digits
    # - underscores, hyphens
    # - ampersands, parentheses, commas, periods
    # - percent-encoded sequences (%XX)
    # - unicode characters (via .+)
    regex = r"[A-Za-z0-9_\-\&\(\)\.,%]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


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

def _fetch_wiki_summary(slug: str) -> str:
    """Helper function to fetch Wikipedia summaries safely."""
    url = f"https://en.wikipedia.org/wiki/{slug}"
    try:
        return get_wikipedia_summary(url)
    except Exception as e:
        logger.error("Failed to fetch Wikipedia summary for %s: %s", url, e)
        return ""

def generate_storymap(request, headline: str, text: str, locations: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Generates a JSON storymap dictionary from headline, text, and location data.
    Uses ThreadPoolExecutor to fetch missing Wikipedia summaries in parallel.
    """
    if not locations:
        locations = []

    # 1. Pre-fetch Wikipedia summaries in parallel for locations missing notes
    wiki_cache = {}
    
    # Use a set to deduplicate requests if multiple locations share the same wikislug
    slugs_to_fetch = {
        loc["wikislug"] for loc in locations 
        if not loc.get("notes") and loc.get("wikislug")
    }

    if slugs_to_fetch:
        # max_workers=5 prevents hammering the Wikipedia API and getting rate-limited
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Map futures to their respective slugs
            future_to_slug = {
                executor.submit(_fetch_wiki_summary, slug): slug 
                for slug in slugs_to_fetch
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_slug):
                slug = future_to_slug[future]
                wiki_cache[slug] = future.result()

    # 2. Initialize the slides list with the header slide
    slides = [{
        "location_line": "true",
        "type": "overview",
        "media": {"caption": "", "credit": "", "url": ""},
        "text": {"headline": headline, "text": text},
    }]

    # 3. Build the location slides declaratively
    for loc in locations:
        notes = loc.get("notes")
        wikislug = loc.get("wikislug")
        media_url = None
        raw_url = loc.get("media_url")
    
        if raw_url:
            if raw_url.startswith("http://") or raw_url.startswith("https://"):
                media_url = raw_url
            else:
                # 1. Create the local path (e.g., "/media/uploads/image.jpg")
                local_path = f"{settings.MEDIA_URL}{raw_url.lstrip('/')}"
                
                # print(f'{local_path=}')
                # 2. Convert it to a fully qualified URL (e.g., "https://yoursite.com/media/uploads/image.jpg")
                media_url = request.build_absolute_uri(local_path)

        # print(raw_url, media_url)
        
        # Resolve the text: Use notes if available, otherwise check our prefetched cache
        slide_text = notes
        if not slide_text and wikislug:
            slide_text = wiki_cache.get(wikislug, "")

        slides.append({
            "background": {"url": ""},
            "location": {
                "lat": loc.get("st_y"),
                "lon": loc.get("st_x"),
                "notes": notes,
                "zoom": "12",
            },
            "media": {
                "caption": loc.get("media_caption"),
                "credit": loc.get("media_credit"),
                "url": media_url,
            },
            "text": {
                "headline": loc.get("name") or None,
                "text": slide_text or "",
            }
        })

    # 4. Construct the final dictionary
    storymap_dict = {
        "storymap": {
            "attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "Up and Down the Line",
            "map_as_image": False,
            "map_subdomains": "",
            "map_type": "osm:standard",# or "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
            "slides": slides,
            "zoomify": False,
        }
    }

    # 5. Safely serialize to JSON
    try:
        return json.dumps(storymap_dict)
    except (TypeError, ValueError) as e:
        logger.error("Failed to serialize storymap to JSON: %s", e)
        # Return a safe fallback rather than crashing the calling view
        return json.dumps({"storymap": {"slides": []}})

def execute_sql_nofieldnames(sql, parameters):

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameters)
            result = cursor.fetchall()

    except Exception as e:
        print(e)

    return result


def execute_sql(sql, parameters):

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
    """
    """
    routemaps = route.wikipedia_routemaps.all()

    if not routemaps:
        return None  # No routemaps found, return None

    sql = """
    SELECT DISTINCT ON (a."id") 
        a."id", a."wikiname", a."wikislug", a."name",
        ST_Y(ST_CENTROID(a.geometry)),
        ST_X(ST_CENTROID(a.geometry)),
        a."notes",
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



def create_folium_map(elrs, locations, base_location=None, height=650, width=1100, timeline=False):

    current_date = f"{timezone.now().date().isoformat()}T00:00:00Z"
    bounding_box = None

    m = folium.Map(
        zoom_start=13,
        location=[51.5072, -0.1276],
        prefer_canvas=True,  # Draws markers on a single canvas instead of individual SVG elements
        height=height,
        width=width,
        tiles=None,
    )

    # Route tile requests through the server so OSM receives the required headers.
    tile_url = reverse("storymaps:proxy_tile", args=(0, 0, 0)).replace(
        "/0/0/0/", "/{z}/{x}/{y}/"
    )
    folium.TileLayer(
        tiles=tile_url,
        attr=settings.MAP_TILE_ATTRIBUTION,
        name="OpenStreetMap",
        overlay=False,
    ).add_to(m)

    # folium.TileLayer(
    #     "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
    #     attr="National Library of Scotland",
    #     name="NLS 25inch",
    #     overlay=True,
    #     show=False,
    # ).add_to(m)


    # # OpenRailwayMap standard layer
    # folium.TileLayer(
    #     tiles="https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
    #     attr=(
    #         'Data <a href="https://www.openstreetmap.org/copyright">'
    #         '&copy; OpenStreetMap contributors</a>, Style: '
    #         '<a href="https://creativecommons.org/licenses/by-sa/2.0/">'
    #         'CC-BY-SA 2.0</a> '
    #         '<a href="https://www.openrailwaymap.org/">OpenRailwayMap</a>'
    #     ),
    #     name="OpenRailwayMap - Standard",
    #     min_zoom=2,
    #     max_zoom=19,
    #     overlay=True,
    #     show=True,
    #     control=True
    # ).add_to(m)


    def format_date(date_str, fmt="%d-%m-%Y"):
        if not date_str:
            return ""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime(fmt)
        except Exception:
            return ""

    def extend_bounding_box(bbox, coords):
        if bbox is None:
            return [coords, coords]
        (min_lat, min_lon), (max_lat, max_lon) = bbox
        lat, lon = coords
        return [
            (min(min_lat, lat), min(min_lon, lon)),
            (max(max_lat, lat), max(max_lon, lon)),
        ]

    def timeline_dates(opened, closed, current_date=current_date):
        start = f"{opened}T00:00:00Z" if opened else None
        end = f"{closed}T00:00:00Z" if closed else current_date
        return start, end

    def build_location_popup(loc):
        st_x, st_y = loc.get("st_x"), loc.get("st_y")
        display_name = loc.get("name") or loc.get("wikiname") or f"({st_y}, {st_x})"

        if loc.get("wikislug"):
            try:
                url = reverse("locations:location_by_slug", args=[loc["wikislug"]])
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
        popup_html = f"<div style='font-size:20px'>{img_html}<span>{popup_name}{opened_html}{closed_html}</span><div style='width: 500px; max-height: 500px; overflow-y: auto; text-align: justify; line-height: 1.5; padding: 8px; word-wrap: break-word; white-space: normal;'>{loc.get('notes', '')}</div></div>"

        tooltip_html = (
            f"<div style='width: 250px; max-height: 1000px; word-wrap: break-word; white-space: normal; font-size: 24px;'>"
            f"<strong>{popup_name}</strong>"
            f"<div style='margin-top: 4px;'>{loc.get('notes', '')}</div>"
            f"</div>"
        )

        # Return popup HTML, formatted tooltip HTML, and timeline ISO dates
        start_date, end_date = timeline_dates(loc.get("opened"), loc.get("closed"))

        if not loc.get("opened"):
            start_date = None
        if not loc.get("closed"):
            end_date = None

        return popup_html, tooltip_html, display_name, start_date, end_date

    def simplify_geojson_data(geojson_dict, tolerance=0.0005):
        """
        Tolerance of 0.0005 is ~55 meters.
        For rail lines, this usually cuts point count by 70-90%.
        """
        if "features" not in geojson_dict:
            return geojson_dict

        for feature in geojson_dict["features"]:
            # Convert to Shapely object
            # geom = shape(feature["geometry"])
            # Simplify: preserve_topology=True keeps lines from self-intersecting
            # simplified_geom = geom.simplify(tolerance, preserve_topology=True)
            # Convert back to GeoJSON dict
            # feature["geometry"] = mapping(simplified_geom)

            # OPTIMIZATION: Reduce the number of properties to just name and ref
            props = feature.get("properties", {})
            feature["properties"] = {
                "name": props.get("name") or props.get("ref") or "Unknown",
                "ref": props.get("ref", ""),
            }
        return geojson_dict

    def truncate_coords(obj, precision=5):
        """
        Recursively round all coordinates in a GeoJSON-like dictionary.
        """
        if isinstance(obj, float):
            return round(obj, precision)
        elif isinstance(obj, dict):
            return {k: truncate_coords(v, precision) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [truncate_coords(x, precision) for x in obj]
        return obj

    # from .utils_unused import load_elr_layer
    # load_elr_layer(m)  # Load the pre-built ELR layer from cache and add to the map

    if elrs:
        all_features = []

        for elr in elrs:
            geojson_data = None
            if isinstance(elr, dict):
                if elr.get("features"):
                    geojson_data = elr
                elif isinstance(elr.get("geojson"), dict):
                    geojson_data = elr["geojson"]

            if not geojson_data:
                continue

            try:
                simplified = simplify_geojson_data(geojson_data, tolerance=0.00001) # tolerance not used in current implementation but kept for future use
                final_data = truncate_coords(simplified, precision=6)
                all_features.extend(final_data.get("features", []))
            except Exception as e:
                logger.error("Error processing ELR payload: %s", e, exc_info=True)

        if all_features:
            combined_geojson = {"type": "FeatureCollection", "features": all_features}

            folium.GeoJson(
                combined_geojson,
                # The smoothing factor can be adjusted to control the level of simplification applied to the geometry. A higher value results in smoother lines, while a lower value retains more detail. That said on this code it appears to make no difference to the output so it is set to 1.0 for now.
                smooth_factor=1.0,
                style_function=lambda x: {
                    "color": "#c94f1a",
                    "weight": 3,
                    "opacity": 0.7,
                },
                highlight_function=lambda x: {"weight": 6, "color": "yellow"},
                name="Railway Network",
            ).add_to(m)

    if base_location and base_location.get("st_x") and base_location.get("st_y"):
        base_coords = (base_location["st_y"], base_location["st_x"])
        bounding_box = extend_bounding_box(bounding_box, base_coords)
        popup_html, tooltip_html, _, _, _ = build_location_popup(base_location)

        folium.Marker(
            location=base_coords,
            icon=folium.Icon(color="red", icon="info-sign"),
            tooltip=folium.Tooltip(
                tooltip_html,
                sticky=False,
                direction="right",
            ),
            popup=folium.Popup(popup_html, max_width=2650),
        ).add_to(m)

    if locations:
        # 1. Build point_data with popup and tooltip included
        point_data = []
        for loc in locations:
            if not loc.get("st_x"):
                continue

            coords = (loc["st_y"], loc["st_x"])
            bounding_box = extend_bounding_box(bounding_box, coords)

            popup_html, tooltip_html, _, start_date, end_date = build_location_popup(loc)
            point_data.append(
                [
                    truncate_coords(loc["st_y"]),  # row[0] - lat
                    truncate_coords(loc["st_x"]),  # row[1] - lng
                    popup_html,  # row[2] - popup
                    tooltip_html,  # row[3] - tooltip
                ]
            )

        # 2. Callback now reads popup/tooltip from row data
        callback = """
            function (row) {
                var marker = L.circleMarker([row[0], row[1]], {
                    radius: 6,
                    fillColor: "#78491c",
                    color: "white",
                    weight: 1,
                    fillOpacity: 0.8
                });

                if (row[2]) {
                    marker.bindPopup(row[2], {maxWidth: 2650});
                }

                if (row[3]) {
                marker.bindTooltip(row[3], {
                    direction: 'right', // Opens to the right of the marker point
                    offset: [15, -10],  // Adjusts position: [pixels right, pixels up]
                    sticky: false       // Keeps it anchored relative to the marker, not mouse pointer
                });
            }

                return marker;
            };
        """

        m.add_child(FastMarkerCluster(point_data, name="Locations", callback=callback))

    if bounding_box:
        m.fit_bounds(bounding_box)

    folium.LayerControl().add_to(m)
    return m._repr_html_()
