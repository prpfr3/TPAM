import os

from bs4 import BeautifulSoup
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import BaseCommand
from locos.models import RouteLocation, RouteMap, Locations

DATAIO_DIR = os.path.join("D:\\Data", "TPAM", "Route_Diagrams")
os.chdir(DATAIO_DIR)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Route Location Data"

    def handle(self, *args, **options):
        # if RouteLocation.objects.exists():
        #     print('Route Locations already loaded. Load halted')
        # else:
            print("Creating Route Locations")
            output_record_count = 0

            for root, dirs, files in os.walk(os.getcwd()):
                for filename in files:

                    filename_splits = filename.split(".")

                    try:
                        routemap_fk, routemap_created = RouteMap.objects.get_or_create(name=filename_splits[0],) 
                    except MultipleObjectsReturned:
                        print(filename_splits[0], ' found multiple times in the RouteMap table')
                        pass
                    else:
                        pass
                        # print(filename_splits[0], " found and route to be updated")

                    page = open(os.path.join(root, filename), encoding="utf-8")
                    template = BeautifulSoup(page, 'html.parser').find_all('table')[0]
                    rows = template.find_all('tr')

                    for row in rows:

                        lineout = []
                        imagesfound = []
                        imagesfound = row.find_all("a", {"class":"image"})  

                        # Look through all the cells and collect the routemap icons
                        # Use recursive=False to prevent an icon being collected more than once where there is a cell in a cell
                        for td in row.find_all('td', recursive=False):
                            
                            if imagesfound == []: # For Routemap type template
                                for img in td.find_all("img"): # In the Routemap case look for "img" rather than "a"
                                    lineout.append(img['src'])
                            else:
                                for a in imagesfound: # For a BS type template
                                    lineout.append(a['href'])

                        # Only further process the row if there is an icon on it; 
                        # This eliminates non relevant and recursive lines
                        # Works correctly for WCML

                        if len(lineout) > 0 and len(lineout) < 5:
                            linetext = ""
                            for td in row.find_all('td', recursive=False):
                                if td.get_text(" ", strip=True) != "":
                                    celltext = td.get_text(" ", strip=True)

                                    href_count = 0
                                    for a in td.find_all("a", href=True):
                                        # Collect only attributes which contain '/wiki/' so that icon hrefs are not collected again, nor other non relevant attributes
                                        if a['href'] \
                                            and '/wiki/' in a['href'] \
                                            and 'Template' not in a['href'] \
                                            and 'File' not in a['href'] \
                                            and a.get_text() != "" \
                                            and a.get_text() in celltext:
                                                oldstring = a.get_text()
                                                newstring = "[" + oldstring + "](" + a['href'] + ")"
                                                celltext = celltext.replace(oldstring, newstring)
                                                href_count += 1
                                                                       
                                    linetext = linetext + celltext

                                    if imagesfound == []: # Only do this for a Routemap type template
                                        output_record_count = output_record_count + 1
                                        l = RouteLocation()
                                        # If the Routemap row has only one href try and associate this with a Location in the database
                                        # If more than one href, then the Location is ambiguous
                                        if href_count == 1:
                                            try:
                                                l.location_fk = Locations.objects.get(wikislug=a['href'])
                                            except:
                                                pass

                                        l.routemap_fk = routemap_fk
                                        l.loc_no = output_record_count
                                        l.label = celltext 
                                        try:
                                            l.save()
                                        except:
                                            print('Error on saving for ', l)
                            
                            if linetext != "" and imagesfound != []: # Only do this for a BSTemplate (after tds merged in linetext)
                                output_record_count = output_record_count + 1
                                l = RouteLocation()
                                # If the Routemap row has only one href try and associate this with a Location in the database
                                # If more than one href, then the Location is ambiguous
                                if href_count == 1:
                                    try:
                                        l.location_fk = Locations.objects.get(wikislug=a['href'])
                                    except:
                                        pass
                                l.routemap_fk = routemap_fk
                                l.loc_no = output_record_count
                                l.label = linetext
                                try:
                                    l.save()
                                except:
                                    print('Error on saving for ', l)
