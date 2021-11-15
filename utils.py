from IPython.core.display import HTML
from IPython import display
from .settings import *
import requests

class Keywords():
    def __init__(self, vars_):
        self.builtInFunctions = set(['abs',       'aiter',    'all',          'any',         'anext',      'ascii',   'bin',        'bool',       'breakpoint', 'bytearray',
                                     'bytes',     'callable', 'chr',          'classmethod', 'compile',    'complex', 'delattr',    'dict',       'dir',        'divmod',
                                     'enumerate', 'eval',     'exec',         'filter',      'float',      'format',  'frozenset',  'getattr',    'globals',    'hasattr',
                                     'hash',      'help',     'hex',          'id',          'input',      'int',     'isinstance', 'issubclass', 'iter',       'len', 
                                     'list',      'locals',   'map',          'max',         'memoryview', 'min',     'next',       'object',     'oct',        'open', 
                                     'ord',       'pow',      'print',        'property',    'range',      'repr',    'reversed',   'round',      'set',        'setattr', 
                                     'slice',     'sorted',   'staticmethod', 'str',         'sum',        'super',   'tuple',      'type',       'vars',       'zip'])
        self.variables = vars_
        self.error = '<p><b><font color="#880000">Ошибка. Вы создали одну или несколько переменных с именем встроенной функции:</font></b></p>'
        self.information = '<p>Исправьте имена переменных и повторите попытку <br> <i>\
                            </p><a href="https://colab.research.google.com/drive/1kUQVE_vTJZEiNJ5yt0Zgg0MRVYslY4b4?usp=sharing"\
                            target="_blank">База знаний | Почему нельзя использовать имена встроенных функций в качестве переменных | УИИ</a>'

    def check(self) -> bool:
        intersection_func = self.builtInFunctions & set(self.variables)
        if len(intersection_func) > 0:
            list_func = ''
            for func in intersection_func:
                list_func += f'<b>&nbsp;&nbsp;&nbsp;&nbsp;{func}</b><br>'
                del self.variables[func]
            display.display(HTML(self.error + list_func + self.information))
            return False
        return True
        
class User():
    def __init__(self, hw_id):
        self.login = ''
        self.id = -1
        self.HW_ID = hw_id
        pass
        
    def autorization(self):
        # Деактивация кнопки
        button_start.disabled = True
        # Список параметров, отправляемых на сервер
        param = {'login': login_text.value,
                 'hw_id': self.HW_ID}
        # Проверка ответов пользователя на сервере
        data = requests.get(os.path.join(SERVER, PAGE_LOGIN), 
                            params=param)  
        if data.json()['result']==-1:
            display.clear_output(wait=True)
            error_programm(f'Указанный email: {login_text.value} не найден!')        
            print('Проверьте правильность введенных данных и повторите попытку')
            button_start.disabled = False
            return False
        elif data.json()['result']==-2:
            display.clear_output(wait=True)
            error_programm(f'В Вашей учебной программе нет данного домашнего задания!')
            print('Обратитесь к куратору для решения данной проблемы')
            button_start.disabled = False
            return False
        else:
            self.login = login_text.value
            self.id = data.json()['result']
            return True 