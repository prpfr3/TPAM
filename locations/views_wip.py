import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from mainmenu.views import pagination

from .forms import *
from .models import *
from .utils import *


class Trackmap(TemplateView):
    template_name = "locations/trackmap.html"

    def get_context_data(self, **kwargs):
        import folium
        import geopandas as gpd

        file = "D:\Data\QGIS\ElhamValleyRailway.geojson"
        track_details = gpd.read_file(file)

        figure = folium.Figure()
        m = folium.Map(
            [
                track_details.geometry.centroid.y[0],
                track_details.geometry.centroid.x[0],
            ],
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
        folium.GeoJson(
            data=track_details["geometry"], popup=track_details["id"]
        ).add_to(m)

        # folium.Icon(icon="cloud").add_to(m)
        # folium.Marker(track_details["geometry"][0], popup=track_details["id"][0], tooltip=tooltip,).add_to(m)

        m.add_to(figure)
        figure.render()
        return {"map": figure}


def depot_vis_timeline(request):
    events = []
    forlooplimiter = 0
    depots = Depot.objects.order_by("depot", "datefield_start")

    for depot in depots:
        if depot.datefield_start and depot.datefield_end:
            forlooplimiter += 1
            ## For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {
                "id": forlooplimiter,
                "content": f"{depot.depot} {depot.code}",
                "start": depot.date_start.replace("??", "01"),
                "end": depot.date_end.replace("??", "01"),
                "event.type": "point",
            }
            events.append(event)

    return render(
        request,
        "locations/depots_vis_timeline.html",
        {"timeline_json": json.dumps(events)},
    )


def county_select(request):
    if request.method == "POST":
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data["locations"]
            county = str(selected_location)
            return HttpResponseRedirect(
                reverse("locations:map_closed_lines", args=[county])
            )
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {
            "location_list": location_list,
            "errors": errors,
        }
        return render(request, "locations/county_select.html", context)


class MapClosedLines(TemplateView):
    template_name = "locations/map_closed_lines.html"

    def get_context_data(self, **kwargs):
        import folium

        import os
        import geopandas as gpd
        from django.conf import settings
        from sqlalchemy import create_engine, text

        county = self.kwargs["county_name"]
        db_connection_url = os.environ.get("DATABASE_URL") or settings.DATABASE_URL
        con = create_engine(db_connection_url)

        # Get all the Closed Route data within the county
        sql = text(
            'SELECT a.* FROM public."locations_routes_geo_closed" as a JOIN public."locations_UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county'
        )
        routes = gpd.GeoDataFrame.from_postgis(
            sql, con, geom_col="geometry", params={"county": county}, crs="EPSG:4326"
        )

        sql = """ 
        SELECT a."name", ST_AsText(a."geometry")
        FROM 
        public."locations_routes_geo_closed" AS a JOIN public."locations_UK_admin_boundaries" as b 
        ON ST_WITHIN(a.geometry, b.geometry) 
        WHERE a."geometry" IS NOT NULL AND b.ctyua19nm = %s;
        """
        routes_sql = execute_sql(sql, [county])

        # Get the county record to calculate the centre of the map
        """ THIS IS GEOPANDAS CODE SUPERSEDED BY NATIVE SQL CODE BELOW TO REMOVE GDAL DEPENDENCIES

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

        sql = """SELECT ST_XMin(geometry), ST_YMin(geometry), ST_XMax(geometry), ST_YMax(geometry),
        ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry))
        FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = %s;"""
        bounds = execute_sql(sql, [county])
        west = bounds[0][0]
        south = bounds[0][1]
        east = bounds[0][2]
        north = bounds[0][3]

        figure = folium.Figure()
        # m = folium.Map([df_county.geometry.centroid.y[0], df_county.geometry.centroid.x[0]], zoom_start= 9, height=500, tiles='cartodbpositron', prefer_canvas=True)
        m = folium.Map(
            [bounds[0][4], bounds[0][5]],
            zoom_start=9,
            height=500,
            tiles="cartodbpositron",
            prefer_canvas=True,
        )
        m.add_to(figure)
        folium.GeoJson(data=routes["geometry"], popup=routes["name"]).add_to(m)
        # folium.GeoJson(data=routes_sql, popup=routes_sql[0]).add_to(m)
        figure.render()
        return {"map": figure, "county": county}
