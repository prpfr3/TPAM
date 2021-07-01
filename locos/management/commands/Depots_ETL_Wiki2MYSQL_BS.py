
# Extracts a list of sheds from Wikipedia and loads into Oracle
# Still under development at 24/01/21

import requests, csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (8.0.22)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

webpage = "https://en.wikipedia.org/wiki/List_of_British_Railways_shed_codes"

try:
    res = requests.get(webpage)
    res.raise_for_status()
    page = requests.get(webpage).text
    df = pd.read_html(webpage, flavor="bs4") 
    print(f'Total tables: {len(df)}') #Returns the number of tables
    #df = pd.read_html(webpage, flavor="bs4", match='Willesden') #Returns only the table with a match. An alternative to the above statement
    
    i = 0
    appended_data = []
    while i <= 5:
      df = pd.read_html(webpage, flavor="bs4")[i]
      #df = pd.read_html(webpage, flavor="bs4", na_values=['none'])[1]
      df = df.rename(columns={
                         df.columns[0]:"code",
                         df.columns[1]:"code_dates",
                         df.columns[2]:"shed",
                         df.columns[3]:"comments"})
      df["shed"].replace('Sub', ': Sub', regex=True, inplace=True)
      df = df.where(df.notnull(), "")
      df.to_csv(os.path.join(DATAIO_DIR, "ETL_Wiki_Depots.csv"), index=False)
      print("\ni = ", i)
      print(df.info())
      print(df.head())
      i += 1
      appended_data.append(df)

    df_clean = pd.concat(appended_data)
    print(type(appended_data))
    print(type(df_clean))

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

        #drop_table_query = "drop table locos_depots"
        #with connection.cursor() as cursor:
        #  cursor.execute(drop_table_query)

        #create_depots_query = """
        #CREATE TABLE locos_depots(
        #    depot_id INT AUTO_INCREMENT PRIMARY KEY,
        #    depot VARCHAR(500),
        #    codes VARCHAR(100),
        #    code_dates VARCHAR(100),
        #    date_opened VARCHAR(20),
        #    date_closed_to_steam VARCHAR(20),
        #    date_closed VARCHAR(20),
        #    pre_grouping_company VARCHAR(20),
        #    grouping_company VARCHAR(20),
        #    BR_region VARCHAR(20),
        #    map VARCHAR(200),
        #    web VARCHAR(200),
        #    comments VARCHAR(100)
        #)"""
        #with connection.cursor() as cursor:
        #  cursor.execute(create_depots_query)
        #  connection.commit()

      ### INSERT depots

        # Insert DataFrame records one by one.
        for i,row in df_clean.iterrows():
            sql = """INSERT INTO locos_depots
                    (codes, code_dates, depot, comments)
                    VALUES (%s, %s, %s, %s) """

            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(row))
                connection.commit()

        sql = "SELECT * FROM `locos_depots`"
        with connection.cursor() as cursor:        
          cursor.execute(sql)
          result = cursor.fetchall()
          for i in result:
              print(i)
                                
except Error as e:
    print(e)

finally:
    connection.close()

