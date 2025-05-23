import polyline
import matplotlib.pyplot as plt
import sched
import time
import API_Helper
import Shape_Helper
import Miscellaneous

TRAIN_TEXT_SIZE = 4
TRAIN_SIZE = 2
TRAIN_COLOR = "black"
TRAIN_MARKER = 'o'

STOP_TEXT_SIZE = 6
STOP_SIZE = 6
STOP_COLOR = "white"
STOP_MARKER = 'o'

update_live_map = True

def Draw_Map_With_Stations(lines, fig=None, axes=None):
    if fig is None or axes is None:
        fig, axes = plt.subplots(figsize=(15, 9))
    fig, axes = Shape_Helper.Draw_All_Lines(lines, fig, axes)
    params = {
        "filter[route]": Miscellaneous.Convert_List_To_CSV(lines)
    }
    stops = API_Helper.Get_Stops(params=params, force_update=True)
    if stops is not None:
        for stop in stops["data"]:
            long = stop["attributes"]["longitude"]
            lat = stop["attributes"]["latitude"]
            name = stop["attributes"]["name"]
            axes.plot(long, lat, marker=STOP_MARKER, color=STOP_COLOR, markersize=STOP_SIZE)
            axes.text(long, lat, name, fontsize=STOP_TEXT_SIZE)
        return fig, axes

def Draw_Map_With_Stations_Vehicles(lines, fig=None, axes=None):
    if fig is None or axes is None:
        fig, axes = plt.subplots(figsize=(15, 9))
    Draw_Map_With_Stations(lines, fig=fig, axes=axes)
    params = {
        "filter[route]": Miscellaneous.Convert_List_To_CSV(lines)
    }
    vehicles = API_Helper.Get_Vehicles(params=params, force_update=True)
    if vehicles is not None:
        for vehicle in vehicles["data"]:
            long = vehicle["attributes"]["longitude"]
            lat = vehicle["attributes"]["latitude"]
            axes.plot(long, lat, marker=TRAIN_MARKER, color=TRAIN_COLOR, markersize=TRAIN_SIZE)
    return fig, axes

def Update_Map_With_Vehicles(lines, fig, axes):
    params = {
        "filter[route]": Miscellaneous.Convert_List_To_CSV(lines)
    }
    vehicles = API_Helper.Get_Vehicles(params=params, force_update=True)
    if vehicles is not None:
        for line in axes.lines:
            if line.get_color() == TRAIN_COLOR:
                line.remove()
        for vehicle in vehicles["data"]:
            long = vehicle["attributes"]["longitude"]
            lat = vehicle["attributes"]["latitude"]
            axes.plot(long, lat, marker=TRAIN_MARKER, color=TRAIN_COLOR, markersize=TRAIN_SIZE)
    return fig, axes

def Continously_Update_Map_With_Vehicles(scheduler, lines, fig, axes):
    if update_live_map:
        try:
            fig, axes = Update_Map_With_Vehicles(lines, fig, axes)
            fig.canvas.draw()
            fig.canvas.flush_events()
            scheduler.enter(15, 1, Continously_Update_Map_With_Vehicles, (scheduler, lines, fig, axes))
        except:
            return