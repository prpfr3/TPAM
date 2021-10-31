#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

output_file = os.path.join("D:\\MLDatasets", "TPAM_DATAIO", "ETL_Wiki_Persons.csv")
Categories = ["Locomotive_builders_and_designers", 
                "English_railway_mechanical_persons",
                "Scottish_railway_mechanical_persons",
                "British_railway_civil_persons",
                "British_railway_pioneers"]

csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')

for Category in Categories:
    url = "https://en.wikipedia.org/wiki/Category:" + Category
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser') 

    output = csv.writer(csvFile)

    try:
        for link in soup.find_all(title=True):
            href = str(link.get('href'))
            if '/wiki' in href and \
                ':' not in href and \
                'List_of' not in href and \
                'Biographical' not in href and \
                'Main_Page' not in href:
                csvrow = []
                csvrow.append(Category)
                csvrow.append(href)
                csvrow.append(link.get('title'))
                output.writerow(csvrow)
    finally:
        pass

csvFile.close()