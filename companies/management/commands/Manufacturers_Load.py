# Loads the data cleansed file into TPAM

import os
from csv import DictReader

from django.core.management import BaseCommand
from companies.models import Manufacturer

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Manufacturer_Load_Final.csv into our Manufacturer model"

    def handle(self, *args, **options):
        if Manufacturer.objects.exists():
            print('Manufacturer data already loaded...continuing.')
        else:
            print("Creating Manufacturer for the first time")

        with open(os.path.join("D:\\Data", "TPAM", "Manufacturer_Load_Final.csv"), encoding="utf-8") as file:   

            for row in DictReader(file):
                m = Manufacturer()
                m.name = row['Builder_Name'] 
                m.wikislug = row['Wikipedia_slug'].replace("/wiki/","")
                m.railuk_manufacturer_code = row['RailUK_Builder_Code']
                m.brd_manufacturer_code = row['BRD_Builder_Code']
                m.brsl_manufacturer_code = row['BRSL_Builder_Code'] #OPC British Railway Steam Locomotives 1948-1968 
                m.date_opened = row['date_built_BRW'] #British Railway Works book
                m.date_closed = row['date_closure_BRW']
                m.pre_grouping_owner = row['pre_grouping_owner']
                m.grouping_owner = row['grouping_owner']
                m.br_region_owner = row['br_region_owner']
                m.save()