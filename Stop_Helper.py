import API_Helper

def Get_List():
    stops = API_Helper.Get_Stops()
    if stops is not None:
        list = [ ]
        for stop in stops["data"]:
            list.append(stop["attributes"]["name"])
        return list
    
def Get_List_Filter_Route(route:str):
    params = {
        "filter[route]": route
    }
    stops = API_Helper.Get_Stops(params=params)
    if stops is not None:
        list = [ ]
        for stop in stops["data"]:
            list.append(stop["attributes"]["name"])
        return list


def Get_ID_From_Name(name):
    stops = API_Helper.Get_Stops()
    if stops is not None:
        for stop in stops["data"]:
            if stop["attributes"]["name"] == name:
                return stop["id"]
            
def Name_Is_Valid(name):
    stops = API_Helper.Get_Stops()
    if stops is not None:
        for stop in stops["data"]:
            if stop["attributes"]["name"] == name:
                return True
    return False