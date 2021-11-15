from . import Ultra_Light, BaseBlock_1_PythonSyntax, utils

autorize = False
def autorization(self):
    global user, autorize
    autorize = user.autorization()
    if not autorize:
        Start(user.HW_ID)
        
def Start(HW_id):    
    user = utils.User(hwid)    
    display.display(login_text)
    display.display(button_start)
    button_start.disabled = False
    button_start.on_click(autorization)
    if autorize:
        if HW_id in [1738]:
            Ultra_Light.Start(HW_id, user)
        elif HW_id == 1739:
            BaseBlock_1_PythonSyntax.Start(HW_id, user)