import csv, os
from urllib.request import urlopen
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUT_FILES = [
    'Class_All_W2_Detail.csv',
    'Class_All_W2_Detail_Blue_Pullmans.csv'
]

output_file = os.path.join(DATAIO_DIR, 'Class_All_W3_Cleansed_Detail.csv')

df_wiki = pd.DataFrame()
 
for input_file in INPUT_FILES:
    csv = pd.read_csv(os.path.join(DATAIO_DIR, input_file), names=range(150), header=None, encoding='utf-8')
    df_wiki = df_wiki.append(csv)

indexNames = df_wiki[ (df_wiki[3] == 'Career')|
                    (df_wiki[3] == 'Performance figures')|
                    (df_wiki[3] == 'Specifications')|
                    (df_wiki[3] == 'Type and origin')|
                    (df_wiki[2] == 'Type and origin')|
                    (df_wiki[2] == 'Performance figures')|
                    (df_wiki[2] == 'Specifications')|   
                    (df_wiki[2] == 'Career')|
                    (df_wiki[2] == 'Configuration:')        
                    ].index

df_wiki.drop_duplicates(subset=[0,1,2,3,4], inplace=True)

df_wiki.replace(' • 1st coupled','Axle load:1st coupled', inplace=True, regex=True)
df_wiki.replace(' • 2nd coupled','Axle load:1st coupled', inplace=True, regex=True)
df_wiki.replace(' • 3rd coupled','Axle load:1st coupled', inplace=True, regex=True)
df_wiki.replace(' • AAR','Configuration:AAR', inplace=True, regex=True)
df_wiki.replace(' • Commonwealth','Configuration:Commonwealth', inplace=True, regex=True)
df_wiki.replace(' • Coupled','Axle load:Coupled', inplace=True, regex=True)
df_wiki.replace(' • Diameter','Boiler:Diameter', inplace=True, regex=True)
df_wiki.replace(' • Drivers','Wheelbase:Drivers', inplace=True, regex=True)
df_wiki.replace(' • Drivers','Wheelbase:Drivers', inplace=True, regex=True)
df_wiki.replace(' • Engine','Wheelbase:Engine', inplace=True, regex=True)
df_wiki.replace(' • Engine','Wheelbase:Engine', inplace=True, regex=True)
df_wiki.replace(' • Firegrate area','Firegrate area', inplace=True, regex=True)
df_wiki.replace(' • Firebox','Heating surface:Firebox', inplace=True, regex=True)
df_wiki.replace(' • Flues','Heating surface:Flues', inplace=True, regex=True)
df_wiki.replace(' • Heating area','Superheater:Heating area', inplace=True, regex=True)
df_wiki.replace(' • Large tubes','Boiler:Large tubes', inplace=True, regex=True)
df_wiki.replace(' • Leading','Axle load:Leading', inplace=True, regex=True)
df_wiki.replace(' • Model','Boiler:Model', inplace=True, regex=True)
df_wiki.replace(' • Over beams','Length:Over beams', inplace=True, regex=True)
df_wiki.replace(' • Over couplers','Length:Over couplers', inplace=True, regex=True)
df_wiki.replace(' • Pitch','Boiler:Pitch', inplace=True, regex=True)
df_wiki.replace(' • Small tubes','Boiler:Small tubes', inplace=True, regex=True)
df_wiki.replace(' • Tender axle','Axle load:Tender axle', inplace=True, regex=True)
df_wiki.replace(' • Tender','Wheelbase:Tender', inplace=True, regex=True)
df_wiki.replace(' • Tender','Wheelbase:Tender', inplace=True, regex=True)
df_wiki.replace(' • Trailing','Axle load:Trailing', inplace=True, regex=True)
df_wiki.replace(' • Tube plates','Boiler:Tube plates', inplace=True, regex=True)
df_wiki.replace(' • Tubes','Heating surface:Tubes', inplace=True, regex=True)
df_wiki.replace(' • Tubes and flues','Heating surface:Tubes and flues', inplace=True, regex=True)
df_wiki.replace(' • Type','Superheater:Type', inplace=True, regex=True)
df_wiki.replace(' • UIC','UIC:AAR', inplace=True, regex=True)
df_wiki.replace(' • Whyte','Whyte:AAR', inplace=True, regex=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in) standard gauge','Standard', inplace=True, regex=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in)','Standard', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge and','Standard;', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge, ','Standard;', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge','Standard', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge5','Standard;5', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gaugeand ','Standard;, ', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm)','Standard', inplace=True, regex=True)
df_wiki.replace('lbf/in2','psi', inplace=True, regex=True)
df_wiki.replace('GWR Number','GWR Standard Number', inplace=True, regex=True)
df_wiki.replace('Standard Number','GWR Standard No.', inplace=True, regex=True)
df_wiki.replace('GWR GWR Standard','GWR Standard', inplace=True, regex=True)
df_wiki.replace('availability','Availability', inplace=True, regex=True)
df_wiki.replace('Availability:','Availability', inplace=True, regex=True)
df_wiki.replace('Route Availability','RA', inplace=True, regex=True)
df_wiki.replace('LNER:RA', 'LNER/BR RA', inplace=True, regex=True)
df_wiki.replace('LNER:RA','RA', inplace=True, regex=True)
df_wiki.replace('GWR:','GWR', inplace=True, regex=True)
df_wiki.replace('Uncoloured','Unclassified', inplace=True, regex=True)
df_wiki.replace('Not classified','Unclassified', inplace=True, regex=True)
df_wiki.replace('GWR: Uncoloured','GWR: Unclassified', inplace=True, regex=True)
df_wiki.replace('GWR: unclassed','GWR: Unclassified', inplace=True, regex=True)
df_wiki.replace('GWR unclassed','GWR: Unclassified', inplace=True, regex=True)
df_wiki.replace('GWR Uncoloured','GWR: Unclassified', inplace=True, regex=True)
df_wiki.replace('Uncoloured','GWR: Unclassified', inplace=True, regex=True)
df_wiki.replace('Unclassified','GWR: Unclassified', inplace=True)
df_wiki.replace('LNER diagram','LNER Diagram', inplace=True)

