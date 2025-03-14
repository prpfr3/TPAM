from django.core.management import BaseCommand
from locations.models import ELR, Location
from django.contrib.gis.geos import LineString
from ...utils import osm_elr_fetch
from datetime import datetime
import os
from csv import DictReader


class Command(BaseCommand):

    help = """
    Derives a new ELR from an existing ELR. This allows ELRs to be split into sub-sections which can be attached to routes and/or be given different opening/closing dates to other parts of the ELR.
    """

    def handle(self, *args, **options):
        input_file = os.path.join("D:\\Data", "TPAM", "Route_Sections_Manual.csv")

        with open(input_file, encoding="utf-8-sig") as file:

            for row in DictReader(file):

                start_location = row["From"]
                end_location = row["To"]
                base_elr = row["ELR Base"]
                variation_elr = row["ELR Variation"]
                date_opened = row.get("Date Opened")
                date_closed = row.get("Date Closed")

                try:
                    start_obj = Location.objects.get(slug=start_location)
                    end_obj = Location.objects.get(slug=end_location)
                except Location.DoesNotExist:
                    print(
                        f"\nCould not retrieve {start_location} or {end_location} for record {row}"
                    )
                    continue  # Skip to the next loop iteration instead of breaking
                except Exception as e:
                    print(
                        f"\nError {e} for {start_location} or {end_location} on record {row}"
                    )

                if not start_obj.geometry or not end_obj.geometry:
                    print(
                        f"\nMissing geometry for {start_location} or {end_location} for record {row}"
                    )
                    continue  # Skip this iteration

                # Extract coordinates
                longitude_start, latitude_start = (
                    start_obj.geometry.x,
                    start_obj.geometry.y,
                )
                longitude_end, latitude_end = end_obj.geometry.x, end_obj.geometry.y

                min_lon, max_lon = min(longitude_start, longitude_end), max(
                    longitude_start, longitude_end
                )
                min_lat, max_lat = min(latitude_start, latitude_end), max(
                    latitude_start, latitude_end
                )

                try:
                    elr_base = ELR.objects.get(itemAltLabel=base_elr)
                except Exception as e:
                    print(f"{base_elr} raised exception {e}")
                    break

                try:
                    elr_new, _ = ELR.objects.get_or_create(
                        itemLabel=f"{start_location}-to-{end_location}"
                    )
                except Exception as e:
                    print(
                        f"{base_elr}-{start_location}-to-{end_location} raised exception {e}"
                    )
                    break

                elr_new.itemAltLabel = f"{variation_elr}"

                if date_opened:
                    elr_new.opened = datetime.strptime(date_opened, "%Y-%m-%d").date()
                if date_closed:
                    elr_new.closed = datetime.strptime(date_closed, "%Y-%m-%d").date()
                elr_new.derived = True
                if start_location:
                    elr_new.start_point = start_obj
                if end_location:
                    elr_new.end_point = end_obj

                if row.get("Max Lat"):
                    max_lat = 59
                if row.get("Min Lat"):
                    min_lat = 49
                if row.get("Max Lon"):
                    max_lat = 2
                if row.get("Min Lon"):
                    max_lat = -7

                bbox = (
                    min_lat,
                    min_lon,
                    max_lat,
                    max_lon,
                )

                elr_geojson = osm_elr_fetch(elr_base.itemAltLabel, bbox)

                if elr_geojson:

                    line_strings = []

                    for feature in elr_geojson["features"]:
                        coordinates = feature["geometry"]["coordinates"]

                        if "properties" in feature:
                            properties = feature["properties"]
                        else:
                            properties = {}

                        # Check if the "tags" field exists
                        if "tags" in properties:
                            tags = properties["tags"]
                        else:
                            tags = {}

                        if elr_new.opened:
                            tags["opened"] = elr_new.opened.isoformat()
                        else:
                            tags.pop("opened", None)

                        if elr_new.closed:
                            tags["closed"] = elr_new.closed.isoformat()
                        else:
                            tags.pop("closed", None)

                        tags["name"] = elr_new.itemLabel

                        # Update the "tags" field within "properties"
                        properties["tags"] = tags

                        # Update the "properties" field within the main data
                        feature["properties"] = properties

                        try:
                            line_strings.append(LineString(coordinates))
                        except Exception as e:
                            print(f"{elr_new} had an exception of {e}")

                elr_new.geojson = elr_geojson
                try:
                    elr_new.save()
                    print(f"Save successful for {elr_new}")
                except Exception as e:
                    print(f"Save failed on {row=} with error {e}")
