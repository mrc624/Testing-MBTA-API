import time
import json
from datetime import datetime
import API_Helper

OUTBOUND_DIRECTION = 0
INBOUND_DIRECTION = 1

OUTBOUND_FLAG = "out"
INBOUND_FLAG = "in"
ARRIVAL_FLAG = "arrive"
UNCERTAINTY_FLAG = "uncertain"
TIME_FLAG = "time"
DEPARTURE_FLAG = "depart"

def Get_Next_Arrival_Departure_Data(stop:str, route:str):
    data = {
        INBOUND_FLAG: {
            ARRIVAL_FLAG: {
                TIME_FLAG: None,
                UNCERTAINTY_FLAG: None
            },
            DEPARTURE_FLAG: {
                TIME_FLAG: None,
                UNCERTAINTY_FLAG: None
            }
        },
        OUTBOUND_FLAG: {
            ARRIVAL_FLAG: {
                TIME_FLAG: None,
                UNCERTAINTY_FLAG: None
            },
            DEPARTURE_FLAG: {
                TIME_FLAG: None,
                UNCERTAINTY_FLAG: None
            }
        }
    }
    params = {
    "filter[stop]": stop,
    "filter[route]": route
    }
    predictions = API_Helper.Get_Predictions(params=params)

    earliest, uncertainty = Find_Earlist_Departure(predictions, INBOUND_DIRECTION)
    data[INBOUND_FLAG][DEPARTURE_FLAG][TIME_FLAG] = earliest
    data[INBOUND_FLAG][DEPARTURE_FLAG][UNCERTAINTY_FLAG] = uncertainty

    earliest, uncertainty = Find_Earlist_Departure(predictions, OUTBOUND_DIRECTION)
    data[OUTBOUND_FLAG][DEPARTURE_FLAG][TIME_FLAG] = earliest
    data[OUTBOUND_FLAG][DEPARTURE_FLAG][UNCERTAINTY_FLAG] = uncertainty

    earliest, uncertainty = Find_Earlist_Arrival(predictions, INBOUND_DIRECTION)
    data[INBOUND_FLAG][ARRIVAL_FLAG][TIME_FLAG] = earliest
    data[INBOUND_FLAG][ARRIVAL_FLAG][UNCERTAINTY_FLAG] = uncertainty

    earliest, uncertainty = Find_Earlist_Arrival(predictions, OUTBOUND_DIRECTION)
    data[OUTBOUND_FLAG][ARRIVAL_FLAG][TIME_FLAG] = earliest
    data[OUTBOUND_FLAG][ARRIVAL_FLAG][UNCERTAINTY_FLAG] = uncertainty
    if API_Helper.DEBUG:
        with open(API_Helper.DEBUG_FOLDER + "next_arrival_departure.json", 'w') as fp:
            json.dump(data, fp, indent=4)
    return data


def Find_Earlist_Departure(predictions, direction):
    earliest = None
    uncertainty = None
    for prediction in predictions["data"]:
        if prediction["attributes"]["direction_id"] == direction:
            if (earliest is None):
                if prediction["attributes"]["departure_time"] != None:
                    earliest = prediction["attributes"]["departure_time"]
                    uncertainty = prediction["attributes"]["departure_uncertainty"]
            else:
                if prediction["attributes"]["departure_time"] != None:
                    if datetime.fromisoformat(str(prediction["attributes"]["departure_time"])) < datetime.fromisoformat(str(earliest)):
                        earliest = prediction["attributes"]["departure_time"]
                        uncertainty = prediction["attributes"]["departure_uncertainty"]
    return earliest, uncertainty

def Find_Earlist_Arrival(predictions, direction):
    earliest = None
    uncertainty = None
    for prediction in predictions["data"]:
        if prediction["attributes"]["direction_id"] == direction:
            if (earliest is None):
                if prediction["attributes"]["arrival_time"] != None:
                    earliest = prediction["attributes"]["arrival_time"]
                    uncertainty = prediction["attributes"]["arrival_uncertainty"]
            else:
                if prediction["attributes"]["arrival_time"] != None:
                    if datetime.fromisoformat(str(prediction["attributes"]["arrival_time"])) < datetime.fromisoformat(str(earliest)):
                        earliest = prediction["attributes"]["arrival_time"]
                        uncertainty = prediction["attributes"]["arrival_uncertainty"]
    return earliest, uncertainty
