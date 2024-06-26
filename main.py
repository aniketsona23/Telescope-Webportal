# Required libraries
import dotenv
import requests, re, synscan
import database
import os

dotenv.load_dotenv()
port = os.environ["PORT"]

# Converts the API request's body to a list of coordinates
def get_coords_list(data):

    beg = data.find("<br/>Az./Alt.: ")
    end = data.find("<br/>", beg + 1)

    lst = data[beg+len("<br/>Az./Alt.: ") : end-len("  <")+1].split('/')

    az = re.split('[Â° \' \" + -]', lst[0])
    alt = re.split('[Â° \' \" + -]', lst[1])

    az.insert(0, lst[0][0])
    alt.insert(0, lst[1][0])
    for i in [1,2,4]:
        az.pop(i)
        alt.pop(i)

    return (az, alt)


# Converts the output of get_coords_list into float values
def coord_to_flt(lst):

    return round(int(lst[0] + '1') * (float(lst[1]) + float(lst[2])/60), 3)


# Returns the az-alt coordinates in float format
def get_coords_flt(data):

    az, alt = get_coords_list(data)
    az_flt, alt_flt = coord_to_flt(az), coord_to_flt(alt)

    return {'az': az_flt, 'alt': alt_flt}


# Fetches the final coordinates of an object given the port number
def fetch_object(obj, port):

    txt = requests.get(f"http://localhost:{port}/api/objects/info?name={obj}").text

    return get_coords_flt(txt)


# Slews the telescope to the coordinates provided
def slew_telescope(coords):

    smc = synscan.motors()
    smc.set_pos(0,0)

    smc.goto(coords['az'], coords['alt'], synchronous=True)

    curr_pos= [smc.axis_get_pos(1), smc.axis_get_pos(2)]
    print(f"Current position of telescope: [Az: {curr_pos[0]}, Alt: {curr_pos[1]}]")

# Track Object 'obj' for 't' time 
def track(t,obj):
    pass
    
# Takes Object name through CLI
def manual_control():

    obj = input("Enter Object Name : ").strip()
    coords = fetch_object(obj.lower(),port)
    print(f"Fetched data on {obj.upper()}: [Az: {coords['az']}, Alt: {coords['alt']}]")
    
    return coords

def web_control():
    
    update = database.insert_new_requests()
    
    if (update):# If there were new requests
        
        objects = database.get_remaining_objects()
        for req in objects:
            coords = fetch_object(req[2].lower(), port)
            print(f"Fetched data on {req[2].upper()}: [Az: {coords['az']}, Alt: {coords['alt']}]")


def main():

    control = input("Enter Control method - Manual(m) or Web(w) : ").strip().lower()
    if control=="m":
        coords = manual_control()
    elif control=="w":
        coords = web_control()
    else:
        print("Enter Valid input !")
        main()

    #slew_telescope(coords)


main()