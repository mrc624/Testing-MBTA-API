import matplotlib.pyplot as plt
import sched
import time
import threading
import Shape_Helper
import API_Helper
import Alert_Helper
import Shape_Helper
import Map_Helper
import Route_Helper

run = True
while run:
    choice = input("Options:\n1: Live Map\n2: Alerts\n9: Kill\n")
    if choice == "1" or choice == "Live Map":
        route_selection = True
        while route_selection:
            choice = input("How would you like to view the routes?\n1: IDs and Short Names\n2: IDs and Long Names\n")
            if choice == "1" or choice == "2":
                route_selection = False
        ID_Names = Route_Helper.Get_ID_Names()
        num = 0
        for id in ID_Names:
            print(str(id) + ": ", end="")
            if choice == "1":
                print(ID_Names[id][Route_Helper.SHORT_NAME_FLAG])
            else:
                print(ID_Names[id][Route_Helper.LONG_NAME_FLAG])
        print("Input the routes by entering the ID\nEnter each one on it's own line\nEnter \"All\" to view all\nEnter \"Done\" when complete")
        route_selection = True
        routes = [ ]
        while route_selection:
            route = input().title()
            if route in routes:
                print("Route already added")
            elif route in ID_Names:
                routes.append(route)
            elif route == "Done":
                route_selection = False
            elif route == "All":
                for id in ID_Names:
                    if id not in routes:
                        routes.append(id)
                route_selection = False
            else:
                print("Invalid input, enter \"Done\" to be complete")
                print("Current routes added:")
                for route in routes:
                    print(route)
        Map_Helper.update_live_map  = True
        fig, axes = Map_Helper.Draw_Map_With_Stations_Vehicles(routes)
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(0, 1, Map_Helper.Continously_Update_Map_With_Vehicles, (scheduler, routes, fig, axes))
        threading.Thread(target=scheduler.run, daemon=True).start()
        plt.show()
        Map_Helper.update_live_map = False
    elif choice == "2" or choice == "Alerts":
        Alert_Helper.View_Alert_Data()
    elif choice == "9" or choice == "Kill":
        run = False