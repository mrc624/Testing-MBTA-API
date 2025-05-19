import os
import json
import requests
from dotenv import load_dotenv

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

DEBUG = True
DEBUG_FOLDER = "Debug\\"

url = "https://api-v3.mbta.com"
vehicles_url = url + "/vehicles"
routes_url = url + "/routes"

default_params = { }

default_headers = {
    "x-api-header":key
}

def Get_Routes(params = default_params, headers = default_headers):
    response = requests.get(routes_url, params=params, headers=headers)
    print("Routes Response: " + str(response.status_code))
    routes = response.json()
    if DEBUG:
        with open(DEBUG_FOLDER + 'routes.json', 'w') as fp:
            json.dump(routes, fp, indent=4)
    return routes

def Get_Vehicles(params = default_params, headers = default_headers):
    response = requests.get(vehicles_url, params=params, headers=headers)
    print("Vehicles Response: " + str(response.status_code))
    vehicles = response.json()
    if DEBUG:
        with open(DEBUG_FOLDER + 'vehicles.json', 'w') as fp:
            json.dump(vehicles, fp, indent=4)
    return vehicles

def Get_ID_to_Names(params = default_params, headers = default_headers):
    routes = Get_Routes()
    ID_to_Names = { }
    for route in routes["data"]:
        route_id = route["id"]
        route_short_name = route["attributes"]["short_name"]
        route_long_name = route["attributes"]["long_name"]
        ID_to_Names[route_id] = {
            "short_name": route_short_name,
            "long_name": route_long_name
        }
    if DEBUG:
        with open(DEBUG_FOLDER + 'routes_id_name.json', 'w') as fp:
            json.dump(ID_to_Names, fp, indent=4)
    return ID_to_Names

def Get_Vehicles_on_Routes_Count(params = default_params, headers = default_headers):
    routes = Get_Routes()
    vehicles = Get_Vehicles()
    vehicles_on_route_count = { }
    for route in routes["data"]:
        vehicles_on_route_count[route["id"]] = 0

    for vehicle in vehicles["data"]:
        route_id = vehicle["relationships"]["route"]["data"]["id"]
        if route_id in vehicles_on_route_count:
            curr_count = vehicles_on_route_count[route_id]
            new_count = curr_count + 1
            vehicles_on_route_count[route_id] = new_count
        else:
            vehicles_on_route_count[route_id] = 1
    if DEBUG:
        with open(DEBUG_FOLDER + 'vehicles_on_route_count.json', 'w') as fp:
            json.dump(vehicles_on_route_count, fp, indent=4)
    return vehicles_on_route_count
