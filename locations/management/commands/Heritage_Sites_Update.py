from django.core.management import BaseCommand
from locations.models import HeritageSite
from urllib.parse import unquote


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        for entry in HeritageSite.objects.all():
            try:
                if entry.wikislug:
                    entry.wikislug = unquote(entry.wikislug)
                    entry.save()
            except Exception as e:
                print(f"Could not decode the string {entry.wikislug}: {e}")
                continue
