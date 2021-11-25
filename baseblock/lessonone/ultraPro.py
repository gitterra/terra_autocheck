# Homework ID 1741
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
from IPython import display as dsp
from ... import utils

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
                elif curr_frag_new.startswith(f'def{text}:'):  # Смотрим, есть ли в ячейке функция с таким именем
                    result = f'\n{fragment}'  # Если есть - записываем в result код ячейки
                elif curr_frag_new.startswith(f'class{text}:'):  # Смотрим, есть ли в ячейке класс с таким именем
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
        need = [["2790", '820']]

    if tag == 2:
        need = [[{'number_elements'}, ['for', '==', 'type', 'isinstance','not', '!=']]]
        args4test = ''' 
def test__only_nums(args):
    new_list = []
    new_list_num = []
    for idx, i in enumerate(args):
        if isinstance(i, (int,float)):
            new_list.append(i)
        else:
            new_list_num.append(idx)
    return new_list, new_list_num 
    '''

        requeriment_vars = {'number_elements':
                            ['список',list]
                            }

    if tag == 3:

        need = [[{'player_1', 'player_2'}], ['print', 'player_']]

        args4test = ''' 
import numpy as np
def test__players(pl1, pl2):
    player_cards = [0,0]                        # Сумма достоинств карт не в игре у первого игрока


    for i in range(len(pl1)):            # Для всех карт первого игрока
        turn_sum = pl1[i] + pl2[i]  # Сумма хода
        # Ход: у кого достоинство карты больше, тому добавление к сумме карт не в игре
        if pl1[i] > pl2[i]: 
            player_cards[0] += turn_sum
        elif pl2[i] > pl1[i]:
            player_cards[1] += turn_sum
    
    if player_cards[0]==player_cards[1]:
        return 4
    return np.argmin(player_cards)
     '''

        requeriment_vars = {'player_1':
                            ['список',list],
                            'player_2':
                            ['список',list]
                            }

    if tag == 4:   
        need = [[{'new_array'}, 'np.array('], ['new_array['], ['new_array.sort(']]
    
        requeriment_vars = {'new_array':
                            ['numpy массив',np.ndarray]
                            }
    if tag == 5:
        need = [['def possible_path(', {'possible_path'}]]

        args4test = ''' 
import numpy as np
def test__possible_path(*lst):

    to_digit = lambda x: int(x) if str(x).isdigit() else x
    # Условие перебора допустимых пар
    all_lists = [lst[::2], lst[1::2]]
    print(all_lists)

    all_lists[0] = np.array(list(map(to_digit, all_lists[0])))
    all_lists[1] = np.array(list(map(to_digit, all_lists[1])))
    print(all_lists)
    results = [0,0]
    for lis in all_lists:
        if lis.dtype == np.int64:
            results[0] = 1
        elif lis.dtype.name =='str32':
            for i in lis:
                if i.isdigit():
                    return False
            results[0] = 1
    
    return sum(results)==2
     '''
        requeriment_vars = {'possible_path':
                            ['функция',types.FunctionType]
                            }



    return need, dont_need, args4test, requeriment_vars, input_replacment
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
    if student_output:    
        all_numbers = []
        for curr_out in student_output:
            all_nums_str = re.findall(r'[\d\.]{2,1000}',curr_out)
            all_nums = list(map(float, all_nums_str))
            all_numbers.extend(all_nums)
        all_numbers = np.array(all_numbers).astype(float)
        if 167718 in all_numbers.astype(int):
            if 167718.45 in all_numbers:
                return True
            else:
                print('\tСделайте округление до 2-ух знаков после запятой.')
                return False
        else:
            print('\tСделайте пересчёт данных.')
            return False
    else:
        print('\tНет вывода расчётов. Для выводов используйте print функцию.')
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
    
    test__module = test__dict['module']


    all_lists = test__find_by_type(student_vars, list)
    
    list_one, list_idx = test__module.test__only_nums(student_module.number_elements)
    all = [list_idx,list_one]
    print_lists = []
    start_vars = np.array([0, 0])

    if student_output:  
        for i in student_output:
            found_lists = re.findall(r'[\[\(][\d ,\.]+[\]\)]',i)
            for some in found_lists:
                print_lists.append(eval(some))
    start_print = np.array([0, 0])
    for value in all_lists.values():
        if np.array([isinstance(i, int) for i in value]).all():
            if np.max(value)< len(student_module.number_elements) and value==list_one:
                start_print[1]+=1
        if value == list_idx:
            start_print[0]+=1
    
    if print_lists:
        for curr_list in print_lists:
            if curr_list == list_idx:
                start_vars[0]+=1
            if curr_list == list_one:
                start_vars[1]+=1
    
    new_start = start_print + start_vars
    vars_dict = {0:'индексами',1:'листами'}
    new_arg = np.argmin(new_start)
    if 0 in new_start:
        for idx,i in enumerate(new_start):
            if not i:
                print(f'\tВ {idx+1} задании  ожидалось {all[idx]}')
                if idx==0:
                    print('\tПомните - мы создаём списки, что содержат индексы.\
                    \n\tА индексы уже создаются по условию.')
                else:
                    print('\tПомните, что мы создаём списки элементов, что являются числом - пусть даже не целым.')

                return False
    return True


    
