import os
from random import randint
from uuid import uuid4 as uuid
from subprocess import run, STDOUT, PIPE, Popen
import numpy as np
import re
import importlib
from io import StringIO 
import sys
import types
import inspect
from termcolor import colored
from tqdm.notebook import tqdm
import runpy

def test__isStringContains(wholeString, word):
    new_list = ['=','(',')','{','}','+','.',',','>','<','\'','\"','?','\\','*','-','@','%','&','|','/',':','!','~','`','#']
    for i in new_list:
        wholeString = wholeString.replace(i, ' ')
    new_wholeString = wholeString.split(' ')
    new_wholeString = [i for i in new_wholeString if i!='']
    return word in new_wholeString

def test__reset_vars():
    test__func_text = ''' 
def test__AnyFunc(func,*args, **kwargs):
    if args or kwargs:
        return eval(func)(*args, **kwargs)
    else:
        return eval(func)
    '''

    with open('reset.py','w') as f:
        f.write(test__func_text)
    from reset import test__AnyFunc
    import builtins
    all_vars = test__AnyFunc('dir')(builtins)
    for i in all_vars:
        globals()[i] = test__AnyFunc(i)

main_path = '/content/sample_data/work'
student_path = os.path.join(main_path, 'student')
test_path = os.path.join(main_path, 'test')

class test__Capturing(list):
    ''' 
        Класс "ловит" все выходы print, что были запущены в коде.
    '''
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def test__reserve_names(some_dict):
    new_dict = []
    from reset import test__AnyFunc
    import builtins
    all_vars = test__AnyFunc('dir')(builtins)
    keywords = test__AnyFunc('dir')(builtins)
    new_one = some_dict.keys()-(some_dict.keys() - keywords)
    for i in new_one:
        curr = f'У вас в коде присутсвует переменная с зарезервированным именем \'{i}\'.\n\
Переименуйте её в другое имя и перезапустите ноутбук для  избежания дополнительных ошибок.\n'
        new_dict.append(curr)
    return new_dict
def test__filter_by_type(some_list, some_type):
    new_list = []
    for var in some_list:
        if isinstance(var, some_type):
            new_list.append(var)
    return new_list
def test__be_not(some_dict, vars):
    some_texts = []
    for key, value in some_dict.items():
        curr_text = f'Отсутсвует {value[0]} \'{key}\'. Перепроверьте название или тип.'
        if key in vars:
            if isinstance(vars[key], value[1]):
                pass
            else:
                some_texts.append(curr_text)
        else:
            some_texts.append(curr_text)
    return some_texts
def test__new_text_with_cond(name_list, text):
    new_text = ''
    some_list = ''
    for curr_row in text.split('\n'):
        if 'test__input_' in curr_row:
            for curr_key, curr_value in name_list.items():
                if curr_key in curr_row:
                    val = re.findall(r'str\(.+\)', curr_row)[0]
                    if val:
                        curr_inp_text = f'{name_list[curr_key][0]} = {val}\n'
                    else:
                        curr_inp_text=''
                    if curr_value[1]:
                        some_list+=curr_inp_text
                    else:
                        some_list = curr_inp_text + some_list
        new_text += f'{curr_row}\n'
    new_text += f'{some_list}\n'
    return new_text
