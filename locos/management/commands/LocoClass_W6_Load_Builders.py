import os
import pandas as pd
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from companies.models import Company, Manufacturer
from locos.models import LocoClass
from people.models import Person

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
TEMP_FILE = "Class_W5_Load_Manufacturers_Temp.csv"
output_file = os.path.join(DATAIO_DIR, TEMP_FILE)

load_type = "WIKIAUTO"  # A load based purely on Wikipedia information
load_type = "WIKIMANUAL"  # A load based on manual cleansing where additional url links may have been added

cleaned = os.path.join(DATAIO_DIR, "Class_All_W3_Cleansed_Detail.csv")
df_cleaned = pd.read_csv(cleaned, header=0, encoding="utf-8")
df_cleaned_manufacturers = df_cleaned.loc[df_cleaned["2"] == "Builder"]
df_cleaned_manufacturers.drop(
    df_cleaned_manufacturers.columns.difference(
        [
            "0",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
        ]
    ),
    1,
    inplace=True,
)
df_cleaned_manufacturers.drop_duplicates(
    subset=["0", "3", "4", "5", "6", "7"], inplace=True
)  # Theoretically redundant if duplicates dropped when cleansing detail

if load_type == "WIKIAUTO":
    df_cleaned_manufacturers.to_csv(output_file, index=False, encoding="utf-8")
