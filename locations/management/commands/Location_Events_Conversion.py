from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from locations.models import (
    ELR,
    LocationHistoricEvent,
    EventType,
    Route,
    Location,
)


class Command(BaseCommand):
    help = (
        "Converts old LocationEvents to the new LocationHistoricEvent generic structure"
    )

    def handle(self, *args, **options):
        # 1. Map old IDs to the NEW 'code' field in EventType model
        type_mapping = {
            1: "OPEN_OFF",  # Official Opening
            2: "CLOSE_PAX",  # Closed to Passengers
            3: "CLOSE_FRT",  # Closed to Freight
            4: "RAZED",  # Razed
            5: "NAME_CHG",  # Name Change
            6: "OWN_CHG",  # Ownership Change
            7: "ACT_PARL",  # Act of Parliament Approval
            8: "PROSP",  # Prospectus Issued
            9: "PROP",  # Proposal Put Forward
            10: "CONST_START",  # Construction Started
            11: "OP_EVENT",  # Operational Event
            12: "CO_INC",  # Company Incorporated
            13: "CLOSED",  # Closed
            14: "RECLOSED",  # Closed Again
            99: "OTHER",  # Other
        }

        old_events = LocationEvent.objects.all()
        created_count = 0

        # Cache ContentTypes to avoid repeated DB hits
        route_ct = ContentType.objects.get_for_model(Route)
        # Note: If your old model didn't have a Location FK,
        # we might need to assume it links to the Route's location or similar.
        # Adjust logic below if you have a Location FK on the old model.

        self.stdout.write(f"Starting conversion of {old_events.count()} events...")

        for old in old_events:
            # A. Get the new EventType object
            # Clean the code from your mapping and search flexibly
            target_code = type_mapping.get(old.type, "OTHER").strip()

            try:
                # icontains is more forgiving than get()
                etype = EventType.objects.filter(code__icontains=target_code).first()
                
                if not etype:
                    # Final safety fallback
                    self.stdout.write(self.style.WARNING(f"Could not find {target_code}, using OTHER"))
                    etype = EventType.objects.get(code="OTHER")
                    
            except EventType.DoesNotExist:
                raise CommandError("Even the 'OTHER' type is missing. Please check your DB.")

            # B. Determine which object to link to (Generic FK)
            # If the old event had a route, link it to the Route.
            # Otherwise, we need a fallback (assuming you might have Location logic)
            target_object = old.route_fk
            if not target_object:
                # If no route is present, skip or handle specifically
                self.stdout.write(
                    self.style.WARNING(f"Skipping event {old.id}: No route_fk found.")
                )
                continue

            # C. Create the new record
            LocationHistoricEvent.objects.create(
                event_type=etype,
                description=old.description,
                displaydate=old.date,  # Carrying over the old string date
                datefield=old.datefield
                or "1900-01-01",  # Ensure we have a date for the index
                content_type=ContentType.objects.get_for_model(target_object),
                object_id=target_object.id,
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully migrated {created_count} events.")
        )
