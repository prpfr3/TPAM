from django.core.management import BaseCommand
from notes.models import Reference


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating full_reference with image name when former empty"

    def handle(self, *args, **options):
        import os

        queryset = Reference.objects.all()

        for entry in queryset:
            try:

                if len(entry.full_reference) < 1 and entry.image:
                    name = entry.image.url.replace("/media/", "")
                    entry.full_reference = str(name)
                    print(f"{entry.full_reference}")
                    entry.save()
            except Exception as e:
                print(f"Could not save reference due to error: {e}")
                continue
