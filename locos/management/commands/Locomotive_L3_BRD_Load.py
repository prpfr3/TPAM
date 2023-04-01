"""
Loads the csv file created by Locos_BRD_Extract.py to Django
"""
import os, datetime
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from locos.models import Locomotive, LocoClassList

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_filename = os.path.join(DATAIO_DIR,"BRD_Locomotive_BRD_Enhanced.csv")

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

def dateformatter(dt):

    if len(dt) == 4:
        dt = f"??/??/{dt}"
    if len(dt) == 7:
        dt = f"??/{dt}"
    dt = dt.replace("Jan-", "??/01/19")
    dt = dt.replace("Feb-", "??/02/19")
    dt = dt.replace("Mar-", "??/03/19")
    dt = dt.replace("Apr-", "??/04/19")
    dt = dt.replace("May-", "??/05/19")
    dt = dt.replace("Jun-", "??/06/19")
    dt = dt.replace("Jul-", "??/07/19")
    dt = dt.replace("Aug-", "??/08/19")
    dt = dt.replace("Sep-", "??/09/19")
    dt = dt.replace("Oct-", "??/10/19")
    dt = dt.replace("Nov-", "??/11/19")
    dt = dt.replace("Dec-", "??/12/19")
    dt = dt.replace("/00/", "/01/") # For the odd case where month is "00"

    recorded_date = dt

    # Having stored the recorded date with ? for unknowns,
    # convert the ?s to a precise date, taking the first day of the month or month of the year
    dt = dt.replace("??/??/", "01/01/")
    dt = dt.replace("??", "01")

    # Take 1 or 2 characters of the day or month depending on leading zeros which the int function does not accept
    month = int(dt[4]) if dt[3] == '0' else int(dt[3:5])
    day = int(dt[1]) if dt[0] == '0' else int(dt[:2])
    try:
        datetime_date = datetime.date(int(dt[6:10]), month, day)
    except Exception:
        datetime_date = None

    return(recorded_date, datetime_date )

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads the BRD_Locos.csv file created by Locos_BRD_Extract.py to Django"

    def handle(self, *args, **options):
        if Locomotive.objects.exists():
            print('Data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        else:
            print("Loading Locomotives")
            with open('D://Data/TPAM/Locomotive_BRD_Enhanced.csv', encoding="utf8") as csvfile:
                for row in DictReader(csvfile):
                    try:
                        l = Locomotive()
                        l.number_as_built = row['Number (as built)']
                        l.brd_slug = row['Number (as built)_a']
                        l.order_number = row['Order']
                        l.brd_order_number_slug = row['Order_a']
                        l.works_number = row['Works Number']
                        l.brd_class_name = row['Class_x']
                        l.brd_class_name_slug = row['Class_a']
                        l.build_date, l.build_datetime = dateformatter(row['Build Date'])
                        l.manufacturer = row['Manufacturer']
                        if row['Withdrawn'] and row['Withdrawn'] != '0':
                            l.withdrawn_date, l.withdrawn_datetime = dateformatter(row['Withdrawn'])
                        l.company_grouping_code = row['Big 4']
                        l.company_pregrouping_code = row['Pre Grouping']
                        l.identifier = ""
                        if l.company_grouping_code:
                            l.identifier = l.identifier + l.company_grouping_code + " "
                        if l.company_pregrouping_code:
                            l.identifier = l.identifier + l.company_pregrouping_code + " "
                        if l.brd_class_name:
                            l.identifier = l.identifier + l.brd_class_name + " "
                        l.identifier += l.number_as_built
                    except Exception as e:
                        import json
                        print(json.dumps(row, sort_keys=True, indent=4))
                        print(f'{e}')
                    try:
                        lcl = LocoClassList.objects.get(brdslug=row['Class_a'])
                    except MultipleObjectsReturned:
                        print(f'Multiple entries found in the Locomotive Class List for {row["Class_a"]}')
                    except ObjectDoesNotExist:
                        pass
                    else:
                        try:
                            l.lococlass = lcl.lococlass_fk
                        except Exception as e:
                            print(row['Class_a'], e)
                    try:
                        l.save()
                    except Exception as e:
                        import json
                        print(json.dumps(row, sort_keys=True, indent=4))
                        print(f'{e}')