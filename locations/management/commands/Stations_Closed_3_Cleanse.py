
# A fuzzy analysis of names has been used to determine which Disused records to map to which Wikipedia records
# This fuzzy analysis improved on a straight join based on station names and minimal cleansing of those names

import os
import pandas as pd

def dataframe_info(dataframe):
    print("\n",f"\n{dataframe.info()=}\n")
    print("\n",f"\n{dataframe.head()=}\n")
    print("\n",f"\n{dataframe.shape=}\n")
    # print("\n",f"\n{dataframe.crs=}\n")
    # print("\n",f"\n{dataframe.total_bounds=}\n")

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
Wikipedia_file = os.path.join(DATAIO_DIR, 'Location_Extract_Wikipedia_Closed_Stations.csv')
Disused_file = os.path.join(DATAIO_DIR, 'Location_Extract_Disused_Stations.csv')

df_wikipedia = pd.read_csv(Wikipedia_file, header=0, encoding='utf-8')
df_disused = pd.read_csv(Disused_file, header=None, encoding='utf-8')

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def checker(strings_to_be_matched,possible_matches):
    names_array=[]
    ratio_array=[]    
    for string_to_be_matched in strings_to_be_matched:
        if string_to_be_matched in possible_matches:
           names_array.append(string_to_be_matched)
           ratio_array.append("100")
        else:   
            # x=process.extractOne(string_to_be_matched,possible_matches,scorer=fuzz.ratio)
            # x=process.extractOne(string_to_be_matched,possible_matches,scorer=fuzz.partial_ratio)
            x=process.extractOne(string_to_be_matched,possible_matches,scorer=fuzz.token_sort_ratio)
            # x=process.extractOne(string_to_be_matched,possible_matches,scorer=fuzz.token_set_ratio)
            names_array.append(x[0])
            ratio_array.append(x[1])
    return names_array,ratio_array

wikipedia_names =  df_wikipedia["Name"].fillna("######").tolist()
disused_names = df_disused[0].fillna("######").tolist()
# For each disused stations page try to match to a wikipedia page (there are less of the former than the latter)
name_match, ratio_match = checker(disused_names, wikipedia_names)

df_mapping = pd.DataFrame()
df_mapping["disused_names"]=pd.Series(disused_names)
df_mapping["wikipedia_names"]=pd.Series(name_match)
df_mapping["estimated_accuracy"]=pd.Series(ratio_match)
# Saves the file as a record of the analysis; it is not used further in other ETL programs
output_file = os.path.join(DATAIO_DIR, 'Location_Disused_Extract_Fuzzy_Analysis.csv')
df_mapping.to_csv(output_file)

# Only keep cross references to Wikipedia pages where there is more than a 90% chance of correctness
df_mapping = df_mapping.loc[pd.to_numeric(df_mapping['estimated_accuracy']) > 90]

df = df_wikipedia.set_index('Name').join(df_mapping.set_index('wikipedia_names'))
df.index.name='Name'
df.reset_index(inplace=True)

df = df.set_index('disused_names').join(df_disused.set_index(df_disused[0]))
df.index.name='disused_name'
df.reset_index(inplace=True)
output_file = os.path.join(DATAIO_DIR, 'Location_Disused_Extract_Joined.csv')
df.to_csv(output_file)