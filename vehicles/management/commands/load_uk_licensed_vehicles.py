"""
Extracts data from UK Government Vehicles Data

VEH0124: Licensed vehicles by make and model and year of first registration: United Kingdom. Dataset available, along with explanatory notes at:-

https://www.gov.uk/government/statistical-data-sets/all-vehicles-veh01

Data is in the form of an ODS dataset (Spreadsheet Open File Format) with multiple tabs of similar format contain a constant number of header rows and a variable number of footer rows which should not be extracted

Requires package odfpy to be installed for the odf engine to be used on the pandas.read_excel
"""

import sys
import os
import pandas as pd 
import numpy as np
from pathlib import Path
from django.core.management import BaseCommand
from vehicles.models import UKLicensedVehicles, VehicleType, VehicleMake, VehicleModel, VehicleVariant

# Part 1: Extract and Transform the Data from the govuk ODS dataset
"""
def veh0124_import(veh0124_file, year):

    cwd = os.getcwd()
    pd.set_option('display.max_columns', None)
    
    try: 
        new_working_directory = Path("D:\MLDatasets\govuk_vehicle_stats")
        os.chdir(new_working_directory)
        print("Working directory is:-", os.getcwd()) 
    except: 
        print("Something wrong with specified data directory. Exception- ")
        print(sys.exc_info())
        sys.exit(0)

    for sheet in ['Cars', 'Motorcycles', 'LGVs', 'HGVs', 'Buses', 'Others']:

        #Read in the Excel sheets varying the number of rows dropped on the bottom by sheet
        #Tidy up Excel column names which have gained numbers due to footnote references, allowing for the 'Others' sheet having different names

        if sheet == 'Others':
            veh0124_sheet = pd.read_excel(veh0124_file, header=6, skipfooter=12, sheet_name=sheet, engine='odf') #12 rows of footnotes skipped
            veh0124_sheet.rename(columns={'Make': 'make', 'Generic model 3': 'model', 'Model 3': 'variant'}, inplace=True)
        else:
            veh0124_sheet = pd.read_excel(veh0124_file, header=6, skipfooter=11, sheet_name=sheet, engine='odf') #11 rows of footnotes skipped
            veh0124_sheet.rename(columns={'Make': 'make', 'Generic model 2': 'model', 'Model 2': 'variant'}, inplace=True)

        print(veh0124_sheet.head())
        print(veh0124_sheet.tail())
        print(veh0124_sheet.shape)
        print('about to melt the dataframe\n')

        veh0124_sheet_melted = veh0124_sheet.melt(id_vars=['make', 'model', 'variant'], var_name='year_licensed', value_name='number_licensed')

        print(veh0124_sheet_melted.head())
        print(veh0124_sheet_melted.tail())
        print(veh0124_sheet_melted.shape)
        print('about to add the extra fields\n')

        #veh0124_sheet_melted['number_licensed'].fillna(0, inplace=True)
        #veh0124_sheet_melted = veh0124_sheet_melted[veh0124_sheet_melted['number_licensed'].notna()]
        veh0124_sheet_melted.dropna(subset = ['number_licensed'], inplace=True)
        veh0124_sheet_melted['vehicle_type'] = sheet
        veh0124_sheet_melted['year_ending'] = year
        
        print(veh0124_sheet_melted.head())
        print(veh0124_sheet_melted.tail())
        print(veh0124_sheet_melted.shape)
        print('about to append the tables\n')

        if sheet == 'Cars':
            veh0124_melted = veh0124_sheet_melted
        else:
            veh0124_melted = veh0124_melted.append(veh0124_sheet_melted, ignore_index=True)

        print(veh0124_melted.head())
        print(veh0124_melted.tail())
        print(veh0124_melted.shape)

        import pandas_profiling as pp
        profile = pp.ProfileReport(veh0124_melted)
        profile.to_file(f"veh0124_melted_{year}.pkl")

        veh0124_melted.to_pickle(f"./{veh0124_file}_melted.pkl")

latest_year = '2020' #Data usually available in May of the following year
veh0124_import(f"veh0124_end_{latest_year}.ods", latest_year)

veh0124_melted = pd.read_pickle(f"veh0124_melted_{year}.pkl")
"""

new_working_directory = Path("D:\MLDatasets\govuk_vehicle_stats")
os.chdir(new_working_directory)
veh0124_melted = pd.read_pickle(f"veh0124_melted_2020.pkl")

# Part 2. Load the data into the Django Model

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Pandas into our RVLicensed model"

    def handle(self, *args, **options):
        #if RVLicensed.objects.exists():
        #    print('Data already loaded...exiting.')
        #    return
        print("Loading Licensed Vehicles Details")

        """
        #This code would be used if we were creating a flat Django table rather than a full normalised table as per the code that follows
        RVLicensed.objects.bulk_create(
            RVLicensed(**vals) for vals in veh0124_melted.to_dict('records')
        )
        """
        i = 1
        for vals in veh0124_melted.to_dict('records'):
            type_fk, type_created = VehicleType.objects.get_or_create(type=vals['vehicle_type'])
            make_fk, make_created = VehicleMake.objects.get_or_create(make=vals['make'], type=type_fk)
            model_fk, model_created = VehicleModel.objects.get_or_create(model=vals['model'], make=make_fk)
            variant_fk, variant_created = VehicleVariant.objects.get_or_create(variant=vals['variant'], model=model_fk)
            l = UKLicensedVehicles()
            l.year_ending = vals['year_ending']
            l.type = type_fk
            l.make = make_fk
            l.model = model_fk
            l.variant = variant_fk
            l.year_licensed = vals['year_licensed']
            l.number_licensed = vals['number_licensed']
            #Code for a short test
            #print(l)
            #i = i + 1
            #if i == 100:
            #    break
            l.save()