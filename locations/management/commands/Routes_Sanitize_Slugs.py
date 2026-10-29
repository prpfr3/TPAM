from django.core.management import BaseCommand
from locations.models import Route


class Command(BaseCommand):
    help = "Re-saves all Route records to sanitize their slugs"

    def handle(self, *args, **options):
        routes = Route.objects.all()
        updated_count = 0

        for route in routes:
            if route.wikipedia_slug:
                route.save()
                updated_count += 1
                self.stdout.write(f"Updated route: {route.name} -> slug: {route.slug}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated_count} route(s).")
        )
