import datetime
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from locations.models import ELR, LocationHistoricEvent, EventType

class Command(BaseCommand):
    help = 'Migrates all ELR date fields into the unified LocationHistoricEvent model'

    def handle(self, *args, **options):
        # 1. Define the mapping: { "ModelField": ("EventType_Code", "Description") }
        field_map = {
            "opened": ("OPENED", "Opened"),
            "opened_freight": ("OPENED_FRT", "Opened for Freight"),
            "opened_passenger": ("OPEN_PAX", "Opened for Passengers"),
            "closed_freight": ("CLOSE_FRT", "Closed for Freight"),
            "closed_passenger": ("CLOSE_PAX", "Closed for Passengers"),
            "closed": ("CLOSED", "Closed"),
        }

        elr_ct = ContentType.objects.get_for_model(ELR)
        
        # 2. Pre-fetch EventTypes into a dictionary for speed
        event_types = {et.code: et for et in EventType.objects.filter(code__in=[v[0] for v in field_map.values()])}
        
        # Verify all event types exist before starting
        missing = [code for code, info in field_map.values() if code not in event_types]
        if missing:
            self.stdout.write(self.style.ERROR(f"Missing EventType codes in DB: {missing}"))
            return

        # 3. Get all ELRs that have at least one date set
        elrs = ELR.objects.all()
        count = 0
        
        self.stdout.write(f"Scanning ELR records...")

        for elr in elrs:
            # 4. For each ELR, check every field in our map
            for field_name, (type_code, desc) in field_map.items():
                date_val = getattr(elr, field_name)
                
                if date_val:
                    # Found a date! Let's migrate it.
                    et_obj = event_types[type_code]
                    display_str = date_val.strftime('%d-%m-%Y')

                    obj, created = LocationHistoricEvent.objects.get_or_create(
                        content_type=elr_ct,
                        object_id=elr.id,
                        event_type=et_obj,
                        defaults={
                            'datefield': date_val,
                            'displaydate': display_str,
                            'description': desc,
                        }
                    )

                    if created:
                        count += 1
                        self.stdout.write(f"Created {type_code} for {elr.itemLabel}")

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} historical events for ELRs."))