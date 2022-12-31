from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import Location, ELR

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from RailReferences.csv into our NaPTAN Rail References rable"

    def handle(self, *args, **options):

        for row in DictReader(open('D://Data/TPAM/Location_ELR.csv')):
            wikislug = row['itemLabel'].replace(' ', '_')
            print(wikislug)

            try:
                locations = Location.objects.filter(wikislug=wikislug)
            except ObjectDoesNotExist:
                print(wikislug, ' not found in the Location table')
            else:
                csv_elr = row['lineAltLabel']
                print(csv_elr[:3])
                try:
                    elr = ELR.objects.get(itemAltLabel=csv_elr[:3])
                    for location in locations:
                        l = Location()
                        l = location
                        l.elr_fk = elr
                        l.save()
                        print(f'location updated with elr_fk of {l.elr_fk}')
                except Exception as e:
                    print(csv_elr, e)