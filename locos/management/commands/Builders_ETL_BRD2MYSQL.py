# Extracts BR Builders from TPAM website saved html page and loads into Oracle

import requests, csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (8.0.22)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

webpage = os.path.join(DATAIO_DIR, "List_of_Builder.html")

try:
    #res.raise_for_status()
    #page = requests.get(webpage).text
    df = pd.read_html(webpage, flavor="bs4")[1]
    #df = pd.read_html(webpage, flavor="bs4", na_values=['none'])[1]
    df_clean = df.rename(columns={
                       df.columns[0]:"builder_code",
                       df.columns[1]:"builder_name",
                       df.columns[2]:"location",
                       df.columns[3]:"date_opened",
                       df.columns[4]:"date_closed",
                       df.columns[5]:"type",
                       df.columns[6]:"steam",
                       df.columns[7]:"diesel",
                       df.columns[8]:"electric",
                       df.columns[9]:"map",
                       df.columns[10]:"web"})
    #df_clean['date_opened'] = pd.to_datetime(df_clean['date_opened'])
    #df_clean = df_clean.drop([df.columns[2],df.columns[3]], axis=1) #To drop columns
    #df_clean = df_clean.drop([0, 27, 70, 76]) #To drop rows
    df_clean = df_clean.where(df_clean.notnull(), "")
    #df_clean['steam'] = df_clean['steam'].astype(int, errors='ignore')
    df_clean.to_csv(os.path.join(DATAIO_DIR, "Builder.csv"), index=False)

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

        drop_table_query = "DROP TABLE locos_builder"
        with connection.cursor() as cursor:
          cursor.execute(drop_table_query)

        create_builder_query = """
        CREATE TABLE locos_builder(
            builder_id INT AUTO_INCREMENT PRIMARY KEY,
            builder_code CHAR(3),
            builder_name VARCHAR(50),
            location VARCHAR(200),
            date_opened VARCHAR(10),
            date_closed VARCHAR(10),
            type VARCHAR(77),
            steam VARCHAR(10),
            diesel VARCHAR(10),
            electric VARCHAR(10),
            map VARCHAR(200),
            web VARCHAR(200)
        )"""
        with connection.cursor() as cursor:
          cursor.execute(create_builder_query)
          connection.commit()

      ### INSERT builder

        # creating column list for insertion
        cols = "`,`".join([str(i) for i in df_clean.columns.tolist()])

        # Insert DataFrame records one by one.
        for i,row in df_clean.iterrows():
            sql = "INSERT INTO `locos_builder` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"

            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(row))
                connection.commit()

        sql = "SELECT * FROM `locos_builder`"
        with connection.cursor() as cursor:        
          cursor.execute(sql)
          result = cursor.fetchall()
          for i in result:
              print(i)
                                
except Error as e:
    print(e)

finally:
    connection.close()