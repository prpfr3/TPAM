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
csvRow = ['Name', 'Wiki', 'Geometry', 'Company', 'Company_Wiki', 'Closed', 'Ref_Wiki']
output.writerow(csvRow)

log_file = os.path.join(DATAIO_DIR, "Locations_Extract_Wikipedia_Closed_Stations.logfile")
csvFile2 = open(log_file, 'wt+', newline='', encoding='utf-8')
output2= csv.writer(csvFile2)

alphabet = ['A', 'B', 'C', 'D-F', 'G', 'H-J', 'K-L', 'M-O', 'P-R', 'S', 'T-V', 'W-Z']
# alphabet = ['K-L'] #For Testing Only

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
            csvRow2 = []

            td_id = 0
            for td in tr.find_all(['td']):
                td_id += 1
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

                    # 25/05/22 New Code to lookup and add geometry
                    if td_id == 1:
                        url_station = "https://en.wikipedia.org" + a['href']
                        try:
                            res = requests.get(url_station)
                            res.raise_for_status()
                            soup = BeautifulSoup(res.text, 'html.parser')
                            coords_html = soup.find_all('span', {'class':'geo'})
                            geometry = ""
                            if coords_html:
                                coords_split = coords_html[0].text.split(';')
                                geometry = 'POINT(' + coords_split[1].strip() + ' ' + coords_split[0].strip() + ')'
                            else:
                                print('No coordinates in Wikipedia (span class="geo") for ', a['href'])
                                csvRow2.append('No coordinates in Wikipedia (span class="geo") for ' + a['href'])
                                output2.writerow(csvRow2)                             
                            csvRow.append(geometry)
                        except requests.exceptions.ConnectionError as err:
                            # eg, no internet
                            raise SystemExit(err)
                        except requests.exceptions.HTTPError as err:
                            # eg, url, server and other errors
                            print('http error for:- ', a['href'])
                            csvRow2.append('http error suggesting no Wikipedia page for:- ' + a['href'])
                            csvRow.append("")
                            output2.writerow(csvRow2)   
                            pass

            if csvRow:
                output.writerow(csvRow)

csvFile.close()