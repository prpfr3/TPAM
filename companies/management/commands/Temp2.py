# import os
# import urllib.parse
# from csv import DictReader

# from django.core.management import BaseCommand
# from companies.models import Company


# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Loads data from Manufacturer_Load_Final.csv into our Manufacturer model"

#     def handle(self, *args, **options):

#         # Update all instances where 'my_field' contains the string 'NULL'
#         Company.objects.filter(code="NULL").update(code=None)


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
            print(entry)
            try:
                old_entry_name = entry.name
                entry.name = urllib.parse.unquote(old_entry_name)
                if entry.name and entry.name != old_entry_name:
                    entry.save()
                    print(old_entry_name, entry.name)

            except Exception as e:
                print(f"Could not save instance due to error: {e}")
                continue

            try:
                old_entry_wikislug = entry.wikislug
                entry.wikislug = urllib.parse.unquote(old_entry_wikislug)
                if entry.wikislug and entry.wikislug != old_entry_wikislug:
                    entry.save()
                    print(old_entry_wikislug, entry.wikislug)

            except Exception as e:
                print(f"Could not save instance due to error: {e}")
                continue
