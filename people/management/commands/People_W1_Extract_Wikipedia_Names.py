#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

output_file = os.path.join("D:\\Data", "TPAM", "People_Extract_Wikipedia.csv")
Categories = [  "English_railway_mechanical_engineers",
                "Scottish_railway_mechanical_engineers",
                "British_railway_civil_engineers",
                "British_railway_pioneers",
                "British_railway_mechanical_engineers",
                "British_railway_civil_engineers",
                "British_railway_inspectors",
                "British_railway_pioneers",
                "British_Rail_people",
                "British_rail_transport_chief_executives",
                "Caledonian_Railway_people",
                "Cambrian_Railways_people",
                "British_railway_entrepreneurs",
                "Directors_of_the_Furness_Railway",
                "Glasgow_and_South_Western_Railway_people",
                "Great_Central_Railway_people", 
                "Directors_of_the_Great_Central_Railway", 
                "Directors_of_the_Glasgow_and_South_Western_Railway", 
                "Great_Eastern_Railway_people", 
                "Directors_of_the_Great_Eastern_Railway", 
                "Directors_of_the_Caledonian_Railway", 
                "Directors_of_the_Cambrian_Railways",
                "Great_Northern_Railway_(Great_Britain)_people", 
                "Directors_of_the_Great_Northern_Railway_(Great_Britain)", 
                "Great_Western_Railway_people", 
                "Directors_of_the_Great_Western_Railway", 
                "London_and_North_Eastern_Railway_people", 
                "London_and_North_Western_Railway_people", 
                "Directors_of_the_London_and_North_Western_Railway", 
                "London_and_South_Western_Railway_people", 
                "London,_Brighton_and_South_Coast_Railway_people", 
                "London,_Midland_and_Scottish_Railway_people", 
                "Midland_Railway_people", 
                "North_Eastern_Railway_(UK)_people", 
                "South_Eastern_and_Chatham_Railway_people", 
                "Southern_Railway_(UK)_people",   ]

# Encoding ensures correct handling on first record \xa0 from Windows files (non-breaking space in Latin1 (ISO 8859-1) and chr(160))
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
                    'Category' not in href and \
                    'Main_Page' not in href:
                    csvrow = [Category, href]
                    """For an article on the complexities of name splitting see:-
                https://stackoverflow.com/questions/259634/splitting-a-persons-name-into-forename-and-surname/259694
                """
                    split_title = link.get('title').rsplit(" (", 1)
                    fullname = split_title[0].rsplit(" ", 1)
                    surname = fullname[1]
                    firstnames = fullname[0]
                    csvrow.extend((split_title[0], firstnames, surname))
                    output.writerow(csvrow)
        finally:
            pass