"""
Takes a list of UK railway companies and wikipedia categories under which they are listed, combines
with a manually maintained list of codes, and loads into the TPAM railway company table
"""

import os
import pandas as pd

from csv import DictReader
from django.core.management import BaseCommand
from companies.models import Company, CompanyCategory

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input1 = os.path.join(DATAIO_DIR, "Companies_Extract_Wikipedia_20230325.csv")
input2 = os.path.join(DATAIO_DIR, "Companies_Manual_Codes.csv")
merged = os.path.join(DATAIO_DIR, "Companies_Merged.csv")

df1 = pd.read_csv(os.path.join(input1), header=0, encoding='utf-8')
df1.drop_duplicates(subset=['category', 'wikislug', 'name'], inplace=True)
df1.sort_values(by=['name'], inplace=True)
df2 = pd.read_csv(os.path.join(input2), header=0, encoding='utf-8')
df_merge = pd.merge(df1, df2, how="left", on="wikislug")
df_merge.to_csv(merged, encoding='utf-8')

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Company Data"

    def handle(self, *args, **options):
        if Company.objects.exists():
            print('Note there is some Company data already loaded...but continuing nevertheless.')
        else:
            print("Creating Companies")
        count = 0
        for row in DictReader(open(merged)):
            if count != 0:
                company_fk, company_created = Company.objects.get_or_create(
                    name=row['name_x'],
                    code=row['code'],
                    wikislug = row['wikislug'],
                    )

                if row['category'] != '':

                    company_category_fk, company_category_created = CompanyCategory.objects.get_or_create(
                        category=row['category'],
                        )
 
                    company_fk.company_category_fk.add(company_category_fk)
                                               
            count = count + 1

        print(f'{count} Companies Loaded along with associated Company Categories')