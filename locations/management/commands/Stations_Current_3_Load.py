from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Creating Locations")
        if Location.objects.exists():
            print('Note there is already data in the table')

        count = 0

        for row in DictReader(open('D://Data/TPAM/Location_Loadfile.csv')):
            if count != 0:
                l = Location()
                l.type = 'Current Station'
                l.wikiname = row['Name']
                l.wikislug = row['NameSlug'].replace('/wiki/', '')
                l.postcode = row['Postcode']
                l.geometry = row['geometry']
                l.atcocode = row['AtcoCode']
                l.tiploccode = row['TiplocCode']
                l.crscode = row['CrsCode']
                l.name = row['StationName']
                l.namelang = row['StationNameLang']
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
