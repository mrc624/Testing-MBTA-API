import matplotlib.pyplot as plt
import sched
import time
import threading
import Shape_Helper
import API_Helper
import Alert_Helper
import Shape_Helper
import Map_Helper

run = True
while run:
    choice = input("Options:\n1: Live Map\n2: Alerts\n9: Kill\n")
    if choice == "1" or choice == "Live Map":
        Map_Helper.update_live_map  = True
        lines = "Orange","Red","Blue","Green-B","Green-C","Green-D","Green-E"
        fig, axes = Map_Helper.Draw_Map_With_Stations_Vehicles(lines)
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(0, 1, Map_Helper.Continously_Update_Map_With_Vehicles, (scheduler, lines, fig, axes))
        threading.Thread(target=scheduler.run, daemon=True).start()
        plt.show()
        Map_Helper.update_live_map = False
    elif choice == "2" or choice == "Alerts":
        Alert_Helper.View_Alert_Data()
    elif choice == "9" or choice == "Kill":
        run = False