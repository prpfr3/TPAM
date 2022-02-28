from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import Locations, Company

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        # if Locations.objects.exists():
        #     print('Data already loaded...exiting.')
        #     print(ALREADY_LOADED_ERROR_MESSAGE)
        #     return
        print("Creating Locations")
        for row in DictReader(open('D://Data/TPAM/Locations_Disused_Extract_Joined.csv')):
            l = Locations()
            l.type = "Closed Station"
            l.wikiname = row['Name']
            l.wikislug = row['Wiki']

            try:
                c = Company.objects.get(wikislug=row['Company_Wiki'])
            except ObjectDoesNotExist:
                print(row['Company_Wiki'], ' not found in the Company table')
            else:
                try:
                    l.company_fk = c
                except Exception as e:
                    print(row['Company_Wiki'], e)
                     
            l.closed = row['Closed']
            l.disused_stations_slug = row['1']
            l.save()