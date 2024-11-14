from django.core.management import BaseCommand
from locations.models import ELR
from datetime import datetime


class Command(BaseCommand):

    help = """
    A utility to update ELRs, both base and customised. Edit out those fields you do not wish to update.
    """

    def handle(self, *args, **options):
        elr = ELR.objects.get(itemAltLabel="SJM1")
        elr.opened = datetime.strptime("1849-07-10", "%Y-%m-%d").date()
        # elr.closed = datetime.strptime("1847-07-09", "%Y-%m-%d").date()

        if elr.geojson:

            for feature in elr.geojson["features"]:

                if "properties" in feature:
                    properties = feature["properties"]
                else:
                    properties = {}

                # Check if the "tags" field exists
                if "tags" in properties:
                    tags = properties["tags"]
                else:
                    tags = {}

                if elr.opened:
                    tags["opened"] = elr.opened.isoformat()
                else:
                    tags.pop("opened", None)

                if elr.closed:
                    tags["closed"] = elr.closed.isoformat()
                else:
                    tags.pop("closed", None)

                tags["name"] = elr.itemLabel

                # Update the "tags" field within "properties"
                properties["tags"] = tags

                # Update the "properties" field within the main data
                feature["properties"] = properties

        elr.save()
