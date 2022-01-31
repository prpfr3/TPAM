"""
Extracts Railway Company page references from Wikipedia based on pre-specified Wikipedia categories
"""

import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

output_file = os.path.join("D:\\Data", "TPAM", "Companies_Extract_Wikipedia.csv")
Categories = ["Early_British_railway_companies",
            "Early_Scottish_railway_companies",
            "Early_Welsh_railway_companies",
            "Pre-grouping_British_railway_companies",
            "Great_Western_Railway_constituents",
            "List_of_constituents_of_the_Great_Western_Railway",
            "London_and_North_Eastern_Railway_constituents",
            "List_of_constituents_of_the_London_and_North_Eastern_Railway",
            "London,_Midland_and_Scottish_Railway_constituents",
            "List_of_constituents_of_the_London,_Midland_and_Scottish_Railway",
            "Southern_Railway_(UK)_constituents",
            "British_joint_railway_companies",
            "Big_four_British_railway_companies",
            "Minor_British_railway_companies",
            "Railway_companies_of_the_United_Kingdom",
            ]

csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
csvrow = []
csvrow.append("category")
csvrow.append("wikislug")
csvrow.append("name")
output.writerow(csvrow)

for Category in Categories:
    url = "https://en.wikipedia.org/wiki/Category:" + Category
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser') 

    for row in soup.find_all(title=True):
        slug = str(row.get('href'))
        if '/wiki' in slug and \
            '/wiki/1948' not in slug and \
            '/wiki/Big_Four_(British_railway_companies)' not in slug and \
            '/wiki/Big_Four_British_railway_companies' not in slug and \
            '/wiki/ISBN_(identifier)' not in slug and \
            '/wiki/Railways_Act_1921' not in slug and \
            '/wiki/Act_of_Parliament' not in slug and \
            '/wiki/Train_operating_company' not in slug and \
            '/wiki/Case_sensitivity' not in slug and \
            ':' not in slug and \
            'List_of' not in slug and \
            "/wiki/British_carriage_and_wagon_numbering_and_classification" not in slug and \
            "/wiki/Railway_Executive_Committee" not in slug and \
            'Main_Page' not in slug:
                csvrow = []
                csvrow.append(Category)
                csvrow.append(slug)
                if slug == "/wiki/North_Eastern_Railway_(United_Kingdom)":
                    csvrow.append('North Eastern Railway')
                else:
                    csvrow.append(row.get('title'))
                output.writerow(csvrow)

# Add companies that don't currently fall into the above categories
csvrow = []
csvrow.append("")
csvrow.append("/wiki/Vale_of_Rheidol_Railway")
csvrow.append("Vale of Rheidol Railway (Narrow Gauge)")
output.writerow(csvrow)

csvrow = []
csvrow.append("")
csvrow.append("/wiki/Lancashire,_Derbyshire_and_East_Coast_Railway")
csvrow.append("Lancashire, Derbyshire and East Coast Railway")
output.writerow(csvrow)

csvrow = []
csvrow.append("")
csvrow.append("/wiki/North_Eastern_Railway_(United_Kingdom)")
csvrow.append("North Eastern Railway")
output.writerow(csvrow)

csvFile.close()