def test__collect_fragments(In,all_need, dont_need = []):

    '''
    Функция нахождения всех ячеек по ключевым строкам с фильтрацией.

        Вход:
            In - История запуска ячеек в ноутбуке
            need - Ключевые слова, по которым находятся все ячейки
            dont_need - Слова-фильтры, которые исключают лишнние ячейки
        
        Выход:
            fragments - Список всех найденных ячеек
    '''

    names_for_list = test__filter_by_type(all_need,str)
    all_names = []
    for curr_name in names_for_list:
        try:
            curr_word = test__find_reqs_args(In,curr_name)+'\n'
            all_names.append(curr_word)
        except:
            pass

    need = test__filter_by_type(all_need,list)

    fragments = ['' for text in all_need]  # Создаем список длиной - кол-во элементов need, ведь мы можем искать сразу несколько ячеек. 
    for fragment in In:  # Проходимся по всей истории запуска
        for idx, text in enumerate(need):  # Проходимся по всем элементам fragment
            curr_text = list(filter(lambda x: isinstance(x,str), text))
            curr_lists = list(filter(lambda x: isinstance(x,list), text))
            curr_sets = list(filter(lambda x: isinstance(x,set), text))

            sets_answer = True
            if curr_lists:
                curr_lists = curr_lists[0]
            else:
                curr_lists = ['']
            if curr_sets:
                curr_sets = list(curr_sets[0])
                for curr_i in curr_sets:
                    sets_answer *= test__isStringContains(fragment, curr_i)

            else:
                curr_sets = True
            if np.array([code in fragment for code in curr_text]).all() and np.array([dont not in fragment for dont in dont_need]).all() and np.array([code in fragment for code in curr_lists]).any() and sets_answer:  # Ищим и фильтруем
                fragments[idx] = fragment.strip()  # Устанавливем последний найденный запуск на idx-ое место списка fragment. 
    fragments =list(set(fragments))
    fragments =list(filter(lambda x: x!='', fragments)) # Удаляем все пустые фильтры
    all_names.extend(fragments)
    return all_names
def test__save_code(tag, found_code, args4test='', add_args = [], input_replacment = 'str(int(float(3.1415926535)))'):

    '''
    Функция сохранения всего подаваемого текста в .py файл.

        Вход:
            tag - Номер задания(нужен для записи названия файла)
            found_code - Весь, найденный код студента
            args4test - Дополнительный код, который потребуется для тестов
            add_args - Дополнительный код, на случай, если в коде участника
                присутсвуют аргументы или функции, что он определил в других
                ячейках, но не в этой.
        
        Выход:
            Возвращает выход функции test__try_task
    '''
    if not os.path.exists(os.path.join(student_path)):
        os.makedirs(os.path.join(student_path))
    student_path_curr = os.path.join(student_path,f'student__{tag}.py')

    if not os.path.exists(os.path.join(test_path)):
        os.makedirs(os.path.join(test_path))
    test_path__test = os.path.join(test_path,f'test__{tag}.py')

    sys.path.insert(1, os.path.join(student_path))
    sys.path.insert(1, os.path.join(test_path))

    rows = []
    row_idx = 0
    for idx in range(len(found_code)):
        if 'input(' in found_code[idx]:
            row_list = []
            for row in found_code[idx].split('\n'):
                if 'input(' in row:
                    row_text = re.findall(r'input\([\'\"a-z].+[\'\"]\)', row)
                    if row_text:
                        row_text = row_text[0].replace('input', 'str')
                        row_all = f'test__input_{row_idx} = {row_text}'
                        rows.append(row_all)
                        row_idx+=1 
                    else:
                        row_all = f'test__input_{row_idx} = str(\'\')'
                        rows.append(row_all)
                        row_idx+=1   
    for idx in range(len(found_code)):
        found_code[idx] = re.sub(r'input\([\'\"a-z].+[\'\"]\)', input_replacment ,found_code[idx])
        found_code[idx] = re.sub(r'input\(\)',input_replacment, found_code[idx])

    for idx in range(len(add_args)):
        add_args[idx] = re.sub(r'input\([\'\"a-z].+[\'\"]\)',input_replacment, add_args[idx])
        add_args[idx] = re.sub(r'input\(\)',input_replacment, add_args[idx])


    with open(student_path_curr, 'w') as f:  # Создаём файл, в который будем записывать данные
        for add in add_args[::-1]:  # Сначала записываем все добавочные переменные и функции для корректной работы кода
            f.write(add+'\n')
        for text in found_code: # Записываем код участника
            f.write(text+'\n')

    with open(test_path__test, 'w') as f:
        f.write(args4test+'\n') # Записываем наш код для тестов
        for some_row in rows:
            f.write(f'{some_row}\n')

    return test__try_task(tag)
def test__find_number(*args):

    '''
    Функция поиска числа  в кортёже. Нужно для определения текущего задания.

        Вход:
            args - Кортёж, в котором присутвует номер

        Выход:
            number_task - Номер задания.
    '''

    all_args = np.array(*args)  # Превращаем кортёж в numpy массив для работы с масками
    type_args = list(map(type, *args))  # Получаем списоок типов всех элементов массива
    mask_types = [i==int for i in type_args]  # Получаем маску для поиска числа
    number_task = int(all_args[mask_types][0])  # Получаем число

    return number_task
