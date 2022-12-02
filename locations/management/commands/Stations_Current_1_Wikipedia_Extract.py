"""
Extracts Railway Location references from Wikipedia based on pre-specified Wikipedia categories

"""
import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = 'url'

output_file = os.path.join(DATAIO_DIR, "Location_Extract_Wikipedia_Stations.csv")
with open(output_file, 'wt+', newline='', encoding='utf-8') as csvFile:
    output = csv.writer(csvFile)
    csvRow = ['Name', 'NameSlug', 'Postcode', 'BingURL', 'Code1', 'NatRailURL1', 'Code2', 'NatRailURL2']
    output.writerow(csvRow)

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y']

    for letter in alphabet:

        if URL_OR_FILE == 'file':
            url = os.path.join(DATAIO_DIR, "Wikipedia_Stations_") + letter.lower() +".html"
            soup = BeautifulSoup(open(url), 'html.parser')
        else:
            url = f"https://en.wikipedia.org/wiki/UK_railway_stations_-_{letter}"
            try:
                print('Trying ', url)
                res = requests.get(url).content.decode('utf-8', 'ignore')
            except requests.exceptions.ConnectionError as err:
                # eg, no internet
                raise SystemExit(err) from err
            except requests.exceptions.HTTPError as err:
                # eg, url, server and other errors
                raise SystemExit(err) from err

            soup = BeautifulSoup(res, 'html.parser') 

        table = soup.find_all('table', {'class':'wikitable'})[0]
        rows = table.find_all('tr')

        for row in rows:
            csvRow= []

            for cell in row.find_all(['td']):
                csvRow.append(cell.get_text())
                if a := cell.find("a", href=True):
                    csvRow.append(a['href'])
                else:
                    csvRow.append("")

            if csvRow:
                output.writerow(csvRow)