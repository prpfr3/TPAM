"""
Deletes from the Locomotive table based on a csv input file
"""
import os
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import Locomotive

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_filename = os.path.join(DATAIO_DIR,"Locomotive_Manual_Deletions.csv")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Deletes from the Locomotive table based on a csv input file"

    def handle(self, *args, **options):

            print("Deleting Locomotives")
            # Encoding of utf-8-sig will treat the Byte Order Mark of //ueff coming from the Excel csv file save as metadata rather than content
            with open(input_filename, encoding="utf-8-sig") as csvfile:
                for row in DictReader(csvfile):
                    print(f'{row=}')
                    try:
                        l = Locomotive.objects.get(id=row['id'])
                    except ObjectDoesNotExist:
                        print(f"Locomotive {row['id']} does not exist")
                    else:
                        try:
                            deleted = l.delete()
                            print(f"Locomotive {row['id']} deleted with deletion function returning {deleted}")
                        except Exception as e:
                            print(f"Locomotive {row['id']} not deleted with error {e}")