def test__reload_import(func):

    '''
    Декоратор для переимпорта модуля
    '''

    def test__inner_func(*args,**kwargs):
        number_task = test__find_number(args)
        if f'student__{number_task}' in sys.modules:
            del sys.modules[f'student__{number_task}']

        return func(*args,**kwargs)

    return test__inner_func
@test__reload_import
def test__try_task(tag):

    '''
        Функция пытается импортировать модуль. Если она встречает ошибку, что какой-то
    аргумент отсутсвует(name 'argument' is not defined), то функция возвращает имя этой переменной.
    В противном случае она возращает значение по умолчанию - None.

        Вход:
            tag - Номер текущего задания
        
        Выход:
            Или None, или имя неопределённой переменной(функции).
    '''


    try:
        with test__Capturing() as output:  # Просто поставил "ловушку" для всех print функций, чтобы на вывод никак не влияло
            module = importlib.import_module(f'student__{tag}')  # Пытаемся импортировать модуль
    except NameError as name_err:  # Если ловим ошибку, то ищем там переменную и возращаем её.
        return re.findall(r'\'\w+\'', str(name_err))[0].replace('\'','')
def test__find_reqs_args(In,text):

    '''
        Функция ищет переменную или функцию во всей истории запусков по одному
    только известному слову. В случае нахождения - возвращает полностью ячейку
    в которой создание переменной(функции) было найдено. Если слово не найдено - 
    будет ошибка с тем, что переменная неопределена.

        Вход:
            In - История запусков
            text - Слово неопределённой переменной

        Выход:
            result - Код ячейки, в которой последний раз создавалась переменная(функция)
            В противном случае ошибка.

    '''
    dont_need = test__all_excepts()
    result = None # Создаём место под код ячейку
    for fragment in In:  # Проходимся по истории запусков
        fragment_new = re.sub(r'\(.+\)','',fragment) # Убираем в ячейке все данные, что
            # есть в скобках, чтобы избежать путаницу создания переменной и
            # использользованием параметра в функции/класса.
        if np.array([dont not in fragment for dont in dont_need]).all():
            fragment_new = fragment_new.replace(' ','') # Текущую ячейку очищаем от всех пробелов
            fragment__rows = fragment.split('\n')
            for curr_frag_new in fragment_new.split('\n'):
                if  curr_frag_new.startswith(f'{text}='):  # Смотрим, есть ли в ней создание переменной
                    result = f'\n{fragment}'  # Если есть - записываем в result код ячейки
                elif curr_frag_new.startswith(f'def{text}('):  # Смотрим, есть ли в ячейке функция с таким именем
                    result = f'\n{fragment}'  # Если есть - записываем в result код ячейки
                elif curr_frag_new.startswith(f'class{text}('):  # Смотрим, есть ли в ячейке класс с таким именем
                    result = f'\n{fragment}'  # Если есть - записываем в result код ячейки
                else:
                    for new_row in fragment__rows:
                        new_new_row = re.sub(r'[, ]+',' ', new_row)
                        row__split = new_new_row.split(' ')
                        if 'import' in row__split and text in row__split:
                            result = f'\n{new_row}'
    if not result:  # Если ничего не записалось - выводим ошибку.
        raise Exception(f'Переменная \'{text}\' не определена.')
    else:
        return result  
def test__all_excepts():

    '''
        Функция, что содержит в себе лист со всеми словами-фильтрами, которые
    нельзя встречать в коде студента

        Вход:
            Ничего 
        
        Выход:
            dont_need - Список всех слов-фильтров 

    '''
    dont_need = ['test__']
    return dont_need
def test__find_by_type(old_dict, type_):
    new_dict = {}
    for key, value in old_dict.items():
        if isinstance(value, type_):
            new_dict[key] = value
    return new_dict
