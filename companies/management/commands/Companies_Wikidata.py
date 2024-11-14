"""
SELECT ?company ?companyLabel ?formationDate ?replaces ?replacesLabel ?dissolutionDate ?absorbedInto ?absorbedIntoLabel WHERE {
  # Define the company as a railway company (Q249556)
  ?company wdt:P31 wd:Q249556 .
  
  # Filter by companies located in the UK (Q145) or Great Britain (Q174193) using UNION effectively
  VALUES ?country { wd:Q174193 wd:Q145 }
  ?company wdt:P17 ?country.

  # Get the company's formation date (P571), dissolution or abolished date (P576), 
  # the company it was absorbed into (P1366), and the company it replaced (P1365)
  OPTIONAL { ?company wdt:P571 ?formationDate. }
  OPTIONAL { ?company wdt:P576 ?dissolutionDate. }
  OPTIONAL { ?company wdt:P1366 ?absorbedInto. }
  OPTIONAL { ?company wdt:P1365 ?replaces. }
  
  # Include labels
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
"""

from csv import DictReader
from django.core.management import BaseCommand
from companies.models import *

input_filename = "D://Data/TPAM/Companies_Wikidata_Extract.csv"


class Command(BaseCommand):
    help = "Loads Wikidata Engineer Line Reference Data"

    def handle(self, *args, **options):

        companies_added = 0

        with open(input_filename, encoding="utf-8-sig") as file:

            for row in DictReader(file):
                instance = Company()
                try:
                    instances = Company.objects.filter(name=row["companyLabel"])
                except Exception as e:
                    print(f'Error {e} for {row["company"]}')

                for instance in instances:
                    instance.wikidata_id = row["company"]
                    instance.name = row["companyLabel"]
                    instance.date_formed = row["formationDate"][0:10]
                    instance.date_succeeded = row["dissolutionDate"][0:10]
                    instance.save()
                    companies_added += 1

                    if row["absorbedInto"]:
                        successors = Company.objects.filter(
                            wikidata_id=row["absorbedInto"]
                        )

                        for successor in successors:
                            instance.successor_company = successor
                            print(
                                f"{instance.wikidata_id} absorbed into {instance.successor_company}"
                            )
                            instance.save()

        print(f"{companies_added=}")
