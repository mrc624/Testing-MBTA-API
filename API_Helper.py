import os
import json
import requests
import sched
import time
from dotenv import load_dotenv
from enum import Enum

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

DEBUG = True
DEBUG_FOLDER = "Debug\\"

GOOD_RESPONSE = 200   

class Categories(Enum):
    alerts = 0
    facilities = 1
    lines = 2
    live_facilities = 3
    prediction = 4
    route = 5
    route_pattern = 6
    schedule = 7
    service = 8
    shape = 9
    stop = 10
    trip = 11
    vehicles = 12

MAIN_URL = "https://api-v3.mbta.com"
URL_FLAG = "url"
JSON_FILE_NAME_FLAG = "file"
TIMESTAMP_FLAG = "timestamp"
INIT_TIMESTAMP = 0
STRING_FLAG = "string"
Category_Data = {
    Categories.alerts: {
        URL_FLAG: MAIN_URL + "/alerts",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Alerts.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Alerts"
    },
        Categories.facilities: {
        URL_FLAG: MAIN_URL + "/facilities",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Facilities.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Facilities"
    },
        Categories.lines: {
        URL_FLAG: MAIN_URL + "/lines",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Lines.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Lines"
    },
        Categories.live_facilities: {
        URL_FLAG: MAIN_URL + "/live_facilities",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Live_Facilities.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Live Facilities"
    },
        Categories.prediction: {
        URL_FLAG: MAIN_URL + "/predictions",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Predictions.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Predictions"
    },
        Categories.route: {
        URL_FLAG: MAIN_URL + "/routes",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Routes.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Routes"
    },
        Categories.route_pattern: {
        URL_FLAG: MAIN_URL + "/route_patterns",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Route_Patterns.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Route Patterns"
    },
        Categories.schedule: {
        URL_FLAG: MAIN_URL + "/schedules",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Schedules.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Schedules"
    },
        Categories.service: {
        URL_FLAG: MAIN_URL + "/services",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Services.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Services"
    },
        Categories.shape: {
        URL_FLAG: MAIN_URL + "/shapes",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Shapes.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Shapes"
    },
        Categories.stop: {
        URL_FLAG: MAIN_URL + "/stops",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Stops.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Stops"
    },
        Categories.trip: {
        URL_FLAG: MAIN_URL + "/trips",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Trips.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Trips"
    },
        Categories.vehicles: {
        URL_FLAG: MAIN_URL + "/vehicles",
        JSON_FILE_NAME_FLAG: DEBUG_FOLDER + "Vehicles.json",
        TIMESTAMP_FLAG: INIT_TIMESTAMP,
        STRING_FLAG: "Vehicles"
    },
}

default_params = { }

default_headers = {
    "x-api-header":key
}

Refresh_Threshold = 15

def Eligible_For_Refresh(Timestamp: int):
    return time.time() - Timestamp >= Refresh_Threshold

def Call_All(): #this should be used for testing only
     for category in Categories:
        Call_API(category)

last_call = 0
call_limiter = 0
try_again_time = 5
def Call_API(category:Categories, force_update = False, params = None, headers = None):
    global last_call
    since_last = time.time() - last_call
    if since_last < call_limiter:
        time.sleep(call_limiter - since_last)
    last_call = time.time()
    response = requests.get(Category_Data[category][URL_FLAG], params=params, headers=headers)
    data = response.json()
    if DEBUG:
        if (response.status_code == GOOD_RESPONSE):
            print("\033[92m" + Category_Data[category][STRING_FLAG] + " Response: " + str(response.status_code) + "\033[0m")
            with open(Category_Data[category][JSON_FILE_NAME_FLAG], 'w') as fp:
                json.dump(data, fp, indent=4)
        else:
            print("\033[91m" + Category_Data[category][STRING_FLAG] + " Response: " + str(response.status_code) + "\033[0m")
    if (response.status_code == GOOD_RESPONSE):
        return data
    else:
        global try_again_time
        print("\033[91mFailed, trying again in: " + str(try_again_time) + "\033[0m")
        time.sleep(try_again_time)
        return Call_API(category, force_update=force_update, params=params, headers=headers)

def Get_Alerts (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.alerts, force_update=force_update, params = params, headers = headers)

def Get_Facilities (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.facilities, force_update=force_update, params = params, headers = headers)

def Get_Lines (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.lines, force_update=force_update, params = params, headers = headers)

def Get_Live_Facilities (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.live_facilities, force_update=force_update, params = params, headers = headers)

def Get_Predictions(force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.prediction, force_update=force_update, params = params, headers = headers)

def Get_Routes (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.route, force_update=force_update, params = params, headers = headers)

def Get_Route_Patterns (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.route_pattern, force_update=force_update, params = params, headers = headers)

def Get_Schedules (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.schedule, force_update=force_update, params = params, headers = headers)

def Get_Services (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.service, force_update=force_update, params = params, headers = headers)

def Get_Shapes (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.shape, force_update=force_update, params = params, headers = headers)

def Get_Stops (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.stop, force_update=force_update, params = params, headers = headers)

def Get_Trips(force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.trip, force_update=force_update, params = params, headers = headers)

def Get_Vehicles (force_update = False, params = default_params, headers = default_headers):
    return Call_API(Categories.vehicles, force_update=force_update, params = params, headers = headers)










def Get_Line_Names(params = default_params, headers = default_headers):
    lines = Get_Lines()
    if lines is not None:
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

def Get_ID_to_Names(params = default_params, headers = default_headers):
    routes = Get_Routes()
    if routes() is not None:
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
    if routes is not None and vehicles is not None:
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