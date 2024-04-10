# # management/commands/load_geojson.py
# from locations.models import UKArea
# from django.core.management.base import BaseCommand
# from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
# import json
# import pyproj


# class Command(BaseCommand):
#     help = "Your command description here"

#     def handle(self, *args, **options):
#         geojson_file_path = "D://Data//TPAM//International_Territorial_Level_1_January_2021_UK_BUC_2022_4731002879923581517.geojson"
#         bng_crs = pyproj.CRS("EPSG:27700")  # British National Grid
#         wgs84_crs = pyproj.CRS("EPSG:4326")  # WGS84 (longitude and latitude)
#         transformer = pyproj.Transformer.from_crs(bng_crs, wgs84_crs, always_xy=True)

#         with open(geojson_file_path) as file:
#             geojson_data = json.load(file)

#         for feature in geojson_data["features"]:
#             properties = feature["properties"]
#             coordinates = feature["geometry"]["coordinates"][0][0]

#             # Convert British National Grid coordinates to WGS84 (longitude and latitude)
#             transformed_coordinates = [
#                 transformer.transform(coord[0], coord[1]) for coord in coordinates
#             ]

#             # Create a list of Polygon objects using the transformed coordinates
#             polygons = [Polygon(transformed_coordinates)]

#             # Create a MultiPolygon using the list of Polygon objects
#             multipolygon = MultiPolygon(polygons)

#             # Create a GeoFeature instance and save it to the database
#             geo_feature = UKArea(
#                 ITL121CD=properties["ITL121CD"],
#                 ITL121NM=properties["ITL121NM"],
#                 BNG_E=properties["BNG_E"],
#                 BNG_N=properties["BNG_N"],
#                 LONG=properties["LONG"],
#                 LAT=properties["LAT"],
#                 geometry=multipolygon,
#             )
#             print(f"At save {coordinates=}, {geo_feature.geometry=}")
#             geo_feature.save()

from locations.models import UKArea
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
import json
import pyproj


class Command(BaseCommand):
    help = "Your command description here"

    def handle(self, *args, **options):
        geojson_file_path = "D://Data//TPAM//International_Territorial_Level_1_January_2021_UK_BUC_2022_4731002879923581517.geojson"
        bng_crs = pyproj.CRS("EPSG:27700")  # British National Grid
        wgs84_crs = pyproj.CRS("EPSG:4326")  # WGS84 (longitude and latitude)
        transformer = pyproj.Transformer.from_crs(bng_crs, wgs84_crs, always_xy=True)

        with open(geojson_file_path) as file:
            geojson_data = json.load(file)

        for feature in geojson_data["features"]:
            properties = feature["properties"]
            coordinates = feature["geometry"]["coordinates"]

            if feature["geometry"]["type"] == "Polygon":
                # Convert British National Grid coordinates to WGS84 (longitude and latitude)
                transformed_coordinates = [
                    transformer.transform(coord[0], coord[1])
                    for coord in coordinates[0]
                ]
                # Create a Polygon object using the transformed coordinates
                geometry = Polygon(transformed_coordinates)
            elif feature["geometry"]["type"] == "MultiPolygon":
                # Convert each part of the MultiPolygon to a Polygon
                polygons = []
                for part in coordinates:
                    flattened_coordinates = [coord for ring in part for coord in ring]
                    transformed_coordinates = [
                        transformer.transform(coord[0], coord[1])
                        for coord in flattened_coordinates
                    ]
                    polygons.append(Polygon(transformed_coordinates))
                # Create a single Polygon using the parts
                geometry = (
                    Polygon(polygons[0])
                    if len(polygons) == 1
                    else MultiPolygon(polygons)
                )
            else:
                # Handle other geometry types as needed
                continue

            # Create a GeoFeature instance and save it to the database
            geo_feature = UKArea(
                ITL121CD=properties["ITL121CD"],
                ITL121NM=properties["ITL121NM"],
                BNG_E=properties["BNG_E"],
                BNG_N=properties["BNG_N"],
                LONG=properties["LONG"],
                LAT=properties["LAT"],
                geometry=geometry,
            )
            print(f"At save {coordinates=}, {geo_feature.geometry=}")
            geo_feature.save()
