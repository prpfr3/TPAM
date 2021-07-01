# Extracts and Saves Midland Locos from TPAM_DATAIO to csv using Pandas and then loads into Oracle
# Under development at 26/01/21

import requests, csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (8.0.22)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

webpage = os.path.join(DATAIO_DIR, "Midland_Locos.html")
try:
    df = pd.read_html(webpage, flavor="bs4")[1]
    df_clean = df.rename(columns={
                       df.columns[0]:"build_date",
                       df.columns[1]:"pre_grouping_class",
                       df.columns[2]:"class",
                       df.columns[3]:"number",
                       df.columns[4]:"wheel_arrangement",
                       df.columns[5]:"designer",
                       df.columns[6]:"manufacturer",
                       df.columns[7]:"order_number",
                       df.columns[8]:"works_number",
                       df.columns[9]:"withdrawn"})
    df_clean.fillna({'number':-1}, inplace=True)
    df_clean['number'] = df_clean['number'].astype('int64')
    df_clean = df_clean.where(df_clean.notnull(), "")
    print(df_clean.info())
    print(df_clean.head())
    df_clean.to_csv(os.path.join(DATAIO_DIR, "BRD_Midland_Locos.csv"), index=False)

except Exception as exc:
    print('Unable to get the file: %s' % (exc))

try:
    with connect(
        host="localhost",
        #user=input("Enter username: "),
        #password=getpass("Enter password: "),
        user="userid",
        password="Password_here",
        database="railways"
        ) as connection:

          #drop_table_query = "DROP TABLE locos_locomotive"
          #with connection.cursor() as cursor:
          #  cursor.execute(drop_table_query)

          #create_locomotive_query = """
          #CREATE TABLE locos_locomotive(
          #    id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
          #    build_date VARCHAR(10),
          #    pre_grouping_class VARCHAR(10),
          #    class VARCHAR(20),
          #    number SMALLINT,
          #    wheel_arrangement VARCHAR(10),
          #    designer VARCHAR(30),
          #    manufacturer VARCHAR(50),
          #    order_number VARCHAR(30),
          #    works_number VARCHAR(30),
          #    withdrawn VARCHAR(15)
          #    #CONSTRAINT fk_wheel_arrangement FOREIGN KEY (wheel_arrangement) REFERENCES wheel_arrangement (Whyte_notation) #Possible future foreign key
          #)"""

          #with connection.cursor() as cursor:
          #  cursor.execute(create_locomotive_query)
          #  connection.commit()

          # Insert DataFrame records one by one.
          for i,row in df_clean.iterrows():
              insert_table_query = """INSERT INTO locos_locomotive
                      (build_date, pre_grouping_class, class, number, wheel_arrangement, designer, manufacturer, order_number, works_number, withdrawn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

              with connection.cursor() as cursor:
                  cursor.execute(insert_table_query, tuple(row))
                  connection.commit()

          show_table_query = "DESCRIBE locos_locomotive"
          with connection.cursor() as cursor:
              cursor.execute(show_table_query)
              for row in cursor.fetchall():
                  print(row)

except Error as e:
    print(e)

finally:
    connection.close()
