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
                if (
                    not lococlass.power_type
                    and lococlass.brdslug
                    and "type=D" in lococlass.brdslug
                ):
                    lococlass.power_type = "Diesel"
                    print("Diesel")
                if (
                    not lococlass.power_type
                    and lococlass.brdslug
                    and "type=S" in lococlass.brdslug
                ):
                    lococlass.power_type = "Steam"
                    print("Steam")
                if lococlass.brdslug:
                    brdslug_split = lococlass.brdslug.split("=")
                    lococlass.brdslug = brdslug_split[-1]
                    print(lococlass.brdslug)
                lococlass.save()
            except Exception as e:
                print(f"Could not save lococlass {lococlass.brdslug} due to error: {e}")
                continue
