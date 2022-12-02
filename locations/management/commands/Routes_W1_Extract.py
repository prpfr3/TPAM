"""
Traverses a set of pre-defined Wikipedia category pages and finds/stores all the url references on those pages 
which are likely Railway Lines along with the category name

Can be run as a full or partial extract by adjusting the categories list

"""
import contextlib
import requests, csv, os
from bs4 import BeautifulSoup

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

output_file = os.path.join(DATAIO_DIR, "Routes.csv")
with open(output_file, 'wt+', newline='', encoding='utf-8') as csvFile:
    output_routes_cvsfile = csv.writer(csvFile)
    csvrow = ["category", "wikislug", "name", "routemap"]
    output_routes_cvsfile.writerow(csvrow)

    Categories = [
        "Closed_railway_lines_in_Greater_Manchester", 
        "Closed_railway_lines_in_London", 
        "Closed_railway_lines_in_London", 
        "Closed_railway_lines_in_North_East_England", 
        "Closed_railway_lines_in_North_West_England", 
        "Closed_railway_lines_in_Scotland", 
        "Closed_railway_lines_in_South_East_England", 
        "Closed_railway_lines_in_South_West_England", 
        "Closed_railway_lines_in_the_East_Midlands", 
        "Closed_railway_lines_in_the_East_of_England",
        "Closed_railway_lines_in_the_West_Midlands_(region)", 
        "Closed_railway_lines_in_Wales",
        "Closed_railway_lines_in_Yorkshire_and_the_Humber", 
        "Industrial_railways_in_England", 
        "Industrial_railways_in_Wales",
        "Light_railways",
        "London_Underground_lines", 
        "Railway_lines_in_England", 
        "Railway_lines_in_London", 
        "Railway_lines_in_North_East_England", 
        "Railway_lines_in_North_West_England", 
        "Railway_lines_in_Northern_Ireland", 
        "Railway_lines_in_Scotland", 
        "Railway_lines_in_South_East_England", 
        "Railway_lines_in_South_West_England", 
        "Railway_lines_in_the_East_Midlands", 
        "Railway_lines_in_the_East_of_England", 
        "Railway_lines_in_the_West_Midlands_(region)", 
        "Railway_lines_in_Wales", 
        "Railway_lines_in_Yorkshire_and_the_Humber", 
        "Railways_on_English_Islands", 
        "Standard_gauge_railways_in_England", 
        "Standard_gauge_railways_in_London", 
        "Standard_gauge_railways_in_Scotland",
        "Standard_gauge_railways_in_Wales",
        ]

    href_fullname_exclusions = [
        "/wiki/Light_Railways_Act_1896",
        "/wiki/Light_railway",
        "/wiki/Railway",
        "/wiki/Chiang_Mai_light_rail_transit",
        "/wiki/Siam_Park_City_Railway",
    ]

    href_string_exclusions = [
    ":",
    "List_of",
    "Biographical",
    "Main_Page",
    "railway station",
    ]

    unique_hrefs = []


    routes_added = 0
    route_templates_added = 0

    for Category in Categories:
        url = f"https://en.wikipedia.org/wiki/Category:{Category}"

        try:
            res = requests.get(url).content.decode('utf-8', 'ignore')
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err) from err
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err) from err

        soup = BeautifulSoup(res, 'html.parser') 

        for link in soup.find_all(title=True):

            href = str(link.get('href'))

            if all(x not in href for x in href_string_exclusions) and \
                href not in href_fullname_exclusions and \
                '/wiki' in href:

                csvrow = [url, href, link.get('title')]
                route_url = f'https://en.wikipedia.org/{href}'
                try:
                    res = requests.get(route_url).content.decode('utf-8', 'ignore')
                except requests.exceptions.ConnectionError as err:
                    # eg, no internet
                    raise SystemExit(err) from err
                except requests.exceptions.HTTPError as err:
                    # eg, url, server and other errors
                    raise SystemExit(err) from err

                soup = BeautifulSoup(res, 'html.parser') 

                with contextlib.suppress(IndexError):
                    table = soup.find_all('table', {'cellspacing':'0'})[0] #Cellspacing limits the tables to those which are routemaps
                    template_link = ""

                    template_link = table.find_all('li', {'class':'nv-view'})[0].find('a').get('href')
                    routes_added += 1
                    if "Template" in template_link: 
                        csvrow.append(template_link)
                        route_templates_added += 1

                output_routes_cvsfile.writerow(csvrow)
                routes_added += 1

print(f"{routes_added=} and {route_templates_added=}")