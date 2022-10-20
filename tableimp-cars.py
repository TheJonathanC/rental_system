import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import tablesimp

csvfile = tablesimp.csvfilecars
hstname = tablesimp.lh
dbnm = tablesimp.dbn
ussr = tablesimp.usr
pw = tablesimp.pswrd

cars = pd.read_csv(csvfile)
print(cars)

try:
    conn = msql.connect(host=hstname, database=dbnm, user=ussr, password=pw)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS cars;')
        print('Creating table....')
        cursor.execute("create table cars(sno int NOT NULL AUTO_INCREMENT,car_name varchar(15),year int(4),timesused int(3),numberplate varchar(7),in_use varchar(1),PRIMARY KEY (sno))")
        print("Table is created....")
        for i,row in cars.iterrows():
            sql = "INSERT INTO cars (car_name,year,timesused,numberplate,in_use) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
        print("table imported to sql")
except Error as e:
    print("Error while connecting to MySQL", e)