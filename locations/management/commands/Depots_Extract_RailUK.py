# Extracts a list of sheds from Wikipedia and loads into the TPAM database

import os
import requests
import pandas as pd
from csv import DictReader

from django.core.management import BaseCommand
from locations.models import Depot

OUTPUTFILE = 'Depots_RailUK_Extract.csv'
url = "https://www.railuk.info/steam/steamshed_search.php"

try:
    res = requests.get(url).content.decode('utf-8', 'ignore')
    df = pd.read_html(res, flavor="bs4")
except requests.exceptions.ConnectionError as err:
    # eg, no internet
    raise SystemExit(err) from err
except requests.exceptions.HTTPError as err:
    # eg, url, server and other errors
    raise SystemExit(err) from err
    
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
   

print(f'Total tables: {len(df)}') #Returns the number of tables
i = 0
appended_data = []
while i < len(df):
    df_table = pd.read_html(res, flavor="bs4")[i]
    # df_table = df_table.rename(columns={
    #                     df_table.columns[0]:"code",
    #                     df_table.columns[1]:"name",
    #                     df_table.columns[2]:"comments"})
    df_table = df_table.where(df_table.notnull(), "")
    i += 1
    appended_data.append(df_table)

df_output = pd.concat(appended_data)
try:
    df_output.to_csv(os.path.join(DATAIO_DIR, OUTPUTFILE), index=False)
except Exception as exc:
    print(f'Unable to open the file: {exc}')