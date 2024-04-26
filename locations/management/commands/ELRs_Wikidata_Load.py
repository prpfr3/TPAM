"""
Loads Engineer Line References from Wikidata
============================================

Run a SPARQL in the Wikidata Query Service https://query.wikidata.org/ as per the following. 
P10271 means that an instance has a property of Engineer's Line Reference

    SELECT DISTINCT ?item ?itemLabel ?itemAltLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
    {
        SELECT DISTINCT ?item WHERE {
        ?item p:P10271 ?statement0.
        ?statement0 (ps:P10271) _:anyValueP10271.
        }
        LIMIT 10000
    }
    }

"""


from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Route, RouteCategory, RouteMap
import pandas as pd
import os
from locations.models import *

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

inputfile = os.path.join(DATAIO_DIR, "Wikidata_ELR.csv")
outputfile = os.path.join(DATAIO_DIR, "Wikidata_ELR_sorted.csv")

dfinput = pd.read_csv(os.path.join(inputfile), header=0, encoding='utf-8')
dfinput = dfinput.sort_values(by=['itemAltLabel'])
dfinput.to_csv(outputfile, encoding='utf-8')


class Command(BaseCommand):
    help = "Loads Wikidata Engineer Line Reference Data"

    def handle(self, *args, **options):
        if ELR.objects.exists():
            print('Wikidata Engineer Line Reference data already loaded...aborting.')
        else:
            print("Creating Engineer Line References")

            ELRs_added = 0

            with open(os.path.join(DATAIO_DIR, "Wikidata_ELR_sorted.csv"), encoding="utf-8") as file:

                for row in DictReader(file):
                    elr = ELR()
                    elr.item = row['item'].replace(
                        "http://www.wikidata.org/entity/", "")
                    itemAltLabel = row['itemAltLabel'].split(',')
                    # If the ELR Code includes superfluous description, move it to the item label as an aka
                    try:
                        elr.itemLabel = f"{row['itemLabel']} (aka. {itemAltLabel[1]})"
                    except Exception:
                        elr.itemLabel = row['itemLabel']
                    elr.itemAltLabel = itemAltLabel[0]
                    elr.save()
                    ELRs_added += 1

            print(f"{ELRs_added=}")