df_wiki.replace('GWR Red','GWR: Red', inplace=True, regex=True)
df_wiki.replace('GWR Double Red','GWR: Double Red', inplace=True, regex=True)
df_wiki.replace('GWR Yellow','GWR: Yellow', inplace=True, regex=True)
df_wiki.replace('BR (WR)','; BR (WR)', inplace=True, regex=True)

df_wiki.replace('131: 1913137: 1914–15','131:1913; 137:1914–15', inplace=True)
df_wiki.replace('1874 (No. 42)1914 (No. 16)','1874 (No. 42); 1914 (No. 16)', inplace=True)

df_wiki.replace(' psi','psi', inplace=True, regex=True)
df_wiki.replace('psi',' psi', inplace=True, regex=True)
df_wiki.replace('  psi',' psi', inplace=True, regex=True)
df_wiki.replace('lb/in2',' psi', inplace=True, regex=True)
df_wiki.replace('all scrapped','All scrapped', inplace=True, regex=True)
df_wiki.replace('coal','Coal', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge and7 ft 1⁄4 in (2,140 mm)','Standard and Broad', inplace=True, regex=True)
df_wiki.replace('7 ft 1⁄4 in (2,140 mm)','Broad', inplace=True, regex=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in)','Standard', inplace=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm)','Standard', inplace=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge','Standard', inplace=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in) standard gauge','Standard', inplace=True, regex=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in)','Standard', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge and','Standard;', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge, ','Standard;', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge','Standard', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge5','Standard;5', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gaugeand ','Standard;, ', inplace=True, regex=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm)','Standard', inplace=True, regex=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in)','Standard', inplace=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm)','Standard', inplace=True)
df_wiki.replace('4 ft 8+1⁄2 in (1,435 mm) standard gauge','Standard', inplace=True)
df_wiki.replace('1,435 mm (4 ft 8+1⁄2 in) standard gauge','Standard', inplace=True)
df_wiki.replace('1 ft 11+3⁄4 in (603 mm),  VoR only4 ft 8+1⁄2 in (1,435 mm) standard gauge','1ft 11+3⁄4 in (603 mm),  VoR only Standard', inplace=True)

df_wiki.replace(' bhp ',' hp ', inplace=True, regex=True)
df_wiki.replace('metric horsepower','hp', inplace=True, regex=True)
df_wiki.replace('horsepower','hp', inplace=True, regex=True)
df_wiki.replace('Engine: 350 hp','hp', inplace=True, regex=True)
df_wiki.replace('Engine:  350 hp','hp', inplace=True, regex=True)

