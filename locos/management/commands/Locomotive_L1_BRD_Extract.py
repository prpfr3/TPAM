"""
Uses the Locomotive Built Search Facility of BRD @ https://www.brdatabase.info/build.php
Works on saved pages, for pre and post 01/01/1946 (date of nationalisation)
"""
import requests, csv, os
from bs4 import BeautifulSoup

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_files = ["Locomotive_BRD_Post_Nat.html", "Locomotive_BRD_Pre_Nat.html"]
output_filename = os.path.join(DATAIO_DIR,"Locomotive_BRD.csv")
csvFile = open(output_filename, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

rowcount = 0

for input_file in input_files:
    res = open(os.path.join(DATAIO_DIR, input_file))

    tables = BeautifulSoup(res, 'html.parser').find_all('table', {'class':'sortable'})

    # Only retrieve the first table of a page which has the individual locomotives. The second table is a summary table
    rows = tables[0].find_all('tr')
    newtable = True

    for row in rows:
        rowcount = rowcount + 1

        csvRow = []

        # If a newtable but not the first table which supplies the output file headers then skip the row
        if newtable and rowcount > 1:
          newtable = False
        else:
          for cell in row.find_all(['td','th']):
            
            text = cell.get_text()
            csvRow.append(text)

            if newtable and rowcount == 1:
              # This will be the header row ('th')
              # Create a column header to hold the attribute (url) for the text
              csvRow.append(text + '_a')

            else: 
              a = cell.find("a", href=True)
              if a:
                # Split the BRD url at ? and keep only the query specifics
                href_splits = a['href'].split('?', 1)
                csvRow.append(href_splits[1])
              else:
                csvRow.append("")

          newtable = False
          output.writerow(csvRow)

csvFile.close()
print('Closing output file', f'{rowcount}' ,'records loaded')