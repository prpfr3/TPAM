from django.core.management import BaseCommand
from locations.models import Location, LocationCategory


class Command(BaseCommand):
    # Show this when the user types help
    help = "Once off utility to create location categories from the type field, after which the type field will be deleted from the model"

    def handle(self, *args, **options):
        import os

        queryset = Location.objects.all()

        for entry in queryset:
            try:
                if entry.type == "Closed Station":
                    category_fk = LocationCategory.objects.get(
                        category=entry.type,
                    )
                    entry.categories.add(category_fk)
                    entry.save()
                elif entry.type == "Current Station":
                    category_fk = LocationCategory.objects.get(
                        category=entry.type,
                    )
                    entry.categories.add(category_fk)
                    entry.save()
                elif entry.type == "Junction":
                    category_fk = LocationCategory.objects.get(
                        category=entry.type,
                    )
                    entry.categories.add(category_fk)
                    entry.save()
            except Exception as e:
                print(f"Could not save location due to error: {e}")
                continue
