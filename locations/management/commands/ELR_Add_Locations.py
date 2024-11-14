from django.core.management import BaseCommand
from locations.models import ELR


class Command(BaseCommand):

    help = """

    Adds locations onto an ELR
    Rather than use this function, it would be better to add locations that are in the Locations table onto the ELR
    
    """

    def handle(self, *args, **options):
        elr_base = ELR.objects.get(itemAltLabel="BLI1-B")
        if elr_base.geojson:
            point_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -0.1411,
                        50.8288,
                    ],  # Replace with your desired coordinates
                },
                "properties": {
                    "name": "Brighton Rail Station",
                    "wikislug": "Brighton_railway_station",
                },
            }

            point_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -0.171032,
                        50.835124,
                    ],  # Replace with your desired coordinates
                },
                "properties": {
                    "name": "Hove railway station",
                    "wikislug": "Hove_railway_station",
                },
            }

            # Append the new point feature to the GeoJSON features list
            elr_base.geojson["features"].append(point_feature)

        elr_base.save()
