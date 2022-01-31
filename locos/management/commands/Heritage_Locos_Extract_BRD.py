#To extract a list of preserved locos from BRD

import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

res = requests.get("https://www.brdatabase.info/preservation.php")
res = open(os.path.join("D:\\Data", "TPAM", "BRD Preserved_Locos.html")) # utf-8 parameter
output_file = os.path.join("D:\\Data", "TPAM", "BRD Preserved_Locos.csv")

try:
    res.raise_for_status()
    print(res)
except Exception as exc:
    print('Unable to get the file: %s' % (exc))

soup = BeautifulSoup(res, 'html.parser') 
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

tables = soup.find_all("table", attrs={"class": "sortable"})

table_data = tables[0].find_all("tr")  # contains 2 rows

t_headers = []
for th in table_data[0].find_all("th"):
    # remove any newlines and extra spaces from left and right
    t_headers.append(th.text.replace('\n', ' ').strip())

t_detail = []
for row in table_data.find_all("tr"):
    # remove any newlines and extra spaces from left and right
    print(row)
    t_detail.append(td.text.replace('\n', ' ').strip())

rows = soup.find_all("tr")
    
# Get all the rows of table
table_rows = []
for tr in table.tbody.find_all("tr"): # find all tr's from table's tbody
    t_row = {}
    # find all td's in tr and zip it with t_header
    for td in tr.find_all("td"): 
        t_row[td] = td.text.replace('\n', '').strip()
    table_rows.append(t_row)

# Put the data for the table with its heading.
data[heading] = table_rows

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

    
rows = soup.find_all(True, {'class':[ 'gr-price__amount', 'gr-price__fractional', 'product-item-anchor no-underline']})
  except:
    print('error in getting the webpage')
    return False
  finally:
    driver.quit()
    
  #with open('C:/Users/paulf/Desktop/Donated _ Oxfam Online Shop.html', 'r') as f:
  #  page = f.read() 

  csvRow = []
  pricefieldcount = 0
  if itemnum == 0:
    csvRow.append('Price')
    csvRow.append('Book')
    csvRow.append('URLlink')
    output.writerow(csvRow)
  csvRow = []

  try:
    for row in rows:
      if is_float(row.get_text()):
        pricefieldcount = pricefieldcount + 1
        if pricefieldcount == 1:
          price = float(row.get_text())
        if pricefieldcount == 2:
          price = price + float(row.get_text())
          csvRow.append(price)
          price = 0
      else:
        csvRow.append(row.get_text())
        if 'href' in row.attrs:
          webpage = 'https://onlineshop.oxfam.org.uk/' + row.attrs['href']
          csvRow.append(webpage)
        output.writerow(csvRow)
        pricefieldcount = 0
        csvRow = []
  except:
    print('error in processing the webpage')
    return False
  finally:
    return True


filename = 'OutputOxfamList.csv'
csvFile = open(filename, 'wt+', newline='')
output = csv.writer(csvFile)

itemnum = 0
OxfamListPage=getLinks(itemnum)

try:
  #while len(OxfamListPage) > 0:
  while getLinks:
  #while itemnum < 400:
      itemnum = itemnum + 54 
      print('itemnum', itemnum)
      OxfamListPage=getLinks(itemnum)
finally:
  csvFile.close() 