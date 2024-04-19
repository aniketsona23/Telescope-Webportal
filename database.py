import pygsheets

client = pygsheets.authorize(service_account_file="./telescope-webportal-384dcfb4abaf.json")

spread = client.open("Telescope requests")
worksht = spread.worksheet("title", "Sheet1") 
requests= (worksht.range("A2:E4"))



def get_requests():
    proper = []
    for row in requests:
        r =[data.value for data in row ]
        proper.append(r)

    return proper

if __name__=="__main__":
    print(get_requests())