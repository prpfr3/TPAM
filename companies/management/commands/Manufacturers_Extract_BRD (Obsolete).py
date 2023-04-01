"""
 Extracts British Locomotive Manufacturer data from BRD Website
"""

import pandas as pd
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen

url_or_file = "file" #set to 'url' or 'file'
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
output_file = os.path.join(DATAIO_DIR, 'Manufacturer_Extract_BRD.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

if url_or_file == "url":
    url = "https://www.brdatabase.info/sites.php?page=manufacturers&action=list"
    #https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testin
    try:
        res = requests.get(url)
        res.raise_for_status()
        res = res.text
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)
else:
    res = open(os.path.join(DATAIO_DIR, "Manufacturer_BRD.html"))

df = pd.read_html(res, flavor="bs4")[1]
df_clean = df.rename(columns={
                    df.columns[0]:"manufacturer_code",
                    df.columns[1]:"manufacturer_name",
                    df.columns[2]:"location",
                    df.columns[3]:"date_opened",
                    df.columns[4]:"date_closed",
                    df.columns[5]:"owner_type",
                    df.columns[6]:"no_steam_built",
                    df.columns[7]:"no_diesel_built",
                    df.columns[8]:"no_electric_built",
                    df.columns[9]:"map",
                    df.columns[10]:"web"})
"""
Some extra cleaning code
df_clean['date_opened'] = pd.to_datetime(df_clean['date_opened'])
df_clean = df_clean.drop([df.columns[2],df.columns[3]], axis=1) #To drop columns
df_clean = df_clean.drop([0, 27, 70, 76]) #To drop rows
df_clean['steam'] = df_clean['steam'].astype(int, errors='ignore')
"""
df_clean = df_clean.where(df_clean.notnull(), "")
df_clean.to_csv(output_file, index=False)