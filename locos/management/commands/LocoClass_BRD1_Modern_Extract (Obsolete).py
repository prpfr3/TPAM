"""
 Extracts and Saves Modern UK Traction Classes from BRDatabase @ https://www.brdatabase.info/ to csv using Beautiful Soup

 urls are in the format
 https://www.brdatabase.info/classes.php?type=S&subtype=GWR&prg=BaR

 Refactored and working correctly at 23/06/21. LOCOCLASS DATA HAS SUBSEQUENTLY BEEN CLEANSED MANUALLY AND THEREFORE THIS SHOULD NOT BE RERUN FOR TPAM
 
 BRD webpages use charset=iso-8859-1. ISO 8859-1 is a single-byte encoding that can represent the first 256 Unicode characters. UTF-8 is a multibyte encoding that can represent any Unicode character. Both encode ASCII exactly the same way.
 
 The csv file can be loaded into Excel by opening an empty file, going to the Data Tab on the menu and choosing 'From Text/CSV'. Choose comma as the delimiter and UTF-8 as the codeset on import.
"""

import requests, csv, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
urls on the BRD site are in the format
 https://www.brdatabase.info/classes.php?type=S&subtype=GWR&prg=BaR and therefore the quickest method of specifying which files, be it from the web or a saved html page from the web, is to use the following format to specify the pages (any html pages should use this same format as the filename). Note that all diesels and all electrics can be extracted using a subtype of All
"""

input_files = ['S&subtype=GWR&prg=BaR', 'S&subtype=GWR&prg=BaR', 'D&subtype=All', 'D&subtype=All', 'E&subtype=All']

# Specify the columns of the tables that contain urls or images
# For Type = E only
url_cols = [1, 2, 5, 7]
img_cols = [10]

# For Type = D only
url_cols = [1, 6, 8]
img_cols = [11]

# For Type = S only
url_cols = [1, 2, 4, 9]
img_cols = [13]

first_input_file = True
url_or_file = "url" #set to 'url' or 'file'
DATAIO_DIR = os.path.join("C:\\Users\\paulf\\Desktop")
output_file = os.path.join(DATAIO_DIR, 'BRD_Loco_Classes.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

for input_file in input_files:   

    if url_or_file == "url":
        url = "http://www.brdatabase.info/classes.php?type=" + input_file
        res = requests.get(url).text
    else:
        full_filename = input_file + '.html'
        res = open(os.path.join(DATAIO_DIR, full_filename))
    soup = BeautifulSoup(res, 'html.parser') 
    tables = soup.find_all('table', {'class':'sortable'})

    for table in tables:
        rows = table.find_all('tr')
        rowcount = 0
        for row in rows:
            csvRow = []
            rowcount = rowcount + 1

          #Ignore headers rows if more than one input file
            if rowcount == 1 and first_input_file == False:
              pass
            else:
              first_input_file = False

              #Add the text cells for a row into the list              
              cellcount = 0
              for cell in row.find_all(['td','th']):
                cellcount = cellcount + 1
                csvRow.append(cell.get_text())

              #Add any url attributes to retain cross-references to the original data
                if cellcount in url_cols: #urls to be captured
                  if rowcount == 1:
                    colhead = cell.get_text() + '_url'
                    csvRow.append(colhead)
                  else:
                    try:
                      csvRow.append(cell.find('a').attrs['href'])
                    except:
                      csvRow.append('')

              #Add any img attributes to retain cross-references to the original data  
                if cellcount in img_cols: #imgs to be captured
                  if rowcount == 1:
                    colhead = cell.get_text() + '_img'
                    csvRow.append(colhead)
                  else:
                    try:
                      csvRow.append(cell.find('img').attrs['src'])
                    except:
                      csvRow.append('')

              output.writerow(csvRow)

csvFile.close()