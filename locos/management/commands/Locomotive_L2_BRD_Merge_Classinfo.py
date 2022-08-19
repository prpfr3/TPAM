"""
Adds some additional information onto the BRD Locomotives Extract
To Help Identify the Locomotive Class
"""

import os
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input1 = os.path.join(DATAIO_DIR, "Locomotive_BRD.csv")
input2 = os.path.join(DATAIO_DIR, "Class_BRD_Steam_Cleansed.csv")
merged = os.path.join(DATAIO_DIR, "Locomotive_BRD_Enhanced.csv")

df1 = pd.read_csv(os.path.join(input1), header=0, encoding='utf-8')
df2 = pd.read_csv(os.path.join(input2), header=0, encoding='utf-8')
df_merge = pd.merge(df1, df2, how="left", on="Class_a")
df_merge = df_merge.replace('Â','', regex=True)
df_merge.drop(columns=['Type_a', 'Works Number_a', 'Wheels_a',
   'Build Date_a', 'Builder_a', 'Code_a', 'First Depot_a', 'Withdrawn_a',
    'Designer_url', 'Wheel_url', 'Number Range', 'First', 'Last', '#', 'Number Range_url', 'Thumbnail', 'Thumbnail_img'], inplace=True)
df_merge.to_csv(merged, encoding='utf-8')
