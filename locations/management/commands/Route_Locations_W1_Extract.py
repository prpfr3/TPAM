"""
Traverses a set of pre-defined category pages and finds/stores all the url references on those pages 
which are likely Railway Lines along with the category name

"""
import requests, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

# Define the Wikipedia Category pages from which the search for templates will commence
categories = [
    # "https://en.wikipedia.org/wiki/Category:Templates_for_railway_lines_of_the_United_Kingdom", 
    "https://en.wikipedia.org/w/index.php?title=Category:Templates_for_railway_lines_of_the_United_Kingdom&pagefrom=Crewe+to+Derby+Line#mw-pages", 
    "https://en.wikipedia.org/w/index.php?title=Category:Templates_for_railway_lines_of_the_United_Kingdom&pagefrom=Jaywick+Miniature+Railway#mw-pages", 
    "https://en.wikipedia.org/w/index.php?title=Category:Templates_for_railway_lines_of_the_United_Kingdom&pagefrom=North+Warwickshire+Line+RDT#mw-pages",
    "https://en.wikipedia.org/w/index.php?title=Category:Templates_for_railway_lines_of_the_United_Kingdom&pagefrom=Southern+Heights+Light+Railway#mw-pages",
    "https://en.wikipedia.org/wiki/Category:Templates_for_railway_lines_of_London",
    "https://en.wikipedia.org/wiki/Category:Templates_for_railway_lines_of_Northern_Ireland",
    "https://en.wikipedia.org/wiki/Category:Templates_for_railway_lines_of_Scotland",
    "https://en.wikipedia.org/w/index.php?title=Category:Templates_for_railway_lines_of_Scotland&pagefrom=Sutherland+Railway#mw-pages",
    "https://en.wikipedia.org/wiki/Category:Templates_for_railway_lines_of_Wales",
]

# Define any templates that should be excluded from the extract
href_fullname_exclusions = [
    "/wiki/Template:UK-railway-routemap",
    "/wiki/Template:Bristol_railway_map/MetroWest",
    "/wiki/Template:Lanarkshire_and_Ayrshire_Railway_Map",
]

# Define any strings that should be excluded if they appear in template names
href_string_exclusions = [
"Templates",
"category",
"Categories",
"categories",
"Category",
]

# Define an array to hold unique template urls (some may be mentioned twice in different categories)
unique_hrefs = []

count = 0

for category in categories:

    # Get the category page
    try:
        res = requests.get(category)
        res.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err) from err
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err) from err

    category_page = BeautifulSoup(res.text, 'html.parser') 

    # Get all the page links in the category page
    for link in category_page.find_all(title=True):

        if count > 5:
            break
        else:
            count =+ 1

        # If the page to be retrieved is already in the unique array, skip it to prevent duplicates
        if link in unique_hrefs:
            print(link, ' duplicate; not processed')
        else:
            unique_hrefs.append()

        href = str(link.get('href'))
        # Get the page but only if it is not in the exclusions
        if all(x not in href for x in href_string_exclusions) \
            and href not in href_fullname_exclusions \
            and '/wiki/Template:' in href:

            # Create a filename for each page
            splits = href.split(":")
            filename = f'{splits[1]}.html'
            if filename == "Bristol_railway_map/MetroWest.html":
                filename = "Bristol_railway_map MetroWest.html"  # A fudge ... that does not work!

            output_file = os.path.join(DATAIO_DIR, "Route_Diagrams", filename)

            try:
                # Open the file, get the page, find the first table (assumed to be a routemap) and write it to the file
                with open(output_file, 'w', encoding='utf-8') as output:

                    href_absolute_url = f'https://en.wikipedia.org{href}'
                    res = requests.get(href_absolute_url)
                    res.raise_for_status()
                    soup = BeautifulSoup(res.text, 'html.parser')
                    template = soup.find_all('table')[0]
                    output.write(str(template))
            except FileNotFoundError:
                print(output_file, "output file issue ...skipping")
            except IndexError:
                print('no table found on page for ', href_absolute_url, "skipping")
            except requests.exceptions.ConnectionError as err:
                # eg, no internet
                raise SystemExit(err) from err
            except requests.exceptions.HTTPError as err:
                # eg, url, server and other errors
                raise SystemExit(err) from err