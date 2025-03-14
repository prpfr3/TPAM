"""
Takes a list of UK ACts of Parliament and loads them into the Reference file
"""

import os
from csv import DictReader
from django.core.management import BaseCommand
from companies.models import Company
from notes.models import Reference

input_file = os.path.join("D:\\Data", "TPAM", "Companies_Extract_AoP.csv")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads or Updates References from a csv file"

    def handle(self, *args, **options):
        print("Adding References")
        with open(input_file, encoding="utf-8-sig") as file:

            references_count = 0
            references_allocated = 0

            for row in DictReader(file):

                try:
                    reference, reference_created = Reference.objects.get_or_create(
                        title=row["title"],
                        url=row["title_url"],
                        type=8,
                    )
                    if row["reference"]:
                        reference.year = str(
                            row["reference"][0:4],
                        )
                        reference.description = str(
                            row["type"] + " " + row["reference"],
                        )
                    else:
                        reference.description = row["type"]
                    # print(reference.description)
                except Exception as e:
                    print(e)

                try:
                    references_count = references_count + 1
                    reference.save()
                    # print(f"{reference} saved")
                except Exception as e:
                    print(f"{reference} not saved due to {e}")

                if "Railway Act" in reference.title:
                    name = reference.title.split(" Act")[0]
                    index = reference.title.find("Railway")
                    if index != -1:
                        name = reference.title[: index + len("Railway")]

                    companies_for_reference = Company.objects.filter(name=name)
                    for company in companies_for_reference:
                        if not company.references.filter(id=reference.id).exists():
                            company.references.add(reference)
                            references_allocated = references_allocated + 1
                        print(f"Reference {reference} added for Company {company}")
                        company.save()

                print(
                    f"{references_count} processed of which {references_allocated} were allocated to companies"
                )
