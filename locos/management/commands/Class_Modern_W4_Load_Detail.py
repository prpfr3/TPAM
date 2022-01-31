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

        with open(os.path.join(DATAIO_DIR, 'Class_Modern_W3_Cleansed_Detail.csv'), encoding="utf-8") as file:   
            for row in DictReader(file):

                if row['1'] == '1':
                    try:
                        c = LocoClass.objects.get(grouping_class_slug=row['0'])
                    except ObjectDoesNotExist:
                        c = LocoClass()
                        c.grouping_class_slug = row['0']
                        c.grouping_class = row['2']
                        c.save()
                    except Exception as e:
                        print(row['1'], e)
                else:
                    if row['2'] == "Adhesive weight": c.adhesive_weight = row['3'] #Steam
                    elif row['2'] == "Alternator": c.alternator = row['3'] #Modern
                    elif row['2'] == "Axle load": c.axle_load = row['3'] #Both
                    elif row['2'] == "Axle load class": c.axle_load_class = row['3'] #Both
                    elif row['2'] == "Bogie": c.bogie = row['3'] #Modern
                    elif row['2'] == "Bogies": c.bogies = row['3'] #Modern
                    elif row['2'] == "Boiler": c.boiler = row['3'] #Steam
                    elif row['2'] == "Boiler pressure": c.boiler_pressure = row['3'] #Steam
                    elif row['2'] == "Boiler:Diameter": c.boiler_diameter = row['3'] #Steam
                    elif row['2'] == "Boiler:Model": c.boiler_model = row['3'] #Steam
                    elif row['2'] == "Boiler:Pitch": c.boiler_pitch = row['3'] #Steam
                    elif row['2'] == "Boiler:Tube plates": c.boiler_tube_plates = row['3'] #Steam
                    elif row['2'] == "Brakeforce": c.brakeforce = row['3'] #Steam
                    elif row['2'] == "Build date": c.build_date = row['3'] #Both
                    elif row['2'] == "Coupled dia.": c.coupled_diameter = row['3'] #Steam
                    elif row['2'] == "Cylinder size": c.cylinder_size = row['3'] #Steam
                    elif row['2'] == "Cylinders": #Steam

                        if row['3'] == 2: row['3'] = "Two"
                        elif row['3'] == 2: row['3'] = "Two"                  
                        elif row['3'] == '2, outside': row['3'] = "Two, outside"
                        elif row['3'] == '4, (2 outside, 2 inside)': row['3'] = "Four, Two outside, Two inside"
                        elif row['3'] == 4: row['3'] = "Four"
                        elif row['3'] == 'Two Inside': row['3'] = "Two, inside"
                        elif row['3'] == 'Two inside': row['3'] = "Two, inside"
                        c.cylinders = row['3']

                    elif row['2'] == "Configuration:AAR": c.wheel_configuration_aar = row['3'] #Modern
                    elif row['2'] == "Configuration:AAR": c.wheel_configuration_aar = row['3'] #Modern  
                    elif row['2'] == "Coolant cap.": c.coolant_capacity = row['3'] #Modern  
                    elif row['2'] == "Couplers": c.couplers = row['3'] #Modern  
                    elif row['2'] == "Current pickup(s)": c.current_pickups = row['3'] #Electric
                    elif row['2'] == "Cylinder size": c.cylinder_size = row['3'] #Diesel & Steam
                    elif row['2'] == "Cylinders": c.cylinders = row['3'] #Diesel & Steam
                    elif row['2'] == "Displacement": c.displacement = row['3'] #Diesel         
                    elif row['2'] == "Disposition": c.disposition = row['3'] #Both
                    elif row['2'] == "Driver dia.": c.driver_diameter = row['3'] #Both
                    elif row['2'] == "Electric system/s": c.electric_systems = row['3'] #Electric       
                    elif row['2'] == "Engine Maximum RPM": c.engine_maximum_rpm = row['3'] #Diesel   
                    elif row['2'] == "Engine type": c.engine_type = row['3'] #Diesel             
                    elif row['2'] == "Factor of adh.": c.adhesion_factor = row['3'] #Steam
                    elif row['2'] == "Firebox:Firegrate area": c.firegrate_area = row['3'] #Steam
                    elif row['2'] == "Firegrate area": c.firegrate_area = row['3'] #Steam
                    elif row['2'] == "Fuel capacity": c.fuel_capacity = row['3'] #Both
                    elif row['2'] == "Fuel type": c.fuel_type = row['3'] #Both
                    elif row['2'] == "Gauge": c.gauge = row['3'] #Both
                    elif row['2'] == "Gear ratio": c.gear_ratio = row['3'] #Modern
                    elif row['2'] == "Generator": c.generator = row['3'] #Diesel
                    elif row['2'] == "Heating surface": c.heating_surface = row['3'] #Steam
                    elif row['2'] == "Heating surface:Â â€¢Â Firebox": c.heating_surface_firebox = row['3'] #Steam
                    elif row['2'] == "Heating surface:Â â€¢Â Tubes and flues": c.heating_surface_tubes_flues = row['3']#Steam
                    elif row['2'] == "Heating surface:Firebox": c.heating_surface_firebox = row['3']#Steam
                    elif row['2'] == "Heating surface:Tubes": c.heating_surface_tubes = row['3']#Steam
                    elif row['2'] == "Heating surface:Flues": c.heating_surface_flues = row['3']#Steam
                    elif row['2'] == "Heating surface:Tubes and flues": c.heating_surface_tubes_flues = row['3']#Steam
                    elif row['2'] == "Height": c.height = row['3']#Both
                    elif row['2'] == "Height:Pantograph": c.height_pantograph = row['3']#Electric
                    elif row['2'] == "High-pressure cylinder": c.high_pressure_cylinder = row['3']#Steam
                    elif row['2'] == "Leading dia:": c.leading_diameter = row['3']#Both
                    elif row['2'] == "Length:": c.length = row['3']#Both
                    elif row['2'] == "Length:Body height": c.length = row['3']#Electric
                    elif row['2'] == "Length:Over beams": c.length_over_beams = row['3']#Both
                    elif row['2'] == "Length:Over Beams": c.length_over_beams = row['3']#Both
                    elif row['2'] == "Loco brake": c.loco_brake = row['3']#Both
                    elif row['2'] == "Loco weight": c.loco_weight = row['3']#Both
                    elif row['2'] == "Low-pressure cylinder": c.low_pressure_cylinder = row['3']#Steam
                    elif row['2'] == "Lubricant cap.": c.lubricant_capacity = row['3']#Steam                
                    elif row['2'] == "Maximum speed": c.maximum_speed = row['3'] #Both
                    elif row['2'] == "Minimum curve": c.minimum_curve = row['3'] #Both
                    elif row['2'] == "Model": c.minimum_curve = row['3'] #Modern
                    elif row['2'] == "MU working": c.mu_working = row['3'] #Modern
                    elif row['2'] == "Nicknames": c.nicknames = row['3'] #Both
                    elif row['2'] == "Number in class": c.number_in_class = row['3']#Both
                    elif row['2'] == "Number rebuilt": c.number_rebuilt = row['3']#Both
                    elif row['2'] == "Numbers": c.numbers = row['3']#Both
                    elif row['2'] == "Official name": c.official_name = row['3']#Both
                    elif row['2'] == "Order number": c.order_number = row['3']#Both
                    elif row['2'] == "Pivot centres": c.pivot_centres = row['3']#Modern
                    elif row['2'] == "Power class": c.power_class = row['3']#Both
                    elif row['2'] == "Power output": c.power_output = row['3']#Modern
                    elif row['2'] == "Power output:1 hour": c.power_output_one_hour = row['3']#Modern
                    elif row['2'] == "Power output:Continuous": c.power_output_continuous = row['3']#Modern
                    elif row['2'] == "Power output:Starting": c.power_output_starting = row['3']#Modern
                    elif row['2'] == "Power type": c.power_type = row['3']#Both
                    elif row['2'] == "Prime mover": c.prime_mover = row['3']#Both
                    elif row['2'] == "Rebuild date": c.rebuild_date = row['3']#Both
                    elif row['2'] == "Rebuilder": c.rebuilder = row['3']#Both
                    elif row['2'] == "Retired": c.retired = row['3']#Both
                    elif row['2'] == "RPM range": c.rpm_range = row['3']#Modern
                    elif row['2'] == "Safety systems": c.safety_systems = row['3']#Modern
                    elif row['2'] == "Serial number": c.serial_number = row['3']#Both
                    elif row['2'] == "Superheater": c.superheater_type = row['3']#Steam
                    elif row['2'] == "Superheater:Type": c.superheater_type = row['3']#Steam
                    elif row['2'] == "Tender cap.": c.tender_capacity = row['3']#Steam
                    elif row['2'] == "Tender type": c.tender_type = row['3']#Steam
                    elif row['2'] == "Tender weight": c.tender_weight = row['3']#Both
                    elif row['2'] == "Total produced": c.number_in_class = row['3']#Modern
                    elif row['2'] == "Total weight": c.total_weight = row['3']#Steam
                    elif row['2'] == "Tractive motors": c.traction_motors = row['3']#Modern
                    elif row['2'] == "Tractive effort": c.tractive_effort = row['3']#Both
                    elif row['2'] == "Trailing dia.": c.trailing_diameter = row['3']#Both
                    elif row['2'] == "Train brakes": c.train_brakes = row['3']#Both
                    elif row['2'] == "Train Heating": c.train_heating = row['3']#Both
                    elif row['2'] == "Transmission": c.transmission = row['3']#Modern
                    elif row['2'] == "UIC": c.UIC = row['3']#Both
                    elif row['2'] == "UIC:AAR": c.UIC = row['3']#Both
                    elif row['2'] == "Valve gear": c.valve_gear = row['3']#Steam
                    elif row['2'] == "Valve_type": c.valve_type = row['3']#Steam
                    elif row['2'] == "Water cap": c.water_capacity = row['3']#Both
                    elif row['2'] == "Wheelbase": c.wheelbase = row['3']#Steam
                    elif row['2'] == "Wheelbase:Engine": c.wheelbase_engine = row['3']#Steam
                    elif row['2'] == "Wheelbase:Tender": c.wheelbase_tender = row['3']#Steam
                    elif row['2'] == "Wheel diameter": c.wheel_diameter = row['3']#Modern
                    elif row['2'] == "Whyte": c.whyte = row['3']#Both
                    elif row['2'] == "Whyte:AAR": c.whyte = row['3']#Both                
                    elif row['2'] == "Width": c.width = row['3']#Both
                    elif row['2'] == "Withdrawn": c.withdrawn = row['3']#Both

                    try:    
                        c.save()
                        # print('SAVED: ', row['1'],'VALUE=', row['2'], '=', row['3'])
                    except Exception as e:
                        print('ERROR: ', row['1'],'VALUE=', row['2'], '=', row['3'], '\n', e, 'LENGTH IS:- ', len(row['3']))