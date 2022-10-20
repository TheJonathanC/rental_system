import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import tablesimp

csvfile = tablesimp.csvfilecarstaken
hstname = tablesimp.lh
dbnm = tablesimp.dbn
ussr = tablesimp.usr
pw = tablesimp.pswrd

carstaken = pd.read_csv(csvfile)
print(carstaken)

try:
    conn = msql.connect(host=hstname, database=dbnm, user=ussr, password=pw)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS carstaken;')
        print('Creating table....')
        cursor.execute("CREATE TABLE carstaken(sno int NOT NULL AUTO_INCREMENT,id int(5),name varchar(15),carname varchar(15),numberplate varchar(7),return_time date, PRIMARY KEY(sno))")
        print("Table is created....")
        for i,row in carstaken.iterrows():
            sql = "INSERT INTO carstaken (id,name,carname,numberplate,return_time) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
        print("table imported to sql")
except Error as e:
    print("Error while connecting to MySQL", e)