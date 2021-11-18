from . import Ultra_Light, utils
from .baseblock.lessonone import light
from IPython import display
from .settings import *

autorize = False

def autorization(self):
    global user, autorize
    autorize = user.autorization()
    Start(user.HW_ID, user.content)
    
def StartHomework(self):
    global user
    if user.HW_ID in [1738]:
        Ultra_Light.Start(user)
    elif user.HW_ID == 1739:
        light.Start(user)
    
        
def Start(homework_id, content):    
    global user, autorize
    # DEBUG
    user = utils.User(homework_id, content)
    user.autorization()
    display.display(button_start)
    button_start.disabled = False
    button_start.on_click(StartHomework)
    return
    
    if not autorize:
        user = utils.User(homework_id, content)    
        display.display(login_text)
        display.display(button_start)
        button_start.disabled = False
        button_start.on_click(autorization)
    else:
        if user.HW_ID in [1738]:
            Ultra_Light.Start(user)
        elif user.HW_ID == 1739:
            light.Start(user)
        autorize = False