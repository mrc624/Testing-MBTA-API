import API_Helper

LONG_NAME_FLAG = "long"
SHORT_NAME_FLAG = "short"

def Get_ID_Names():
    routes = API_Helper.Get_Routes()
    if routes is not None:
        data = { }
        for route in routes["data"]:
            data[route["id"]] = {
                LONG_NAME_FLAG: route["attributes"]["long_name"],
                SHORT_NAME_FLAG: route["attributes"]["short_name"]
            }
        return data
    
def Get_List():
    routes = API_Helper.Get_Routes()
    if routes is not None:
        list = [ ]
        for route in routes["data"]:
            list.append(route["attributes"]["name"])
        return list

def Get_List_Filter_Type(type:str):
    routes = API_Helper.Get_Routes()
    if routes is not None:
        list = [ ]
        for route in routes["data"]:
            if route["attributes"]["description"] == type:
                list.append(route["id"])
    return list

def Get_Route_Types():
    routes = API_Helper.Get_Routes()
    types = [ ]
    for route in routes["data"]:
        if route["attributes"]["description"] not in types:
            types.append(route["attributes"]["description"])
    return types

def Type_Is_Valid(type):
    routes = API_Helper.Get_Routes()
    for route in routes["data"]:
        if route["attributes"]["description"] == type:
            return True
    return False
