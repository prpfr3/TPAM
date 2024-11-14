from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from locations.models import Location, ELR, ELRLocation

"""
# Run the following Wikidata SPARQL query at https://query.wikidata.org/ and save to a csv file called "Locations_Stations_Wikidata.csv"
# Project Webscraping, file Wikidata_SPARQLWrapper.ipynb has an example of how to do this using Python

SELECT DISTINCT ?item ?itemLabel ?operator ?operatorLabel ?geo ?openedLabel ?closedLabel ?image ?adminareaLabel ?countyLabel ?elrnameLabel ?disused ?railscot ?adjacentLabel ?towards ?interchangeLabel ?elr ?distance ?inceptionLabel ?elevationLabel ?ownedby ?ownedbyLabel ?architectLabel
WHERE
{
  ?item wdt:P31 wd:Q55488.# Q55488 Railway Station #wd:Q10283556. Workshop Q6138323.
  {?item wdt:P17 wd:Q145}
  UNION
  {?item wdt:P17 wd:Q174193} # (i.e. UK or UK of Great Britain & Ireland)

  OPTIONAL{?item wdt:P625 ?geo .}
  OPTIONAL{?item wdt:P137 ?operator .}
  OPTIONAL{?item wdt:P1619 ?opened .}
  OPTIONAL{?item wdt:P3999 ?closed .}
  OPTIONAL{?item wdt:P18 ?image .}
  OPTIONAL{?item wdt:P131 ?adminarea .}
  OPTIONAL{?item wdt:P7959 ?county .}
  OPTIONAL{?item wdt:P795 ?route .}
  OPTIONAL{?item wdt:P11437 ?disused .}
  OPTIONAL{?item wdt:P10987 ?railscot .}
  OPTIONAL{?item p:P197 [ ps:P197 ?adjacent ; pq:P5051 ?towards ; pq:P81 ?interchange] .}
  OPTIONAL{?item p:P795 [ ps:P795 ?elrname ; pq:P6710 ?distance ; pq:P10271 ?elr] .}
  OPTIONAL{?item wdt:P571 ?inception .}
  OPTIONAL{?item wdt:P2044 ?elevation .}
  OPTIONAL{?item wdt:P127 ?ownedby .}
  OPTIONAL{?item wdt:P84 ?architect .}

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
    """
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Locations_Stations_Wikidata.csv into the LocationsELR Table"

    def handle(self, *args, **options):

        with open(
            os.path.join(DATAIO_DIR, "Location_Stations_Wikidata_2024-07-21.csv"),
            encoding="utf-8",
        ) as file:

            elrloc = ELRLocation()

            count = 0
            saved_count = 0
            for row in DictReader(file):

                count = count + 1
                # if count > 20:
                #     break
                location_slug = row["itemLabel"].replace(" ", "_")

                try:
                    locations = Location.objects.filter(wikislug=location_slug)
                except ObjectDoesNotExist:
                    print(location_slug, " not found in the Location table")
                except MultipleObjectsReturned:
                    print(location_slug, " multiple instances returned")
                except Exception as e:
                    print(location_slug, e)
                else:
                    try:
                        elr = ELR.objects.get(itemAltLabel=row["elr"])
                    except ObjectDoesNotExist:
                        print(row["elr"], " not found in the ELR table")
                    except MultipleObjectsReturned:
                        print(row["elr"], " multiple instances returned")
                    except Exception as e:
                        print(elr, e)
                    else:
                        for location in locations:
                            try:
                                elrloc, elrloc_created = (
                                    ELRLocation.objects.get_or_create(
                                        location_fk=location, elr_fk=elr
                                    )
                                )
                                if elrloc_created:
                                    print(
                                        f"{elr.itemAltLabel} added to location {location.name}"
                                    )
                            except Exception as e:
                                print(
                                    f"error {e} getting or creating elr location {location} {elr}"
                                )

                            if row["distance"] != "":
                                elrloc.distance = float(row["distance"])
                            else:
                                elrloc.distance = None
                            try:
                                elrloc.save()
                                # print(f"{elrloc} saved")
                            except Exception as e:
                                print(f"error {e} saving {elrloc}")
