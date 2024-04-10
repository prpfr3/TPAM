# Extracts a list of sheds from Wikipedia and loads into the TPAM database

import os
from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location
from django.core.exceptions import ObjectDoesNotExist
from companies.models import Company

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUTFILE = "Depots_Cleansed.csv"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Depot Codes"

    def handle(self, *args, **options):
        if Location.objects.exists():
            print("Depot codes data already exists but continuing.")
        else:
            print("Creating Depot Codes for the first time")

        def add_company_to_instance(instance, company_slug, field_name):
            try:
                c = Company.objects.get(name=company_slug)
            except ObjectDoesNotExist:
                print(
                    f"The {field_name} company {company_slug} for location {instance} is not in the database"
                )
            except Exception as e:
                print(company_slug, e)
            else:
                try:
                    getattr(instance, field_name).add(c)
                    instance.save()
                except Exception as e:
                    print(company_slug, e)

        with open(os.path.join(DATAIO_DIR, INPUTFILE), encoding="utf-8-sig") as file:
            for row in DictReader(file):
                row_name = row["name"]
                instance = Location.objects.get(name=row_name)

                if row["Nationalisation"]:
                    add_company_to_instance(
                        instance, row["Nationalisation"], "owner_operators"
                    )

                # Example usage for row['fields']
                if row["Grouping"]:
                    add_company_to_instance(
                        instance, row["Grouping"], "owner_operators"
                    )

                # Example usage for row['fieldb']
                if row["Pre-Grouping"]:
                    add_company_to_instance(
                        instance, row["Pre-Grouping"], "owner_operators"
                    )
