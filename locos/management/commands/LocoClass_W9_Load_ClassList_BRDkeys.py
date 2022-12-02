from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClassList, LocoClass, Locomotive
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads the BRD classes against the Wikipedia classes where available"

    def handle(self, *args, **options):
        print("Adding BRD Keys to LocoClassLists")
        import os
        with open(os.path.join(DATAIO_DIR, 'Class_Wikipedia_BRD_Mapping.csv'), encoding="utf-8-sig") as file:   
            for row in DictReader(file):

                if row['BRD_Class_No']: # i.e. if there is a BRD reference in column 2
                    try:
                        """
                        There may be multiple wikipedia slug entries in the Mapping csv file for a single BRD_slug
                        because of redirects but only one of them will be in the lococlass table e.g.
                        Wikislug LNER Class A = BRD slug 000262 (redirects to NER Class Y)
                        Wikislug NER Class Y = BRD slug 000262 
                        Only NER Class Y is in the Lococlass table
                        """
                        slug = row['wikiname'].replace('/wiki','')
                        c = LocoClass.objects.get(wikiname=slug)
                    except ObjectDoesNotExist:
                        print(slug, ' is not in the LocoClass table')
                    except Exception as e:
                        print(slug, e)
                    else:
                        c.brdslug = row['BRD_Class_Slug']
                        c.save()

                        try:
                            locomotives_queryset = Locomotive.objects.filter(brd_class_name_slug=row['BRD_Class_Slug'])
                        except ObjectDoesNotExist:
                            print(row['brdslug'], ' is not in the Locomotive table')
                        except Exception as e:
                            print(e)
                        else:
                            for locomotive in locomotives_queryset:
                                locomotive.lococlass = c
                                locomotive.save()
                                print(locomotive, ' updated with lococlass ', locomotive.lococlass)

                        try:
                            cl = LocoClassList.objects.get(name=slug)
                        except ObjectDoesNotExist:
                            print(slug, ' is not in the LocoClassList table')
                        except Exception as e:
                            print(slug, e)
                        else:
                            cl.brdslug = row['BRD_Class_Slug']
                            cl.save()