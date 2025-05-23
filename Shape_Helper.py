import API_Helper
import Miscellaneous
import polyline
import matplotlib.pyplot as plt




import json

def Draw_All_Lines(routes_to_draw, fig, axes):
    params = {
        "filter[route]": Miscellaneous.Convert_List_To_CSV(routes_to_draw)
    }
    routes = API_Helper.Get_Routes()
    trips = API_Helper.Get_Trips(params=params)
    shapes = API_Helper.Get_Shapes(params=params)
    vehicles = API_Helper.Get_Vehicles(params=params)
    trip_id_color = { }
    for vehicle in vehicles["data"]:
        trip_id = vehicle["relationships"]["trip"]["data"]["id"]
        if trip_id not in trip_id_color:
            for route in routes["data"]:
                if route["id"] == vehicle["relationships"]["route"]["data"]["id"]:
                    trip_id_color[trip_id] = route["attributes"]["color"]
    shape_id_color = { }
    for trip_id in trip_id_color:
        shape_id = 0
        for trip in trips["data"]:
            if trip["id"] == trip_id:
                shape_id = trip["relationships"]["shape"]["data"]["id"]
        if shape_id not in shape_id_color and shape_id != 0:
            shape_id_color[shape_id] = trip_id_color[trip_id]   
    for shape in shapes["data"]:
        if shape["id"] in shape_id_color:
            cords = polyline.decode(shape["attributes"]["polyline"])
            lat, long = zip(*cords)
            axes.plot(long, lat, color="#" + shape_id_color[shape["id"]])
    return fig, axes

def Draw_Polyline(encoded):
    cords = polyline.decode(encoded)
    long, lat = zip(*cords)
    plt.figure(figsize=(10, 6))
    plt.plot(long, lat, marker='o')
    plt.title("Decoded Polyline Path")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()