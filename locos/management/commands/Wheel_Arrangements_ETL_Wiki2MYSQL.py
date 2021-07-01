""" Extracts and Saves Wikipedia Wheel arrangements to csv using Pandas and then loads into Oracle

    Working correctly at 24/01/21 for MySQL and on 23/06/21 for PostGres. Significant changes needed for the PostGres sql string which does not expect table or fieldnames to be in quotes, whereas mysql does.

    Both an SQL load and ORM load are available below. However, as at 23/06/21 the SQL load expects the database fieldnames to be all lowercase as they are in the Django model definition, whereas the ORM load expects them to be capitalised. 

"""

import requests, csv
import pandas as pd
import configparser
import os
import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (e.g. 8.0.25)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
res = requests.get("https://en.wikipedia.org/wiki/Wheel_arrangement")
try:
    res.raise_for_status()
    page = requests.get("https://en.wikipedia.org/wiki/Wheel_arrangement").text
    df = pd.read_html(page, flavor="bs4", na_values=['none'])[2]
    df_clean = df.rename(columns={df.columns[0]:"UIC_system",
                       df.columns[1]:"Whyte_notation",
                       df.columns[2]:"American_name",
                       df.columns[3]:"Visual"})
    df_clean = df_clean.where(df_clean.notnull(), None)
    print(df_clean.head())
    df_clean.to_csv(os.path.join(DATAIO_DIR, "Wheel_arrangement.csv"), index=False)

except Exception as exc:
    print('Unable to get the file: %s' % (exc))

config = configparser.ConfigParser()
KEYS_DIR = os.path.join("D:\\MLDatasets", "API_Keys")
config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
db_pswd = config['MySQL']['p']

"""
try:
    with psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password=db_pswd,
        database="TPAM"
        ) as connection:

      #  drop_table_query = "DROP TABLE locos_wheelarrangement"
      #  with connection.cursor() as cursor:
      #    cursor.execute(drop_table_query)

      #  create_wheel_arrangement_query = "
      #  CREATE TABLE locos_wheelarrangement(
      #      wheelid SMALLINT,
      #      UIC_system VARCHAR(20),
      #      Whyte_notation VARCHAR(20),
      #      American_name VARCHAR(75),
      #      Visual VARCHAR(20),
      #      CONSTRAINT pk_wheel_arrangement PRIMARY KEY (wheelid) 
      #  )"
      #  with connection.cursor() as cursor:
      #    cursor.execute(create_wheel_arrangement_query)
      #    connection.commit()

      # ALTER statement added separately just as an example of how a key can be changed post creation
      #  alter_wheel_arrangement_query = "
      #  ALTER TABLE locos_wheelarrangement
      #      MODIFY wheelid SMALLINT UNSIGNED AUTO_INCREMENT
      #  "
      #  with connection.cursor() as cursor:
      #    cursor.execute(alter_wheel_arrangement_query)
      #    connection.commit()

      # INSERT wheel_arrangement

        # creating column list for insertion
        cols = ",".join([str(i) for i in df_clean.columns.tolist()])

        # Insert DataFrame records one by one.
        for i,row in df_clean.iterrows():
            sql = "INSERT INTO locos_wheelarrangement (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"

            print(f'{sql=}', '/n', f'{tuple(row)=}')
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(row))
                connection.commit()

        sql = "SELECT * FROM locos_wheelarrangement"
        with connection.cursor() as cursor:        
          cursor.execute(sql)
          result = cursor.fetchall()
          for i in result:
              print(i)

except Error as e:
    print(e)

finally:
    connection.close()
"""
from csv import DictReader
from django.core.management import BaseCommand
from locos.models import WheelArrangement

ALREADY_LOADED_ERROR_MESSAGE = "To reload the data from the CSV file,first either (a) delete and recreate the database table to reset keys to start at zero or (b) drop all the table records in which cases the keys will be initialised starting at the last unused value"

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the model"

    def handle(self, *args, **options):
        if WheelArrangement.objects.exists():
            print('The tables already contains data...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating Wheel Arrangements")
        import os
        DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
        for csv in [
          'Wheel_arrangement.csv',
          ]:
          for row in DictReader(open(os.path.join(DATAIO_DIR, csv), encoding='utf-8')):
              c = WheelArrangement()
              print(row)
              c.uic_system = row['UIC_system']
              c.whyte_notation = row['Whyte_notation']
              c.american_name = row['American_name']
              c.visual = row['Visual']
              c.save()