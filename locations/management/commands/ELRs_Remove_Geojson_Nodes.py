from django.core.management import BaseCommand
from locations.models import ELR


def remove_nodes_key(json_data):
    # Iterate over each feature in the "features" list
    for feature in json_data.get("features", []):
        # Access properties and check for the "nodes" key
        properties = feature.get("properties", {})
        if "nodes" in properties:
            del properties["nodes"]  # Remove the "nodes" key
    return json_data


class Command(BaseCommand):
    # Show this when the user types help
    help = "Updates one, one or more or all elr instances, with or without going to OpenRailMaps to get the geojson"

    def handle(self, *args, **options):

        elrs = ELR.objects.all()
        for elr in elrs:
            if elr.geojson:
                elr.geojson = remove_nodes_key(elr.geojson)
                elr.save()
