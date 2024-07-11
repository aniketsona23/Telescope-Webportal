import mysql.connector
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

#Initialize MySQL connection
conn  = mysql.connector.connect(host="localhost",user=os.environ["MYSQL_USER"],password=os.environ["MYSQL_PASS"],database=os.environ["DB_NAME"])
if conn.is_connected():
    print("MySql connected !")
else:
    print("MySQL not Connected !")
cur = conn.cursor()

# # Initialize google sheet Connection
# client = pygsheets.authorize(service_account_file="./telescope-webportal-key.json")
# spread = client.open("Telescope requests")
# worksht = spread.worksheet("title", "Sheet1") 
# requests= (worksht.range("A2:E4"))



 
def get_local_requests():
    '''
    Description
    ----------
    Fetches all local requests from local server

    Returns
    -------
    List
        List of all rows, where each row is a list having each column value  
    '''
    cur.execute("SELECT * FROM User_Requests ;")
    local_requests = cur.fetchall()
    return local_requests


def insert_new_requests():

    ''' 
    Description
    -----------
    Adds New Requests to Local SQL server

    This function checks if number of requests in local server is equal to on google sheeet.
    If not, then adds the new Requests from sheet to local server.
    
    Returns
    -------
    True 
        If there were new requests and added to server
    
    False
        If there were no new requests'''
    
    local_requests = get_local_requests()
    cloud_requests  = get_cloud_requests()

    if len(local_requests)!=len(cloud_requests):
        new_requests = len(cloud_requests) - len(local_requests)
        for i in range(new_requests,0,-1):
            cur.execute(f"INSERT INTO User_Requests values {tuple(cloud_requests[-(i)])};")
        conn.commit()
        return True
    return False

def get_remaining_objects():
    '''
    Description
    -----------
    Fetches Objects not clicked from Local Database (status=0)
    
    Returns
    -------
    List
        List of remaining Requests, each request as a list'''
    
    cur.execute("SELECT * FROM User_Requests WHERE status=0;")
    remaining_objects = cur.fetchall()
    return remaining_objects

if __name__=="__main__":
    print(insert_new_requests())