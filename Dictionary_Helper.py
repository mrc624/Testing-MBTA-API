import os
import json
import requests
from dotenv import load_dotenv

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

DEBUG = True
DEBUG_FOLDER = "Debug\\"

url = "https://api-v3.mbta.com"
alerts_url = url + "/alerts"
facilities_url = url + "/facilities"
lines_url = url + "/lines"
live_facilities_url = url + "/live_facilities"
prediction_url = url + "/prediction"
route_url = url + "/routes"
route_pattern_url = url + "route_patterns"
schedule_url = url + "/schedules"
service_url = url + "/services"
shape_url = url + "/shapes"
stop_url = url + "/stops"
trip_url = url + "/trips"
vehicles_url = url + "/vehicles"

default_params = { }

default_headers = {
    "x-api-header":key
}

def Get_Routes(params = default_params, headers = default_headers):
    response = requests.get(route_url, params=params, headers=headers)
    routes = response.json()
    if DEBUG:
        print("Routes Response: " + str(response.status_code))
        with open(DEBUG_FOLDER + 'routes.json', 'w') as fp:
            json.dump(routes, fp, indent=4)
    return routes

def Get_Vehicles(params = default_params, headers = default_headers):
    response = requests.get(vehicles_url, params=params, headers=headers)
    vehicles = response.json()
    if DEBUG:
        print("Vehicles Response: " + str(response.status_code))
        with open(DEBUG_FOLDER + 'vehicles.json', 'w') as fp:
            json.dump(vehicles, fp, indent=4)
    return vehicles

def Get_ID_to_Names(params = default_params, headers = default_headers):
    routes = Get_Routes(params=params, headers=headers)
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
    routes = Get_Routes(params=params, headers=headers)
    vehicles = Get_Vehicles(params=params, headers=headers)
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

def Get_Lines(params = default_params, headers = default_headers):
    response = requests.get(lines_url, params=params, headers=headers)
    lines = response.json()
    if DEBUG:
        print("Lines Response: " + str(response.status_code))
        with open(DEBUG_FOLDER + 'lines.json', 'w') as fp:
            json.dump(lines, fp, indent=4)
    return lines

def Get_Line_Names(params = default_params, headers = default_headers):
    lines = Get_Lines(params=params, headers=headers)
    line_names = { }
    for line in lines["data"]:
        line_names[line["id"]] = {
            "short_name": line["attributes"]["short_name"],
            "long_name": line["attributes"]["long_name"]
        }
    if DEBUG:
        with open(DEBUG_FOLDER + 'line_names.json', 'w') as fp:
            json.dump(line_names, fp, indent=4)
    return line_names