import os
import pandas as pd
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from companies.models import Company, Manufacturer
from people.models import Person
from locos.models import LocoClass

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
TEMP_FILE = "Class_W5_Load_Designers_Temp.csv"
output_file = os.path.join(DATAIO_DIR, TEMP_FILE)

cleaned = os.path.join(DATAIO_DIR, "Class_All_W3_Cleansed_Detail.csv")
df_cleaned = pd.read_csv(cleaned, header=0, encoding="utf-8")
df_cleaned_designers = df_cleaned.loc[df_cleaned["2"] == "Designer"]
# print(df_cleaned_designers.head())
df_cleaned_designers.drop(
    df_cleaned_designers.columns.difference(["0", "3", "4", "5", "6", "7"]),
    1,
    inplace=True,
)  # Drops the columns beyond 8
df_cleaned_designers.drop_duplicates(
    subset=["0", "3", "4", "5", "6", "7"], inplace=True
)  # Theoretically redundant if duplicates dropped when cleansing detail
# print(df_cleaned_designers.head())
df_cleaned_designers.to_csv(output_file, index=False, encoding="utf-8")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the ClassManufacturer model"

    def handle(self, *args, **options):
        with open(os.path.join(DATAIO_DIR, TEMP_FILE), encoding="utf-8") as file:
            for row in DictReader(file):
                lococlass = LocoClass()
                try:
                    slug = row["0"].replace("/wiki/", "")
                    lococlass = LocoClass.objects.get(lococlasslist__wikislug=slug)
                except ObjectDoesNotExist:
                    print(f"{slug} not found in the Lococlass wikipedia_slug field")
                else:
                    # columns = ['4', '5', '6', '7']
                    columns = ["4"]  # Only one designer now allowed

                    for column in columns:
                        if row[column] != "":
                            slug = row[column].replace("/wiki/", "")
                            try:
                                lococlass.designer_person = Person.objects.get(
                                    wikitextslug=slug
                                )
                                lococlass.save()
                            except ObjectDoesNotExist:
                                try:
                                    lococlass.designer_company = Company.objects.get(
                                        wikislug=slug
                                    )
                                    lococlass.save()
                                except ObjectDoesNotExist:
                                    try:
                                        lococlass.designer_company = (
                                            Manufacturer.objects.get(wikislug=slug)
                                        )
                                        print(
                                            slug,
                                            "is a Manufacturer which is not accepted as a designer",
                                        )
                                    except Exception:
                                        print(
                                            slug,
                                            " not in the company, person or manufacturer table",
                                        )
                                        continue
