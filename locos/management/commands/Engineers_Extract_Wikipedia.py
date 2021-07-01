#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

res = requests.get("https://en.wikipedia.org/wiki/Category:English_railway_mechanical_engineers")
#res = open(os.path.join("D:\\MLDatasets", "TPAM_DATAIO", "English_railway_mechanical_engineers.html"))
output_file = os.path.join("D:\\MLDatasets", "TPAM_DATAIO", "ETL_Wiki_English_railway_mechanical_engineers")

try:
    res.raise_for_status()
    print(res)
except Exception as exc:
    print('Unable to get the file: %s' % (exc))

soup = BeautifulSoup(res.text, 'html.parser') 
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

try:
  for link in soup.find_all(title=True):
    csvrow = []
    csvrow.append(link.get('href'))
    #csvrow.append(link.get('title'))
    csvrow.append(link.get_text())
    print(csvrow)
    output.writerow(csvrow)
finally:
    csvFile.close()