#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

#res = requests.get("https://en.wikipedia.org/wiki/List_of_British_heritage_and_private_railways")
res = open(os.path.join('D:\Data\TPAM', 'Heritage Railway List utf8.htm'))
output_file = os.path.join("D:\\Data", "TPAM", "ETL_Wiki_List_of_British_heritage_and_private_railways.csv")

#try:
#    res.raise_for_status()
#    print(res)
#except Exception as exc:
#    print('Unable to get the file: %s' % (exc))

soup = BeautifulSoup(res, 'html.parser', from_encoding="utf-8") 
#csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
data = soup.find_all('a')

try:
  output.writerow(['location', 'url'])
  include_in_output = False
  for li in data:
    print('li', li)
    #a = li.find('a')
    #print('a', a)
    csvrow = []
    csvrow.append(li.get_text())
    url = li.get('href')
    if "/wiki/" in url:
      slug = url.replace('https://en.wikipedia.org/wiki/', '')
    else:
      print('invalid url in row: ', li)
      slug = ''
    csvrow.append(slug)
    output.writerow(csvrow) 
finally:
    csvFile.close()