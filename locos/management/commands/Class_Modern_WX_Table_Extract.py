# Extracts and Saves Modern UK Traction Classes from Wikipedia to csv using Beautiful Soup
# Working correctly at 27/03/21

import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://en.wikipedia.org/wiki/List_of_British_Rail_modern_traction_locomotive_classes"

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

try:
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser') 
    filename = os.path.join(DATAIO_DIR,"List_of_British_Rail_modern_traction_locomotive_classes.csv")
    tables = soup.find_all('table', {'class':'wikitable'})
    tablecount = 0
    csvFile = open(filename, 'wt+', newline='', encoding='utf-8')

    for table in tables:
      tablecount = tablecount + 1
      rows = table.find_all('tr')

      output = csv.writer(csvFile, delimiter=':', quoting=csv.QUOTE_MINIMAL)
      rowcount = 0
      for row in rows:
          csvRow = []
          rowcount = rowcount + 1
          if rowcount in [1, 2] and tablecount > 1:
            pass
          else:
            cellcount = 0
            for cell in row.find_all(['td','th']):
              cellcount = cellcount + 1
              if cellcount == 12: #Ignore the last cell with the newline indicator
                pass
              else:
                csvRow.append(cell.get_text())
              if cellcount in [1]: #List columns that have urls we wish to capture'
                try:
                  csvRow.append(cell.find('a').attrs['href'])
                except:
                  csvRow.append('N/A')
              try:
                 colspan = cell.attrs['colspan']
                 print(colspan)
                 cellcount == cellcount + colspan - 1
              except:
                 pass
            #if rowcount == 1:
            #  csvRow.append('designer')
            #  csvRow.append('company')
            #  csvRow.append('grouping_company')
            #elif rowcount > 2 and rowcount < 29:
            #  csvRow.append('63')
            #elif rowcount > 29 and rowcount < 72:
            #  csvRow.append('59')
            #elif rowcount > 72 and rowcount < 78:
            #  csvRow.append('33')
            #elif rowcount > 78:
            #  csvRow.append('39')
            #if rowcount > 2:
            #  csvRow.append('MR')
            #  csvRow.append('LMS')
            print(csvRow)
            output.writerow(csvRow)
finally:
    csvFile.close()