def test__output_comp_3(student_dict, test__dict,input_replacment, In):

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
    

    limit = 10
    start = 0
    for i in range(limit):
        play_1 = np.random.randint(6,11, 6) 
        play_2 = np.random.randint(6,11, 6)
        while np.array(play_1==play_2).any():
            play_1 = np.random.randint(6,11, 6)    
            play_2 = np.random.randint(6,11, 6)

        play_1, play_2 = list(play_1), list(play_2)

        play_1_copy = play_1.copy()
        play_2_copy = play_2.copy()  
        all_rows = student_text.split('\n')
        for idx, row in enumerate(all_rows):
            row = row.replace(' ','')
            for i in range(1,3):
                if f'player_{i}=' in row:
                    new_text = locals()[f'play_{i}']
                    all_rows[idx] = f'player_{i} = {new_text}'
        
        student_path_curr = os.path.join(student_path, 'student__3.py')
        with open(student_path_curr, 'w') as f:
            f.write('\n'.join(all_rows))
        if 'student__3' in sys.modules:
            del sys.modules['student__3']

        with test__Capturing() as student_output:
            student_module = importlib.import_module(f'student__3')
            execfile(student_path_curr)

        if student_output:
            curr_winner = re.findall(r'player_\d',student_output[-1])
            if not curr_winner:
                curr_num = 'ничья'
            else:
                curr_num = curr_winner[0]
        

        student_vars = {i: student_module.__dict__[i] for i in student_module.__dict__.keys() if not (i.startswith('__'))}
        
        old_vars = dict()
        for key, value in student_vars.items():
            if '1' in key or '2' in key:
                old_vars.update({key:value})
        sort_vars_ints = dict(sorted(test__find_by_type(old_vars, int).items()))
        sort_vars_lists = dict(sorted(test__find_by_type(old_vars, list).items()))
        sort_vars_ints_dict = dict()
        new_dict = dict()
        for key, value in sort_vars_lists.items():
            if 'player_1' == key or 'player_2' == key:
                pass
            elif not np.array([type(i)==int for i in value]).all():
                pass
            else:
                new_dict.update({key:value})
        
        for key, value in sort_vars_ints.items():
            if 'player_1' == key or 'player_2' == key:
                pass
            elif key=='i':
                pass
            else:
                sort_vars_ints_dict.update({key:value})

        new_number = 3
        new_lists = 3
        new_out = 3
        if sort_vars_ints_dict.values():
            new_number = np.argmin(list(sort_vars_ints_dict.values()))

        if new_dict.values():
            new_lists = np.argmin([sum(i) for i in new_dict.values()])
        if student_output:
            last = student_output[-1]
            if 'player_1' in last or 'перв' in last.lower():
                new_out = 0
            elif 'player_2' in last or 'втор' in last.lower():
                new_out = 1


        etalon = test__module.test__players(student_vars['player_1'],student_vars['player_2'])
        if new_lists==etalon or new_number==etalon or new_out==etalon:
            start+=1
        elif etalon==4:
            start+=1

    print(f'Тестов пройдено {start} из {limit}.', end=' ')
    if start==limit:
        return True
    else:
        print('Задача решена не верно. Доработайте.)')
        return False





    
def test__output_comp_4(student_dict,test__dict, input_replacment, In):

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
    student_vars = student_dict['variables']
    student_text = student_dict['text']
    all_types = student_vars['new_array'].dtype
    if len(all_types)!=3:
        print(f'\tВ вашем массиве должны храниться данные 3-ёх типов. Сейчас там {len(all_types)} типа данных.')
        return False
    new_text = student_text.replace(' ','')
    all_revars = re.findall(r'new_array[\[\]\'\"A-zА-я]+=\d+', new_text)
    all_sort = re.findall(r'new_array\.sort\([A-zА-я\'\"= ]+\)', new_text)
    if not all_revars:
        print('\tУ вас отсутсвует изменение значения по ключу.')
        return False
    if not all_sort:
        print('\tУ вас отсутсвует сортировка массива методом .sort.')
        return False
    
    return True

    
def test__output_comp_5(student_dict, test__dict,input_replacment, In):
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
    student_text = student_dict['text']

    test__module = test__dict['module']

    func_name = 'possible_path'
    way  = None
    with test__Capturing() as student_output:
        res_1 = test__module.test__possible_path(*['H'])
        try :
            student_module, student_vars = test__update_module(In,student_module, func_name, ['H'])
            way = 0
        except TypeError:
            student_module, student_vars = test__update_module(In,student_module, func_name, *['H'])
            way = 1

    limit = 100
    start = 0
    for lim in range(limit):
        curr_length = np.random.randint(3,7)
        curr_path = []
        for i in range(curr_length):
            nums = [np.random.randint(1,5),'H']
            poss = [0.5,0.5]
            if curr_path:
                if curr_path[-1] == 'H':
                    poss = [0.8,0.2]
                else:
                    poss = [0.2,0.8]
            rand_num = np.random.choice(nums, p=poss)
            if rand_num.isdigit():
                rand_num = int(rand_num)
            curr_path.append(rand_num)

        with test__Capturing() as student_output:
            res_1 = test__module.test__possible_path(*curr_path)
            if way:
                res_2 = student_module.possible_path(*curr_path)
            else:
                res_2 = student_module.possible_path(curr_path)


        new_2 = False
        if student_output and not res_2:
            if 'False' in student_output[0]:
                new_2 = False
            elif 'True' in student_output[0]:
                new_2 = True
            
        if (res_1 == res_2 or res_1==new_2) and res_2!=None:
            start+=1

    print(f'\tТестов пройдено {start} из {limit}.', end=' ')
    if start==limit:
        return True
    elif start>0:
        print('Задача решена не верно. Доработайте.)')
        return False
    else:
        print('Перепроверьте, чтобы ваша функция возвращала через return True или False. Доработайте.')
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
    res = test__fullTest(user.content['In'])
    if res:
        print('Все задания выполнены верно. Работа принята (10 баллов)')
    else:
        print('Работа выполнена некорректно. Исправьте указанные ошибки и перезпустите проверку')
    keywords = utils.Keywords(user.content)
    keywords.check()


def Start(_user):
    global user
    user = _user
    check_homework(None)
    
        
    
