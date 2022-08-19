"""
Traverses a set of pre-defined category pages and finds/stores all the url references on those pages 
which are likely Railway Lines along with the category name

"""
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

output_file = os.path.join(DATAIO_DIR, "Routes_All_W1.csv")
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output1 = csv.writer(csvFile)


csvrow = ["category", "wikislug", "name", "routemap"]
output1.writerow(csvrow)

Categories = ["https://en.wikipedia.org/wiki/Category:Railway_lines_in_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_Northern_Ireland", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_the_East_Midlands", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_the_East_of_England",
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_London", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_London", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_London", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_Greater_Manchester", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_North_East_England", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_North_West_England", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_South_East_England", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_South_West_England", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_the_West_Midlands_(region)", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_Yorkshire_and_the_Humber", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_the_East_Midlands", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_the_East_of_England", 
    "https://en.wikipedia.org/wiki/Category:Standard_gauge_railways_in_England", 
    "https://en.wikipedia.org/wiki/Category:Industrial_railways_in_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_London", 
    "https://en.wikipedia.org/wiki/Category:London_Underground_lines", 
    "https://en.wikipedia.org/wiki/Category:Standard_gauge_railways_in_London", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_North_East_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_North_West_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_the_West_Midlands_(region)", 
    "https://en.wikipedia.org/wiki/Category:Railways_on_English_Islands", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_South_East_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_South_West_England", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_Yorkshire_and_the_Humber", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_Northern_Ireland", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_Scotland", 
    "https://en.wikipedia.org/wiki/Category:Closed_railway_lines_in_Scotland", 
    "https://en.wikipedia.org/wiki/Category:Standard_gauge_railways_in_Scotland", 
    "https://en.wikipedia.org/wiki/Category:Railway_lines_in_Wales", 
    "https://en.wikipedia.org/wiki/Category:Industrial_railways_in_Wales",]

href_fullname_exclusions = [
]

href_string_exclusions = [
":",
"List_of",
"Biographical",
"Main_Page",
"railway station",
]

unique_hrefs = []

for url in Categories:

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)

    soup = BeautifulSoup(res.text, 'html.parser') 

    count = 0
    for link in soup.find_all(title=True):
        if count > 2:
            exit
        else:
            count += 1
        href = str(link.get('href'))
        if not any(x in href for x in href_string_exclusions) and \
                href not in href_fullname_exclusions and \
                '/wiki' in href:
            
                csvrow = []
                csvrow.append(url)
                csvrow.append(href)
                csvrow.append(link.get('title'))
                
                # Get the route template name associated with this page
                try:
                    href_absolute = 'https://en.wikipedia.org/' + href
                    res = requests.get(href_absolute)
                    res.raise_for_status()
                    soup = BeautifulSoup(res.text, 'html.parser')
                    table = soup.find_all('table', {'cellspacing':'0'})[0] #Cellspacing limits the tables to those which are routemaps
                    template_link = ""
                    template_link = table.find_all('li', {'class':'nv-view'})[0].find('a').get('href')

                    if "Template" in template_link: csvrow.append(template_link)
                except IndexError:
                    print('no route template link for ', href)
                    pass
                except requests.exceptions.ConnectionError as err:
                    # eg, no internet
                    raise SystemExit(err)
                except requests.exceptions.HTTPError as err:
                    # eg, url, server and other errors
                    raise SystemExit(err)

                output1.writerow(csvrow)
                # print(csvrow)
        else:
            print(href, " was excluded")

csvFile.close()