def test__import_module(In,tag):
    '''
        Функция импорта модуля и "ловли" всех выходов print функции.
        
        Вход:
            tag - Номер текущего задания.
        
        Выход:
            output - Все выходы print функции
            module - Имопртированный модуль текущего .py файла, что мы выбрали.
            all_vars - Все переменные в модуле
            text - Весь модуль в виде текста
         
    '''
    student_path__curr = os.path.join(student_path,f'student__{tag}.py')
    if f'student__{tag}' in sys.modules:
        del sys.modules[f'student__{tag}']
    with test__Capturing() as student__output:
        module = importlib.import_module(f'student__{tag}')
        execfile(student_path__curr)
    
    text  = inspect.getsource(module)

    all_vars = {i: module.__dict__[i] for i in module.__dict__.keys() if not (i.startswith('__'))}
    
    student_dict = {'module':module,'variables':all_vars,"text":text, 'output':student__output}

    test_path_curr = os.path.join(test_path,f'test__{tag}.py')
    if f'test__{tag}' in sys.modules:
        del sys.modules[f'test__{tag}']
    
    test__module_name = f'test__{tag}'

    test__module, test__output = test__add_for_test(In, test__module_name, student_dict['variables'])
    test__text = inspect.getsource(test__module)

    test__vars = {i: test__module.__dict__[i] for i in test__module.__dict__.keys() if not (i.startswith('__'))}





    test__dict = {'module':test__module,'variables':test__vars,"text":test__text, 'output':test__output}
    return student_dict, test__dict
def test__add_for_test(In,module_name, student_vars):
    path = test_path
    name = module_name
    test_path_curr = os.path.join(path, name+'.py')

    with open(test_path_curr, 'r') as f:
        text = f.read()
    while True:
        try:
            module = test__reload_module(test_path_curr, text, name)
            with test__Capturing() as out:
                execfile(test_path_curr)
                return module, out
        except NameError as name_err:
            name_err = re.findall(r'\'\w+\'', str(name_err))[0].replace('\'','')
            if name_err in student_vars:
                try:
                    curr_text = inspect.getsource(student_vars[name_err])+'\n'
                except TypeError: 
                    curr_answer = student_vars[name_err]
                    if not isinstance(curr_answer, (int, float)):
                        curr_answer = f'\'{curr_answer}\''

                    curr_text = f'{name_err} = {curr_answer}\n'
                text = curr_text+text
            else:
                curr_text = test__find_reqs_args(In, name_err)
                text = curr_text+text
            module = test__reload_module(test_path_curr, text, name)

def test__task(In, tag):
    test__reset_vars()
    '''
        Функция сочетает в себе все предыдущие функции в "одну" кнопку.

        Вход:
            In - История запусков ячеек
            tag - Номер задания

        Выход:
            Выход функции test__output_comp_{текущее задание}
    '''

    need, dont_need, args4test,requeriment_vars, input_replacment = test__item_task(tag)  # Собираем все ключевые слова, фильтры и коды для тестов
    found_code = test__collect_fragments(In, need, dont_need).copy()  # По ключевым словам и фильтрам находим все ячейки студента
    if not found_code:  # Если студент не запустил свой код или невыполнил - выводим сообщение.
        if not requeriment_vars:    
            print(f'На {tag} задание не найдено решение.')
            return False
        else:
            curr = ' '.join(found_code)
            for key, value in requeriment_vars.items():
                if key not in curr:
                    print(f'Отсутсвует {value[0]} \'{key}\'. Перепроверьте название или тип.')
            return False
    found_code_copy = found_code.copy()
    add_args = []  # Сюда будут добавлятся ячейки кода при возникновения ошибки - "name 'argument' is not definded"
    error_word = test__save_code(tag, found_code_copy, args4test, add_args, input_replacment)  # Находим имя аругмента, который требовался, но не был определён в ячейке студента
    while error_word:  # Если слово с ошибкой есть - запускаем цикл, в противном случае цикл не будет работать
        found_code_copy = found_code.copy()
        find_it = test__find_reqs_args(In, error_word)  # По слову в истории ищем ячейку с определением этой переменной
        add_args.append(find_it)  # Добавляем в список ячейку
        error_word = test__save_code(tag, found_code_copy, args4test, add_args, input_replacment)  # Пересоздаём файл и пытаемся снова "словить" ошибку, если будет такова
    student_dict, test__dict = test__import_module(In,tag)  # На готовый код импортируем и "ловим" все print выводы.
    all_vars = student_dict['variables']
    
    test__ress = test__reserve_names(all_vars)
    if test__ress:
        for test__curr in test__ress:
            print(colored(test__curr, 'red'))
        return False
     
    
    check_for_reqs = test__be_not(requeriment_vars, student_dict['variables'])
    if check_for_reqs:
        for i in check_for_reqs:
            print(f'{i}')
        return False
    
    
    return globals()[f'test__output_comp_{tag}'](student_dict, test__dict, input_replacment, In)  # Передаём аргументы в нужную функцию.

