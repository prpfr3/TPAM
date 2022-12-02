# Extracts BR Builders from TPAM website saved html page and loads into Oracle

import os
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
webpage = os.path.join(DATAIO_DIR, "BRD List_of_Depots.html")
OUTPUTFILE = "Depots_BRD_Extract"

df = pd.read_html(webpage, flavor="bs4")[1]

df = df.drop([df.columns[9],df.columns[10]], axis=1) 
df = df.rename(columns={
                    df.columns[0]:"depot",
                    df.columns[1]:"codes",
                    df.columns[2]:"code_dates",
                    df.columns[3]:"date_opened",
                    df.columns[4]:"date_closed_to_steam",
                    df.columns[5]:"date_closed",
                    df.columns[6]:"pre_grouping_company",
                    df.columns[7]:"grouping_company",
                    df.columns[8]:"BR_region"})

#df_clean = df_clean.drop([0, 27, 70, 76]) #To drop rows
print(df.info())
df_clean = df.where(df.notnull(), "")
#df_clean['steam'] = df_clean['steam'].astype(int, errors='ignore')
try:
    df_clean.to_csv(os.path.join(DATAIO_DIR, OUTPUTFILE), index=False)
except Exception as exc:
    print(f'Unable to open the file: {exc}')