# Homework ID 1749
from IPython import display as dsp
from ... import utils

'''

Здесь Ваши функции автопроверки

'''


#
# ОБЯЗАТЕЛЬНЫЙ БЛОК
#

def check_homework(self):
    dsp.clear_output(wait=True)
    global user

    '''

    Здесь код вызова функций автопроверки ДЗ

    '''

    # Проверка на пересечение имён
    # Пока оформляем это в качестве рекомендации (НЕ ОШИБКА)
    # Просто оставляйте этот код здесь
    keywords = utils.Keywords(user.content)
    keywords.check()


def Start(_user):
    global user
    user = _user
    check_homework(None)