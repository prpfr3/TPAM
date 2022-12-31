from django.core.management import BaseCommand
from locos.models import Location

class Command(BaseCommand):

    def handle(self, *args, **options):

        locations = Location.objects.all()

        for location in locations:
            l = location
            if l.wikislug:
                l.wikislug = l.wikislug.replace('/wiki/', '')
                l.save()
            # else:
            #     print(f'location {l} has no wikiname')