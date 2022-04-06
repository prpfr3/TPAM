from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Locations

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        if Locations.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating Locations")
        for row in DictReader(open('D://Data/TPAM/Locations_LoadFile_Current_Stations.csv')):
            l = Locations()
            l.type = 'Current Station'
            l.wikiname = row['Name']
            l.wikislug = row['NameSlug']
            l.postcode = row['Postcode']
            l.geometry = row['geometry']
            l.atcocode = row['AtcoCode'] 
            l.tiploccode = row['TiplocCode']
            l.crscode = row['CrsCode']
            l.stationname = row['StationName']
            l.stationnamelang = row['StationNameLang']
            l.gridtype = row['GridType']
            l.easting = row['Easting']
            l.northing = row['Northing'] 
            l.creationdatetime = row['CreationDateTime']
            l.modificationdatetime = row['ModificationDateTime']
            l.revisionnumber = row['RevisionNumber']
            l.modification = row['Modification']
            l.save()