"""
Extracts the List of British Heritage and Private Railways from Wikipedia

Largely redundant as the original extract has been manually added to since loading into TPAM

May be of future use for a Delta comparison of the Wikipedia list and contents of the TPAM database to identify new records
"""
from encodings import utf_8
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = 'url'

output_file = os.path.join(DATAIO_DIR, "Heritage_Railways.csv")
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
csvRow = ['Name', 'Wiki', 'Company', 'Company_Wiki', 'Closed', 'Ref_Wiki']
output.writerow(csvRow)

if URL_OR_FILE == 'file':
    url = os.path.join(DATAIO_DIR, "List of British heritage and private railways - Wikipedia.html")
    soup = BeautifulSoup(open(url), 'html.parser')
else:
    url = "https://en.wikipedia.org/wiki/List_of_British_heritage_and_private_railways"
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

rows = soup.find_all('li')
print(type(rows))

for row in rows:
    csvRow= []

    a = row.find("a", href=True)
    if a and \
      '/wiki/' in a['href'] and \
      'Category' not in a['href']:
        csvRow.append(a['href'])
        csvRow.append(row.get_text())
        print(csvRow)
        output.writerow(csvRow)

csvFile.close()