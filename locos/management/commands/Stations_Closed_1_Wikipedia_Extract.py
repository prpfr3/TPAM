"""
Extracts Railway Location references from Wikipedia based on pre-specified Wikipedia categories
"""

import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = 'url'

output_file = os.path.join(DATAIO_DIR, "Locations_Extract_Wikipedia_Closed_Stations.csv")
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
csvRow = ['Name', 'Wiki', 'Company', 'Company_Wiki', 'Closed', 'Ref_Wiki']
output.writerow(csvRow)

alphabet = ['A', 'B', 'C', 'D-F', 'G', 'H-J', 'K-L', 'M-O', 'P-R', 'S', 'T-V', 'W-Z']
# alphabet = ['G', 'H-J'] #For Testing Only

for letter in alphabet:

    if URL_OR_FILE == 'file':
        url = os.path.join(DATAIO_DIR, "List_of_closed_railway_stations_in_Britain:_") + letter.lower() +".html"
        soup = BeautifulSoup(open(url), 'html.parser')
    else:
        url = "https://en.wikipedia.org/wiki/List_of_closed_railway_stations_in_Britain:_" + letter
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser') 
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err)   

    tables = soup.find_all('table', {'class':'wikitable'})

    for table in tables:
        trs = table.find_all('tr')

        for tr in trs:
            csvRow= []

            for td in tr.find_all(['td']):
                if td.get_text() == " ":
                    # This condition trys to deals with a misformat on the Llanstephan entry of 
                    # https://en.wikipedia.org/wiki/List_of_closed_railway_stations_in_Britain:_K-L
                    # though does not work. Manual workaround of a post extract edit used.
                    pass
                else:
                    without_line_breaks = td.get_text().replace("\n", "")
                    csvRow.append(without_line_breaks)
                    a = td.find("a", href=True)
                    if a:
                        csvRow.append(a['href'])
                    else:
                        csvRow.append("")

            if csvRow:
                output.writerow(csvRow)

csvFile.close()