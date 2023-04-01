"""
Adds some additional information onto the BRD Locomotives Extract
To Help Identify the Locomotive Class
"""

import os
import pandas as pd

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
input1 = os.path.join(DATAIO_DIR, "Locomotive_BRD.csv")
input2 = os.path.join(DATAIO_DIR, "Class_BRD_Steam_Cleansed.csv")
output = os.path.join(DATAIO_DIR, "Locomotive_BRD_Enhanced.csv")

df_input1 = pd.read_csv(os.path.join(input1), header=0, encoding='utf-8')
df_input2 = pd.read_csv(os.path.join(input2), header=0, encoding='utf-8')
df_output = pd.output(df_input1, df_input2, how="left", on="Class_a")
df_output = df_output.replace('Â','', regex=True)
df_output.drop(columns=['Type_a', 'Works Number_a', 'Wheels_a',
   'Build Date_a', 'Manufacturer_a', 'Code_a', 'First Depot_a', 'Withdrawn_a',
    'Designer_url', 'Wheel_url', 'Number Range', 'First', 'Last', '#', 'Number Range_url', 'Thumbnail', 'Thumbnail_img'], inplace=True)
df_output.to_csv(output, encoding='utf-8')
