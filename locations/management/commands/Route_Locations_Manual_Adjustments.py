from csv import DictReader
from django.core.management import BaseCommand
from locations.models import RouteLocation, Location, RouteMap
from django.core.exceptions import ObjectDoesNotExist
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    help = "Manual adjustments to routelocations"

    def handle(self, *args, **options):

        print("Applying Route Location Manual Changes")

        with open(os.path.join(DATAIO_DIR, "RouteLocations_Manual.csv"), encoding="utf-8-sig") as file:

            for row in DictReader(file):

                try:
                    rl, rl_created = RouteLocation.objects.get_or_create(
                        loc_no=row['loc_no'], )
                except Exception as e:
                    print(e)
                rl.loc_no = row['loc_no']
                if rl.label:
                    rl.label = row['label']
                elif row['name']:
                    rl.label = row['name']
                if row['linear_reference']:
                    rl.linear_reference = row['linear_reference']
                rl.note = row['note']

                try:
                    if row['wikislug']:
                        l = Location.objects.get(wikislug=row['wikislug'])
                        rl.location_fk = l
                except ObjectDoesNotExist:
                    missing = row['wikislug']
                    print(
                        f'{rl.loc_no}, wikislug {missing} not found in the Location table')
                else:
                    try:
                        if row['name']:
                            l = Location.objects.get(
                                name=row['name'])
                            rl.location_fk = l
                    except ObjectDoesNotExist:
                        missing = row['name']
                        print(
                            f'{rl.loc_no}, name {missing} not found in the Location table')

                try:
                    if row['routemap_name']:
                        rm, rm_created = RouteMap.objects.get_or_create(
                            name=row['routemap_name'])
                        rl.routemap = rm
                except Exception as e:
                    print(
                        f'{rl.loc_no}, {rl.label}, {e}')

                rl.save()

                if rl_created:
                    print(
                        f'New route location created for {row}/n')
                else:
                    print(
                        f'Existing route location adjusted for {row}/n')
