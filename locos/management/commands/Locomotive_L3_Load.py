"""
Loads the csv file created by Locos_BRD_Extract.py to Django
"""
import os, datetime
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import Locomotive, LocoClassList

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_filename = os.path.join(DATAIO_DIR,"BRD_Locomotive_BRD_Enhanced.csv")

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

def dateformatter(dt):

        if len(dt) == 4: dt = "??/??/" + dt # If only the year, pad out the da and month 
        if len(dt) == 7: dt = "??/" + dt # If only the year and month but no day, padd out the day
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
        if dt[3] == '0': 
            month = int(dt[4])
        else:
            month = int(dt[3:5])
            
        if dt[0] == '0': 
            day = int(dt[1])
        else:
            day = int(dt[0:2])

        try:
            datetime_date = datetime.date(int(dt[6:10]), month, day)
        except:
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
                    print(f'{row=}')
                    l = Locomotive()
                    l.brd_number_as_built = row['Number (as built)']
                    l.brd_slug = row['Number (as built)_a']
                    l.brd_order_number = row['Order']
                    l.brd_order_number_slug = row['Order_a']
                    l.brd_works_number = row['Works Number']
                    l.brd_class_name = row['Class_x']
                    l.brd_class_name_slug = row['Class_a']
                    l.brd_build_date_recorded, l.brd_build_date_datetime = dateformatter(row['Build Date'])
                    l.brd_builder = row['Builder']
                    if row['Withdrawn'] and row['Withdrawn'] != '0':
                        l.brd_withdrawn_date_recorded, l.brd_withdrawn_date_datetime = dateformatter(row['Withdrawn'])
                    l.brd_company_grouping_code = row['Big 4']
                    l.brd_company_pregrouping_code = row['Pre Grouping']
                    l.identifier = ""
                    if l.brd_company_grouping_code:
                        l.identifier = l.identifier + l.brd_company_grouping_code + " "
                    if l.brd_company_pregrouping_code:
                        l.identifier = l.identifier + l.brd_company_pregrouping_code + " "
                    if l.brd_class_name:
                        l.identifier = l.identifier + l.brd_class_name + " "
                    l.identifier = l.identifier + l.brd_number_as_built

                    try:
                        c = LocoClassList.objects.get(brdslug=row['Class_a'])
                    except ObjectDoesNotExist:
                        pass
                    else:
                        try:
                            l.lococlass = c
                        except Exception as e:
                            print(row['Class_a'], e)
                            
                    l.save()