import requests

# Define the base URL for the Stellarium API
base_url = 'http://localhost:8090/api/objects/'

# Make the request to Stellarium API
categories = ["NebulaMgr","NebulaMgr:5","StarMgr","SolarSystem"]


def getObjDetails(objName):
    print(objName)
    details = requests.get(f"{base_url}info?name={objName}&format=json").json()
    return {"type":details["type"],"rise":details["rise"],"set":details["set"],"mag":details["vmag"]}

objects_dict = {}

for type in categories:
    objects =eval( requests.get(f"{base_url}listobjectsbytype?type={type}").text)
    for obj in objects:
        try:
            objects_dict[obj] = getObjDetails(obj)
        except requests.exceptions.JSONDecodeError:
            continue

print(objects)
