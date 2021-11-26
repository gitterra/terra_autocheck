from . import Ultra_Light, utils
from . import baseblock
from IPython import display
from .settings import *

#autorize = False
'''
def autorization(self):
    global user, autorize
    autorize = user.autorization()
    Start(user.HW_ID, user.content)
'''
 
def StartHomework(self):
    global user
    if user.HW_ID in [1738, 1461, 1465, 1469, 1523, 1527, 1531, 1535, 1539, 1543, 1547, 1551, 1555, 1559, 1563, 1567, 1625]:    
        Ultra_Light.Start(user)
    elif user.HW_ID == 1739:
        baseblock.lessonone.light.Start(user)
    elif user.HW_ID == 1740:
        baseblock.lessonone.pro.Start(user)
    elif user.HW_ID == 1741:
        baseblock.lessonone.ultraPro.Start(user)
    elif user.HW_ID == 1743:
        baseblock.lessontwo.light.Start(user)
    elif user.HW_ID == 1744:
        baseblock.lessontwo.pro.Start(user)
    elif user.HW_ID == 1745:
        baseblock.lessontwo.ultraPro.Start(user)
    elif user.HW_ID == 1747:
        baseblock.lessonthree.light.Start(user)
    elif user.HW_ID == 1748:
        baseblock.lessonthree.pro.Start(user)
    elif user.HW_ID == 1749:
        baseblock.lessonthree.ultraPro.Start(user)
    elif user.HW_ID == 1751:
        baseblock.lessonfour.light.Start(user)
    elif user.HW_ID == 1752:
        baseblock.lessonfour.pro.Start(user)
    elif user.HW_ID == 1753:
        baseblock.lessonfour.ultraPro.Start(user)
    elif user.HW_ID == 1755:
        baseblock.lessonfive.light.Start(user)
    elif user.HW_ID == 1756:
        baseblock.lessonfive.pro.Start(user)
    elif user.HW_ID == 1757:
        baseblock.lessonfive.ultraPro.Start(user)
    elif user.HW_ID == 1759:
        baseblock.lessonsix.light.Start(user)
    elif user.HW_ID == 1760:
        baseblock.lessonsix.pro.Start(user)
    elif user.HW_ID == 1761:
        baseblock.lessonsix.ultraPro.Start(user)
    elif user.HW_ID == 1763:
        baseblock.lessonseven.light.Start(user)
    elif user.HW_ID == 1764:
        baseblock.lessonseven.pro.Start(user)
    elif user.HW_ID == 1765:
        baseblock.lessonseven.ultraPro.Start(user)
    elif user.HW_ID == 1767:
        baseblock.lessoneight.light.Start(user)
    elif user.HW_ID == 1768:
        baseblock.lessoneight.pro.Start(user)
    elif user.HW_ID == 1769:
        baseblock.lessoneight.ultraPro.Start(user)
    elif user.HW_ID == 1771:
        baseblock.lessonnine.light.Start(user)
    elif user.HW_ID == 1772:
        baseblock.lessonnine.pro.Start(user)
    elif user.HW_ID == 1773:
        baseblock.lessonnine.ultraPro.Start(user)
    elif user.HW_ID == 1775:
        baseblock.lessonten.light.Start(user)
    elif user.HW_ID == 1776:
        baseblock.lessonten.pro.Start(user)
    elif user.HW_ID == 1777:
        baseblock.lessonten.ultraPro.Start(user)
    elif user.HW_ID == 1779:
        baseblock.lessoneleven.light.Start(user)
    elif user.HW_ID == 1780:
        baseblock.lessoneleven.pro.Start(user)
    elif user.HW_ID == 1781:
        baseblock.lessoneleven.ultraPro.Start(user)
    elif user.HW_ID == 1783:
        baseblock.lessontwelve.light.Start(user)
    elif user.HW_ID == 1784:
        baseblock.lessontwelve.pro.Start(user)
    elif user.HW_ID == 1785:
        baseblock.lessontwelve.ultraPro.Start(user)
    elif user.HW_ID == 1787:
        baseblock.lessonthirteen.light.Start(user)
    elif user.HW_ID == 1788:
        baseblock.lessonthirteen.pro.Start(user)
    elif user.HW_ID == 1789:
        baseblock.lessonthirteen.ultraPro.Start(user)
    elif user.HW_ID == 1791:
        baseblock.lessonfourteen.light.Start(user)
    elif user.HW_ID == 1792:
        baseblock.lessonfourteen.pro.Start(user)
    elif user.HW_ID == 1793:
        baseblock.lessonfourteen.ultraPro.Start(user)
    elif user.HW_ID == 1795:
        baseblock.lessonfifteen.light.Start(user)
    elif user.HW_ID == 1796:
        baseblock.lessonfifteen.pro.Start(user)
    elif user.HW_ID == 1797:
        baseblock.lessonfifteen.ultraPro.Start(user)
    elif user.HW_ID == 1799:
        baseblock.lessonsixteen.light.Start(user)
    elif user.HW_ID == 1800:
        baseblock.lessonsixteen.pro.Start(user)
    elif user.HW_ID == 1801:
        baseblock.lessonsixteen.ultraPro.Start(user)
    
        
def Start(homework_id, content):    
    global user, autorize
    # DEBUG
    user = utils.User(homework_id, content)
    user.autorization()
    #display.display(button_start)
    #button_start.disabled = False
    #button_start.on_click(StartHomework)
    StartHomework(None)

    return
    
    '''
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
            baseblock.lessonone.light.Start(user)
        autorize = False
    '''
