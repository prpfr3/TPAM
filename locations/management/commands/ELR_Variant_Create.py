from django.core.management import BaseCommand
from locations.models import ELR
from django.contrib.gis.geos import LineString
from ...utils import osm_elr_fetch
from datetime import datetime


class Command(BaseCommand):

    help = """
    Derives a new ELR from an existing ELR. This allows ELRs to be split into sub-sections which can be attached to routes and/or be given different opening/closing dates to other parts of the ELR.
    """

    def handle(self, *args, **options):
        elr_base = ELR.objects.get(itemAltLabel="SMJ2")
        elr_new, _ = ELR.objects.get_or_create(itemAltLabel="SMJ2-A")
        elr_new.itemLabel = "Burton Salmon to Ferrybridge North Junction"
        elr_new.opened = datetime.strptime("1850-04-01", "%Y-%m-%d").date()
        # elr_new.closed = datetime.strptime("1847-07-09", "%Y-%m-%d").date()
        elr_new.derived = True
        # Change one or more of 49, -7, 59, 2 to limit the extent of the ELR
        elr_geojson = osm_elr_fetch(
            elr_base.itemAltLabel,
            (
                53.712,
                -7,
                59,
                2,
            ),
        )

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
        elr_new.save()
