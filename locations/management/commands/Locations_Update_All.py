from django.core.management import BaseCommand
from locations.models import Location
from urllib.parse import unquote


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        queryset = Location.objects.all()

        # for entry in queryset:
        #     try:
        #         if entry.name is None and entry.wikiname is not None:
        #             entry.name = entry.wikiname
        #             print(f"Location name set to {entry.wikiname}")
        #             entry.save()
        #     except Exception as e:
        #         print(f"Could not save location due to error: {e}")
        #         continue

        for entry in queryset:
            try:
                if entry.wikislug:
                    entry.wikislug = unquote(entry.wikislug)
                    entry.save()
            except Exception as e:
                print(f"Could not decode the string {entry.wikislug}: {e}")
                continue
