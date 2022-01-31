# Loads the data cleansed file into TPAM

import os
from csv import DictReader

from django.core.management import BaseCommand
from locos.models import Builder

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Builder_Load_Final.csv into our Builder model"

    def handle(self, *args, **options):
        if Builder.objects.exists():
            print('Builder data already loaded...continuing.')
        else:
            print("Creating Builder for the first time")

        with open(os.path.join("D:\\Data", "TPAM", "Builder_Load_Final.csv"), encoding="utf-8") as file:   

            for row in DictReader(file):
                print(row)
                m = Builder()
                m.name = row['Builder_Name'] 
                m.wikislug = row['Wikipedia_slug']
                m.railuk_builder_code = row['RailUK_Builder_Code']
                m.brd_builder_code = row['BRD_Builder_Code']
                m.brsl_builder_code = row['BRSL_Builder_Code']
                m.date_opened = row['date_built_BRW']
                m.date_closed = row['date_closure_BRW']
                m.pre_grouping_owner = row['pre_grouping_owner']
                m.grouping_owner = row['grouping_owner']
                m.br_region_owner = row['br_region_owner']
                m.save()