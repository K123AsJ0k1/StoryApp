from app import app

def create_misc(*attributes):
    misc = ""
    first_time = True
    
    for attribute in attributes:
        if first_time:
            misc = attribute
            first_time = False
            continue
        misc = misc + "," + attribute
        
    return misc 
