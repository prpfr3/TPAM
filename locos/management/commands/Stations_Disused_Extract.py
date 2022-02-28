"""
Extracts Railway Location references from Disused Stations website based on pre-specified Wikipedia categories
"""

import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = 'url'

output_file = os.path.join(DATAIO_DIR, "Locations_Extract_Disused_Stations.csv")
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y']
# alphabet = ['A']

for letter in alphabet:

    if URL_OR_FILE == 'file':
        url = os.path.join(DATAIO_DIR, "Disused_Stations_sites_") + letter.lower() +".html"
        soup = BeautifulSoup(open(url), 'html.parser')
    else:
        url = "http://disused-stations.org.uk//sites_" + letter.lower()

        try:
            print('Trying ', url)
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser') 
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err)   

    for row in soup.find_all('a'):
        # Some duplicate hrefs mistakenly on this site without names, so only get them if there is also a label
        # Ignore the lines at the bottom of the page with a url of just '/'
        if row['href'] and row.get_text() and row['href'] != '/':
            csvRow =[]
            csvRow.append(row.get_text())
            csvRow.append(row['href'])
            output.writerow(csvRow)

csvFile.close()