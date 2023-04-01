import requests, csv, os, time
from bs4 import BeautifulSoup
from csv import DictReader

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
unique_urls = []

input_file = os.path.join(DATAIO_DIR, 'People_Load.csv')

output_file = os.path.join(DATAIO_DIR, 'People_Detail_Extract_Wikipedia.csv')
with open(output_file, 'wt+', newline='', encoding='utf-8') as csvFile:
    output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    slugcount = 0
    for row in DictReader(open(input_file)):
        wikislug=row['wikitextslug']
        url = f"https://en.wikipedia.org{wikislug}"
        if url in unique_urls:
            continue
        unique_urls.append(url)
        slugcount = slugcount + 1
        time.sleep(2)

        print(url)
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err) from err
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err)

        soup = BeautifulSoup(res.text, 'html.parser')

        for table in soup.find_all('table', class_="infobox"):
            rowcount = 0
            for row in table.find_all(['tr']):
                rowcount += 1
                if rowcount > 10:
                    break
                csvRow = [wikislug, rowcount]
                for cellcount, cell in enumerate(row.find_all(['td','th']), start=1):
                    csvRow.append(cell.get_text())
                    if cell.find('a', class_="image"):
                            csvRow.append(cell.find('a', class_="image").get('href'))
                    if cellcount != 1:
                        csvRow.extend(link.get('href') for link in cell.find_all('a'))
                output.writerow(csvRow)

                for cell in row.find_all(['td','th']):

                    if cell.find('span', class_="bday"):
                        print('found a birthday')
                        rowcount += 1
                        csvRow = [
                            wikislug,
                            rowcount,
                            'bday',
                            cell.find('span', class_="bday").get_text(),
                        ]
                        output.writerow(csvRow)
                    if cell.find('div', class_="birthplace"):
                        rowcount += 1
                        csvRow = []
                        csvRow.extend(
                            (
                                wikislug,
                                rowcount,
                                'birthplace',
                                cell.find(
                                    'div', class_="birthplace"
                                ).get_text(),
                            )
                        )
                        output.writerow(csvRow)
                    if cell.find('span', style="display:none"):
                        print('found a deathday')
                        rowcount += 1
                        csvRow = []
                        csvRow.extend(
                            (
                                wikislug,
                                rowcount,
                                'died',
                                cell.find(
                                    'span', style="display:none"
                                ).get_text(),
                            )
                        )
                        output.writerow(csvRow)
                    if cell.find('div', class_="deathplace"):
                        rowcount += 1
                        csvRow = []
                        csvRow.extend((wikislug, rowcount, 'deathplace'))
                        output.writerow(csvRow)
                        csvRow.append(cell.find('div', class_="deathplace").get_text())