df_wiki.replace('square feet','sq ft', inplace=True, regex=True)
# df_wiki.replace('LT','long tons', inplace=True, regex=True) # Commented out as impacts LT&SR as well as Long Tons
df_wiki.replace(' tons','tons', inplace=True, regex=True)
df_wiki.replace('tons',' tons', inplace=True, regex=True)
df_wiki.replace('Mph','mph', inplace=True, regex=True)
df_wiki.replace('  mph','mph', inplace=True, regex=True)
df_wiki.replace(' mph','mph', inplace=True, regex=True)
df_wiki.replace('mph',' mph', inplace=True, regex=True)
df_wiki.replace('Lots ','Lots:', inplace=True, regex=True)
df_wiki.replace('Lot ','Lot:', inplace=True, regex=True)
df_wiki.replace('Unclassed','Unclassified', inplace=True, regex=True)

df_wiki.replace(' – ', '–', inplace=True)
df_wiki.replace('–','-', inplace=True, regex=True)
df_wiki.replace('49: 2903: 5','49:2,903:5', inplace=True, regex=True)
df_wiki.replace('131: 6137: 6','131:6,137:6', inplace=True, regex=True)
df_wiki.replace('Slideor','Slide or', inplace=True, regex=True)
df_wiki.replace('Slide valve','Slide', inplace=True, regex=True)
df_wiki.replace('Slide valves','Slide', inplace=True, regex=True)
df_wiki.replace('slide valves','Slide', inplace=True, regex=True)
df_wiki.replace('Piston valves','Piston', inplace=True, regex=True)
df_wiki.replace('piston valves','piston', inplace=True, regex=True)
df_wiki.replace('piston','Piston', inplace=True, regex=True)
df_wiki.replace("Walschaerts'","Walschaerts", inplace=True, regex=True)
df_wiki.replace("Stephenson's","Stephenson", inplace=True, regex=True)
df_wiki.replace("Joy valve gear","Joy", inplace=True, regex=True)
df_wiki.replace("orWalschaerts","or Walschaerts", inplace=True, regex=True)
df_wiki.replace("Joy (Slide)","Joy", inplace=True, regex=True)
df_wiki.replace("Allan (straight link)","Allan", inplace=True, regex=True)
df_wiki.replace("Allan straight link","Allan", inplace=True, regex=True)

df_wiki.replace('inches','in', inplace=True, regex=True)
df_wiki.replace('-inch',' in', inplace=True, regex=True)
df_wiki.replace('10 in ','10 in', inplace=True, regex=True)
df_wiki.replace('8 in ','8 in', inplace=True, regex=True)
df_wiki.replace('→ ',';') 
df_wiki.replace(' » ',';') 
df_wiki.replace('→ ',';') 
df_wiki.replace(' →',';') 
df_wiki.replace(' » ',';') 
df_wiki.replace('Great Western Railway','GWR', inplace=True, regex=True)
df_wiki.replace('North British Railway','NBR', inplace=True, regex=True)
df_wiki.replace('British Railways','B.R.', inplace=True, regex=True)
df_wiki.replace('British Rail','B.R.', inplace=True, regex=True)
df_wiki.replace('London, Midland and Scottish Railway','LMSR', inplace=True, regex=True)
df_wiki.replace('London & NER','LNER', inplace=True, regex=True)
df_wiki.replace('London NER','LNER', inplace=True, regex=True)
df_wiki.replace('London and North Eastern Railway','LNER', inplace=True, regex=True)
df_wiki.replace('Southern Railway','SR', inplace=True, regex=True)
df_wiki.replace('North Eastern Railway','NER', inplace=True, regex=True)
df_wiki.replace('Great Central Railway','GCR', inplace=True, regex=True)
df_wiki.replace('Great Northern Railway','GNR', inplace=True, regex=True)
df_wiki.replace('South Eastern and Chatham Railway','SECR', inplace=True, regex=True)
df_wiki.replace('South Eastern Railway','SER', inplace=True, regex=True)
df_wiki.replace('Southern Region of B.R.', 'B.R', inplace=True, regex=True)
df_wiki.replace('London, Chatham and Dover Railway','LC&DR', inplace=True, regex=True)
df_wiki.replace('London Brighton and South Coast Railway','LBSCR', inplace=True, regex=True)
df_wiki.replace('Lancashire & Yorkshire Railway','L&YR', inplace=True, regex=True)

df_wiki.replace(' • ',' ', inplace=True, regex=True)

