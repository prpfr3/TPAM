#To extract and save a Wikipedia Table
#Based on Pluralsight https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup

import requests, csv
from bs4 import BeautifulSoup

# Step 1: Sending a HTTP request to a URL
#url = "https://en.wikipedia.org/wiki/Locomotive_of_the_Midland_Railway"
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Step 2: Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
# print(soup.prettify()) # print the parsed data of html

# Step 3: Analyze the HTML tag, where your content lives
# Create a data dictionary to store the data.
data = {}
#Get the table having the class wikitable
wiki_table = soup.find("table", attrs={"class": "wikitable"})
wiki_table_data = wiki_table.tbody.find_all("tr")  # contains 2 rows

# Get all the headings of Lists
headings = []
for td in wiki_table_data[0].find_all("td"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.b.text.replace('\n', ' ').strip())

# Get all the tables contained in "wiki_table"
for table, heading in zip( wiki_table_data[0].find_all("table"), headings):
    # Get headers of table
    t_headers = []
    for th in table.find_all("th"):
        # remove any newlines and extra spaces from left and right
        t_headers.append(th.text.replace('\n', ' ').strip())
    
    # Get all the rows of table
    table_data = []
    for tr in table.tbody.find_all("tr"): # find all tr's from table's tbody
        t_row = {}
        # find all td's in tr and zip it with t_header
        for td, th in zip(tr.find_all("td"), t_headers): 
            t_row[th] = td.text.replace('\n', '').strip()
        table_data.append(t_row)

    # Put the data for the table with its heading.
    data[heading] = table_data


# Step 4: Export the data to csv
"""
Will create a separate csv for each table
"""
for topic, table in data.items():
    # Create csv file for each table
    with open(f"{topic}.csv", 'w') as out_file:
        # Each 3 table has headers as following
        headers = [ 
            "Country/Territory",
            "GDP(US$million)",
            "Rank"
        ] # == t_headers
        writer = csv.DictWriter(out_file, headers)
        # write the header
        writer.writeheader()
        for row in table:
            if row:
                writer.writerow(row)
