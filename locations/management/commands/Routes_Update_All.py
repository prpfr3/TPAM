from django.core.management import BaseCommand
from locations.models import RouteLocation, RouteMap
import urllib.parse


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        queryset = RouteMap.objects.all()

        for entry in queryset:
            try:
                old_entry_name = entry.name
                entry.name = urllib.parse.unquote(entry.name)
                entry.save()
                # print(old_entry_name, entry.name)
            except Exception as e:
                print(f"Could not save routelocation due to error: {e}")
                continue
