import requests, csv, os, time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from csv import DictReader

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

input_file = os.path.join(DATAIO_DIR, 'Class_Modern_W1B_Unique_Names.csv')

output_file = os.path.join(DATAIO_DIR, 'Class_Modern_W2_Scrape_Detail.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

for row in DictReader(open(input_file)):
    time.sleep(2)
    wikislug=row['wikislug']
    url = "https://en.wikipedia.org" + wikislug
    print(url)
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

    for table in soup.find_all('table', class_="infobox"):
        rowcount = 0
        for row in table.find_all(['tr']):
            csvRow = []
            rowcount += 1
            csvRow.append(wikislug)
            csvRow.append(rowcount)
            cellcount = 0
            for cell in row.find_all(['td','th']):
                cellcount += 1
                csvRow.append(cell.get_text())
                if cell.find('a', class_="image"):
                        csvRow.append(cell.find('a', class_="image").get('href'))            
                if cellcount != 1:
                    for link in cell.find_all('a'):
                        csvRow.append(link.get('href'))
            print(csvRow)
            output.writerow(csvRow)

csvFile.close()