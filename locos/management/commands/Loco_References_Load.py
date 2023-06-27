import os
import datetime
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from locos.models import LocoClass, LocoClassSighting, Location, Reference

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUT_FILES = ['References_Peak.csv',]


def inserter(s, a, n):
    """
    s: The original string
    a: The characters you want to append
    n: The position you want to append the characters
    """
    return s[:n]+a+s[n:]


def dateformatter(dt):
    """
    Takes a partial or full date in various formats and returns:-

    recorded_date: In format DD/MM/YYYY with the character ? where parts of the date were not supplied
    datetime_date: A datetime format date with 01 substituted where the day or date was not known. Allows partial dates to be used in calculations of ages, graphing etc.
    """
    if len(dt) == 4:  # Assumes that the four digits are a year, adding unknown day and month
        dt = f"??/??/{dt}"
    elif len(dt) == 7:  # Assumes that the date is MM/YYYY, adding unknown day
        dt = f"??/{dt}"
    # Assumes that the format is MMM-YY or MMM YY and insert 19 to give a four digit year:
    elif len(dt) == 6:
        dt = inserter(dt, "19", 4)
        dt = dt.replace("Jan-", "??/01/")
        dt = dt.replace("Feb-", "??/02/")
        dt = dt.replace("Mar-", "??/03/")
        dt = dt.replace("Apr-", "??/04/")
        dt = dt.replace("May-", "??/05/")
        dt = dt.replace("Jun-", "??/06/")
        dt = dt.replace("Jul-", "??/07/")
        dt = dt.replace("Aug-", "??/08/")
        dt = dt.replace("Sep-", "??/09/")
        dt = dt.replace("Oct-", "??/10/")
        dt = dt.replace("Nov-", "??/11/")
        dt = dt.replace("Dec-", "??/12/")
        dt = dt.replace("Jan ", "??/01/")
        dt = dt.replace("Feb ", "??/02/")
        dt = dt.replace("Mar ", "??/03/")
        dt = dt.replace("Apr ", "??/04/")
        dt = dt.replace("May ", "??/05/")
        dt = dt.replace("Jun ", "??/06/")
        dt = dt.replace("Jul ", "??/07/")
        dt = dt.replace("Aug ", "??/08/")
        dt = dt.replace("Sep ", "??/09/")
        dt = dt.replace("Oct ", "??/10/")
        dt = dt.replace("Nov ", "??/11/")
        dt = dt.replace("Dec ", "??/12/")
    elif len(dt) == 8:  # Assumes that the format is MMM-YYYY or MMM YYYY, converting the 3 alpha month to 2 numerics
        dt = dt.replace("Jan-", "??/01/")
        dt = dt.replace("Feb-", "??/02/")
        dt = dt.replace("Mar-", "??/03/")
        dt = dt.replace("Apr-", "??/04/")
        dt = dt.replace("May-", "??/05/")
        dt = dt.replace("Jun-", "??/06/")
        dt = dt.replace("Jul-", "??/07/")
        dt = dt.replace("Aug-", "??/08/")
        dt = dt.replace("Sep-", "??/09/")
        dt = dt.replace("Oct-", "??/10/")
        dt = dt.replace("Nov-", "??/11/")
        dt = dt.replace("Dec-", "??/12/")
        dt = dt.replace("Jan ", "??/01/")
        dt = dt.replace("Feb ", "??/02/")
        dt = dt.replace("Mar ", "??/03/")
        dt = dt.replace("Apr ", "??/04/")
        dt = dt.replace("May ", "??/05/")
        dt = dt.replace("Jun ", "??/06/")
        dt = dt.replace("Jul ", "??/07/")
        dt = dt.replace("Aug ", "??/08/")
        dt = dt.replace("Sep ", "??/09/")
        dt = dt.replace("Oct ", "??/10/")
        dt = dt.replace("Nov ", "??/11/")
        dt = dt.replace("Dec ", "??/12/")

    recorded_date = dt

    """
        Having stored the recorded date with ? for unknowns,
        convert the ?s to the best edited precise date, 
        taking the first day of the month or first month of the year
        """
    dt = dt.replace("??/??/", "01/01/")
    dt = dt.replace("??", "01")

    # Take 1 or 2 characters of the day or month depending on leading zeros which the int function does not accept
    # print(f'{dt=}')
    month = int(dt[4]) if dt[3] == '0' else int(dt[3:5])
    try:
        day = int(dt[1]) if dt[0] == '0' else int(dt[:2])
    except ValueError:
        print(f'ERROR {dt=} {recorded_date=} {len(dt)=}')

    try:
        datetime_date = datetime.date(int(dt[6:10]), month, day)
    except Exception:
        datetime_date = None

    return (recorded_date, datetime_date)


class Command(BaseCommand):
    help = "Load Sightings"

    def handle(self, *args, **options):

        print("Creating Sightings")

        for INPUT_FILE in INPUT_FILES:

            with open(os.path.join(DATAIO_DIR, INPUT_FILE), encoding="utf-8") as file:
                for row in DictReader(file):

                    s, created = Reference.objects.get_or_create(
                        ref=row['\ufeffid'])
                    if row['type']:
                        s.type = row['type']
                    if row['url']:
                        s.url = row['url']
                    if row['notes']:
                        s.notes = row['notes']
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
                    if row['locos']:
                        s.loco = row['locos']
                    if row['lococlass']:
                        try:
                            lococlass_fk = LocoClass.objects.get(
                                wikiname=row['lococlass'])
                            lcs = LocoClassSighting()
                            lcs.loco_class = lococlass_fk
                            lcs.reference = s
                            lcs.save()
                        except ObjectDoesNotExist:
                            print(row['lococlass'],
                                  ' not found in the LocoClass table')
                    if row['date']:
                        s.date, s.date_datetime = dateformatter(row['date'])
                    if row['location_description']:
                        s.location_description = row['location_description']
                        try:
                            s.location_fk = Location.objects.get(
                                wikiname=row['location_description'])
                        except ObjectDoesNotExist:
                            print(
                                row['location_description'], ' not found in the Location table. Location added as description rather than foreign key')
                            s.location_description = row['location_description']
                        except MultipleObjectsReturned:
                            print(row['location_description'],
                                  ' found multiple times in the Location table')
                    s.full_reference = row['full_reference'] or ""
                    s.save()
