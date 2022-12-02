#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

output_file = os.path.join("D:\\Data", "TPAM", "Persons_Extract_Wikipedia.csv")
Categories = ["Locomotive_builders_and_designers", 
                "English_railway_mechanical_engineers",
                "Scottish_railway_mechanical_engineers",
                "British_railway_civil_engineers",
                "British_railway_pioneers"]

with open(output_file, 'wt+', newline='', encoding='utf-8') as csvFile:
    for Category in Categories:
        url = f"https://en.wikipedia.org/wiki/Category:{Category}"
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'html.parser') 

        output = csv.writer(csvFile)

        try:
            for link in soup.find_all(title=True):
                href = str(link.get('href'))
                if '/wiki' in href and \
                    ':' not in href and \
                    'List_of' not in href and \
                    'Biographical' not in href and \
                    'Main_Page' not in href:
                    csvrow = []
                    csvrow.append(Category)
                    csvrow.append(href)
                    """For an article on the complexities of name splitting see:-
                https://stackoverflow.com/questions/259634/splitting-a-persons-name-into-forename-and-surname/259694
                """
                    split_title = link.get('title').rsplit(" (", 1)
                    fullname = split_title[0].rsplit(" ", 1)
                    surname = fullname[1]
                    firstnames = fullname[0]
                    csvrow.append(split_title[0]) # i.e. the title field minus anything in parentheses
                    csvrow.append(firstnames)
                    csvrow.append(surname)
                    output.writerow(csvrow)
        finally:
            pass