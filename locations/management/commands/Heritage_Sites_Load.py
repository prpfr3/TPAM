from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from locations.models import HeritageSite
from mainmenu.models import MyDjangoApp

ALREADY_LOADED_ERROR_MESSAGE = """Empty the table before running this load"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Load the Heritage Site tables from a pre-cleaned csv file"

    def handle(self, *args, **options):
        import os

        do_not_load = ['Miniature Railway', 'Proposed',
                       'Defunct', 'Isle of Man', 'Channel Islands']

        with open(os.path.join("D:\\Data", "TPAM", "Heritage_Railways_Master.csv"), encoding="utf-8") as file:
            for row in DictReader(file):

                if row['Type'] not in do_not_load:

                    try:
                        h = HeritageSite.objects.get(name=row['Name'])
                    except ObjectDoesNotExist:
                        print('Creating ', row['Name'])
                    except Exception as e:
                        print(row['Column1'], e)
                    else:
                        print('Updating ', row['Name'])

                    h = HeritageSite()

                    m = MyDjangoApp.objects.get(id=2)

                    h.tpam_type = m  # 2 is the MyDjangoApp key for Heritage Railways
                    print(row)
                    h.name = row['Name']
                    h.type = row['Type']
                    h.country = row['Country']
                    h.wikislug = row['\ufeffWikiPage']
                    h.save()
