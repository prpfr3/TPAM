"""
Loads the BRD classes against Wikipedia classes, as manually mapped in the input file

In the TPAM database there is one instance of a loco class for a wikipedia page. Where there are multiple urls
for a class because the class is known by multiple names, Wikipedia uses redirects to a single page for a class.
In TPAM the multiple class names have been concatenated into one. 

It is therefore important that the input file for this program either uses the correct class name (which may have
in TPAM have been constructed from multiple names) or uses the unique wikipedia slug.

"""

from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass, Locomotive
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("Adding BRD Keys to Loco Classes")

        with open(
            os.path.join(DATAIO_DIR, "Class_BRD_Wikipedia_Mapping.csv"),
            encoding="utf-8-sig",
        ) as file:
            for row in DictReader(file):

                if row["brdslug"]:
                    try:
                        wikiname = row["wikiname"].replace("British Rail", "BR")
                        c = LocoClass.objects.get(name=wikiname)
                    except ObjectDoesNotExist:
                        print(wikiname, " is not in the LocoClass table")
                    except Exception as e:
                        print(wikiname, e)
                    else:
                        brdslug_before = c.brdslug
                        c.brdslug = row["brdslug"]
                        c.save()

                        if brdslug_before != c.brdslug:
                            print(
                                f"{brdslug_before} changed to {c.brdslug} for {c} with {len(locomotives_queryset)} locos)"
                            )

                        try:
                            locomotives_queryset = Locomotive.objects.filter(
                                brd_class_name_slug=row["brdslug"]
                            )
                        except ObjectDoesNotExist:
                            print(row["brdslug"], " is not in the Locomotive table")
                        except Exception as e:
                            print(e)
                        else:
                            if len(locomotives_queryset) != 0:
                                count = 0
                                for locomotive in locomotives_queryset:
                                    locomotive.lococlass = c
                                    locomotive.save()
                                    count += 1
                                print(
                                    count,
                                    " locomotives updated with lococlass ",
                                    locomotive.lococlass,
                                )
