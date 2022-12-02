from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Location

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):
        print("Creating Locations")
        if Location.objects.exists():
            print('Note there is already data in the table')

        count= 0

        for row in DictReader(open('D://Data/TPAM/Location_Loadfile.csv')):
            if count != 0:
                l = Location()
                l.type = 'Current Station'
                l.wikiname = row['Name'].replace('/wiki/','')
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
            count += 1

        print(f'{count} railway stations loaded as locations')