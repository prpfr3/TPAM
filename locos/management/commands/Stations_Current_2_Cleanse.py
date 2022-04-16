
# A fuzzy analysis of names has been used to determine which Naptan records to map to which Wikipedia records
# This improved on a straight join based on station names and minimal cleansing of those names
# However, CRSCode is in the Wikipedia file and could potentially improve on even the fuzzy analysis

import os
import pandas as pd

def dataframe_info(dataframe):
    print("\n",f"\n{dataframe.info()=}\n")
    print("\n",f"\n{dataframe.head()=}\n")
    print("\n",f"\n{dataframe.shape=}\n")
    # print("\n",f"\n{dataframe.crs=}\n")
    # print("\n",f"\n{dataframe.total_bounds=}\n")

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
Wikipedia_file = os.path.join(DATAIO_DIR, 'Locations_Extract_Wikipedia_Stations.csv')
Naptan_file = os.path.join(DATAIO_DIR, 'NaPTANRailReferences.csv')

df_wikipedia = pd.read_csv(Wikipedia_file, header=0, encoding='utf-8')
df_naptan = pd.read_csv(Naptan_file, header=0, encoding='utf-8')

df_naptan['StationNameClean'] = df_naptan['StationName']
df_naptan['StationNameClean'].replace(' Railway Station','', inplace=True, regex=True)
df_naptan['StationNameClean'].replace(' Rail Station','', inplace=True, regex=True)
df_naptan['StationNameClean'].replace('Metrocentre','Metro Centre (Gateshead)', inplace=True, regex=True)

# LET OP ! Fuzzy matching uses 'Name' rather than 'NameSlugClean' so following redundant at the moment
df_wikipedia['NameSlugClean'] = df_wikipedia['NameSlug']
df_wikipedia['NameSlugClean'].replace('/wiki/','', inplace=True, regex=True)
df_wikipedia['NameSlugClean'].replace('_',' ', inplace=True, regex=True)

df_wikipedia['Name'].replace('Abbey Wood','Abbey Wood (London)', inplace=True, regex=True)

# Not Used, Other than a Useful Reference to see how a non-fuzzy match performs
df_wikipedia['Code1'].replace(' Timetable ','', inplace=True, regex=True)
df_joined = df_wikipedia.set_index('Code1').join(df_naptan.set_index('CrsCode'))
output_file = os.path.join(DATAIO_DIR, 'Locations_Joined_onCrsCode.csv')
df_joined.index.name='Name'
df_joined.to_csv(output_file)

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
            x=process.extractOne(string_to_be_matched,possible_matches,scorer=fuzz.token_set_ratio)
            names_array.append(x[0])
            ratio_array.append(x[1])
    return names_array,ratio_array

wikipedia_names =  df_wikipedia["Name"].fillna("######").tolist()
naptan_names = df_naptan["StationNameClean"].fillna("######").tolist()
name_match, ratio_match = checker(wikipedia_names, naptan_names)

df_mapping = pd.DataFrame()
df_mapping["wikipedia_name"]=pd.Series(wikipedia_names)
df_mapping["naptan_bestguess"]=pd.Series(name_match)
df_mapping["estimated_accuracy"]=pd.Series(ratio_match)
output_file = os.path.join(DATAIO_DIR, 'Locations_Extract_Fuzzy_Analysis.csv')
df_mapping.to_csv(output_file)

df = df_wikipedia.set_index('Name').join(df_mapping.set_index('wikipedia_name'))
df.index.name='Name'
df.reset_index()
df = df.set_index('naptan_bestguess').join(df_naptan.set_index('StationNameClean'))
df.index.name='Name'
df.reset_index()
output_file = os.path.join(DATAIO_DIR, 'Locations_Extract_Joined.csv')
df.to_csv(output_file)

import shapely, folium, webbrowser
# COMMENTED OUT TO PREVENT VIRTUAL ENV INSTALL PROBLEMS
# import geopandas as gpd
# from shapely.geometry import Point
# gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Easting, df.Northing))
# gdf.crs = "epsg:27700"
# gdf.to_crs(epsg=4326, inplace=True)
# output_file = os.path.join(DATAIO_DIR, 'Locations_LoadFile.csv')
# df.to_csv(output_file)
# print(gdf.head())

# m2 = folium.Map([51.28, 00.16], zoom_start= 10, tiles='cartodbpositron')
# folium.GeoJson(data=gdf["geometry"]).add_to(m2)
# m2.save('temporary_map2.html')
# webbrowser.open('temporary_map2.html', new=2)