from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClassList, LocoClass
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into a LocoClassList model"

    def handle(self, *args, **options):
        print("Creating LocoClassLists")
        import os
        with open(os.path.join(DATAIO_DIR, 'Class_All_W3_Cleansed_Detail.csv'), encoding="utf-8") as file:   
            for row in DictReader(file):
                if row['1'] == "0":
                    try:
                        c = LocoClassList.objects.get(wikislug=row['0'])
                    except ObjectDoesNotExist:
                        c = LocoClassList()
                        c.wikislug = row['0'].replace('/wiki/','')
                        c.name = row['0'].replace('_',' ')
                        c.name = c.name.replace('%26','&')
                        c.name = c.name.replace('%22','"')
                        c.name = c.name.replace("%27","'")
                        c.name = c.name.replace('%E2%80%93','-')
                        c.name = c.name.replace('/wiki/','')
                        c.lococlass_fk = LocoClass.objects.get(wikiname=row['2'])                        
                        c.save()
                        print(c.wikislug, ' added to LocoClassList')
                    except Exception as e:
                        print(row[0], e)
                    else:
                        print(row['0'], ' already loaded')