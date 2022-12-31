import os
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from locos.models import LocoClass, LocoClassSighting, Location

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUT_FILES = ['Sightings_Peak.csv',]

class Command(BaseCommand):
    help = "Load Sightings"

    def handle(self, *args, **options):

        print("Creating Sightings")

        for INPUT_FILE in INPUT_FILES:

            with open(os.path.join(DATAIO_DIR, INPUT_FILE), encoding="utf-8") as file:   
                for row in DictReader(file):

                    s, created = Reference.objects.get_or_create(ref=row['\ufeffid'])
                    if row['type']: s.type = row['type']
                    if row['url']: s.url = row['url']
                    if row['notes'] : s.notes = row['notes']
                    # COMMENTED OUT AWAITING CLARITY ON DEFINITION OF UNIQUE NUMBER
                    # if row['locos']:
                    #     try:
                    #         loco_fk = Locomotive.objects.get(brd_number_as_built=row['locos'])
                    #         ls = LocoSighting()
                    #         ls.loco = loco_fk
                    #         ls.reference = s
                    #         ls.save()
                    #     except ObjectDoesNotExist:
                    #         print(row['locos'], ' not found in the Locomotive table')
                    if row['lococlass']:
                        try:
                            lococlass_fk = LocoClass.objects.get(wikiname=row['lococlass'])
                            lcs = LocoClassSighting()
                            lcs.loco_class = lococlass_fk
                            lcs.reference = s
                            lcs.save()
                        except ObjectDoesNotExist:
                            print(row['lococlass'], ' not found in the LocoClass table')
                    if row['date']: s.date = row['date']
                    if row['location_description']: 
                        s.location_description = row['location_description']
                        try:
                            s.location_fk = Location.objects.get(wikiname=row['location_description'])
                        except ObjectDoesNotExist:
                            print(row['location_description'], ' not found in the Location table')
                        except MultipleObjectsReturned:
                            print(row['location_description'], ' found multiple times in the Location table')
                    s.citation = row['citation'] or ""
                    s.save()