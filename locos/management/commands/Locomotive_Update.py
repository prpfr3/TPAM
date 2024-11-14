from django.core.management import BaseCommand
from locos.models import Locomotive


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        locomotives = Locomotive.objects.all()

        for locomotive in locomotives:
            locomotive.brd_class_name_slug.replace("action=class&type", "").replace(
                "&id=", ""
            )
            try:

                locomotive.save()
            except Exception as e:
                print(
                    f"Could not save locomotive {locomotive.brd_slug} due to error: {e}"
                )
                continue
