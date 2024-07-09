# Reload of PersonRoles from a Postgres csv backup

import os

from csv import DictReader
from django.core.management import BaseCommand
from people.models import PersonRole


class Command(BaseCommand):
    # Show this when the user types help
    help = "Reload of PersonRoles from a Postgres csv backup"

    def handle(self, *args, **options):
        if PersonRole.objects.exists():
            print("PersonRoles already loaded...halting load.")
            exit

        # This form of statement top ensure correct treatement of unusual unicode characters
        with open(
            os.path.join("D:\\Data", "TPAM", "people_person_role_2023_06_19.csv"),
            encoding="utf-8",
        ) as file:
            for row in DictReader(file):
                pr = PersonRole()
                pr.person_id = row["person_id"]
                pr.role_id = row["role_id"]
                pr.save()
