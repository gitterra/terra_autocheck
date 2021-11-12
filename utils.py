from termcolor import colored
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
        self.error = colored('Ошибка. Вы создали одну или несколько переменных с именем встроенной функции:', color='red', attrs=['bold'])
        self.information = '\nИсправьте имена переменных и повторите попытку' \
                            +'\n\x1B[3mПочему нельзя использовать имена встроенных функций в качестве переменных:\x1B[3m \n' \
                            + colored('https://colab.research.google.com/drive/16B6zPNQ1rt-RI-F_aKxxz3v87GM9x8E-?usp=sharing', color='blue')                             

    def check(self):
        intersection_func = self.builtInFunctions & set(self.variables)
        if len(intersection_func) > 0:
            print(self.error)          
            for func in intersection_func:
                print(colored(f'  {func}', attrs=['bold']))
                del self.variables[func]
            print(self.information)