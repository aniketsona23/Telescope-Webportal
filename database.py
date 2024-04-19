import pygsheets
import mysql.connector
import json

envs = json.load(open("./envs.json"))
conn  = mysql.connector.connect(host="localhost",user=envs["mysql_user"],password=envs["mysql_pass"],database="Telescope_Webportal")

if conn.is_connected():
    print("MySql connected !")
else:
    print("MySQL not Connected !")

cur = conn.cursor()
client = pygsheets.authorize(service_account_file="./telescope-webportal-key.json")

spread = client.open("Telescope requests")
worksht = spread.worksheet("title", "Sheet1") 
requests= (worksht.range("A2:E4"))



def get_requests():
    proper = []
    for row in requests:
        r =[data.value for data in row ]+["0"]
        proper.append(r)

    return proper

def insert_new_requests():
    cur.execute("SELECT * FROM User_Requests ;")
    local_requests = cur.fetchall()
    cloud_requests  = get_requests()

    if len(local_requests)!=len(cloud_requests):
        new_requests = len(cloud_requests) - len(local_requests)
        for i in range(new_requests,0,-1):
            cur.execute(f"INSERT INTO User_Requests values {tuple(cloud_requests[-(i)])};")
        conn.commit()
        return True
    return False

def get_remaining_objects():
    cur.execute("SELECT * FROM User_Requests WHERE status='0';")
    remaining_objects = cur.fetchall()
    return remaining_objects

if __name__=="__main__":
    print(insert_new_requests())