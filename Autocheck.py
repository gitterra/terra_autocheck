from . import Ultra_Light, BaseBlock_1_PythonSyntax, utils
from IPython import display
from .settings import *

autorize = False

def autorization(self):
    global user, autorize
    autorize = user.autorization()
    Start(user.HW_ID, user.content)
        
def Start(homework_id, content): 
    global user, autorize
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
            BaseBlock_1_PythonSyntax.Start(user)
        autorize = False