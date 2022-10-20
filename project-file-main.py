import mysql.connector
import random
import pandas as pd
from datetime import date
from tabulate import tabulate

#connection to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database="school12ip"
)
mycursor = mydb.cursor() 

#date
today = date.today()
d1 = today.strftime("%Y-%m-%d")

#introduction
print("INFORMATICS PROJECT")
print("---------------------")
print("Made by: Asif Salim, Mohammed Abbasi, Jonathan Correa")
print("\n~ Car rental system ~")
print("Greetings, welcome to the car rental system!")
name = input("Whats your name: ")

#looping the options menu
while True:
    print("\n",name,"choose from the below options:")
    print("1. New customer, New entry")
    print("2. Check details")
    print("3. Check available cars")
    print("4. Choose car")
    print("5. Return car")
    print("6. Exit the system")
    ans = int(input("\nEnter your option number: "))
    
    #1. New entry
    if ans == 1:
        cid = random.randint(10000,99999)
        dlics=int(input("Driving license id: "))
        print("Have you used any of our cars before")
        c_used = int(input("if yes how many times? (if no enter 0): "))
        sql1 = "insert into customers values(NULL,%s,%s,%s,%s,%s)"
        val1 = (name,cid,d1,c_used,dlics)
        mycursor.execute(sql1, val1)
        mydb.commit()
        print("Thank you for registering with us!")
        print("Make sure to remember your id,",cid)
        print("\nDetails entered:")
        print(cid,"-",name,"-",dlics)
        
    #2. Check your details
    elif ans == 2:
        id1 = int(input("Enter your id: "))
        sql2 = "select id,name,driving_license,cars_used,date_of_join from customers where name = %s and id = %s"
        val2 = (name,id1)
        mycursor.execute(sql2,val2)
        myresult1 = mycursor.fetchall()
        print(tabulate(myresult1, headers=['id', 'name','driving_lics','cars_used','date_of_join'], tablefmt='psql2'))
        print("Make sure to remember your id")
        sql21 = "SELECT name,id,carname,numberplate from carstaken where id=%s"
        val21 = (id1,)
        mycursor.execute(sql21,val21)
        myresult21 = mycursor.fetchall()
        print(tabulate(myresult21, headers=['name', 'id', 'carname', 'numberplate'], tablefmt='psql'))
    
    #3. Check available cars
    elif ans == 3:
        print("Here are the cars available to rent:")
        mycursor.execute("SELECT sno,car_name,year FROM cars where in_use='N'")
        myresult2 = mycursor.fetchall()
        print(tabulate(myresult2, headers=['sno', 'name','year_bought'], tablefmt='psql'))
    
    #4. Choose car
    elif ans == 4:
        mycursor.execute("SELECT sno,car_name,year FROM cars where in_use='N'")
        myresult2 = mycursor.fetchall()
        print(tabulate(myresult2, headers=['sno', 'name','year_bought'], tablefmt='psql'))
        choosecar = int(input("\nWhich car would you like to choose (enter serial number): "))
        returndate = input("Enter date of return (yyyy-mm-dd): ")
        sql4 = "insert into carstaken (id,name,carname,numberplate) select a.id, a.name, b.car_name, b.numberplate from customers a,cars b where a.name = %s and b.sno = %s;"
        val4 = (name,choosecar)
        mycursor.execute(sql4,val4)
        sql5 = "update carstaken set return_time=%s where name=%s"
        val5 = (returndate,name)
        mycursor.execute(sql5,val5)
        mydb.commit()
        sql6 = "SELECT name,id,carname,numberplate from carstaken where name=%s"
        val6 = (name,)
        mycursor.execute(sql6,val6)
        myresult3 = mycursor.fetchall()
        print(tabulate(myresult3, headers=['name', 'id', 'carname', 'numberplate'], tablefmt='psql'))
        print("Remember to remember your numberplate")
        sql7 = "update cars set in_use='Y' where sno=%s"
        val7 = (choosecar,)
        mycursor.execute(sql7,val7)
        mydb.commit()
        sql8 = "update customers set cars_used=cars_used+1 where name=%s"
        val8 = (name,)
        mycursor.execute(sql8,val8)
        mydb.commit()
        sql81 = "update cars set timesused=timesused+1 where sno=%s"
        val81 = (choosecar,)
        mycursor.execute(sql81,val81)
        mydb.commit()
        
    #5. Return car/Cancel car
    elif ans == 5:
        
        platenumber = input("Enter the number plate of the car you are returning: ")
        sql9 = "delete from carstaken where name= %s and numberplate= %s"
        val9 = (name, platenumber)
        mycursor.execute(sql9,val9)
        mydb.commit()
        sql10 = "update cars set in_use='N' where numberplate=%s"
        val10 = (platenumber,)
        mycursor.execute(sql10,val10)
        mydb.commit()
        print("\nHope you enjoyed your experience with the car!")
        
    #6. Exit the system
    elif ans == 6:
        print("Thank you",name,"!")
        break
    
    #7. EXTRA
    elif ans == 7:
        print("extra menu:")
        print("1: select all tables")
        print("2: insert csv into py")
        print("3: view data")
        print("4: insert csv into sql")
        ans2 = input("-> :")
        
        while True:
            if ans2 == 1:
                mycursor.execute("SELECT * FROM cars")
                myresult71 = mycursor.fetchall()
                print(tabulate(myresult71, headers=['sno', 'car_name','year','timesused','numberplate','in_use'], tablefmt='msql1'))
                  
                print('\n')
                mycursor.execute("SELECT * FROM customers")
                myresult72 = mycursor.fetchall()
                print(tabulate(myresult72, headers=['sno', 'name','id','date_of_join','cars_used','driving_license'], tablefmt='msql2'))
                  
                print('\n')
                mycursor.execute("SELECT * FROM carstaken")
                myresult73 = mycursor.fetchall()
                print(tabulate(myresult73, headers=['sno', 'id','name','carname','numberplate','return_time'], tablefmt='msql3'))
                    
            elif ans2 == 2:
                print("problem")
                break
    
    else:
        print("\nOh no, you have entered someting wrong!")