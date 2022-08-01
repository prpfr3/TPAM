"""
Loading of UK Administrative Areas

Dataset:-
https://data.gov.uk/dataset/278685e8-2991-444d-9134-2af48645216b/countries-december-2015-full-clipped-boundaries-in-great-britain

"""
import os
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd
import configparser

def shapefile_postgres_preprocessing(filename):
    
    # Read in the Shapefile and ensure it is in the 4326 CRS of OpenStreetMap
    shapefile = gpd.read_file(filename)
    shapefile_4326  = shapefile.to_crs(epsg=4326)
    #shapefile.set_index(shapefile.Name,inplace=True)

    print("\n",f"\n{filename=}")
    print("\n",f"\n{shapefile.head()=}\n")
    print("\n",f"\n{shapefile_4326.crs=}\n")
    print("\n",f"\n{shapefile_4326.total_bounds=}\n")
    print("\n",f"\n{shapefile_4326.info()=}\n")
    print("\n",f"\n{shapefile_4326.head()=}\n")
    print("\n",f"\n{shapefile_4326.shape=}\n")

    return(shapefile_4326)

config = configparser.ConfigParser()
KEYS_DIR = os.path.join("D:\\Data", "API_Keys")
config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
db_pswd = config['MySQL']['p']
#Assumes a PostGIS DB created in pgAdmin with the chosen db using "CREATE EXTENSION postgis"
engine = create_engine('postgresql://postgres:family@localhost/TPAM')

pd.set_option('display.max_columns', None)

os.chdir(os.path.join('D:\\Data\\UK_Admin_Boundaries'))
gpd_UK_admin_boundaries = shapefile_postgres_preprocessing("Counties_and_Unitary_Authorities__December_2019__Boundaries_UK_BFE.shp")
gpd_UK_admin_boundaries.to_postgis(name="UK_admin_boundaries", if_exists='append', index=False, con=engine)