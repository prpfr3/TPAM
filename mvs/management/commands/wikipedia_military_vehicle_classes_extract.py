"""
To extract and save a Wikipedia or other HTML Table

Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160). Load the csv file as UTF-8 in Excel from the Data Menu Tab / From Text/CSV

Be aware the csv may contain manual added lines which can b e lost when this program overwites the file. Take a backup first.
"""

import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

res = requests.get("https://en.wikipedia.org/wiki/List_of_military_vehicles")
output_file = os.path.join("D:\\MLDatasets", "TPAM_DATAIO", "ETL_Wiki_List_of_military_vehicles.csv")

try:
    res.raise_for_status()
    print(res)
except Exception as exc:
    print('Unable to get the file: %s' % (exc))

soup = BeautifulSoup(res.text, 'html.parser') 
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
data = soup.find_all('div', {'class':'mw-parser-output'})

try:
  output.writerow(['Description', 'Name', 'Slug', 'Ref1', 'RefSlug1', 'Ref2', 'RefSlug2', 'Ref3', 'RefSlug3', 'Ref4', 'RefSlug4', 'Ref5', 'RefSlug5'])
  process_output = False
  for li in data[0].find_all('li'):
    li_string = str(li)
    if li_string.startswith('<li>1V152'):#Other rows ignored until we reach this first real content row
      process_output = True
    if process_output == True:
      csvrow = []
      csvrow.append(li.get_text())
      for a in li.find_all('a'):
        csvrow.append(a.get('title'))
        url = a.get('href')
        if "/wiki/" in url:
          slug = url.replace('/wiki/', '')
        else:
          print('invalid url in row: ', li)
          slug = ''
        csvrow.append(slug)
      output.writerow(csvrow)
    if li_string.startswith('<li>YW750'):#Marks the end of the content
      process_output = False
finally:
    csvFile.close()