import os
import json
import requests
from dotenv import load_dotenv

load_dotenv("key.env")

key = str(os.getenv('MBTA_API_KEY'))

print("\n Key: " + key + "\n")

url = "https://api-v3.mbta.com"
vehicles_url = url + "/vehicles"
routes_url = url + "/routes"

params = { }

headers = {
    "x-api-header":key
}

response = requests.get(routes_url, params=params, headers=headers)
print("Routes Response: " + str(response.status_code))
routes = response.json()

with open('routes.json', 'w') as fp:
    json.dump(routes, fp, indent=4)


response = requests.get(vehicles_url, params=params, headers=headers)
print("Vehicles Response: " + str(response.status_code))
vehicles = response.json()

with open('vehicles.json', 'w') as fp:
    json.dump(vehicles, fp, indent=4)

route_id_name = { }

for route in routes["data"]:
    route_id = route["id"]
    route_name = route["attributes"]["long_name"]
    route_id_name[route_id] = route_name

with open('routes_id_name.json', 'w') as fp:
    json.dump(route_id_name, fp, indent=4)

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

with open('vehicles_on_route_count.json', 'w') as fp:
    json.dump(vehicles_on_route_count, fp, indent=4)

vehicles_on_route_count_long = { }

for id in route_id_name:
    count = vehicles_on_route_count[id]
    vehicles_on_route_count_long[route_id_name[id]] = count
    print("run")

with open('vehicles_on_route_count_long.json', 'w') as fp:
    json.dump(vehicles_on_route_count_long, fp, indent=4)






#with open('result.json', 'w') as fp:
#    json.dump(data, fp, indent=4)
