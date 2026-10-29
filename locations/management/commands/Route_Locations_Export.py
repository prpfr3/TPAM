import os
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from locations.models import Location, LocationHistoricEvent, RouteLocation
from openpyxl import Workbook


class Command(BaseCommand):
    help = """
    Export all RouteLocation records for a given routemap to Excel files.

    The first Excel file contains the RouteLocation records, and the second Excel file contains the LocationHistoricEvent records for the locations referenced in the RouteLocation records.

    To execute:- python manage.py Route_Locations_Export  "S&DJR_RDT"
    """

    DATAIO_DIR = os.path.join("C:\\Users\\paulf\\OneDrive\\Data", "TPAM")
    os.chdir(DATAIO_DIR)

    def add_arguments(self, parser): 
        parser.add_argument(
            "routemap_name",
            type=str,
            help="name of the routemap to extract records for",
        )

    def handle(self, *args, **kwargs):
        routemap_name = kwargs["routemap_name"]
        output_file = f"RouteLocations_{routemap_name}.xlsx"
        history_output_file = f"LocationHistoryEvents_{routemap_name}.xlsx"

        records = RouteLocation.objects.filter(
            routemap__name=routemap_name
        ).order_by("loc_no")

        if not records.exists():
            self.stdout.write(f"No records found for routemap name {routemap_name}")
            return

        route_field_names = [
            "id",
            "routemap",
            "loc_no",
            "location_fk",
            "location_slug",
            "location_wikislug",
            "linear_reference",
            "note",
        ]

        location_ids = [
            record.location_fk_id for record in records if record.location_fk_id
        ]
        unique_location_ids = list(dict.fromkeys(location_ids))

        history_events = []
        history_field_names = [
            "id",
            "event_type",
            "event_type_label",
            "description",
            "displaydate",
            "datefield",
            "location_id",
            "location_name",
            "location_slug",
            "location_wikislug",
            "event_date_added",
        ]

        if unique_location_ids:
            location_content_type = ContentType.objects.get_for_model(Location)
            history_events = LocationHistoricEvent.objects.filter(
                content_type=location_content_type,
                object_id__in=unique_location_ids,
            ).select_related("event_type").order_by("datefield")

            locations_by_id = {
                loc.id: loc
                for loc in Location.objects.filter(id__in=unique_location_ids)
            }

        try:
            # ---------------------------
            # WRITE ROUTE LOCATIONS EXCEL
            # ---------------------------
            wb = Workbook()
            ws = wb.active
            ws.title = "RouteLocations"

            ws.append(route_field_names)

            for record in records:
                ws.append([
                    record.id,
                    str(record.routemap),
                    record.loc_no,
                    record.location_fk_id,
                    record.location_fk.slug if record.location_fk else None,
                    record.location_fk.wikislug if record.location_fk else None,
                    record.linear_reference,
                    record.note,
                ])

            wb.save(output_file)

            self.stdout.write(
                f"Successfully exported {records.count()} RouteLocation records to {output_file}"
            )

            # ---------------------------
            # WRITE HISTORY EVENTS EXCEL
            # ---------------------------
            def strip_tz(value):
                if hasattr(value, "tzinfo") and value.tzinfo is not None:
                    return value.replace(tzinfo=None)
                return value

            # ---------------------------
            # WRITE HISTORY EVENTS EXCEL
            # ---------------------------
            if unique_location_ids:
                wb2 = Workbook()
                ws2 = wb2.active
                ws2.title = "LocationHistoryEvents"

                ws2.append(history_field_names)

                for event in history_events:
                    location = locations_by_id.get(event.object_id)

                    ws2.append([
                        event.id,
                        event.event_type.code if event.event_type else None,
                        event.event_type.label if event.event_type else None,
                        event.description,
                        strip_tz(event.displaydate),
                        strip_tz(event.datefield),
                        event.object_id,
                        location.name if location else None,
                        location.slug if location else None,
                        location.wikislug if location else None,
                        strip_tz(event.date_added),
                    ])

                wb2.save(history_output_file)

                self.stdout.write(
                    f"Successfully exported {history_events.count()} LocationHistoricEvent records to {history_output_file}"
                )

            else:
                self.stdout.write(
                    "No LocationForeignKey values were present, so no LocationHistoryEvents file was created."
                )

        except Exception as e:
            self.stderr.write(f"An error occurred: {e}")