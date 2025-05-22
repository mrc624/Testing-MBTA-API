import matplotlib.pyplot as plt
import sched
import time
import threading
import Shape_Helper
import API_Helper
import Alert_Helper
import Shape_Helper
import Map_Helper

#lines = "Green-B,Green-C,Green-D,Green-E,Blue,Red,Orange,Silver"
lines = "Orange","Red","Blue","Green-B","Green-C","Green-D","Green-E"
fig, axes = Map_Helper.Draw_Map_With_Stations_Vehicles(lines)
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(0, 1, Map_Helper.Continously_Update_Map_With_Vehicles, (scheduler, lines, fig, axes))
threading.Thread(target=scheduler.run, daemon=True).start()

plt.show()

"""
run = True
while run:
    Alert_Helper.Print_Effect_Options()
    effect = input("\nInput an Effect\n")
    if not Alert_Helper.Print_Headers(effect):
        print("Invalid\n")
    if effect == "Kill":
        run = False
        """