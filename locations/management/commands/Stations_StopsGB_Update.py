import os
from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from locations.models import Location, LocationCategory


class Command(BaseCommand):

    def handle(self, *args, **options):

        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        current_date = datetime.now().strftime("%Y-%m-%d")
        INPUT_LOADFILE = os.path.join(
            DATAIO_DIR,
            f"Location_Stations_StopsGB.csv",
        )

        LOGFILE = os.path.join(
            DATAIO_DIR,
            f"Location_StopsGB_Update_{current_date}.log",
        )

        # Retrieve key of "Current Station" Category
        current_station_category = LocationCategory.objects.get(
            category="Current Station"
        )

        closed_station_category = LocationCategory.objects.get(
            category="Closed Station"
        )

        count = 0
        count_added = 0
        count_updated = 0

        with open(INPUT_LOADFILE, encoding="utf-8-sig") as file:
            for row in DictReader(file):
                count += 1
                if (
                    count != 0
                    and row["selected_entity_type"] == "station"
                    and row["ghost_entry"] == "FALSE"
                ):

                    StopsGB_wikislug = row["selected_entity_label"].replace(" ", "_")
                    locations_wikislug = Location.objects.filter(
                        wikislug=StopsGB_wikislug
                    )

                    StopsGB_wikiname = row["selected_entity_label"].replace(
                        " railway station", ""
                    )
                    locations_wikiname = Location.objects.filter(
                        wikiname=StopsGB_wikiname
                    )

                    if locations_wikislug.exists():
                        for l in locations_wikislug:
                            self.update_location(l, row, new=False)
                            count_updated += 1
                    elif locations_wikiname.exists():
                        for l in locations_wikiname:
                            self.update_location(l, row, new=False)
                            count_updated += 1
                    else:
                        # l = Location()
                        # self.update_location(l, row, new=True)
                        # print(f"New location created for {row} ")
                        count_added += 1

        print(
            f"{count_added} & {count_updated} railway station locations NOT FOUND or UPDATED respectively"
        )

    def update_location(self, location, row, new=False):
        # print(f"Current Location Data {location}")
        # print(f"{row}")
        if new:
            location.wikislug = row["selected_entity_label"].replace(" ", "_")
            # print(f"New location {location.wikislug} being added")

        location.wikidata_id = row["selected_entity"]
        location.RCH_StopsGB_PlaceId = row["PlaceId"]
        location.RCH_StopsGB_StationId = row["StationId"]
        location.RCH_StopsGB_Place = row["Place"]
        location.RCH_StopsGB_AbbrStation = row["AbbrStation"]
        location.RCH_StopsGB_Station = row["Station"]
        location.RCH_StopsGB_Altnames = row["Altnames"]
        location.RCH_StopsGB_Predicted_Place = row["predicted_place"]

        if row["Opening"] != "unknown":
            location.opened = row["Opening"]

        if row["Closing"] != "unknown" and row["Closing"] != "still open":
            location.closed = row["Closing"]

        location.geometry = f"POINT ({row['selected_entity_longitude']} {row['selected_entity_latitude']})"

        try:
            location.save()
        except Exception as e:
            print(f"Error {e} for {location.name}")

        # if new and row["Closing"] == "still open":
        #     try:
        #         # location.categories.add(current_station_category)
        #         print(f"New location {location} categorised as current")
        #     except Exception as e:
        #         print(f"Error {e} for location {location.id}")

        # if new and row["Closing"] != "still open":
        #     try:
        #         # location.categories.add(closed_station_category)
        #         print(f"New location {location} categorised as closed")
        #     except Exception as e:
        #         print(f"Error {e} for location {location.id}")
