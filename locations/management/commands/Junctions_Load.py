from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Location

input_filename = 'D://Data/TPAM/Location_Junctions_Loadfile.csv'

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        print("Loading Junctions")

        count= 0

        with open(input_filename, encoding="utf-8-sig") as csvfile:
            for row in DictReader(csvfile):
                l = Location()
                l.type = 'Junction'
                l.geometry = f"POINT ({row['@lon']} {row['@lat']})"
                l.stationname = row['name']
                l.stationnamealt = row['alt_name']
                l.osm_node = row['@id']
                print(l)
                l.save()
            count += 1

        print(f'{count} junctions loaded as locations')