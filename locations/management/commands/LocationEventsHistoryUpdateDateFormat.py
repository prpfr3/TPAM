# Run: python manage.py shell
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import LocationHistoricEvent
from django.db import transaction
import os


class Command(BaseCommand):
    # Show this when the user types help
    help = "Adjusts Locations based on csv input"

    def handle(self, *args, **options):

      events = LocationHistoricEvent.objects.all()
      count = 0

      with transaction.atomic():
          for event in events:
              print(event_displaydate:=event.displaydate)
              old_val = event.displaydate
              if not old_val:
                  continue

              # 1. Standardize separators: / becomes -
              new_val = old_val.replace('/', '-')

              # 2. Reformat YYYY-MM-DD to DD-MM-YYYY
              # We split by '-' and check if the first part is a 4-digit year
              parts = new_val.split('-')
              if len(parts) == 3 and len(parts[0]) == 4:
                  # Reorder: Day-Month-Year
                  new_val = f"{parts[2]}-{parts[1]}-{parts[0]}"

              # Only save if something actually changed
              if new_val != old_val:
                  event.displaydate = new_val
                  event.save()
                  count += 1

      print(f"Successfully updated {count} display dates.")