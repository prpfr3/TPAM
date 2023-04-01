import os
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass
from companies.models import Company

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUT_FILES = [
                # 'Class_Steam_W3_Detail_Cleansed.csv', 
                'Class_All_W3_Cleansed_Detail.csv'
                ]

class Command(BaseCommand):
    help = "Loads data from a csv file into a LocoClass model"

    def handle(self, *args, **options):

        print("Creating LocoClass to OwnerOperator Table")

        for INPUT_FILE in INPUT_FILES:

            with open(os.path.join(DATAIO_DIR, INPUT_FILE), encoding="utf-8") as file:   
                for row in DictReader(file):
                    if row['2'] == "Operators":
                        try:
                            slug = row['0'].replace('/wiki/', '')
                            l = LocoClass.objects.get(lococlasslist__wikislug=slug)
                        except ObjectDoesNotExist:
                            print(row['0'], ' not found in the Lococlass wikipedia_name_slug field')
                        else:
                            for column in ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']:
                                if 'wiki' in row[column]:
                                    try:
                                        slug = row[column].replace('/wiki/','')
                                        c, created = Company.objects.get_or_create(wikislug=slug)
                                        print("Created:-", created)
                                    except Exception as e:
                                        print(row[column], e)
                                    else:
                                        try:
                                            c.lococlass_owneroperator.add(l)
                                        except Exception as e:
                                            print(row[column], e)