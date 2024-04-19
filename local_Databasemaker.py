import mysql.connector

conn  = mysql.connector.connect(host="localhost",user="root",password="@@Aniket.984",database="Telescope_Webportal")

if conn.is_connected():
    print("MySql connected !")

cur = conn.cursor()

cur.execute("Create Table User_Requests (request_id varchar(10),object varchar(30),ID varchar(10),email varchar(50),time_request time);")
conn.commit()
