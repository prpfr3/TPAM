import contextlib
import os

from bs4 import BeautifulSoup
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import BaseCommand
from locations.models import RouteLocation, RouteMap, Location

DATAIO_DIR = os.path.join("D:\\Data", "TPAM", "Route_Diagrams")
os.chdir(DATAIO_DIR)

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Route Location Data"

    def handle(self, *args, **options):
        # if RouteLocation.objects.exists():
        #     print('Route Location already loaded. Load halted')
        # else:
        print("Creating Route Location")
        output_record_count = 0

        for root, dirs, files in os.walk(os.getcwd()):
            for filename in files:

                filename_splits = filename.split(".")

                try:
                    routemap_fk, routemap_created = RouteMap.objects.get_or_create(name=filename_splits[0],)
                except MultipleObjectsReturned:
                    print(filename_splits[0], ' found multiple times in the RouteMap table')
                page = open(os.path.join(root, filename), encoding="utf-8")
                template = BeautifulSoup(page, 'html.parser').find_all('table')[0]
                rows = template.find_all('tr')

                for row in rows:

                    lineout = []
                    rows_with_icons = []
                    rows_with_icons = row.find_all("a", {"class":"image"})  

                    for td in row.find_all('td', recursive=False):

                        if rows_with_icons == []: # For Routemap type template
                            lineout.extend(img['src'] for img in td.find_all("img"))
                        else:
                            for a in rows_with_icons: # For a BS type template
                                lineout.append(a['href'])

                    # Only further process the row if there is an icon on it; 
                    # This eliminates non relevant and recursive lines
                    # Works correctly for WCML (i.e. the complex West Coast Main Line template)

                    if lineout and len(lineout) < 5:
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
                                            newstring = f"[{oldstring}](" + a['href'] + ")"
                                            celltext = celltext.replace(oldstring, newstring)
                                            href_count += 1

                                linetext = linetext + celltext

                                if rows_with_icons == []: # Only do this for a Routemap type template
                                    output_record_count = output_record_count + 1
                                    l = RouteLocation()
                                    # If the Routemap row has only one href try and associate this with a Location in the database
                                    # If more than one href, then the Location is ambiguous
                                    if href_count == 1:
                                        slug = a["href"].replace('/wiki/','')
                                        with contextlib.suppress(Exception):
                                            l.location_fk = Location.objects.get(wikislug=slug)
                                    l.routemap = routemap_fk
                                    l.loc_no = output_record_count
                                    l.label = celltext
                                    try:
                                        l.save()
                                    except Exception as e:
                                        print(f'Error {e} on saving for {l.routemap}\n{l.loc_no=}\n{l.label=}\n')

                        if linetext != "" and rows_with_icons != []: # Only do this for a BSTemplate (after tds merged in linetext)
                            output_record_count = output_record_count + 10
                            l = RouteLocation()
                            # If the Routemap row has only one href try and associate this with a Location in the database
                            # If more than one href, then the Location is ambiguous
                            if href_count == 1:
                                slug = a["href"].replace('/wiki/','')
                                with contextlib.suppress(Exception):
                                    l.location_fk = Location.objects.get(wikislug=slug)
                            l.routemap = routemap_fk
                            l.loc_no = output_record_count
                            l.label = linetext
                            try:
                                l.save()
                            except Exception as e:
                                print(f'Error {e} on saving for {l.routemap}\n{l.loc_no=}\n{l.label=}\n')