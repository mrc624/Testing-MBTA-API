import API_Helper
import Alert_Helper

API_Helper.Get_ID_to_Names()
API_Helper.Get_Vehicles_on_Routes_Count()
API_Helper.Get_Lines()
API_Helper.Get_Line_Names()
API_Helper.Get_Alerts()
API_Helper.Get_Facilities()

run = True

while run:
    Alert_Helper.Print_Effect_Options()
    effect = input("\nInput an Effect\n")
    if not Alert_Helper.Print_Headers(effect):
        print("Invalid\n")
    if effect == "Kill":
        run = False