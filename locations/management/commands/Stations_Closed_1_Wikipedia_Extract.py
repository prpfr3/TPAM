"""
Extracts Railway Location references from Wikipedia based on pre-specified Wikipedia categories
"""


import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = 'url'

output_file = os.path.join(DATAIO_DIR, "Location_Extract_Wikipedia_Closed_Stations.csv")
with open(output_file, 'wt+', newline='', encoding='utf-8') as csvFile:
    output = csv.writer(csvFile)
    csv_output_row = ['Name', 'Wiki', 'Geometry', 'Company', 'Company_Wiki', 'Closed', 'Ref_Wiki']
    output.writerow(csv_output_row)

    log_file = os.path.join(DATAIO_DIR, "Location_Extract_Wikipedia_Closed_Stations.logfile")
    csvLogfile = open(log_file, 'wt+', newline='', encoding='utf-8')
    outputLogfile= csv.writer(csvLogfile)

    alphabet = ['A', 'B', 'C', 'D-F', 'G', 'H-J', 'K-L', 'M-O', 'P-R', 'S', 'T-V', 'W-Z']
    alphabet = ['T-V', 'W-Z']

    stations_added = 0

    for letter in alphabet:

        if URL_OR_FILE == 'file':
            url = os.path.join(DATAIO_DIR, "List_of_closed_railway_stations_in_Britain:_") + letter.lower() +".html"
            soup = BeautifulSoup(open(url), 'html.parser')
        else:
            url = f"https://en.wikipedia.org/wiki/List_of_closed_railway_stations_in_Britain:_{letter}"

            try:
                res = requests.get(url)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')
                print(f'Retrieved page {letter}')
            except requests.exceptions.ConnectionError as err:
                # eg, no internet
                raise SystemExit(err) from err
            except requests.exceptions.HTTPError as err:
                # eg, url, server and other errors
                raise SystemExit(err) from err   

        tables = soup.find_all('table', {'class':'wikitable'})

        for table in tables:
            trs = table.find_all('tr')

            for tr in trs:
                csv_output_row= []
                csv_logfile_row = []

                for td_id, td in enumerate(tr.find_all(['td']), start=1):

                    without_line_breaks = td.get_text().replace("\n", "")
                    csv_output_row.append(without_line_breaks)
                    a = td.find("a", href=True)
                    if a:
                        csv_output_row.append(a['href'])
                    else:
                        csv_output_row.append("")

                    if td_id == 1 and a: # Very occasionally there is no "a" in the first cell
                        geometry = ""
                        try:
                            url_station = "https://en.wikipedia.org" + a['href']
                            res = requests.get(url_station)
                            res.raise_for_status()
                            soup = BeautifulSoup(res.text, 'html.parser')
                            if coords_html := soup.find_all('span', {'class': 'geo'}):
                                coords_split = coords_html[0].text.split(';')
                                geometry = f'POINT({coords_split[1].strip()} {coords_split[0].strip()})'
                            else:
                                csv_logfile_row.append('No coordinates in Wikipedia (span class="geo") for ' + a['href'])
                                outputLogfile.writerow(csv_logfile_row)                            
                        except requests.exceptions.ConnectionError as err:
                            # eg, no internet
                            raise SystemExit(err) from err
                        except IndexError:
                            csv_output_row.append("")
                            csv_logfile_row.append('No url on the page for:-' + a['href'])
                            outputLogfile.writerow(csv_logfile_row)
                        except requests.exceptions.HTTPError as err:
                            # eg, url, server and other errors
                            csv_output_row.append("")
                            csv_logfile_row.append('http error suggesting no Wikipedia page for:- ' + a['href'])
                            outputLogfile.writerow(csv_logfile_row)
                        csv_output_row.append(geometry)
                        
                if csv_output_row:
                    output.writerow(csv_output_row)
                    stations_added += 1

csv_logfile_row.append(f'{stations_added=}')