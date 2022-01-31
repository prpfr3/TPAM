import os
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input_file = os.path.join(DATAIO_DIR, 'Class_Modern_W2_Scrape_Detail.csv')
output_file = os.path.join(DATAIO_DIR, 'Class_Modern_W3_Cleansed_Detail.csv')

df_wiki = pd.read_csv(input_file, names=range(50), header=None, encoding='utf-8')
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

indexNames = df_wiki[ (df_wiki[3] == 'Type and origin') | 
                    (df_wiki[3] == 'Performance figures') |
                    (df_wiki[3] == 'Specifications')   |      
                    (df_wiki[3] == 'Career')  |    
                    (df_wiki[2] == 'Type and origin') | 
                    (df_wiki[2] == 'Performance figures') |
                    (df_wiki[2] == 'Specifications')   |      
                    (df_wiki[2] == 'Career')     |  
                    (df_wiki[2] == 'Configuration:')        
                    ].index
df_wiki.drop(indexNames , inplace=True)

df_wiki.to_csv(output_file, index=False, encoding='utf-8')