elif load_type == "WIKIMANUAL":
    manufacturers = os.path.join(
        DATAIO_DIR,
        "Class_Steam_Manually_Cleansed_Builder_to_Builder_Slug.csv",
    )
    df_manufacturers = pd.read_csv(manufacturers, header=0, encoding="utf-8")
    df_merged_manufacturers = df_cleaned_manufacturers.merge(
        df_manufacturers, left_on=["3"], right_on=["a"], how="left"
    )
    df_merged_manufacturers.drop(["3", "a"], axis=1, inplace=True)
    df_merged_manufacturers.to_csv(output_file, index=False, encoding="utf-8")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the ClassManufacturer model"

    def handle(self, *args, **options):
        with open(os.path.join(DATAIO_DIR, TEMP_FILE), encoding="utf-8-sig") as file:
            for row in DictReader(file):
                c = LocoClass()
                try:
                    classslug = row["0"].replace("/wiki/", "")
                    c = LocoClass.objects.get(lococlasslist__wikislug=classslug)
                except ObjectDoesNotExist:
                    print(classslug, " not found in the Lococlass wikislug field")
                except MultipleObjectsReturned:
                    print(f"Multiple entries for {classslug} found in LocoClassList")
                else:
                    if load_type == "WIKIAUTO":
                        columns = [
                            "4",
                            "5",
                            "6",
                            "7",
                            "8",
                            "9",
                            "10",
                            "11",
                            "12",
                            "13",
                            "14",
                            "15",
                            "16",
                        ]
                    elif load_type == "WIKIMANUAL":
                        columns = ["b", "c", "d", "e", "f", "g", "h", "i"]

                    for column in columns:
                        if row[column] == "/wiki/Ashford_railway_works":
                            row[column] = "/wiki/Ashford_railway_works"
                        if row[column] == "/wiki/Ashford_Works":
                            row[column] = "/wiki/Ashford_railway_works"
                        if row[column] == "/wiki/Vulcan_Iron_Works":
                            row[column] = "/wiki/Vulcan_Iron_Works#Locomotives"
                        if row[column] == "/wiki/H._K._Porter,_Inc":
                            row[column] = "/wiki/H.K._Porter,_Inc."
                        if row[column] == "/wiki/Hawthorn_Leslie_and_Company":
                            row[column] = "/wiki/R._&_W._Hawthorn,_Leslie_and_Company"
                        if row[column] == "/wiki/Hawthorn_Leslie_%26_Co":
                            row[column] = "/wiki/R._&_W._Hawthorn,_Leslie_and_Company"
                        if row[column] == "/wiki/Hawthorn_Leslie":
                            row[column] = "/wiki/R._%26_W._Hawthorn,_Leslie_and_Company"
                        if row[column] == "/wiki/Nasmyth,_Gaskell_and_Company":
                            row[column] = "/wiki/Nasmyth,_Gaskell_and_Company"
                        if row[column] == "/wiki/Vulcan_Foundry":
                            row[column] = "/wiki/Vulcan_Foundry"
                        if row[column] == "/wiki/Neilson_and_Company":
                            row[column] = "/wiki/Neilson_and_Company"
                        if row[column] == "/wiki/Kerr,_Stuart_and_Company":
                            row[column] = "/wiki/Kerr,_Stuart_and_Company"
                        if row[column] == "/wiki/Kerr,_Stuart_%26_Company":
                            row[column] = "/wiki/Kerr,_Stuart_and_Company"
                        if row[column] == "/wiki/Kerr,_Stuart_%26_Co.":
                            row[column] = "/wiki/Kerr,_Stuart_and_Company"
                        if row[column] == "/wiki/Kerr_Stuart":
                            row[column] = "/wiki/Kerr,_Stuart_and_Company"
                        if row[column] == "/wiki/St._Rollox_railway_works":
                            row[column] = "/wiki/Glasgow_Works"
                        if row[column] == "/wiki/Sharp,_Stewart_and_Company":
                            row[column] = "/wiki/Sharp,_Stewart_and_Company"
                        if row[column] == "/wiki/Gorton_locomotive_works":
                            row[column] = "/wiki/Gorton_Locomotive_Works"
                        if row[column] == "/wiki/Gorton_Works":
                            row[column] = "/wiki/Gorton_Locomotive_Works"
                        if row[column] == "/wiki/North_British_Locomotive_Co.":
                            row[column] = "/wiki/North_British_Locomotive_Company"
                        if row[column] == "/wiki/Beyer,_Peacock_%26_Co.":
                            row[column] = "/wiki/Beyer,_Peacock_and_Company"
                        if row[column] == "/wiki/Beyer,_Peacock_%26_Company":
                            row[column] = "/wiki/Beyer,_Peacock_and_Company"
                        if row[column] == "/wiki/Beyer_Peacock":
                            row[column] = "/wiki/Beyer,_Peacock_and_Company"
                        if row[column] == "/wiki/Kitson_%26_Co.":
                            row[column] = "/wiki/Kitson_and_Company"
                        if row[column] == "/wiki/Kitson_%26_Company":
                            row[column] = "/wiki/Kitson_and_Company"
                        if row[column] == "/wiki/Yorkshire_Engine_Co.":
                            row[column] = "/wiki/Yorkshire_Engine_Company"
                        if row[column] == "/wiki/Electro-Motive_Diesel":
                            row[column] = "/wiki/Yorkshire_Engine_Company"
                        if row[column] == "/wiki/F._C._Hibberd_%26_Co_Ltd":
                            row[column] = "/wiki/F._C._Hibberd_&_Co."
                        if row[column] == "/wiki/Harland_%26_Wolff":
                            row[column] = "/wiki/Harland_and_Wolff"
                        if row[column] == "/wiki/Ruston_%26_Hornsby":
                            row[
                                column
                            ] = "/wiki/Ruston_(engine_manufacturer)#Ruston_&_Hornsby"
                        if row[column] == "/wiki/Vossloh_Espa%C3%B1a":
                            row[column] = "/wiki/MACOSA#Vossloh_España"
                        if row[column] == "/wiki/Vossloh":
                            row[column] = "/wiki/MACOSA#Vossloh_España"
                        if row[column] == "/wiki/Gateshead":
                            row[column] = "/wiki/Gateshead_TMD#Gateshead_Railway_Works"
                        if row[column] == "/wiki/Gateshead_railway_works":
                            row[column] = "/wiki/Gateshead_TMD#Gateshead_Railway_Works"
                        if row[column] == "/wiki/Gateshead_works":
                            row[column] = "/wiki/Gateshead_TMD#Gateshead_Railway_Works"
                        if row[column] == "/wiki/Brighton_Works":
                            row[column] = "/wiki/Brighton_railway_works"
                        if row[column] == "/wiki/Darlington_railway_works":
                            row[column] = "/wiki/Darlington_Works"
                        if row[column] == "/wiki/Doncaster_railway_works":
                            row[column] = "/wiki/Doncaster_Works"
                        if row[column] == "/wiki/Crewe_works":
                            row[column] = "/wiki/Crewe_Works"
                        if row[column] == "/wiki/Nine_Elms_Works":
                            row[column] = "/wiki/Nine_Elms_Locomotive_Works"
                        if row[column] == "/wiki/Robert_Stephenson_%26_Co.":
                            row[column] = "/wiki/Robert_Stephenson_and_Company"
                        if row[column] == "/wiki/Neilson_%26_Co.":
                            row[column] = "/wiki/Neilson_and_Company"
                        if row[column] == "/wiki/Neilson,_Reid_and_Company":
                            row[column] = "/wiki/Neilson_and_Company"
                        if row[column] == "/wiki/Neilson,_Reid_%26_Co.":
                            row[column] = "/wiki/Neilson_and_Company"
                        if row[column] == "/wiki/Sharp,_Stewart_%26_Co.":
                            row[column] = "/wiki/Sharp,_Stewart_and_Company"
                        if row[column] == "/wiki/Sharp_Stewart":
                            row[column] = "/wiki/Sharp,_Stewart_and_Company"
                        if row[column] == "/wiki/Sharp_Stewart_and_Company":
                            row[column] = "/wiki/Sharp,_Stewart_and_Company"
                        if row[column] == "/wiki/Nasmyth,_Wilson_%26_Co.":
                            row[column] = "/wiki/Nasmyth,_Gaskell_and_Company"
                        if row[column] == "/wiki/William_Beardmore_%26_Co.":
                            row[column] = "/wiki/William_Beardmore_and_Company"
                        if row[column] == "/wiki/W.G._Bagnall":
                            row[column] = "/wiki/W._G._Bagnall"
                        if row[column] == "/wiki/Soci%C3%A9t%C3%A9_Franco-Belge":
                            row[column] = "/wiki/Société_Franco-Belge"
                        if row[column] == "/wiki/D%C3%BCbs_%26_Co.":
                            row[column] = "/wiki/Dübs_and_Company"
                        if row[column] == "/wiki/D%C3%BCbs_%26_Company":
                            row[column] = "/wiki/Dübs_and_Company"
                        if row[column] == "/wiki/D%C3%BCbs_and_Company":
                            row[column] = "/wiki/Dübs_and_Company"
                        if row[column] == "/wiki/R_%26_W_Hawthorn":
                            row[column] = "/wiki/R_and_W_Hawthorn"
                        if row[column] == "/wiki/R._%26_W._Hawthorn_%26_Co.":
                            row[column] = "/wiki/R_and_W_Hawthorn"
                        if (
                            row[column]
                            == "/wiki/Soci%C3%A9t%C3%A9_Alsacienne_de_Constructions_M%C3%A9caniques"
                        ):
                            row[
                                column
                            ] = "/wiki/Société_Alsacienne_de_Constructions_Mécaniques"
                        if (
                            row[column]
                            == "/wiki/R._%26_W._Hawthorn,_Leslie_and_Company"
                        ):
                            row[column] = "/wiki/R._&_W._Hawthorn,_Leslie_and_Company"
                        if row[column] == "/wiki/Gorton_Foundry":
                            row[column] = "/wiki/Gorton_Locomotive_Works"
                        if row[column] == "/wiki/Dick,_Kerr_%26_Co.":
                            row[column] = "/wiki/Dick,_Kerr_&_Co."
                        if row[column] == "/wiki/Andrew_Barclay_Sons_%26_Co":
                            row[column] = "/wiki/Andrew_Barclay_Sons_&_Co."
                        if row[column] == "/wiki/Andrew_Barclay_%26_Sons_Co.":
                            row[column] = "/wiki/Andrew_Barclay_Sons_&_Co."
                        if row[column] != "":
                            # print('row 2', row[column])
                            try:
                                slug = row[column].replace("/wiki/", "")
                                # print(slug)
                                manufacturer = Manufacturer.objects.get(wikislug=slug)
                                c.manufacturers.add(manufacturer)
                                c.save()
                            except ObjectDoesNotExist:
                                try:
                                    person = Person.objects.get(wikitextslug=slug)
                                    print(
                                        f"The manufacturer {slug} for class {classslug} is a person {person}, not a manufacturer"
                                    )
                                except ObjectDoesNotExist:
                                    try:
                                        company = Company.objects.get(wikislug=slug)
                                        print(
                                            f"The manufacturer {slug} for class {classslug} is a company {company}, not a manufacturer"
                                        )
                                    except ObjectDoesNotExist:
                                        print(
                                            f"The manufacturer {slug} for class {classslug} is neither a manufacturer, company or person"
                                        )
                                        continue
                            except Exception as err:
                                print(row, err)