def test__update_module(In, module, func_name, *args, **kwargs):
    path = student_path
    name = module.__name__
    file_path = os.path.join(path, name+'.py')
    with open(file_path,'r') as f:
        text = f.read()
    module = test__reload_module(file_path,text,name)
    while True:
        try:
            with test__Capturing() as out:
                func = getattr(module, func_name)
                func(*args,**kwargs)
                all_vars = {i: module.__dict__[i] for i in module.__dict__.keys() if not (i.startswith('__'))}
                return module, all_vars

        except NameError as name_err:
            curr_word = re.findall(r'\'\w+\'', str(name_err))[0].replace('\'','')
            curr_text = test__find_reqs_args(In, curr_word)+'\n'
            text = curr_text+text
            module = test__reload_module(file_path,text, name)

def test__reload_module(path, text, name):
    if name in sys.modules:
        del sys.modules[name]
    with open(path, 'w') as f:
        f.write(text)
    with test__Capturing() as out:
        module = importlib.import_module(name)
    
    return module

def test__fullTest(In):
    all_test = {}
    with tqdm(total=5) as pbar:
        for i in range(1,6):
            with test__Capturing() as out:
                try:
                    answer = test__task(In, i)
                    if answer:
                        pbar.update(1)
                    if not answer:
                        all_test[i] = out
                except SyntaxError:
                    all_test[i] = [colored('Ошибка синтаксиса Python','red')]
                except IndentationError:
                    all_test[i] = [colored('Ошибка отсупов в языке Python','red')]
                except:
                    all_test[i] = [colored(str(sys.exc_info()[1]),'red')]

    if all_test:
        for i in range(1,6):
            if i in  all_test:
                print(f'В {i} задании')
                for curr_row in all_test[i]:
                    print(f'\t{curr_row}')
        return False
    print('Вы справились с всеми задачами!')
    return True

def test__item_task(tag):

    '''
        Функция содержит в себе все переменные и код, что минимально нужно для
    создания файла проверки.

        Вход:
            tag - Номер задания
            
        Выход:
            need - Список триггер слов для поиска нужных нам ячеек
            dont_need - Список триггер слов для фильтрации всех найденных ячеек кода
            args4test - Код для тестов, если потребуется
    '''

    

    dont_need = test__all_excepts()
    args4test = '2+2'
    input_replacment = 'str(int(float(3.1415926535)))'
    requeriment_vars = {}

    
    if tag == 1:
        need = [["Число простое", 'print(']]
        args4test = '''
def test___check_1(n):                                          
    d = 0                                     
    for i in range(2, n//2 + 1):              
        if (n % i == 0):                     
            d = i                            

    if d != 0:                                
        return False # Составное
    else:
        return True # Простое'''
    
    
    if tag == 2:
        need = [[{'eratosphen'}]]
        args4test = ''' 
def test__prime_list(end_number):

    def test__prime_number(number):
        """
        Функция проверки числа на простоту.
        Вход: число
        Выход: True - если число простое, False - если нет
        """

        for i in range(2, number//2 + 1):     # Для чисел от 2 до половины заданного:
            if (number % i == 0):             # Если заданное число делится на i без остатка,
                return False                  # то число не простое

        return True
    return [i for i in range(2, end_number + 1) if test__prime_number(i)]

 '''
        requeriment_vars = {
            'eratosphen':['переменная', int]
        }

    if tag == 3:
        need = [[{'leap_year'}, 'def leap_year']]
        args4test = '''
def test__student_func(years):
    if (years % 4 == 0 and years % 100 != 0) or (years % 400 == 0):
        return 'Високосный'
    else:
        return 'Обычный'
        '''
        requeriment_vars = {
            'leap_year':['функция', types.FunctionType]
        }
    
    if tag == 4:
        need = [['def', {'fibonacci'}, 'def fib']]
        args4test = ''' 
def test__fibonacci(n):
    a, b = 1, 1
    new_list = []
    for i in range(n):                                        
        new_list.append(a)
        a, b = b, a + b  
    return new_list   '''
        requeriment_vars = {
            'fibonacci':['функция', types.FunctionType]
        }

    if tag == 5:
        need = [['def',{'calculator'}, 'def calc']]
        args4test = ''' 
def test__calculator(a, b, c):
    if b==0:
        return 'Деление на 0'
    if c == "+":
        return a + b
    elif c == "-":
        return a - b
    elif c == "*":
        return a * b
    elif c == "/":
        return a / b
    else:
        return "Неизвестная операция!" '''
        requeriment_vars = {
            'calculator':['функция', types.FunctionType]
        }




    return need, dont_need, args4test,requeriment_vars, input_replacment
