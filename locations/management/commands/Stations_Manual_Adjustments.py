from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import Location
from companies.models import Company
from urllib.parse import unquote
import os


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads stations into as Locations or adjusts existing Locations"

    def handle(self, *args, **options):

        print("Making Adjustments")
        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        with open(os.path.join(DATAIO_DIR, 'Location_Stations_Disused_Loadfile_Manual_Adjustments.csv'), encoding="utf-8") as file:
            for row in DictReader(file):
                wikislug = row['Wiki'].replace('/wiki/', '')
                l, route_created = Location.objects.get_or_create(
                    wikiname=row['Name'], wikislug=wikislug)
                if row['status'] == 'Closed':
                    l.type = "Closed Station"
                elif row['status'] == 'Current':
                    l.type = "Current Station"
                l.wikiname = row['Name']
                l.wikislug = unquote(wikislug)
                l.geometry = row['Geometry']

                # COMPANY CURRENTLY NOT IN THE LOCATION MODEL
                # try:
                #     company_wiki = unquote(row['Company_Wiki'].encode('utf-8'))
                #     c = Company.objects.get(wikislug=company_wiki)
                # except ObjectDoesNotExist:
                #     print(company_wiki, ' not found in the Company table')
                # else:
                #     try:
                #         l.company_fk = c
                #     except Exception as e:
                #         print(row['Company_Wiki'], e)

                l.closed = row['Closed']
                l.disused_stations_slug = row['1']
                l.save()

                if route_created:
                    print(
                        f'New location created for {wikislug} as {l.wikiname}, {l.wikislug}')
                else:
                    print(
                        f'Existing location adjusted for {wikislug} as {l.wikiname}, {l.wikislug}')
