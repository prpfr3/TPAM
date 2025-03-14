from django.core.management import BaseCommand
from companies.models import Company
import urllib.parse


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        queryset = Company.objects.all()

        for entry in queryset:
            try:
                if entry.name is None:
                    entry.name = entry.wikislug.replace("_", " ")
                if entry.wikislug:
                    entry.wikislug = urllib.parse.unquote(entry.wikislug)
                if entry.name:
                    entry.name = urllib.parse.unquote(entry.name)

                entry.save()
                # print(old_entry_wikislug, entry.wikislug)
            except Exception as e:
                print(f"Could not save company due to error: {e}")
                continue
