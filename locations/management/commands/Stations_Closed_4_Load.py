from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import Location
from companies.models import Company

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        # if Location.objects.exists():
        #     print('Data already loaded...exiting.')
        #     print(ALREADY_LOADED_ERROR_MESSAGE)
        #     return
        print("Creating Location")
        for row in DictReader(open('D://Data/TPAM/Location_Disused_Extract_Joined.csv')):
            l = Location()
            l.type = "Closed Station"
            l.wikiname = row['Name']
            l.wikislug = row['Wiki'].replace('/wiki/','')
            l.geometry = row['Geometry']

            try:
                company_wiki = row['Company_Wiki'].replace('/wiki/', '').replace('%26','&').replace('%22','').replace('%27',"'").replace('%E2%80%93','-')
                c = Company.objects.get(wikislug=company_wiki)
            except ObjectDoesNotExist:
                print(company_wiki, ' not found in the Company table')
            else:
                try:
                    l.company_fk = c
                except Exception as e:
                    print(row['Company_Wiki'], e)
                     
            l.closed = row['Closed']
            l.disused_stations_slug = row['1']
            l.save()