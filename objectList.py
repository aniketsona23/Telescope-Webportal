import requests

base_url = 'http://localhost:8090/api/objects/'

categories = ["NebulaMgr","NebulaMgr:5","StarMgr","SolarSystem"]

# Returns type,rise and set time and magnitude of obj given
def getObjDetails(objName):
    details = requests.get(f"{base_url}info?name={objName}&format=json").json()
    return {"type":details["type"],"rise":details["rise"],"set":details["set"],"mag":details["vmag"]}

#contains keys as objname and values as its details dictionary
objects_dict = {}


for type in categories:
    objects =eval( requests.get(f"{base_url}listobjectsbytype?type={type}").text)#get list of objects of "type"
    for obj in objects:
        try:
            objects_dict[obj] = getObjDetails(obj)
        except requests.exceptions.JSONDecodeError:# when obj not found
            continue

print(objects)
