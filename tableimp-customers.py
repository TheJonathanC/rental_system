import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import tablesimp

csvfile = tablesimp.csvfilecustomers
hstname = tablesimp.lh
dbnm = tablesimp.dbn
ussr = tablesimp.usr
pw = tablesimp.pswrd

customers = pd.read_csv(csvfile)
print(customers)

try:
    conn = msql.connect(host=hstname, database=dbnm, user=ussr, password=pw)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS customers;')
        print('Creating table....')
        cursor.execute("create table customers(sno int NOT NULL AUTO_INCREMENT,name varchar(15),id int(5), date_of_join date,cars_used int(2), driving_license int(8),PRIMARY KEY(sno))")
        print("Table is created....")
        for i,row in customers.iterrows():
            sql = "INSERT INTO customers (name,id,date_of_join,cars_used,driving_license) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
        print("table imported to sql")
except Error as e:
        print("Error while connecting to MySQL", e)