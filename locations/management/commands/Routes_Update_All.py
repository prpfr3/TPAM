from django.core.management import BaseCommand
from notes.models import Reference


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        queryset = Reference.objects.all()

        for entry in queryset:
            try:
                entry.save()
            except Exception as e:
                print(f"Could not save location due to error: {e}")
                continue
