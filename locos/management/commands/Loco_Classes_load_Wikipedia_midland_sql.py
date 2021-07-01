# Extracts and Saves Midland Locomotive Classes from Wikipedia to csv using Pandas and then loads into MySQL
# Working correctly at 24/01/21

import requests, csv, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector #needs mysql-connector-python from pip (8.0.22)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error
from unicodedata import normalize

try:
    with connect(
        host="localhost",
        #user=input("Enter username: "),
        #password=getpass("Enter password: "),
        user="userid",
        password="enterpassword",
        database="railways"
        ) as connection:

        #drop_table_query = "DROP TABLE locos_lococlass"
        #with connection.cursor() as cursor:
        #  cursor.execute(drop_table_query)

        #create_locos_lococlass_query = """
        #CREATE TABLE locos_lococlass(
        #    id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        #    pre_grouping_company VARCHAR(100),
        #    grouping_company VARCHAR(100),
        #    pre_grouping_class VARCHAR(100),
        #    loco_class VARCHAR(100),
        #    BR_power_class VARCHAR(5),
        #    wheel_id SMALLINT,
        #    wheel_arrangement VARCHAR(100),
        #    number_built SMALLINT UNSIGNED ZEROFILL,
        #    number_range VARCHAR(100),
        #    designer VARCHAR(200),
        #    manufacturer VARCHAR(200),
        #    years_built VARCHAR(100),
        #    years_withdrawn VARCHAR(100),
        #    date_built_en VARCHAR(100),
        #    lner_class VARCHAR(100),
        #    notes VARCHAR(200)
        #    #CONSTRAINT fk_wheel_arrangement FOREIGN KEY (wheel_arrangement) REFERENCES wheel_arrangement (Whyte_notation) #Possible future foreign key
        #)"""
        #with connection.cursor() as cursor:
        #  cursor.execute(create_locos_lococlass_query)
        #  connection.commit()

        # Insert DataFrame records one by one.
        for i,row in df_clean.iterrows():
            insert_table_query = """INSERT INTO locos_lococlass
                    (pre_grouping_class, wheel_arrangement, manufacturer, years_built, number_built, years_withdrawn, notes, designer2, pre_grouping_company, grouping_company)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            with connection.cursor() as cursor:
                cursor.execute(insert_table_query, tuple(row))
                connection.commit()

        insert_table_query = """INSERT INTO locos_lococlass
                (pre_grouping_company, grouping_company)
                VALUES ('MR', 'LMS') """
        with connection.cursor() as cursor:
            cursor.execute(insert_table_query)
            connection.commit()

        print("\nCreating temporary table of wheel arrangement ids\n")
        create_temp_query = """CREATE TEMPORARY TABLE temptable
        (classid SMALLINT, wheelid SMALLINT)"""
        with connection.cursor() as cursor:
          cursor.execute(create_temp_query)
          connection.commit()

        print("\nInserting wheel arrangement ids into the loco classes table\n")  
        insert_table_query = """INSERT INTO temptable
        SELECT lc.id, wa.id
        FROM locos_lococlass lc INNER JOIN locos_wheelarrangement wa
          ON lc.wheel_arrangement = wa.Whyte_notation"""
        with connection.cursor() as cursor:
            cursor.execute(insert_table_query)

        update_table_query = """UPDATE locos_lococlass
        SET locos_lococlass.wheelid = temptable.id 
        WHERE locos_lococlass.id = lc.id"""
        print(row)

        #show_table_query = "DESCRIBE locos_lococlass"
        #with connection.cursor() as cursor:
        #    cursor.execute(show_table_query)
        #    for row in cursor.fetchall():
        #        print(row)

        #print("\n2-6-0 Locomotive Classes\n")
        #show_table_query = """SELECT pre_grouping_class 
        #    FROM locos_lococlass
        #    WHERE wheel_arrangement = "2-6-0"
        #    ORDER by pre_grouping_class"""
        #with connection.cursor() as cursor:
        #    cursor.execute(show_table_query)
        #    for row in cursor.fetchall():
        #        print(row)

        #print("\nFetch 5 Locomotive classes with over 100 built\n")
        #show_table_query = """SELECT pre_grouping_class, wheel_arrangement, manufacturer, number_built
        #    FROM locos_lococlass
        #    WHERE number_built > 100
        #    ORDER by wheel_arrangement"""
        #with connection.cursor() as cursor:
        #    cursor.execute(show_table_query)
        #    for row in cursor.fetchmany(size=5):
        #        print(row)
        #    cursor.fetchall() #Clears all remaining records to prevent an error

        #print("\nFetch one Locomotive class concatenated with year with over 100 built\n")
        #show_table_query = """SELECT CONCAT(pre_grouping_class, "(", years_built, ")"), wheel_arrangement, manufacturer, number_built
        #    FROM locos_lococlass
        #    WHERE number_built > 100
        #    ORDER by wheel_arrangement"""
        #with connection.cursor() as cursor:
        #    cursor.execute(show_table_query)
        #    for row in cursor.fetchone():
        #        print(row)
        #    cursor.fetchall() #Clears all remaining records to prevent an error

        ##INNER JOIN
        #print("\nInner Join counting classes by UIC_system\n")
        #show_table_query = """SELECT CONCAT(UIC_system, " ", Visual), COUNT(*) as num
        #    FROM wheel_arrangement
        #    INNER JOIN locos_lococlass
        #      ON Whyte_notation = locos_lococlass.wheel_arrangement
        #    GROUP BY UIC_system
        #    ORDER by num DESC"""
        #with connection.cursor() as cursor:
        #    cursor.execute(show_table_query)
        #    for row in cursor.fetchall():
        #        print(row)

        ##UPDATE QUERY
        #classid = input("Enter classid: ")
        #updated_comment = input("Enter comment update: ")

        ##FOLLOWING METHOD VULNERABLE TO SQL INJECTION
        #update_query = """UPDATE locos_lococlass
        #                  SET notes = "%s"
        #                  WHERE classid = "%s";

        #                  SELECT * FROM locos_lococlass
        #                  WHERE classid = "%s" 
        #                  """ 

        ##THIS METHOD NOT VULNERABLE TO SQL INJECTION
        #update_query = """UPDATE locos_lococlass
        #                  SET notes = %s
        #                  WHERE classid = %s;

        #                  SELECT * FROM locos_lococlass
        #                  WHERE classid = %s
        #                  """ 

        #input_tuple = (updated_comment, classid, classid)

        #with connection.cursor() as cursor:
        #    #for result in cursor.execute(update_query, multi=True): #VULNERABILITY
        #    for result in cursor.execute(update_query, input_tuple, multi=True): #returns an iterator for multi=True
        #      if result.with_rows: #runs a for loop on the iterator but only if there is rows produced
        #        print(result.fetchall()) #a fetchall is needed to make sure all returned rows are processed
        #    connection.commit()

        #delete_query = "DELETE FROM locos_lococlass WHERE classid = 1"
        #with connection.cursor() as cursor:
        #    cursor.execute(delete_query)
        #    connection.commit()

        #print("\nCalculating the length of the longest notes field\n")
        #query = """SELECT LENGTH(notes) notes_length
        #FROM locos_lococlass"""
        #with connection.cursor() as cursor:
        #    cursor.execute(query)
        #    print(row)

        #print("\nGets the positions of a string in a field\n")
        #query = """
        #SELECT POSITION('Johnson' IN notes)
        #FROM locos_lococlass"""
        #with connection.cursor() as cursor:
        #    cursor.execute(query)
        #    for row in cursor.fetchall():
        #        print(row)

        #print("\nSame as above but gets the position of a string starting from other than the first position\n")
        #select_query = """
        #SELECT LOCATE('Johnson', notes, 5)
        #FROM locos_lococlass  
        #"""
        #with connection.cursor() as cursor:
        #    cursor.execute(query)
        #    for row in cursor.fetchall():
        #        print(row)

except Error as e:
    print(e)

finally:
    connection.close()