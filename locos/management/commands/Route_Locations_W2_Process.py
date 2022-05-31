import os

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management import BaseCommand
from locos.models import RouteLocation, RouteMap

DATAIO_DIR = os.path.join("D:\\Data", "TPAM", "Route_Diagrams")
os.chdir(DATAIO_DIR)

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Route Location Data"

    def handle(self, *args, **options):
        if RouteLocation.objects.exists():
            print('Route Locations already loaded. Load halted')
        else:
            print("Creating Route Locations")

            for root, dirs, files in os.walk(os.getcwd()):
                for filename in files:
                    # print(filename)
                    res = open(os.path.join(root, filename), encoding="utf-8")

                    # Get the first table in the file (there should only be one)
                    try:
                        routetable = BeautifulSoup(res, 'html.parser').find_all('table')[0]
                    except IndexError:
                        print('no routetable for ', filename, "skipping")
                        pass
                    else:
                        trs = routetable.find_all('tr')

                        output_record_count = 0

                        for tr in trs:
                            output_record = []
                            # for each cell in a table row.....
                            for td in tr.find_all('td', recursive=False):
                                # If it is a cell with route icons, retrieve them into a list and append to the output file
                                # but exclude images with no title (e.g. Manchester Metrolink symbol not on routemap)
                                if td.find_all("img"):
                                    images = ""
                                    try:
                                        for img in td.find_all('img'):
                                            images = images + img['title'] + " "
                                        output_record.append(images)
                                    except:
                                        pass
                                # If it is not cell with an image (a.k.a. route icon) see get any text in it
                                else:
                                    text =""
                                    href =[]
                                    # See if there is a further sub-table with text in it (happens where a row is described with multiple locations and urls)
                                    for td_subcell in td.find_all('td'):
                                        text = text + td_subcell.get_text() + " "
                                    # ...but if there isn't a subcell of the cell, get the text from the cell
                                    if text == "":
                                        text = td.get_text().replace('\n', '')
                                    output_record.append(text)

                                    # Build a list of all the links (to stations, routes etc)
                                    for a in td.find_all("a", href=True):
                                        if a['href'] and '/wiki/' in a['href'] and 'Template' not in a['href']:
                                            href.append(a['href'])
                                    output_record.append(href)

                            if len(output_record) > 2:
                                output_record_count = output_record_count + 1
                                filename_splits = filename.split(".")
                                l = RouteLocation()

                                try:
                                    r, routemap_created = RouteMap.objects.get_or_create(name=filename_splits[0],) 
                                except MultipleObjectsReturned:
                                    print(filename_splits[0], ' found multiple times in the RouteMap table')
                                    pass
                                else:
                                    l.routemap_fk = r
                                l.tr = output_record_count
                                try: l.td1 = output_record[1]
                                except: pass
                                try: l.td2 = output_record[2] 
                                except:pass
                                try: l.td3 = output_record[3]
                                except:pass
                                try: l.td4 = output_record[4]
                                except:pass
                                try: l.td5 = output_record[5]
                                except:pass
                                try: l.td6 = output_record[6]
                                except:pass
                                l.save()
