import API_Helper
import Alert_Helper

API_Helper.Refresh()

run = True

while run:
    Alert_Helper.Print_Effect_Options()
    effect = input("\nInput an Effect\n")
    if not Alert_Helper.Print_Headers(effect):
        print("Invalid\n")
    if effect == "Kill":
        run = False