def test__output_comp_1(student_dict, test__dict, input_replacment, In):

    '''
        Функция получает все выходы и функции студента, если таковы есть.
    Выход его функции и эталонной будет сравниваться проверками. Если все выходы 
    двух функций будут одинаковы, то все проверки он пройдёт. Если же нет, то задание не засчитается.

        Вход:
            output - Всё print выводы кода студента
            module -  Модуль кода студента, откуда можно использовать функции
        
        Выход:
            True/False - сдал или не сдад студент
    '''
    student_output = student_dict['output']
    student_text = student_dict['text']
    

    test__module = test__dict['module']

    task__dict = 'простое'
    limit = 100

    if 'str(int(float(3.1415926535)))' not in student_text:
        print('\tВ вашей работе отсутсвует input функция.')
        return False

    start__task = 0
    all_problems = []
    for i in range(limit):
        number = np.random.randint(10,100)
        if i in range(10):
            number = i
        new_text = student_text.replace(input_replacment, f'\'{number}\'')

        student_path_curr = os.path.join(student_path, 'student__1.py')

        with open(student_path_curr, 'w') as f:
            f.write(new_text)
        with test__Capturing() as student_output:
            execfile(student_path_curr)
        if student_output:
            if task__dict in student_output[0] and 'не' not in student_output[0].split(' '):
                curr_result = True
            else:
                curr_result = False

            if test__module.test___check_1(number)==curr_result:
                start__task+=1
            else:
                all_problems.append(number)



    all_problems = set(all_problems)
    all_problems = [i for i in all_problems][:5]    
    if start__task==limit:
        return True
    else:
        print(f'\tПроверок пройдено {start__task} из {limit}. Доработайте.\n\tВот первые {len(all_problems)} чисел, что не прошли проверку:',\
*all_problems)
        return False
def test__output_comp_2(student_dict, test__dict, input_replacment, In):



    '''
        Функция получает все выходы и функции студента, если таковы есть.
    Выход его функции и эталонной будет сравниваться проверками. Если все выходы 
    двух функций будут одинаковы, то все проверки он пройдёт. Если же нет, то задание не засчитается.

        Вход:
            output - Всё print выводы кода студента
            module -  Модуль кода студента, откуда можно использовать функции
        
        Выход:
            True/False - сдал или не сдад студент
    '''
    student_output = student_dict['output']
    student_module = student_dict['module']
    student_vars = student_dict['variables']
    student_text = student_dict['text']
    

    test__module = test__dict['module']


    student_text = student_text.replace(input_replacment, '51')


    student_path_curr = os.path.join(student_path, 'student__2.py')
    with open(student_path_curr, 'w') as f:
        f.write(student_text)
    
    if 'student__2' in sys.modules:
        del sys.modules['student__2']
    
    with test__Capturing() as student_output:
        student_module = importlib.import_module(f'student__2')

    student_vars = {i: student_module.__dict__[i] for i in student_module.__dict__.keys() if not (i.startswith('__'))}

    new_dict = test__find_by_type(student_vars, list)
    new_list = []
    new_lists = []
    for i in student_output:
        curr_list = re.findall(r'\[.+\]',i)
        curr_number = re.findall(r'\d+',i)
        if curr_number:
            curr_number = eval(curr_number[0])
        if curr_list:
            curr_list = eval(curr_list[0])
        if isinstance(curr_list, list):
            new_lists.append(curr_list)
        if isinstance(curr_number, int):
            new_list.append(curr_number)
    new_lists.append(new_list)
    test__list = test__module.test__prime_list(50)
    check__list  = np.array([curr_list == test__list for curr_list in new_lists]).any()

    if check__list:
        return True
    else:
        print(f'\tИспользуйте переменную \'eratosphen\' внутри ячейки вывода ответа. Так же \
проверьте чтобы ответ соответствовал списку:\
\n\t{test__list}.')
        print('\tДоработайте 2-ую задачу.')
