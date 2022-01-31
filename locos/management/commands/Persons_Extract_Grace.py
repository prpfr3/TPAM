#To extract and save a Wikipedia or other HTML Table
##Note that the import may bring in some UTF-8 characters of \xa0 which is non-breaking space in Latin1 (ISO 8859-1) and chr(160)
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.gracesguide.co.uk/Category:Biography_-_Railways"
soup = BeautifulSoup(requests.get(url).text, 'html.parser') 

output_file = os.path.join("D:\\Data", "TPAM", "Persons_Extract_Grace.csv")
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)

href_in_listofnames = False

for link in soup.find_all(title=True):

    href = str(link.get('href'))

    if href == "/Richard_Henry_Abbatt":
        href_in_listofnames = True

    if href_in_listofnames == True:
        csvrow = []
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

    if href == "/Cesare_Zanetti":
        href_in_listofnames = False

csvFile.close()