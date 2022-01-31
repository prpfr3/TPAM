"""
 Extracts British Locomotive Builder list from RailUK
"""
import requests, csv, os, re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

url = "https://railuk.info/steam/builder_search.php"
url_or_file = "file" #set to 'url' or 'file'
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
output_file = os.path.join(DATAIO_DIR, 'Builder_Extract_RailUK.csv')
csvFile = open(output_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

if url_or_file == "url":
    #https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testin
    try:
        res = requests.get(url).text
        res.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)
else:
    res = open(os.path.join(DATAIO_DIR, "Builder_Extract_RailUK.html"))

df = pd.read_html(res, flavor="bs4")[0]
print(df.head())
print(df.info())
df_clean = df.rename(columns={
                    df.columns[0]:"builder_code",
                    df.columns[1]:"builder_name",
                    })
"""
Some extra cleaning code
df_clean['date_opened'] = pd.to_datetime(df_clean['date_opened'])
df_clean = df_clean.drop([df.columns[2],df.columns[3]], axis=1) #To drop columns
df_clean = df_clean.drop([0, 27, 70, 76]) #To drop rows
df_clean['steam'] = df_clean['steam'].astype(int, errors='ignore')
"""
df_clean = df_clean.where(df_clean.notnull(), "")
df_clean.to_csv(output_file, index=False)
print(df_clean.info())
print(df_clean.head())