def test__output_comp_3(student_dict, test__dict, input_replacment, In):
    '''
        Функция получает все выходы и функции студента, если таковы есть.
    Выход его функции и эталонной будет сравниваться проверками. Если все выходы 
    двух функций будут одинаковы, то все проверки он пройдёт. Если же нет, то задание не засчитается.

        Вход:
            output - Всё print выводы кода студента
            module -  Модуль кода студента, откуда можно использовать функции
        
        Выход:
            True/False - сдал или не сдад студент
    '''
    student_output = student_dict['output']
    student_module = student_dict['module']
    student_vars = student_dict['variables']
    

    test__module = test__dict['module']
    
    func_name = 'leap_year'

    student_module, student_vars = test__update_module(In, student_module, func_name,312)

    limit = 100
    start = [0, 0]
    for i in range(limit):
        rand = np.random.randint(100,2000)
        corr_answer = test__module.test__student_func(rand)
        with test__Capturing() as student_output:
            ret = student_vars[func_name](rand)
        if ret:
            if ret.lower() == corr_answer.lower():
                start[0] +=1
        if student_output:
            if student_output[0].lower() == corr_answer.lower():
                start[1] +=1
        
    print(f'\tПроверок пройдено {max(start)} из {limit}.', end=' ')
    if max(start)==limit:
        return True
    else:
        print('\tДоработайте  задание')
        return False
    
def test__output_comp_4(student_dict, test__dict, input_replacment, In):
    '''
        Функция получает все выходы и функции студента, если таковы есть.
    Выход его функции и эталонной будет сравниваться проверками. Если все выходы 
    двух функций будут одинаковы, то все проверки он пройдёт. Если же нет, то задание не засчитается.

        Вход:
            output - Всё print выводы кода студента
            module -  Модуль кода студента, откуда можно использовать функции
        
        Выход:
            True/False - сдал или не сдад студент
    '''

    student_output = student_dict['output']
    student_module = student_dict['module']
    student_vars = student_dict['variables']
    

    test__module = test__dict['module']

    func_name = 'fibonacci'

    student_module, student_vars =  test__update_module(In, student_module,func_name, 4)


    limit = 20
    start = [0, 0]
    all_errors_return = []
    all_errors_output = []
    for i in range(limit):
        rand = i+5
        corr_answer = test__module.test__fibonacci(rand)
        with test__Capturing() as student_output:
            ret = student_vars[func_name](rand)
        if ret:
            ret = list(student_vars[func_name](rand))
            if ret == corr_answer:
                start[0] +=1
            else:
                all_errors_return.append([[rand, corr_answer],[rand,ret]])
        if student_output:
            curr_text  =' '.join(student_output)
            all_out = re.findall(r'[\[\(].+[\]\)]', curr_text)
            if all_out:
                all_out = list(eval(all_out[0]))
                if list(eval(all_out)) == corr_answer:
                    start[1] +=1
                else:
                    all_errors_output.append([[rand, corr_answer],[rand,all_out]])
    
    all_errors_return = all_errors_return[:5]
    all_errors_output = all_errors_output[:5]    
        
    print(f'\tПроверок пройдено {max(start)} из {limit}.', end=' ')
    if max(start)==limit:
        return True
    elif max(start)>=0:
        if all_errors_return:
            our_list = all_errors_return
        elif all_errors_output:
            our_list = all_errors_output
        else:
            print('\tВаша функция должна возвращать значение - лист или генератор. Используйте return или yield соответсвенно.')
            return False
             
        for curr in our_list:
            print(f'\tДля числа {curr[1][0]} вывелась последовательность {curr[1][1]}\n\t\tКогда требовалось получить: {curr[0][1]}', end='\n\n')
        return False
        


    else:
        print('\tДоработайте задание')
        return False
    
