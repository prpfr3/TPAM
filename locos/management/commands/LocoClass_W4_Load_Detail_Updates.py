from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data updates from a csv file into a LocoClass model"

    def handle(self, *args, **options):
        print("Creating Loco class details")
        with open(os.path.join(DATAIO_DIR, 'Class_All_W3_Cleansed_Detail_Delta.csv'), encoding="utf-8") as file:   
             for row in DictReader(file):

                # First check the Class Exists; held in the first column of the spreadsheet
                try:
                    c = LocoClass.objects.get(wikipedia_name=row['\ufeffClass'])
                except ObjectDoesNotExist:
                    print(row['\ufeffClass'], ' does not exist in the database')
                except Exception as e:
                    print(row['\ufeffClass'], e)
                else:
                    if row['Field'] == "Wikipedia Name": c.wikipedia_name = row['Value']
                    elif row['Field'] == "Axle load": c.axle_load = row['Value']
                    elif row['Field'] == "Adhesive weight": c.adhesive_weight = row['Value']
                    elif row['Field'] == "Boiler": c.boiler = row['Value']
                    elif row['Field'] == "Boiler pressure": c.boiler_pressure = row['Value']
                    elif row['Field'] == "Boiler:Diameter": c.boiler_diameter = row['Value']
                    elif row['Field'] == "Boiler:Model": c.boiler_model = row['Value']
                    elif row['Field'] == "Boiler:Pitch": c.boiler_pitch = row['Value']
                    elif row['Field'] == "Boiler:Tube plates": c.boiler_tube_plates = row['Value']
                    elif row['Field'] == "Build Date": c.build_date = row['Value']
                    elif row['Field'] == "Coupled diameter": c.coupled_diameter = row['Value']
                    elif row['Field'] == "Cylinder size": c.cylinder_size = row['Value']
                    elif row['Field'] == "Cylinders": c.cylinders = row['Value']
                    elif row['Field'] == "Disposition": c.disposition = row['Value']
                    elif row['Field'] == "Driver dia.": c.driver_diameter = row['Value']
                    elif row['Field'] == "Factor of adh.": c.adhesion_factor = row['Value']
                    elif row['Field'] == "Firebox:Firegrate area": c.firegrate_area = row['Value']
                    elif row['Field'] == "Firegrate area": c.firegrate_area = row['Value']
                    elif row['Field'] == "Fuel capacity": c.fuel_capacity = row['Value']
                    elif row['Field'] == "Fuel type": c.fuel_type = row['Value']
                    elif row['Field'] == "Gauge": c.gauge = row['Value']
                    elif row['Field'] == "Heating surface": c.heating_surface = row['Value']
                    elif row['Field'] == "Heating surface:Firebox": c.heating_surface_firebox = row['Value'].wikipedia
                    elif row['Field'] == "Heating surface:Tubes": c.heating_surface_tubes = row['Value']
                    elif row['Field'] == "Heating surface:Flues": c.heating_surface_flues = row['Value']
                    elif row['Field'] == "Heating surface:Tubes and flues": c.heating_surface_tubes_flues = row['Value']
                    elif row['Field'] == "Height": c.height = row['Value']
                    elif row['Field'] == "High-pressure cylinder": c.high_pressure_cylinder = row['Value']
                    elif row['Field'] == "Leading dia:": c.leading_diameter = row['Value']
                    elif row['Field'] == "Length:": c.length = row['Value']
                    elif row['Field'] == "Length:Over beams": c.length_over_beams = row['Value']
                    elif row['Field'] == "Loco brake": c.loco_brake = row['Value']
                    elif row['Field'] == "Loco weight": c.loco_weight = row['Value']
                    elif row['Field'] == "Low-pressure cylinder": c.low_pressure_cylinder = row['Value']
                    elif row['Field'] == "Maximum speed": c.maximum_speed = row['Value']
                    elif row['Field'] == "Minimum curve": c.minimum_curve = row['Value']
                    elif row['Field'] == "Nicknames": c.nicknames = row['Value']
                    elif row['Field'] == "Number in class": c.number_in_class = row['Value']
                    elif row['Field'] == "Number rebuilt": c.number_rebuilt = row['Value']
                    elif row['Field'] == "Numbers": c.numbers = row['Value']
                    elif row['Field'] == "Official name": c.official_name = row['Value']
                    elif row['Field'] == "Order number": c.order_number = row['Value']
                    elif row['Field'] == "Power class": c.power_class = row['Value']
                    elif row['Field'] == "Power type": c.power_type = row['Value']
                    elif row['Field'] == "Rebuild date": c.rebuild_date = row['Value']
                    elif row['Field'] == "Rebuilder": c.rebuilder = row['Value']
                    elif row['Field'] == "Retired": c.retired = row['Value']
                    elif row['Field'] == "Serial number": c.serial_number = row['Value']
                    elif row['Field'] == "Superheater": c.superheater_type = row['Value']
                    elif row['Field'] == "Superheater:Type": c.superheater_type = row['Value']
                    elif row['Field'] == "Tender cap.": c.tender_capacity = row['Value']
                    elif row['Field'] == "Tender type": c.tender_type = row['Value']
                    elif row['Field'] == "Tender weight": c.tender_weight = row['Value']
                    elif row['Field'] == "Total weight": c.total_weight = row['Value']
                    elif row['Field'] == "Tractive effort": c.tractive_effort = row['Value']
                    elif row['Field'] == "Trailing dia.": c.trailing_diameter = row['Value']
                    elif row['Field'] == "Train brakes": c.train_brakes = row['Value']
                    elif row['Field'] == "Train Heating": c.train_heating = row['Value']
                    elif row['Field'] == "UIC": c.uic = row['Value']
                    elif row['Field'] == "Valve gear": c.valve_gear = row['Value']
                    elif row['Field'] == "Valve_type": c.valve_type = row['Value']
                    elif row['Field'] == "Water cap": c.water_capacity = row['Value']
                    elif row['Field'] == "Wheelbase": c.wheelbase = row['Value']
                    elif row['Field'] == "Wheelbase:Engine": c.wheelbase_engine = row['Value']
                    elif row['Field'] == "Wheelbase:Tender": c.wheelbase_tender = row['Value']
                    elif row['Field'] == "Whyte": c.whyte = row['Value']
                    elif row['Field'] == "Width": c.width = row['Value']
                    elif row['Field'] == "Withdrawn": c.withdrawn = row['Value']

                try:    
                    c.save()
                    print('SAVED: ', row['\ufeffClass'], row['Field'], '=', row['Value'])
                except Exception as e: 
                    print('ERROR: ', row['\ufeffClass'], row['Field'], '=', row['Value'], '\n', e, 'LENGTH IS:- ', len(row['Value']))