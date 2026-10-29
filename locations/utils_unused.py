# An alternative approach loads a pre-processed ELR layer of ALL ELRs from a static file, which is much faster than processing on the fly. The build_elr_layer command should be run after any ELR updates to regenerate the cached layer.

from django.conf import settings
import folium
import json
import os

from folium.plugins import Timeline, TimelineSlider


def load_elr_layer(map):
    """Load the pre-built ELR GeoJSON layer from cache and add to map."""
    static_dirs = settings.STATICFILES_DIRS
    if not static_dirs:
        return

    elr_layer_path = os.path.join(str(static_dirs[0]), "geojson", "elr_layer.json")

    if not os.path.exists(elr_layer_path):
        return  # or log a warning

    with open(elr_layer_path, encoding="utf-8") as f:
        combined_geojson = json.load(f)

    folium.GeoJson(
        combined_geojson,
        smooth_factor=5.0,
        style_function=lambda x: {
            "color": "#c94f1a",
            "weight": 3,
            "opacity": 0.7,
        },
        highlight_function=lambda x: {"weight": 6, "color": "yellow"},
        name="Railway Network",
    ).add_to(map)


# Function for adding a timeline layer to the map
def add_timeline(map, features):
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
    timeline_layer.add_to(map)

    TimelineSlider(
        auto_play=False,
        show_ticks=True,
        date_options="YYYY",
        enable_keyboard_controls=True,
        playback_duration=30000,
        show=False,
    ).add_timelines(tl).add_to(map)