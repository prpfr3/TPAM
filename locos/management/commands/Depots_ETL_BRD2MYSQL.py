# Extracts BR Builders from TPAM website saved html page and loads into Oracle
# Still under development at 24/01/21

import requests, csv
import pandas as pd
import os
from bs4 import beautifulsoup4
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (8.0.23)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

webpage = os.path.join(DATAIO_DIR, "BRD List_of_Depots.html")


try:
    #res.raise_for_status()
    #page = requests.get(webpage).text
    df = pd.read_html(webpage, flavor="bs4")[1]
    #df = pd.read_html(webpage, flavor="bs4", na_values=['none'])[1]

    df_clean = df.rename(columns={
                       df.columns[0]:"depot",
                       df.columns[1]:"codes",
                       df.columns[2]:"code_dates",
                       df.columns[3]:"date_opened",
                       df.columns[4]:"date_closed_to_steam",
                       df.columns[5]:"date_closed",
                       df.columns[6]:"pre_grouping_company",
                       df.columns[7]:"grouping_company",
                       df.columns[8]:"BR_region",
                       df.columns[9]:"map",
                       df.columns[10]:"web"})
    #df_clean['date_opened'] = pd.to_datetime(df_clean['date_opened'])
    #df_clean = df_clean.drop([df.columns[2],df.columns[3]], axis=1) #To drop columns
    #df_clean = df_clean.drop([0, 27, 70, 76]) #To drop rows
    print(df_clean.info())
    df_clean = df_clean.where(df_clean.notnull(), "")
    #df_clean['steam'] = df_clean['steam'].astype(int, errors='ignore')
    df_clean.to_csv(os.path.join(DATAIO_DIR, "Depots.csv"), index=False)
    print(df_clean.info())
    print(df_clean.head())

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

        drop_table_query = "DROP TABLE depots"
        with connection.cursor() as cursor:
          cursor.execute(drop_table_query)

        create_depots_query = """
        CREATE TABLE depots(
            depot_id INT AUTO_INCREMENT PRIMARY KEY,
            depot VARCHAR(50),
            codes VARCHAR(100),
            code_dates VARCHAR(100),
            date_opened VARCHAR(20),
            date_closed_to_steam VARCHAR(20),
            date_closed VARCHAR(20),
            pre_grouping_company VARCHAR(20),
            grouping_company VARCHAR(20),
            BR_region VARCHAR(20),
            map VARCHAR(200),
            web VARCHAR(200)
        )"""
        with connection.cursor() as cursor:
          cursor.execute(create_depots_query)
          connection.commit()

      ### INSERT depots

        # creating column list for insertion
        cols = "`,`".join([str(i) for i in df_clean.columns.tolist()])

        # Insert DataFrame records one by one.
        for i,row in df_clean.iterrows():
            sql = "INSERT INTO `depots` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"

            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(row))
                connection.commit()

        sql = "SELECT * FROM `depots`"
        with connection.cursor() as cursor:        
          cursor.execute(sql)
          result = cursor.fetchall()
          for i in result:
              print(i)
                                
except Error as e:
    print(e)

finally:
    connection.close()