df_wiki.replace('BR Swindon Works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('GWR Swindon Works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('British Railways, Swindon Works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('BR Swindon Works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('GWR/BR Swindon Works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('GWR Swindon','Swindon Works', inplace=True, regex=True)
df_wiki.replace('Swindon Works works','Swindon Works', inplace=True, regex=True)
df_wiki.replace('Swindon Works, GWR','Swindon Works', inplace=True, regex=True)
df_wiki.replace('loco:','Loco:', inplace=True, regex=True)
df_wiki.replace('imperial gallons','imp gal', inplace=True, regex=True)
df_wiki.replace('gallons','imp gal', inplace=True, regex=True)

df_wiki.replace(' • 1 hour','Power output:1 hour', inplace=True, regex=True)
df_wiki.replace(' • Continuous','Power output:Continuous', inplace=True, regex=True)
df_wiki.replace(' • Body','Length:Body', inplace=True, regex=True)
df_wiki.replace(' • AAR','Configuration:AAR', inplace=True, regex=True)
df_wiki.replace(' • Body height','Height:Body', inplace=True, regex=True)
df_wiki.replace(' • Bogie','Bogie', inplace=True, regex=True)
df_wiki.replace(' • Commonwealth','Configuration:Commonwealth', inplace=True, regex=True)
df_wiki.replace(' • Over beams','Length:Over Beams', inplace=True, regex=True)
df_wiki.replace(' • Pantograph','Height:Pantograph', inplace=True, regex=True)
df_wiki.replace(' • Rating 1 hour','Power output:1 hour', inplace=True, regex=True)
df_wiki.replace(' • Starting','Power output:Starting', inplace=True, regex=True)
df_wiki.replace(' • UIC','UIC:AAR', inplace=True, regex=True)
df_wiki.replace(' • Whyte','Whyte:AAR', inplace=True, regex=True)
df_wiki.replace('Engine RPM: • Maximum RPM', "Engine Maximum RPM", inplace=True, regex=True)

df_wiki.replace('availability','Availability', inplace=True, regex=True)
df_wiki.replace('Availability:','Availability', inplace=True, regex=True)
df_wiki.replace('Route Availability','RA', inplace=True, regex=True)
df_wiki.replace('Route Availability:','RA', inplace=True, regex=True)
df_wiki.replace('GWR: ●Blue[5]','RA', inplace=True, regex=True)
df_wiki.replace('WR: Yellow[3]','RA', inplace=True, regex=True)

df_wiki.replace(' bhp ',' hp ', inplace=True, regex=True)

df_wiki.replace('Mph','mph', inplace=True, regex=True)
df_wiki.replace('  mph','mph', inplace=True, regex=True)
df_wiki.replace(' mph','mph', inplace=True, regex=True)
df_wiki.replace('mph',' mph', inplace=True, regex=True)
df_wiki.replace('inches','in', inplace=True, regex=True)
df_wiki.replace('-inch',' in', inplace=True, regex=True)

df_wiki.replace('1,500 V DC','1500 V DC', inplace=True, regex=True)
df_wiki.replace('catenary','Catenary', inplace=True, regex=True)
df_wiki.replace('Direct Current','DC', inplace=True, regex=True)

df_wiki.replace('DC generator','DC', inplace=True, regex=True)

df_wiki.replace('■ Orange Square','Orange Square', inplace=True, regex=True)
df_wiki.replace('◆ Red Diamond','Red Diamond', inplace=True, regex=True)
df_wiki.replace('◆ White Diamond','White Diamond', inplace=True, regex=True)
df_wiki.replace('● Red Circle','Red Circle', inplace=True, regex=True)
df_wiki.replace('★ Blue Star','Blue Star', inplace=True, regex=True)

df_wiki.replace('four stroke','Four-stroke', inplace=True, regex=True)
df_wiki.replace('two-stroke','Two-stroke', inplace=True, regex=True)
df_wiki.replace('diesel','Diesel', inplace=True, regex=True)
df_wiki.replace('Diesel Engine','Diesel', inplace=True, regex=True)
df_wiki.replace('gas turbine','Gas turbine', inplace=True, regex=True)

df_wiki.replace('British Railways','British Rail', inplace=True, regex=True)

df_wiki.replace(' • ',' ', inplace=True, regex=True)
df_wiki.replace(' – ', '–', inplace=True)
df_wiki.replace('–','-', inplace=True, regex=True)

df_wiki.to_csv(output_file, mode='a', index=False, encoding='utf-8', header=not os.path.exists(output_file))