def test__output_comp_5(student_dict, test__dict, input_replacment, In):

    '''
        Функция получает все выходы и функции студента, если таковы есть.
    Выход его функции и эталонной будет сравниваться проверками. Если все выходы 
    двух функций будут одинаковы, то все проверки он пройдёт. Если же нет, то задание не засчитается.

        Вход:
            output - Всё print выводы кода студента
            module -  Модуль кода студента, откуда можно использовать функции
        
        Выход:
            True/False - сдал или не сдад студент
    '''
    student_module = student_dict['module']
    student_text = student_dict['text']
    

    test__module = test__dict['module']

    def test__order(args, idx):
        a_0,a_1,a_2 = args
        new_list = [None, None, None]
        new_list[idx] = a_2
        help_list = [i for i in range(len(new_list)) if new_list[i]==None]
        for idx, i in enumerate(help_list):
            new_list[i] = locals()[f'a_{idx}']
        return tuple(new_list)

    limit = 100
    start = 0
    operations = {0:'+',1:'-',2:'*',3:'/'}
    func_text = inspect.getsource(student_module.calculator).replace(' ','')
    find_all_vars = func_text.split('\n')[0]
    find_all_vars = re.findall(r'\(.+\)',find_all_vars)[0]
    find_all_vars = re.sub(r'[\(\)]', '',find_all_vars)

    number = 0
    try:
        vars = find_all_vars.split(',')
        a, b, c = vars
    except ValueError:
        print('\tВаша функция должна принимать 3 аргумента: 2 числа, и арифметическую операцию.')
        return False
    else:
        for idx, i in enumerate(vars):
            if f'{i}==':
                number = idx
    
    func_name = 'calculator'

    student_module, student_vars =  test__update_module(In, student_module,func_name, *test__order([1, 1,'+'],number))

    vars_for_res_2 = test__order([1, 0,'/'],number)
    try:
        result_2 = student_vars[func_name](*vars_for_res_2)
    except ZeroDivisionError:
        print('\tПроверка на деление на 0 не прошла. Доработайте функцию, чтобы она возвращала текстовое предупреждение о том, что знаменателем на число ввели 0.')
        return False

    for i in range(limit):
        var_1 = np.random.randint(500)
        var_2 = np.random.randint(500)
        oper = operations[np.random.randint(4)]

        result_1 = test__module.test__calculator(var_1, var_2, oper)

        vars_for_res_2 = test__order([var_1, var_2,oper],number)

        result_2 = student_vars[func_name](*vars_for_res_2)


        if not isinstance(result_1,str) and not isinstance(result_2,str):
            if result_1 == result_2:
                start+=1
            else:
                print('\t',result_1,result_2, 'Не прошли проверку на результат' )    
        elif isinstance(result_1,str) and isinstance(result_2,str):
            start+=1
            


        

        
    print(f'Проверок пройдено {start} из {limit}.', end=' ')
    if start==limit:
        return True
    else:
        print('Доработайте задание')
        return False
    
    

def send_homework():
    global user
    param = {'hwid': user.HW_ID,
             'questions': json.dumps([78] * 10),
             'answers':'',
             'status': 1,
             'user_id': user.id
            }
    
    # Добавление ответов пользователя в параметры
    param['answers'] = json.dumps([1]*10)
    
    # Проверка ответов пользователя на сервере
    data = requests.get(os.path.join(SERVER, PAGE_CHECK), 
                        params=param)
    print(data.json()['result'])  

def check_homework(self):
    dsp.clear_output(wait=True)
    global user
    keywords = utils.Keywords(user.content)
    if keywords.check():
        res = test__fullTest(user.content['In'])    
        if res:
            send_homework()
            return    
    dsp.display(button_check) # Вывод кнопки «Проверить»    
    button_check.layout.display = 'block' # Отображение кнопки «Проверить»

    
def Start(_user):
    global user 
    user = _user
    check_homework(None)
    button_check.on_click(check_homework)
    
        
    
