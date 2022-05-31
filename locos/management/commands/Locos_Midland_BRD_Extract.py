""""""

import requests, csv, os
from bs4 import BeautifulSoup

url_or_file = "file"
input_file = "BRD Midland Locomotives.html"
url = "https://www.brdatabase.info/companies.php?page=LMS&prg=MR"
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

if url_or_file == "url":

    try:
        res = requests.get(url).text
        res.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)

else:
    res = open(os.path.join(DATAIO_DIR, input_file))

filename = os.path.join(DATAIO_DIR,"BRD Midland Locomotives.csv")
csvFile = open(filename, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

tables = BeautifulSoup(res, 'html.parser').find_all('table', {'class':'sortable'})

for table in tables:
    rows = table.find_all('tr')

    rowcount = 0

    for row in rows:
        rowcount = rowcount + 1

        if rowcount == 1:
          csvRow = ['grouping', 'pre_grouping', 'build_date', 'class_url', 'mr_class', 'lms_class', 'loco_url', 'first_mr_number', 'wheels', 'designer_url', 'designer', 'manufacturer_url', 'manufacturer', 'order_number', 'works_url', 'works_number', 'withdrawn',]
        else:
          csvRow = ['LMS', 'MR']

          cellcount = 0
          for cell in row.find_all(['td','th']):

            cellcount = cellcount + 1

            if cellcount in [2, 4, 6, 7, 9]:
                a = cell.find("a", href=True)
                if a:
                  csvRow.append(a['href'])
                else:
                  csvRow.append("")

            if cellcount == 11: #Ignore the last cell with the newline indicator
              pass
            else:
              csvRow.append(cell.get_text())

        output.writerow(csvRow)

csvFile.close()
print('CLosing output file', f'{rowcount}' ,'records loaded')