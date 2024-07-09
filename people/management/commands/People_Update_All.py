from django.core.management import BaseCommand
from people.models import Person
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Utility populating slugs (Model function provides the slug on save)"

    def handle(self, *args, **options):
        import os

        people = Person.objects.all()

        for person in people:
            try:
                person.save()
            except Exception as e:
                print(f"Could not save person due to error: {e}")
                continue
