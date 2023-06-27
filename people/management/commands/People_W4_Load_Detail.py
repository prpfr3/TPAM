from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from people.models import Person
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


def clean_died(died_uncleansed):
    preclean = died_uncleansed
    deathdate_cleansed = ""
    deathdate_partial_cleansed = ""
    deathplace = ""

    # If we come across ( we know we have a date and we will start to process it)
    in_parentheses = False
    # Used to checkk if already has been one set of parentheses
    first_parenthesis_processed = False
    full_reference = False  # Flags if character is part of full_reference

    died_uncleansed = died_uncleansed.replace("-Jan-", "-01-")
    died_uncleansed = died_uncleansed.replace("-Feb-", "-02-")
    died_uncleansed = died_uncleansed.replace("-Mar-", "-03-")
    died_uncleansed = died_uncleansed.replace("-Apr-", "-04-")
    died_uncleansed = died_uncleansed.replace("-May-", "-05-")
    died_uncleansed = died_uncleansed.replace("-Jun-", "-06-")
    died_uncleansed = died_uncleansed.replace("-Jul-", "-07-")
    died_uncleansed = died_uncleansed.replace("-Aug-", "-08-")
    died_uncleansed = died_uncleansed.replace("-Sep-", "-09-")
    died_uncleansed = died_uncleansed.replace("-Oct-", "-10-")
    died_uncleansed = died_uncleansed.replace("-Nov-", "-11-")
    died_uncleansed = died_uncleansed.replace("-Dec-", "-12-")
    died_uncleansed = died_uncleansed.replace(" January ", "-01-")
    died_uncleansed = died_uncleansed.replace(" February ", "-02-")
    died_uncleansed = died_uncleansed.replace(" March ", "-03-")
    died_uncleansed = died_uncleansed.replace(" April ", "-04-")
    died_uncleansed = died_uncleansed.replace(" May ", "-05-")
    died_uncleansed = died_uncleansed.replace(" June ", "-06-")
    died_uncleansed = died_uncleansed.replace(" July ", "-07-")
    died_uncleansed = died_uncleansed.replace(" August ", "-08-")
    died_uncleansed = died_uncleansed.replace(" September ", "-09-")
    died_uncleansed = died_uncleansed.replace(" October ", "-10-")
    died_uncleansed = died_uncleansed.replace(" November ", "-11-")
    died_uncleansed = died_uncleansed.replace(" December ", "-12-")
    died_uncleansed = died_uncleansed.replace("January ", "-01-")
    died_uncleansed = died_uncleansed.replace("February ", "-02-")
    died_uncleansed = died_uncleansed.replace("March ", "-03-")
    died_uncleansed = died_uncleansed.replace("April ", "-04-")
    died_uncleansed = died_uncleansed.replace("May ", "-05-")
    died_uncleansed = died_uncleansed.replace("June ", "-06-")
    died_uncleansed = died_uncleansed.replace("July ", "-07-")
    died_uncleansed = died_uncleansed.replace("August ", "-08-")
    died_uncleansed = died_uncleansed.replace("September ", "-09-")
    died_uncleansed = died_uncleansed.replace("October ", "-10-")
    died_uncleansed = died_uncleansed.replace("November ", "-11-")
    died_uncleansed = died_uncleansed.replace("December ", "-12-")
    died_uncleansed = died_uncleansed.replace("96 years", "aged 96 years")
    died_uncleansed = died_uncleansed.replace("Ã", "")
    died_uncleansed = died_uncleansed.replace("aged 73", "")
    died_uncleansed = died_uncleansed.replace("74 Grove Street", "Grove Street")

    for char in died_uncleansed:
        # print(type(char), char)

        if char.isnumeric():  # As soon as a numeric appears, stop dropping alphabetics
            drop_alpha = False
        if char.isalpha():  # As soon as an alphabetic appears, stop dropping commas
            drop_comma = False

        if char == "(":
            in_parentheses = True
        if char == ")" and first_parenthesis_processed == False:
            in_parentheses = False
            first_parenthesis_processed = True
        if char == "[":
            full_reference = True
        if char == "]":
            full_reference = False
        if char == "(":
            in_parentheses = True
        if char == ")":
            in_parentheses = False
        if char.isalpha() and in_parentheses == True:  # Age must b e in the parens so treat as processed
            first_parenthesis_processed = True

        if char.isnumeric() and in_parentheses == True and first_parenthesis_processed == False and full_reference == False:
            deathdate_cleansed = deathdate_cleansed + char
        if char == "-" and in_parentheses == True and first_parenthesis_processed == False and full_reference == False:
            deathdate_cleansed = deathdate_cleansed + char

        if char.isnumeric() and in_parentheses == False and full_reference == False:
            deathdate_partial_cleansed = deathdate_partial_cleansed + char
        # if char == "-" and in_parentheses == False and full_reference == False:
        #     deathdate_partial_cleansed = deathdate_partial_cleansed + char

        if char.islower() and in_parentheses == False:
            deathplace = deathplace + char
        if char.isupper() and in_parentheses == False:
            deathplace = deathplace + " " + char
        if char == "," and in_parentheses == False:
            deathplace = deathplace + char

    if deathdate_cleansed:
        deathdate_partial_cleansed = ""
    if len(deathdate_partial_cleansed) == 4:
        deathdate_partial_cleansed = "????" + deathdate_partial_cleansed
    if len(deathdate_partial_cleansed) == 5:
        deathdate_partial_cleansed = "??0" + deathdate_partial_cleansed
    if len(deathdate_partial_cleansed) == 6:
        deathdate_partial_cleansed = "??" + deathdate_partial_cleansed
    if len(deathdate_partial_cleansed) == 7:
        deathdate_partial_cleansed = "0" + deathdate_partial_cleansed
    if len(deathdate_partial_cleansed) == 8:
        deathdate_cleansed = deathdate_partial_cleansed[4:8] + "-" + \
            deathdate_partial_cleansed[2:4] + "-" + \
            deathdate_partial_cleansed[0:2]
        deathdate_partial_cleansed = ""

    deathplace = deathplace.lstrip()

    if deathdate_partial_cleansed != "":
        print("Could only parse ", preclean, " as ", deathdate_partial_cleansed)

    return (deathdate_cleansed, deathplace)


