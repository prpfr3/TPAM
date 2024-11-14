"""
Takes a list of UK Acts of Parliament, tries to strip out the Company Name, searches for the Company name in the database and, if found, adds the act to the Company

06/09/24 Yet to enable the saving of the updates, whilst awaiting registration of more companies found mentioned in the list of acts
"""

import os
from csv import DictReader
from django.core.management import BaseCommand
from companies.models import Company, CompanyCategory
from notes.models import Reference
from datetime import datetime

input_file = os.path.join("D:\\Data", "TPAM", "Companies_Extract_AoP.csv")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads or Updates References from a csv file"

    def handle(self, *args, **options):
        print("Adding References")
        with open(input_file, encoding="utf-8-sig") as file:

            companies_not_found = []
            no_of_acts_added = 0

            for row in DictReader(file):

                try:
                    reference = Reference.objects.get(
                        title=row["title"],
                        url=row["title_url"],
                        type=8,
                    )

                    railway_in_act = row["title"].split("Railway")[0] + "Railway"
                    railway_in_act = railway_in_act.replace("The ", "")
                except Reference.DoesNotExist:
                    reference = None
                except Exception as e:
                    print(f" Error {e} for {row['title']}")

                try:
                    company = Company.objects.get(
                        name=railway_in_act,
                    )
                except Company.DoesNotExist:
                    company = None
                    if railway_in_act not in companies_not_found:
                        companies_not_found.append(railway_in_act)
                except Company.MultipleObjectsReturned:
                    print(f"Multiple Companies returned for {railway_in_act}")
                except Exception as e:
                    print(f" Error {e} for {railway_in_act}")

                if (
                    company
                    and reference
                    and company.references.filter(id=reference.id).exists()
                ):
                    company.references.add(reference)
                    no_of_acts_added += 1
                    print(f"{reference.title} saved to {company.name}")
                    # company.save()

        no_of_companies_not_found = 0

        import csv

        output_file = os.path.join(
            "D:\\Data", "TPAM", "Companies_with_AOP_not_in_TPAM.csv"
        )
        with open(output_file, "wt+", newline="", encoding="utf-8") as csvFile:
            output = csv.writer(csvFile)
            companies_not_found.sort()
            for company in companies_not_found:
                csvrow = []
                no_of_companies_not_found += 1
                csvrow.append(company)
                output.writerow(csvrow)

        print(f"No of Companies Not Found is {no_of_companies_not_found}")
        print(f"No of acts added to companies is {no_of_acts_added}")
