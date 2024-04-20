import mysql.connector
import dotenv
import os

dotenv.load_dotenv()
conn  = mysql.connector.connect(host="localhost",user=os.environ["MYSQL_USER"],password=os.environ["MYSQL_PASS"],database=os.environ["DB_NAME"])

if conn.is_connected():
    cur = conn.cursor()

    cur.execute("Create Table User_Requests (request_id varchar(10),object varchar(30),ID varchar(10),email varchar(50),time_request time,status int);")
    conn.commit()
