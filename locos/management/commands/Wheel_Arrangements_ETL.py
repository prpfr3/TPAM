# """ COMMENTED OUT BECAUSE PSYCOPG2 CAUSES ISSUE ON DIGITAL OCEAN PRODUCTION
# Extracts and Saves Wikipedia Wheel arrangements to csv using Pandas and then loads into Oracle

# Working correctly at 24/01/21 for MySQL and refactored on 05/01/22 for PostGres.
# Significant changes needed for the PostGres sql string which does not expect table or fieldnames to be in quotes, whereas mysql does.

# Both an SQL load and ORM load are available below. However, as at 23/06/21 the SQL load expects the database fieldnames to be all lowercase as they are in the Django model definition, whereas the ORM load expects them to be capitalised.

# """
# import requests, csv
# import pandas as pd
# import configparser
# import os
# import psycopg2
# import mysql.connector #needs mysql-connector-python from pip (e.g. 8.0.25)

# url = "https://en.wikipedia.org/wiki/Wheel_arrangement"
# DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
# csvfile = os.path.join(DATAIO_DIR, "Wheel_arrangement.csv")
# output_file = open(csvfile, 'wt+', newline='', encoding='utf-8')
# output = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

# #https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testin
# try:
#     res = requests.get(url)
#     res.raise_for_status()
# except requests.exceptions.ConnectionError as err:
#     # eg, no internet
#     raise SystemExit(err) from err
# except requests.exceptions.HTTPError as err:
#     # eg, url, server and other errors
#     raise SystemExit(err) from err

# df = pd.read_html(res.text, flavor="bs4", na_values=['none'])[1]
# print(df.head())
# df_clean = df.rename(columns={df.columns[0]:"UIC_system",
#                     df.columns[1]:"Whyte_notation",
#                     df.columns[2]:"American_name",
#                     df.columns[3]:"Visual"})
# df_clean = df_clean.where(df_clean.notnull(), None)
# print(df_clean.head())
# df_clean.to_csv(csvfile, encoding='utf-8', index=False)

# config = configparser.ConfigParser()
# KEYS_DIR = os.path.join("D:\\Data", "API_Keys")
# config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
# db_pswd = config['MySQL']['p']


# try:
#     with psycopg2.connect(
#         host="localhost",
#         port="5432",
#         user="postgres",
#         password=db_pswd,
#         database="TPAM"
#         ) as connection:

#         drop_table_query = "DROP TABLE locos_wheelarrangement"
#         with connection.cursor() as cursor:
#             cursor.execute(drop_table_query)

#         create_wheel_arrangement_query = """
#         CREATE TABLE locos_wheelarrangement(
#             wheelid SMALLINT,
#             UIC_system VARCHAR(20),
#             Whyte_notation VARCHAR(20),
#             American_name VARCHAR(75),
#             Visual VARCHAR(20),
#             CONSTRAINT pk_wheel_arrangement PRIMARY KEY (wheelid)
#         )"""
#         with connection.cursor() as cursor:
#             cursor.execute(create_wheel_arrangement_query)
#             connection.commit()

#         # Example shows post-creation alteration
#         alter_wheel_arrangement_query = """
#             ALTER TABLE locos_wheelarrangement
#             MODIFY wheelid SMALLINT UNSIGNED AUTO_INCREMENT
#             """

#         # Inserting data into the table
#         with connection.cursor() as cursor:
#             cursor.execute(alter_wheel_arrangement_query)
#             connection.commit()

#         # creating column list for insertion
#         cols = ",".join([str(i) for i in df_clean.columns.tolist()])

#         for i,row in df_clean.iterrows():
#             sql = "INSERT INTO locos_wheelarrangement (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"

#             print(f'{sql=}/n{tuple(row)=}')
#             with connection.cursor() as cursor:
#                 cursor.execute(sql, tuple(row))
#                 connection.commit()

#         sql = "SELECT * FROM locos_wheelarrangement"
#         with connection.cursor() as cursor:
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             for i in result:
#                 print(i)

# except Exception as e:
#     print(e)

# finally:
#     connection.close()


# from csv import DictReader
# from django.core.management import BaseCommand
# from locos.models import WheelArrangement
# import os

# ALREADY_LOADED_ERROR_MESSAGE = "To reload the data from the CSV file,first either (a) delete and recreate the database table to reset keys to start at zero or (b) drop all the table records in which cases the keys will be initialised starting at the last unused value"

# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Loads data from a csv file into the model"

#     def handle(self, *args, **options):
#         if WheelArrangement.objects.exists():
#             print('The tables already contains data...exiting.')
#             print(ALREADY_LOADED_ERROR_MESSAGE)
#             return
#         print("Creating Wheel Arrangements")

#         DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
#         for row in DictReader(open(csvfile, encoding='utf-8')):
#             c = WheelArrangement()
#             print(row)
#             c.uic_system = row['UIC_system']
#             c.whyte_notation = row['Whyte_notation']
#             c.american_name = row['American_name']
#             c.visual = row['Visual']
#             c.save()