def clean_born(born_uncleansed):
    preclean = born_uncleansed
    birthdate_cleansed = ""
    birthdate_partial_cleansed = ""
    birthplace = ""

    drop_alpha = True  # Drop alphabetic characters until after we have processed a numeric date
    # Drop commas (in dates) until we reach an alpha which will be part of an address
    drop_comma = True
    # If we come across ( we know we have a date and we will start to process it)
    in_parentheses = False
    full_reference = False  # Flags if character is part of full_reference

    born_uncleansed = born_uncleansed.replace(" January ", "-01-")
    born_uncleansed = born_uncleansed.replace(" February ", "-02-")
    born_uncleansed = born_uncleansed.replace(" March ", "-03-")
    born_uncleansed = born_uncleansed.replace(" April ", "-04-")
    born_uncleansed = born_uncleansed.replace(" May ", "-05-")
    born_uncleansed = born_uncleansed.replace(" June ", "-06-")
    born_uncleansed = born_uncleansed.replace(" July ", "-07-")
    born_uncleansed = born_uncleansed.replace(" August ", "-08-")
    born_uncleansed = born_uncleansed.replace(" September ", "-09-")
    born_uncleansed = born_uncleansed.replace(" October ", "-10-")
    born_uncleansed = born_uncleansed.replace(" November ", "-11-")
    born_uncleansed = born_uncleansed.replace(" December ", "-12-")
    born_uncleansed = born_uncleansed.replace("January ", "-01-")
    born_uncleansed = born_uncleansed.replace("February ", "-02-")
    born_uncleansed = born_uncleansed.replace("March ", "-03-")
    born_uncleansed = born_uncleansed.replace("April ", "-04-")
    born_uncleansed = born_uncleansed.replace("May ", "-05-")
    born_uncleansed = born_uncleansed.replace("June ", "-06-")
    born_uncleansed = born_uncleansed.replace("July ", "-07-")
    born_uncleansed = born_uncleansed.replace("August ", "-08-")
    born_uncleansed = born_uncleansed.replace("September ", "-09-")
    born_uncleansed = born_uncleansed.replace("October ", "-10-")
    born_uncleansed = born_uncleansed.replace("November ", "-11-")
    born_uncleansed = born_uncleansed.replace("December ", "-12-")
    born_uncleansed = born_uncleansed.replace("74 Grove Street", "Grove Street")

    for char in born_uncleansed:

        if char.isnumeric():  # As soon as a numeric appears, stop dropping alphabetics
            drop_alpha = False
        if char.isalpha():  # As soon as an alphabetic appears, stop dropping commas
            drop_comma = False

        if char == "(":
            in_parentheses = True
        if char == ")":
            in_parentheses = False
        if char == "[":
            full_reference = True
        if char == "]":
            full_reference = False

        if char.isnumeric() and in_parentheses == True:
            birthdate_cleansed = birthdate_cleansed + char
        if char == "-" and in_parentheses == True:
            birthdate_cleansed = birthdate_cleansed + char

        if char.isnumeric() and in_parentheses == False and full_reference == False:
            birthdate_partial_cleansed = birthdate_partial_cleansed + char

        if char.islower() and drop_alpha == False:
            birthplace = birthplace + char
        if char.isupper() and drop_alpha == False:
            birthplace = birthplace + " " + char
        if char == "," and drop_comma == False:
            birthplace = birthplace + char

    if birthdate_cleansed:
        birthdate_partial_cleansed = ""
    if len(birthdate_partial_cleansed) == 4:
        birthdate_partial_cleansed = "????" + birthdate_partial_cleansed
    if len(birthdate_partial_cleansed) == 5:
        birthdate_partial_cleansed = "??0" + birthdate_partial_cleansed
    if len(birthdate_partial_cleansed) == 6:
        birthdate_partial_cleansed = "??" + birthdate_partial_cleansed
    if len(birthdate_partial_cleansed) == 7:
        birthdate_partial_cleansed = "0" + birthdate_partial_cleansed
    if len(birthdate_partial_cleansed) == 8:
        birthdate_cleansed = birthdate_partial_cleansed[4:8] + "-" + \
            birthdate_partial_cleansed[2:4] + "-" + \
            birthdate_partial_cleansed[0:2]
        birthdate_partial_cleansed = ""

    if len(birthdate_cleansed) == 4:
        birthdate_cleansed = birthdate_cleansed + "-??-??"

    birthplace = birthplace.lstrip()

    if birthdate_partial_cleansed != "":
        print("Could only parse ", preclean, " as ", birthdate_partial_cleansed)
    return (birthdate_cleansed, birthplace)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into a Persons model"

    def handle(self, *args, **options):
        print("Creating Person details")
        import os

        # This form of statement top ensure correct treatement of unusual unicode characters
        with open(os.path.join(DATAIO_DIR, 'People_Detail_Extract_Wikipedia.csv'), encoding="utf-8") as file:
            for row in DictReader(file):
                try:
                    c = Person.objects.get(
                        wikitextslug=row['Column1'].replace('/wiki/', ''))
                except Exception as e:
                    print(row['Column1'], e)
                else:
                    if row['Column3'] == "Born":
                        c.birthdate, c.birthplace = clean_born(row['Column4'])
                    if row['Column3'] == "Died":
                        c.dieddate, c.diedplace = clean_died(row['Column4'])
                    elif row['Column3'] == "Nationality":
                        if row['Column4'] == "British[1]":
                            row['Column4'] = "British"
                        if row['Column4'] == "England":
                            row['Column4'] = "English"
                        c.nationality = row['Column4']
                    elif row['Column3'] == "Occupation":
                        c.occupation = row['Column4']

                    try:
                        c.save()
                    except Exception as e:
                        print(row['Column1'], 'VALUE=', row['Column3'],
                              '=', row['Column4'], '\n', e)
