# Extracts and Saves Midland Locomotive Classes from Wikipedia to csv using Pandas and then loads into MySQL
# Working correctly at 24/01/21

import requests, csv, os
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Locomotives_of_the_Midland_Railway"

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
    
try:
    res = requests.get(url)
    res.raise_for_status()
except requests.exceptions.ConnectionError as err:
    # eg, no internet
    raise SystemExit(err)
except requests.exceptions.HTTPError as err:
    # eg, url, server and other errors
    raise SystemExit(err)

filename = os.path.join(DATAIO_DIR,"LocoClass_Wikitable_Midland_Scrape.csv")
csvFile = open(filename, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

filename = os.path.join(DATAIO_DIR,"LocoClass_Wikitable_Midland_Builder_Mapping.csv")
csvFile2 = open(filename, 'wt+', newline='', encoding='utf-8')
output2 = csv.writer(csvFile2)


soup = BeautifulSoup(res.text, 'html.parser') 
table = soup.find_all('table', {'class':'wikitable'}) [0]
rows = table.find_all('tr')
rowcount = 0

for row in rows:
    rowcount = rowcount + 1
    if rowcount in [2, 29, 72 ,78]:
      pass
    else:
      if rowcount == 1:
        csvRow = ['grouping_company', 'company', 'designer_slug', 'class_slug', 'class', 'wheel_slug', 'wheels', 'pre1907_numbers', 'post1907_numbers', 'builder_nos', 'built', 'number_built', 'withdrawn', 'notes']
        csvRow2 = ['grouping_company', 'company', 'designer_slug', 'class_slug', 'class', 'wheel_slug', 'wheels', 'pre1907_numbers', 'post1907_numbers', 'builder_slug']
        output2.writerow(csvRow2)
      else:
        csvRow = ['LMS', 'MR']
        csvRow2 = ['LMS', 'MR']

      if rowcount > 2 and rowcount < 29:
        csvRow.append('/wiki/Matthew_Kirtley')
      elif rowcount > 29 and rowcount < 72:
        csvRow.append('/wiki/Samuel_Waite_Johnson')
      elif rowcount > 72 and rowcount < 78:
        csvRow.append('/wiki/Richard_Deeley')
      elif rowcount > 78:
        csvRow.append('/wiki/Henry_Fowler_(engineer)')

      if rowcount != 1:
        csvRow2 = csvRow.copy()

        cellcount = 0
        for cell in row.find_all(['td','th']):

          cellcount = cellcount + 1

          if cellcount in [1, 2]:
              a = cell.find("a", href=True)
              if a and 'wiki' in a['href']:
                csvRow.append(a['href'])
              else:
                csvRow.append("")

          if cellcount in [5]:
              for a in cell.find_all("a", href=True):
                csvRow2 = csvRow.copy()
                csvRow2.append(a['href'])
                output2.writerow(csvRow2)


          if cellcount == 10: #Ignore the last cell with the newline indicator
            pass
          elif cellcount == 1:
            cell_cleansed = cell.get_text().replace(' class', '')
            cell_cleansed = cell_cleansed.replace('Class ', '')
            csvRow.append(cell_cleansed)            
          else:
            csvRow.append(cell.get_text())

      output.writerow(csvRow)

csvFile.close()
csvFile2.close()