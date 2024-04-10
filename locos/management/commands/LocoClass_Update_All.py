from django.core.management import BaseCommand
from locos.models import LocoClass


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        lococlasses = LocoClass.objects.all()

        for lococlass in lococlasses:
            try:
                # lococlass.wikiname = lococlass.wikiname.replace("","")
                lococlass.save()
            except Exception as e:
                print(f"Could not save lococlass {lococlass} due to error: {e}")
                continue
