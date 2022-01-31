"""
Traverses a set of pre-defined category pages and finds/stores all the url references on those pages 
which are likely Locomotive Classes along with the category name
"""
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

output_file1 = os.path.join(DATAIO_DIR, "Class_Modern_W1A_Scrape_Names.csv")
csvFile1 = open(output_file1, 'wt+', newline='', encoding='utf-8')
output1 = csv.writer(csvFile1)

csvrow1 = []
csvrow1.append("category")
csvrow1.append("wikislug")
csvrow1.append("name")
output1.writerow(csvrow1)

output_file2 = os.path.join(DATAIO_DIR, "Class_Modern_W1B_Unique_Names.csv")
csvFile2 = open(output_file2, 'wt+', newline='', encoding='utf-8')
output2 = csv.writer(csvFile2)

csvrow2 = []
csvrow2.append("wikislug")
csvrow2.append("name")
output2.writerow(csvrow2)

Categories = ["https://en.wikipedia.org/wiki/Category:Standard_gauge_locomotives_of_Great_Britain", 
                ]

class_exclusions = [
"/wiki/BR_Standard_Class_4_2-6-0_76084",
]

string_exclusions = [
    ":",
    "List_of",
    "Biographical",
    "Locomotive",
    "locomotive",
    "Main_Page",
    ]

string_inclusions = ["British", "Eurotunnel", "LMS", "GWR", "LNER", ]

unique_hrefs = []

for url in Categories:

    try:
        res = requests.get(url)
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
                any(x in href for x in string_inclusions) and \
                href not in class_exclusions and \
                '/wiki' in href:
            
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
        else:
            print(href, " was excluded")

csvFile1.close()
csvFile2.close()