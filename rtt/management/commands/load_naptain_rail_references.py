from csv import DictReader
from django.core.management import BaseCommand
from rtt.models import NaPTANRailReferences

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        if NaPTANRailReferences.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating NaPTANRailReferences")
        for row in DictReader(open('D://MLDatasets/TPAM_DATAIO/NaPTANRailReferences.csv')):
            c = NaPTANRailReferences()
            c.atcocode = row['AtcoCode'] 
            c.tiploccode = row['TiplocCode']
            c.crscode = row['CrsCode']
            c.stationname = row['StationName']
            c.stationnamelang = row['StationNameLang']
            c.gridtype = row['GridType']
            c.easting = row['Easting']
            c.northing = row['Northing'] 
            c.creationdatetimetime = row['CreationDateTime']
            c.modificationdatetime = row['ModificationDateTime']
            c.revisionnumber = row['RevisionNumber']
            c.modification = row['Modification']
            c.save()
