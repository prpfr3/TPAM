#Contains other get requests yet to be fully developed at 24/01/21

import mysql.connector #needs mysql-connector-python from pip (8.0.22)
from getpass import getpass #getpass is built-in
from mysql.connector import connect, Error

#Use once for creating a database
try:
    with connect( #use of with simplifies the connection closure process
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
        create_db_query = "CREATE DATABASE railways"
        with connection.cursor() as cursor:
          cursor.execute(create_db_query)
        print(connection)
except Error as e:
    print(e)

#Connecting to an existing database
try:
    with connect(
        host="localhost",
        #user=input("Enter username: "),
        #password=getpass("Enter password: "),
        user="userid",
        password="Password_here",
        database="railways"
        ) as connection:

        print("Successful connection to:", connection)
        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)


####### POWER TYPE SECTION #######

        create_power_type_query = """
        CREATE TABLE power_type(
            power_type_id INT AUTO_INCREMENT PRIMARY KEY,
            power_type VARCHAR(20)
        )"""
        with connection.cursor() as cursor:
          cursor.execute(create_power_type_query)
          connection.commit()
            
        show_table_query = "DESCRIBE power_type"
        with connection.cursor() as cursor:
          cursor.execute(show_table_query)
          result = cursor.fetchall()
          for row in result:
              print(row)
                
        drop_table_query = "DROP TABLE power_type"
        with connection.cursor() as cursor:
          cursor.execute(drop_table_query)

####### DESIGNER SECTION #######

        create_designer_query = """
        CREATE TABLE designer(
            designer_id INT AUTO_INCREMENT PRIMARY KEY,
            designer VARCHAR(20)
        )"""
        with connection.cursor() as cursor:
          cursor.execute(create_designer_query)
          connection.commit()
            
        show_table_query = "DESCRIBE designer"
        with connection.cursor() as cursor:
          cursor.execute(show_table_query)
          result = cursor.fetchall()
          for row in result:
              print(row)
                
        drop_table_query = "DROP TABLE designer"
        with connection.cursor() as cursor:
          cursor.execute(drop_table_query)

####### COMPANY SECTION #######

        create_company_query = """
        CREATE TABLE company(
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            company VARCHAR(20)
        )"""
        with connection.cursor() as cursor:
          cursor.execute(create_company_query)
          connection.commit()
            
        show_table_query = "DESCRIBE company"
        with connection.cursor() as cursor:
          cursor.execute(show_table_query)
          result = cursor.fetchall()
          for row in result:
              print(row)
                
        drop_table_query = "DROP TABLE company"
        with connection.cursor() as cursor:
          cursor.execute(drop_table_query)
                      
except Error as e:
    print(e)

finally:
    connection.close()