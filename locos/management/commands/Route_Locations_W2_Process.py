import os

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
                        print(filename_splits[0], " found and route to be updated")

                    page = open(os.path.join(root, filename), encoding="utf-8")

                    template = BeautifulSoup(page, 'html.parser').find_all('table')[0]
                    rows = template.find_all('tr')

                    # rows = [r for r in template.findAll('tr') if r.find('tr')]

                    for row in rows:

                        lineout = []
                        imagesfound = []

                        for td in row.find_all('td', recursive=False):

                            imagesfound = td.find_all("a", {"class":"image"})

                            for a in imagesfound: # Targets a BS type template
                                try:
                                    lineout.append("Icon:" + a['href'])
                                except:
                                    pass

                        for td in row.find_all('td', recursive=False): # Targets a Routemap type template           
                            
                            if imagesfound == []: 
                                for img in td.find_all("img"):
                                    try:
                                        lineout.append("Icon:" + img['title'])
                                    except:
                                        pass

                        if len(lineout) > 0: # Only go on to complete the line if there is an icon on it; this eliminates non relevant and recursive lines
                            text = "Text:"
                            text = text + row.get_text().replace('\n', '')
                            text = text.rstrip()
                            if text != "Text:" and text != "Text:vteLegend":
                                lineout.append(text)

                            for a in row.find_all("a", href=True):
                                href = "Href:"
                                if a['href'] and '/wiki/' in a['href'] and 'Template' not in a['href'] and 'File' not in a['href']:
                                    lineout.append(href + a['href'])

                            if len(lineout) > 0 and len(lineout) < 20:
                                # print(lineout)

                                output_record_count = output_record_count + 1
                                
                                # print(f'({lineout=})')
                                for lineitem in lineout:
                                    # print(f'({lineitem=})')
                                    l = RouteLocation()
                                    l.routemap_fk = routemap_fk
                                    l.loc_no = output_record_count
                                    item = str(lineitem)
                                    # if "Icon:/wiki/" in item:
                                    #     l.type = 'Icon'
                                    #     item = item.rstrip('.svg')
                                    #     l.item = item.lstrip('Icon:/wiki/File:BSicon_')
                                    # elif "Icon:" in item:
                                    #     l.type = 'Icon'
                                    #     l.item = item.lstrip('Icon:')
                                    if "Text:" in item:
                                        l.type = 'Text'
                                        l.item = item.lstrip('Text:')
                                        l.save()
                                    elif "Href:" in item:
                                        l.type = 'Wikislug'
                                        l.item = item.lstrip('Href:')
                                        try:
                                            l.location_fk = Locations.objects.get(wikislug=l.item)
                                        except:
                                            print(l.item, 'not in Locations table')
                                        l.save()
