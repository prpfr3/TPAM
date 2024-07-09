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
                try:
                    l = Location.objects.get(
                        wikiname=row['current_wikiname'], wikislug=row['current_wikislug'])
                except ObjectDoesNotExist:
                    print(
                        f'No database entry for {row["current_wikiname"]} {row["current_wikislug"]} not found')
                except Exception as e:
                    print(f'Error on {row["current_wikiname"]}')
                else:
                    if row['status'] == 'Closed':
                        l.type = "Closed Station"
                    elif row['status'] == 'Current':
                        l.type = "Current Station"
                    if l.wikiname:
                        l.wikiname = row['Name']
                    if l.wikislug:
                        l.wikislug = unquote(row['current_wikislug'])
                    if l.geometry:
                        l.geometry = row['Geometry']
                    if l.atcocode:
                        l.atcocode = row['AtcoCode']
                    if l.tiploccode:
                        l.tiploccode = row['TiplocCode']
                    if l.crscode:
                        l.crscode = row['CrsCode']
                    if l.name:
                        l.name = row['StationName']
                    if l.namelang:
                        l.namelang = row['StationNameLang']
                    if l.gridtype:
                        l.gridtype = row['GridType']
                    if l.easting:
                        l.easting = row['Easting']
                    if l.northing:
                        l.northing = row['Northing']
                    if l.creationdatetime:
                        l.creationdatetime = row['CreationDateTime']
                    if l.modificationdatetime:
                        l.modificationdatetime = row['ModificationDateTime']
                    if l.revisionnumber:
                        l.revisionnumber = row['RevisionNumber']
                    if l.modification:
                        l.modification = row['Modification']

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

                    print(
                        f'Existing location adjusted for {l.wikiname}, {l.wikislug}')
