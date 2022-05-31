import requests, csv, os, time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from csv import DictReader

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

input_file = os.path.join(DATAIO_DIR, 'Class_All_W1_ClassNames_DeduplicatedB.csv')

output_file = os.path.join(DATAIO_DIR, 'Class_All_W2_Detail.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

rowcount = 0
for row in DictReader(open(input_file)):
    time.sleep(2)
    rowcount += 1
    # if rowcount == 5:
    #     break
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
    
    entrycount = 0
    csvRow = []
    csvRow.append(wikislug)
    csvRow.append(entrycount)
    csvRow.append(soup.find('h1').get_text())
    output.writerow(csvRow)

    for table in soup.find_all('table', class_="infobox"):
        for entry in table.find_all(['tr']):
            csvRow = []
            entrycount += 1
            csvRow.append(wikislug)
            csvRow.append(entrycount)
            cellcount = 0
            for cell in entry.find_all(['td','th']):
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