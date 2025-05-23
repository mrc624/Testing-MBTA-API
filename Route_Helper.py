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