"""
 Extracts British Locomotive Manufacturer data from Wikipedia
"""
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://en.wikipedia.org/wiki/Category:Locomotive_manufacturer_of_the_United_Kingdom"
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
output_file = os.path.join(DATAIO_DIR, 'Manufacturer_Extract_Wikipedia.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

#https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testin
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
    if '/wiki' in href and \
        ':' not in href and \
        'List_of' not in href and \
        'United_Kingdom' not in href and \
        'Main_Page' not in href:
        csvrow = []
        csvrow.append(href)
        csvrow.append(link.get('title'))
        output.writerow(csvrow)

csvFile.close()