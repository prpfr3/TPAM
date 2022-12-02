"""
Loads a CSV file of manually prepared data into the LocationEvent table.

"""
import os, datetime
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import LocationEvent, Location, Route

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_filename = os.path.join(DATAIO_DIR,"LocationEvents.csv")

ALREADY_LOADED_ERROR_MESSAGE = """
Delete the current data from the table being loaded into BEFORE executing this command
"""

def inserter(s,a,n):
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

    if len(dt) == 4: # Assumes that the four digits are a year, adding unknown day and month
            dt = f"??/??/{dt}"
    elif len(dt) == 7: # Assumes that the date is MM/YYYY, adding unknown day
            dt = f"??/{dt}"
    elif len(dt) == 6: # Assumes that the format is MMM-YY or MMM YY and insert 19 to give a four digit year:
        dt = inserter(dt,"19",4)
    elif len(dt) == 8: # Assumes that the format is MMM-YYYY or MMM YYYY, converting the 3 alpha month to 2 numerics
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
    print(f'{dt=}')
    month = int(dt[4]) if dt[3] == '0' else int(dt[3:5])
    day = int(dt[1]) if dt[0] == '0' else int(dt[:2])

    try:
        datetime_date = datetime.date(int(dt[6:10]), month, day)
    except Exception:
        datetime_date = None

    return(recorded_date, datetime_date )

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads a CSV file of manually prepared data into the LocationEvent table"

    def handle(self, *args, **options):

            print("Loading LocationEvents")
            # Encoding of utf-8-sig will treat the Byte Order Mark of //ueff coming from the Excel csv file save as metadata rather than content
            with open(input_filename, encoding="utf-8-sig") as csvfile:
                for row in DictReader(csvfile):
                    print(f'{row=}')
                    le = LocationEvent()
                    le.type = row['type']
                    le.description = row['description']
                    le.date, le.datefield = dateformatter(row['date'])
                    # An alternative if location_wikislug is not present
                    le.location_description = row['location_description']           
                 
                    try:
                        loc = Location.objects.get(wikislug=row['location_wikislug'])
                    except ObjectDoesNotExist:
                        print(f"Location Wikipedia Slug {row['location_wikislug']} cannot be found in the TPAM database")
                    else:
                        try:
                            le.location_fk = loc
                        except Exception as e:
                            print(loc, e)

                    try:
                        route = Route.objects.get(wikipedia_slug=row['route_wikislug'])
                    except ObjectDoesNotExist:
                        print(f"Route Wikipedia Slug {row['route_wikislug']} cannot be found in the TPAM database")
                    else:
                        try:
                            le.route_fk = route
                        except Exception as e:
                            print(route, e)
                            
                    try:
                        le.save()
                        print(f'{le.type} {le.description} saved')
                    except Exception as e:
                        print(f'{le.type} {le.description} not saved due to {e}')