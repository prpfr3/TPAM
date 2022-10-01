"""
FULL OR DELTA EXTRACT OF LOCOMOTIVE CLASSES

Traverses a set of pre-defined category pages and finds/stores all the url references on those pages 
checking to see if they are already present in the database before writing to an output file

Note that even after deduplication two urls could lead to the same webpage, 
due to a redirect (e.g. if a locomotive class had both an LNER and a NER class name)
"""
import csv
import os

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from locos.models import LocoClassList


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into a LocoClass model"

    def handle(self, *args, **options):

        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        REQUEST_HEADERS = {'User-Agent': 'LocoClass_W1_Scrape_Names.py; https://github.com/prpfr3/TPAM)'}

        output_file1 = os.path.join(DATAIO_DIR, "Class_All_W1_ClassNames_Full_delta.csv")
        csvFile1 = open(output_file1, 'wt+', newline='', encoding='utf-8')
        output1 = csv.writer(csvFile1)

        csvrow1 = []
        csvrow1.append("category")
        csvrow1.append("wikislug")
        csvrow1.append("name")
        output1.writerow(csvrow1)

        output_file2 = os.path.join(DATAIO_DIR, "Class_All_W1_ClassNames_Deduplicated_delta.csv")
        csvFile2 = open(output_file2, 'wt+', newline='', encoding='utf-8')
        output2 = csv.writer(csvFile2)

        csvrow2 = []
        csvrow2.append("wikislug")
        csvrow2.append("name")
        output2.writerow(csvrow2)

        Categories = ["https://en.wikipedia.org/wiki/Category:Standard_gauge_steam_locomotives_of_Great_Britain", 
                        "https://en.wikipedia.org/w/index.php?title=Category:Standard_gauge_steam_locomotives_of_Great_Britain&pagefrom=Gwr+1340+Trojan%0AGWR+No.+1340+Trojan#mw-pages",
                        "https://en.wikipedia.org/w/index.php?title=Category:Standard_gauge_steam_locomotives_of_Great_Britain&pagefrom=List+of+SECR+K+and+SR+K1+class+locomotives#mw-pages",
                        "https://en.wikipedia.org/w/index.php?title=Category:Standard_gauge_steam_locomotives_of_Great_Britain&pagefrom=Lswr+L12+Class%0ALSWR+L12+class#mw-pages",
                        "https://en.wikipedia.org/wiki/Category:London,_Midland_and_Scottish_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Caledonian_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Furness_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Glasgow_and_South_Western_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Highland_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Lancashire_and_Yorkshire_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:London_and_North_Western_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Midland_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:North_London_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Northern_Counties_Committee_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Somerset_and_Dorset_Joint_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:London_and_North_Eastern_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Great_Central_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Great_Eastern_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Great_Northern_Railway_(Great_Britain)_locomotives",
                        "https://en.wikipedia.org/wiki/Category:North_British_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:North_Eastern_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Hull_and_Barnsley_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Lancashire,_Derbyshire_and_East_Coast_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Southern_Railway_(UK)_locomotives",
                        "https://en.wikipedia.org/wiki/Category:London_and_South_Western_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:London,_Brighton_and_South_Coast_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:South_Eastern_and_Chatham_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Great_Western_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Barry_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Cambrian_Railways_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Port_Talbot_Railway_and_Docks_Company_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Rhymney_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Taff_Vale_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Lynton_and_Barnstaple_Railway_locomotives",
                        "https://en.wikipedia.org/wiki/Category:Standard_gauge_locomotives_of_Great_Britain", # Primarily Modern Locomotive Classes
                        ]

        # Pages that are not to be processed; primarily because they are not a class but rather a specific locomotive from within a a class
        class_exclusions = [
        "/wiki/BR_Standard_Class_4_2-6-0_76084",
        "/wiki/BR_Standard_Class_5_73050",
        "/wiki/BR_Standard_Class_5_73082_Camelot",
        "/wiki/BR_Standard_Class_5_73096",
        "/wiki/BR_Standard_Class_5_73129",
        "/wiki/BR_Standard_Class_5_73156",
        "/wiki/BR_Standard_Class_6_72010_Hengist",
        "/wiki/BR_Standard_Class_7_70013_Oliver_Cromwell",
        "/wiki/BR_Standard_Class_9F_92220_Evening_Star",
        "/wiki/GWR_1000_Class_1014_County_of_Glamorgan",
        "/wiki/GWR_2800_Class_2807",
        "/wiki/GWR_2900_Class_2999_Lady_of_Legend",
        "/wiki/GWR_3200_Class_9017_Earl_of_Berkeley",
        "/wiki/GWR_3700_Class_3440_City_of_Truro",
        "/wiki/GWR_4000_Class_4003_Lode_Star",
        "/wiki/GWR_4073_Class_4073_Caerphilly_Castle",
        "/wiki/GWR_4073_Class_4079_Pendennis_Castle",
        "/wiki/GWR_4073_Class_5029_Nunney_Castle",
        "/wiki/GWR_4073_Class_5043_Earl_of_Mount_Edgcumbe",
        "/wiki/GWR_4073_Class_5051_Earl_Bathurst",
        "/wiki/GWR_4073_Class_5080_Defiant",
        "/wiki/GWR_4073_Class_7027_Thornbury_Castle",
        "/wiki/GWR_4073_Class_7028_Cadbury_Castle",
        "/wiki/GWR_4073_Class_7029_Clun_Castle",
        "/wiki/GWR_4200_Class_4277",
        "/wiki/GWR_4575_Class_5542",
        "/wiki/GWR_4900_Class_4920_Dumbleton_Hall",
        "/wiki/GWR_4900_Class_4930_Hagley_Hall",
        "/wiki/GWR_4900_Class_4936_Kinlet_Hall",
        "/wiki/GWR_4900_Class_4953_Pitchford_Hall",
        "/wiki/GWR_4900_Class_4965_Rood_Ashton_Hall",
        "/wiki/GWR_4900_Class_4979_Wootton_Hall",
        "/wiki/GWR_4900_Class_5900_Hinderton_Hall",
        "/wiki/GWR_4900_Class_5952_Cogan_Hall",
        "/wiki/GWR_4900_Class_5967_Bickmarsh_Hall",
        "/wiki/GWR_4900_Class_5972_Olton_Hall",
        "/wiki/GWR_6000_Class_6000_King_George_V",
        "/wiki/GWR_6000_Class_6023_King_Edward_II",
        "/wiki/GWR_6000_Class_6024_King_Edward_I",
        "/wiki/GWR_6800_Class_6880_Betton_Grange",
        "/wiki/GWR_6959_Class_6960_Raveningham_Hall",
        "/wiki/GWR_6959_Class_6984_Owsden_Hall",
        "/wiki/GWR_6959_Class_6989_Wightwick_Hall",
        "/wiki/GWR_6959_Class_6990_Witherslack_Hall",
        "/wiki/GWR_6959_Class_6998_Burton_Agnes_Hall",
        "/wiki/GWR_6959_Class_7903_Foremarke_Hall",
        "/wiki/GWR_6959_Class_7927_Willington_Hall",
        "/wiki/GWR_7800_Class_7802_Bradley_Manor",
        "/wiki/GWR_7800_Class_7808_Cookham_Manor",
        "/wiki/GWR_7800_Class_7812_Erlestoke_Manor",
        "/wiki/GWR_7800_Class_7819_Hinton_Manor",
        "/wiki/GWR_7800_Class_7820_Dinmore_Manor",
        "/wiki/GWR_7800_Class_7821_Ditcheat_Manor",
        "/wiki/GWR_7800_Class_7822_Foxcote_Manor",
        "/wiki/GWR_7800_Class_7827_Lydham_Manor",
        "/wiki/GWR_7800_Class_7828_Odney_Manor",
        "/wiki/LMS_Coronation_Class_6220_Coronation",
        "/wiki/LMS_Coronation_Class_6235_City_of_Birmingham",
        "/wiki/LMS_Jubilee_Class_5552_Silver_Jubilee",
        "/wiki/LMS_Jubilee_Class_5593_Kolhapur",
        "/wiki/LMS_Jubilee_Class_5596_Bahamas",
        "/wiki/LMS_Jubilee_Class_5690_Leander",
        "/wiki/LMS_Jubilee_Class_5699_Galatea",
        "/wiki/LMS_Jubilee_Class_5731_Perseverance",
        "/wiki/LMS_Princess_Coronation_Class_6229_Duchess_of_Hamilton",
        "/wiki/LMS_Princess_Coronation_Class_6233_Duchess_of_Sutherland",
        "/wiki/LMS_Princess_Coronation_Class_6256_Sir_William_A._Stanier_F.R.S.",
        "/wiki/LMS_Princess_Royal_Class_6201_Princess_Elizabeth",
        "/wiki/LMS_Princess_Royal_Class_6203_Princess_Margaret_Rose",
        "/wiki/LMS_Royal_Scot_Class_6100_Royal_Scot",
        "/wiki/LMS_Royal_Scot_Class_6115_Scots_Guardsman",
        "/wiki/LMS_Royal_Scot_Class_6170_British_Legion",
        "/wiki/LMS_Stanier_Class_5_4-6-0_4767",
        "/wiki/LMS_Stanier_Class_5_4-6-0_4806",
        "/wiki/LMS_Stanier_Class_5_4-6-0_4871",
        "/wiki/LMS_Stanier_Class_5_4-6-0_4932",
        "/wiki/LMS_Stanier_Class_5_4-6-0_5000",
        "/wiki/LMS_Stanier_Class_5_4-6-0_5110",
        "/wiki/LMS_Stanier_Class_5_4-6-0_5212",
        "/wiki/LMS_Stanier_Class_5_4-6-0_5231",
        "/wiki/LMS_Stanier_Class_5_4-6-0_5305",
        "/wiki/LMS_Stanier_Class_5_4-6-0_44686/7",
        "/wiki/LMS_Stanier_Class_8F_8151",
        "/wiki/LMS_Stanier_Class_8F_8233",
        "/wiki/LNER_B17_Class_61673_Spirit_of_Sandringham",
        "/wiki/LNER_Class_A4_2509_Silver_Link",
        "/wiki/LNER_Class_A4_4464_Bittern",
        "/wiki/LNER_Class_A4_4468_Mallard",
        "/wiki/LNER_Class_A4_4469_Sir_Ralph_Wedgwood",
        "/wiki/LNER_Class_A4_4483_Kingfisher",
        "/wiki/LNER_Class_A4_4488_Union_of_South_Africa",
        "/wiki/LNER_Class_A4_4489_Dominion_of_Canada",
        "/wiki/LNER_Class_A4_4496_Dwight_D_Eisenhower",
        "/wiki/LNER_Class_A4_4498_Sir_Nigel_Gresley",
        "/wiki/LNER_Class_A4_4902_Seagull",
        "/wiki/LNER_Class_A4_60034_Lord_Faringdon",
        "/wiki/LNER_P2_Class_2007_Prince_of_Wales",
        "/wiki/LNWR_George_the_Fifth_class_2013_Prince_George",
        "/wiki/LSWR_O2_Class_W24_Calbourne",
        "/wiki/SR_Lord_Nelson_Class_850_Lord_Nelson",
        "/wiki/SR_Merchant_Navy_Class_35006_Peninsular_%26_Oriental_S._N._Co.",
        "/wiki/SR_Merchant_Navy_Class_35009_Shaw_Savill",
        "/wiki/SR_Merchant_Navy_Class_35018_British_India_Line",
        "/wiki/SR_Merchant_Navy_Class_35022_Holland_America_Line",
        "/wiki/SR_Merchant_Navy_Class_35027_Port_Line",
        "/wiki/SR_Merchant_Navy_Class_35028_Clan_Line",
        "/wiki/SR_West_Country_class_21C127_Taw_Valley",
        "/wiki/Caledonian_Railway",
        "/wiki/Highland_Railway",
        "/wiki/LNER_Pacifics",
        "/wiki/Great_Central_Railway",
        "/wiki/Great_Northern_Railway_(Great_Britain)",
        "/wiki/Great_Britain",
        "/wiki/Southern_Railway_(UK)",
        "/wiki/London_and_South_Western_Railway",
        "/wiki/Great_Western_Railway",
        "/wiki/GWR_absorbed_locos_1922_on",
        "/wiki/Standard_Goods",
        "/wiki/Rhymney_Railway",
        "/wiki/Taff_Vale_Railway",
        "/wiki/Lynton_and_Barnstaple_Railway",
        ]

        # Pages referred to on the categories pages, identified by strings, that are not to a class
        string_exclusions = [
        ":",
        "List_of",
        "Biographical",
        "Locomotive",
        "locomotive",
        "/wiki/Standard_gauge",
        "/wiki/Steam_locomotive",
        "/wiki/Case_sensitivity",
        "/wiki/London,_Midland_and_Scottish_Railway",
        "/wiki/2-2-4-0T",
        "/wiki/2_ft_and_600_mm_gauge_railways",
        "/wiki/Great_Western_Railway_Power_and_Weight_Classification",
        "Main_Page",

        ]

        unique_hrefs = []

        for url in Categories:

            try:    
                res = requests.get(url, headers=REQUEST_HEADERS)
                res.raise_for_status()
            except requests.exceptions.ConnectionError as err:
                # eg, no internet
                raise SystemExit(err)
            except requests.exceptions.HTTPError as err:
                # eg, url, server and other errors
                raise SystemExit(err)

            soup = BeautifulSoup(res.text, 'html.parser') 

            for link in soup.find_all(title=True):
                href = str(link.get('href'))
                if not any(x in href for x in string_exclusions) and \
                        href not in class_exclusions and \
                        '/wiki' in href:

                        try:
                            c = LocoClassList.objects.get(wikislug=href)
                        except ObjectDoesNotExist:
                            csvrow1 = []
                            csvrow1.append(url)
                            csvrow1.append(href)
                            csvrow1.append(link.get('title'))
                            output1.writerow(csvrow1)

                            if href in unique_hrefs:
                                continue
                            else:
                                unique_hrefs.append(href)
                                csvrow2 = []
                                csvrow2.append(href)
                                csvrow2.append(link.get('title'))
                                output2.writerow(csvrow2)
                        except Exception as e:
                            print(href, e)
                        else:
                            print(href, ' class is already in the database')
                    
                else:
                    print(href, " not loaded as in the exclusion criteria")

        csvFile1.close()
        csvFile2.close()