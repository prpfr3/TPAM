from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into a LocoClass model"

    def handle(self, *args, **options):
        print("Creating Loco class details")
        import os

        with open(os.path.join(DATAIO_DIR, 'LocoClass_Detail_Cleansed_Wikipedia.csv'), encoding="utf-8") as file:   
            for row in DictReader(file):

                if row['Column2'] == "1":
                    try:
                        c = LocoClass.objects.get(grouping_class_slug=row['Column1'])
                    except ObjectDoesNotExist:
                        c = LocoClass()
                        c.grouping_class_slug = row['Column1']
                        c.grouping_class = row['Column3']
                        c.save()
                    except Exception as e:
                        print(row['Column1'], e)
                else:
                    if row['Column3'] == "Axle load": c.axle_load = row['Column4']
                    elif row['Column3'] == "Adhesive weight": c.adhesive_weight = row['Column4']
                    elif row['Column3'] == "Boiler": c.boiler = row['Column4']
                    elif row['Column3'] == "Boiler pressure": c.boiler_pressure = row['Column4']
                    elif row['Column3'] == "Boiler:Diameter": c.boiler_diameter = row['Column4']
                    elif row['Column3'] == "Boiler:Model": c.boiler_model = row['Column4']
                    elif row['Column3'] == "Boiler:Pitch": c.boiler_pitch = row['Column4']
                    elif row['Column3'] == "Boiler:Tube plates": c.boiler_tube_plates = row['Column4']
                    elif row['Column3'] == "Build date": c.build_date = row['Column4']
                    elif row['Column3'] == "Coupled dia.": c.coupled_diameter = row['Column4']
                    elif row['Column3'] == "Cylinder size": c.cylinder_size = row['Column4']
                    elif row['Column3'] == "Cylinders":

                        if row['Column4'] == 2: row['Column4'] = "Two"
                        elif row['Column4'] == 2: row['Column4'] = "Two"                  
                        elif row['Column4'] == '2, outside': row['Column4'] = "Two, outside"
                        elif row['Column4'] == '4, (2 outside, 2 inside)': row['Column4'] = "Four, Two outside, Two inside"
                        elif row['Column4'] == 4: row['Column4'] = "Four"
                        elif row['Column4'] == 'Two Inside': row['Column4'] = "Two, inside"
                        elif row['Column4'] == 'Two inside': row['Column4'] = "Two, inside"
                        c.cylinders = row['Column4']

                    elif row['Column3'] == "Disposition": c.disposition = row['Column4']
                    elif row['Column3'] == "Driver dia.": c.driver_diameter = row['Column4']
                    elif row['Column3'] == "Factor of adh.": c.adhesion_factor = row['Column4']
                    elif row['Column3'] == "Firebox:Firegrate area": c.firegrate_area = row['Column4']
                    elif row['Column3'] == "Firegrate area": c.firegrate_area = row['Column4']
                    elif row['Column3'] == "Fuel capacity": c.fuel_capacity = row['Column4']
                    elif row['Column3'] == "Fuel type": c.fuel_type = row['Column4']
                    elif row['Column3'] == "Gauge": c.gauge = row['Column4']
                    elif row['Column3'] == "Heating surface": c.heating_surface = row['Column4']
                    elif row['Column3'] == "Heating surface:Â â€¢Â Firebox": c.heating_surface_firebox = row['Column4']
                    elif row['Column3'] == "Heating surface:Â â€¢Â Tubes and flues": c.heating_surface_tubes_flues = row['Column4']
                    elif row['Column3'] == "Heating surface:Firebox": c.heating_surface_firebox = row['Column4']
                    elif row['Column3'] == "Heating surface:Tubes": c.heating_surface_tubes = row['Column4']
                    elif row['Column3'] == "Heating surface:Flues": c.heating_surface_flues = row['Column4']
                    elif row['Column3'] == "Heating surface:Tubes and flues": c.heating_surface_tubes_flues = row['Column4']
                    elif row['Column3'] == "Height": c.height = row['Column4']
                    elif row['Column3'] == "High-pressure cylinder": c.high_pressure_cylinder = row['Column4']
                    elif row['Column3'] == "Leading dia:": c.leading_diameter = row['Column4']
                    elif row['Column3'] == "Length:": c.length = row['Column4']
                    elif row['Column3'] == "Length:Over beams": c.length_over_beams = row['Column4']
                    elif row['Column3'] == "Loco brake": c.loco_brake = row['Column4']
                    elif row['Column3'] == "Loco weight": c.loco_weight = row['Column4']
                    elif row['Column3'] == "Low-pressure cylinder": c.low_pressure_cylinder = row['Column4']
                    elif row['Column3'] == "Maximum speed": c.maximum_speed = row['Column4']
                    elif row['Column3'] == "Minimum curve": c.minimum_curve = row['Column4']
                    elif row['Column3'] == "Nicknames": c.nicknames = row['Column4']
                    elif row['Column3'] == "Number in class": c.number_in_class = row['Column4']
                    elif row['Column3'] == "Number rebuilt": c.number_rebuilt = row['Column4']
                    elif row['Column3'] == "Numbers": c.numbers = row['Column4']
                    elif row['Column3'] == "Official name": c.official_name = row['Column4']
                    elif row['Column3'] == "Order number": c.order_number = row['Column4']
                    elif row['Column3'] == "Power class": c.power_class = row['Column4']
                    elif row['Column3'] == "Power type": c.power_type = row['Column4']
                    elif row['Column3'] == "Rebuild date": c.rebuild_date = row['Column4']
                    elif row['Column3'] == "Rebuilder": c.rebuilder = row['Column4']
                    elif row['Column3'] == "Retired": c.retired = row['Column4']
                    elif row['Column3'] == "Serial number": c.serial_number = row['Column4']
                    elif row['Column3'] == "Superheater": c.superheater_type = row['Column4']
                    elif row['Column3'] == "Superheater:Type": c.superheater_type = row['Column4']
                    elif row['Column3'] == "Tender cap.": c.tender_capacity = row['Column4']
                    elif row['Column3'] == "Tender type": c.tender_type = row['Column4']
                    elif row['Column3'] == "Tender weight": c.tender_weight = row['Column4']
                    elif row['Column3'] == "Total weight": c.total_weight = row['Column4']
                    elif row['Column3'] == "Tractive effort": c.tractive_effort = row['Column4']
                    elif row['Column3'] == "Trailing dia.": c.trailing_diameter = row['Column4']
                    elif row['Column3'] == "Train brakes": c.train_brakes = row['Column4']
                    elif row['Column3'] == "Train Heating": c.train_heating = row['Column4']
                    elif row['Column3'] == "UIC": c.uic = row['Column4']
                    elif row['Column3'] == "Valve gear": c.valve_gear = row['Column4']
                    elif row['Column3'] == "Valve_type": c.valve_type = row['Column4']
                    elif row['Column3'] == "Water cap": c.water_capacity = row['Column4']
                    elif row['Column3'] == "Wheelbase": c.wheelbase = row['Column4']
                    elif row['Column3'] == "Wheelbase:Engine": c.wheelbase_engine = row['Column4']
                    elif row['Column3'] == "Wheelbase:Tender": c.wheelbase_tender = row['Column4']
                    elif row['Column3'] == "Whyte": c.whyte = row['Column4']
                    elif row['Column3'] == "Width": c.width = row['Column4']
                    elif row['Column3'] == "Withdrawn": c.withdrawn = row['Column4']

                    try:    
                        c.save()
                        # print('SAVED: ', row['Column1'],'VALUE=', row['Column3'], '=', row['Column4'])
                    except Exception as e:
                        print('ERROR: ', row['Column1'],'VALUE=', row['Column3'], '=', row['Column4'], '\n', e, 'LENGTH IS:- ', len(row['Column4']))