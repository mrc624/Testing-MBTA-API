import API_Helper

def Get_Current_Effects():
    current_effects = [ ]
    alerts = API_Helper.Get_Alerts()
    for alert in alerts["data"]:
        if alert["attributes"]["effect"] not in current_effects:
            current_effects.append(alert["attributes"]["effect"])
    return current_effects

def Is_Valid_Effect(effect):
    return effect in Get_Current_Effects()

def Format_Effect_As_Text(effect: str):
    return effect.replace("_", " ").title()

def Format_Effect_As_System(effect: str):
    return effect.replace(" ", "_").upper()

def Print_Effect_Options():
    for effect in Get_Current_Effects():
        print(Format_Effect_As_Text(effect))

def Print_Effect_Count(effect=None): #still needs to be coded for specific effect
    if effect == None:
        effect_count = { }
        alerts = API_Helper.Get_Alerts()
        for alert in alerts["data"]:
            alert_effect = alert["attributes"]["effect"]
            if alert_effect in effect_count:
                curr_count = effect_count[alert_effect]
                new_count = curr_count + 1
                effect_count[alert_effect] = new_count
            else:
                effect_count[alert_effect] = 1
        for curr_effect in effect_count:
            print(Format_Effect_As_Text(curr_effect) + ": " + str(effect_count[curr_effect]))

def Print_Headers(effect):
    alerts = API_Helper.Get_Alerts()
    effect = Format_Effect_As_System(effect)
    if effect in Get_Current_Effects():
        for alert in alerts["data"]:
            if alert["attributes"]["effect"] == effect:
                print("\n" + alert["attributes"]["header"] + "\n")
        return True
    else:
        return False
    
def View_Alert_Data():
    run = True
    while run:
        Print_Effect_Options()
        effect = input("\nInput an Effect\n")
        if not Print_Headers(effect):
            print("Invalid\n")
        else:
            run = False