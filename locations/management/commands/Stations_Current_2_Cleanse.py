"""
The CRScode is used to match records from the Wikipedia extract with the Naptan file
Most of the records from Wikipedia without Naptan records are for Northern Ireland.
"""

import os
import pandas as pd
import geopandas as gpd
import folium, webbrowser
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")


def dataframe_info(dataframe):
    print("\n", f"\n{dataframe.info()=}\n")
    print("\n", f"\n{dataframe.head()=}\n")
    print("\n", f"\n{dataframe.shape=}\n")
    print("\n", f"\n{dataframe.crs=}\n")
    print("\n", f"\n{dataframe.total_bounds=}\n")


DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUT_WIKIPEDIA = os.path.join(
    DATAIO_DIR, f"Location_Stations_Current_Wikipedia_Extract_{current_date}.csv"
)
INPUT_NAPTAN = os.path.join(DATAIO_DIR, "NaPTANRailReferences.csv")
OUTPUT_LOADFILE = os.path.join(
    DATAIO_DIR, f"Location_Stations_Current_Loadfile_{current_date}.csv"
)

df_wikipedia = pd.read_csv(INPUT_WIKIPEDIA, header=0, encoding="utf-8-sig")
df_naptan = pd.read_csv(INPUT_NAPTAN, header=0, encoding="utf-8-sig")

df_naptan["StationNameClean"] = df_naptan["StationName"]
df_naptan["StationNameClean"].replace(" Railway Station", "", inplace=True, regex=True)
df_naptan["StationNameClean"].replace(" Rail Station", "", inplace=True, regex=True)
df_naptan["StationNameClean"].replace(
    "Metrocentre", "Metro Centre (Gateshead)", inplace=True, regex=True
)

df_wikipedia["NameSlug"].replace("/wiki/", "", inplace=True, regex=True)
df_wikipedia["NameSlugClean"] = df_wikipedia["NameSlug"]
df_wikipedia["NameSlugClean"].replace("_", " ", inplace=True, regex=True)
df_wikipedia["Name"].replace(
    "Abbey Wood", "Abbey Wood (London)", inplace=True, regex=True
)
df_wikipedia["Code1"].replace(" Timetable ", "", inplace=True, regex=True)
df_joined = df_wikipedia.set_index("Code1").join(df_naptan.set_index("CrsCode"))
df_joined.index.name = "CrsCode"
df_joined.drop(
    columns=[
        "StationNameLang",
        "GridType",
        "CreationDateTime",
        "ModificationDateTime",
        "RevisionNumber",
        "Modification",
    ],
    inplace=True,
)

gdf = gpd.GeoDataFrame(
    df_joined, geometry=gpd.points_from_xy(df_joined.Easting, df_joined.Northing)
)
gdf.crs = "epsg:27700"
gdf.to_crs(epsg=4326, inplace=True)
gdf.to_csv(OUTPUT_LOADFILE)

print(gdf.head())

m2 = folium.Map([51.28, 00.16], zoom_start=10, tiles="cartodbpositron")
folium.GeoJson(data=gdf["geometry"]).add_to(m2)
m2.save("temporary_map2.html")
webbrowser.open("temporary_map2.html", new=2)
