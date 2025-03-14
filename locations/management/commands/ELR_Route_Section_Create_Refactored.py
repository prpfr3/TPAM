import os
import logging
from datetime import datetime
from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.gis.geos import LineString
from django.utils.dateparse import parse_date
from locations.models import ELR, Location
from ...utils import osm_elr_fetch

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    Derives a new ELR from an existing ELR. This allows ELRs to be split into sub-sections which can be attached to routes and/or be given different opening/closing dates to other parts of the ELR.
    """

    def handle(self, *args, **options):
        input_file = os.path.join("D:\\Data", "TPAM", "Route_Sections_Manual.csv")

        if not os.path.exists(input_file):
            logger.error(f"File not found: {input_file}")
            return

        new_elrs = []

        with open(input_file, encoding="utf-8-sig") as file:
            for row in DictReader(file):
                start_location, end_location = row["From"], row["To"]
                base_elr, variation_elr = row["ELR Base"], row["ELR Variation"]
                date_opened, date_closed = row.get("Date Opened"), row.get(
                    "Date Closed"
                )

                try:
                    start_obj = Location.objects.get(slug=start_location)
                    end_obj = Location.objects.get(slug=end_location)
                except Location.DoesNotExist:
                    logger.warning(
                        f"Skipping record: Could not find {start_location} or {end_location}. Row: {row}"
                    )
                    continue

                if not start_obj.geometry or not end_obj.geometry:
                    logger.warning(
                        f"Skipping record: Missing geometry for {start_location} or {end_location}"
                    )
                    continue

                # Extract coordinates
                min_lon, max_lon = sorted([start_obj.geometry.x, end_obj.geometry.x])
                min_lat, max_lat = sorted([start_obj.geometry.y, end_obj.geometry.y])

                # Override bbox if provided in CSV
                if row.get("Max Lat"):
                    max_lat = 59
                if row.get("Min Lat"):
                    min_lat = 49
                if row.get("Max Lon"):
                    max_lat = 2
                if row.get("Min Lon"):
                    max_lat = -7

                bbox = (min_lat, min_lon, max_lat, max_lon)

                try:
                    elr_base = ELR.objects.get(itemAltLabel=base_elr)
                except ELR.DoesNotExist:
                    logger.error(f"Skipping record: Base ELR {base_elr} does not exist")
                    continue

                elr_new, created = ELR.objects.get_or_create(
                    itemLabel=f"{start_location}-to-{end_location}",
                    defaults={"itemAltLabel": variation_elr},
                )

                elr_new.opened = parse_date(date_opened) if date_opened else None
                elr_new.closed = parse_date(date_closed) if date_closed else None
                elr_new.derived = True
                elr_new.start_point = start_obj
                elr_new.end_point = end_obj

                elr_geojson = osm_elr_fetch(elr_base.itemAltLabel, bbox)

                if elr_geojson:
                    line_strings = []
                    for feature in elr_geojson.get("features", []):
                        coordinates = feature["geometry"].get("coordinates", [])
                        try:
                            line_strings.append(LineString(coordinates))
                        except Exception as e:
                            logger.warning(
                                f"Error processing line string for {elr_new}: {e}"
                            )

                        feature.setdefault("properties", {}).setdefault(
                            "tags", {}
                        ).update(
                            {
                                "opened": (
                                    elr_new.opened.isoformat()
                                    if elr_new.opened
                                    else None
                                ),
                                "closed": (
                                    elr_new.closed.isoformat()
                                    if elr_new.closed
                                    else None
                                ),
                                "name": elr_new.itemLabel,
                            }
                        )

                elr_new.geojson = elr_geojson
                new_elrs.append(elr_new)

        if new_elrs:
            try:
                ELR.objects.bulk_update(
                    new_elrs,
                    [
                        "geojson",
                        "opened",
                        "closed",
                        "derived",
                        "start_point",
                        "end_point",
                    ],
                )
                logger.info(f"Successfully saved {len(new_elrs)} ELR records.")
            except Exception as e:
                logger.error(f"Bulk save failed: {e}")
