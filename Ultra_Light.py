import requests, os, random, json
from .settings import *
from . import utils
import ipywidgets as widgets
from IPython import display
from termcolor import colored
import numpy as np
import functools

# Функция проверки ответов пользователя
def check_homework(self):  
    global user
    # Список параметров, отправляемых на сервер
    param = {'hwid': user.HW_ID,
             'questions': json.dumps(questions_id),
             'answers':'',
             'status': 0,
             'user_id': user.id
            }
    # Получение ответов пользователя
    user_answers = [answer_buttons[i].options.index(answer_buttons[i].value) 
                    + 1 if answer_buttons[i].value else 0 for i in range(10)]
    
    # Добавление ответов пользователя в параметры
    param['answers'] = json.dumps(user_answers)
    
    # Проверка ответов пользователя на сервере
    data = requests.get(os.path.join(SERVER, PAGE_CHECK), 
                        params=param)
    # Проверка ответа сервера
    if data.status_code!=200 and data.status_code!=500:
        # Если сервер не обработал запрос
        display.clear_output(wait=True)
        utils.error_programm(f'Ошибка обработки запроса (status_code={data.status_code})')
        return
    else:
        # Получение результатов проверки
        result = json.loads(data.json()['result'])
   
    # Визуализация правильных/неправильных ответов на кнопках
    for i, r in enumerate(result):
        if r:
            answer_buttons[i].button_style = 'success'      
        else:
            answer_buttons[i].button_style = 'danger'
        answer_buttons[i].disabled = True
    button_check.layout.display = 'None' # Скрытие кнопки "Проверить"        
    print()
    print()    
    # Отображение результата тестирования
    if sum(result) < 10:
        # Если есть ошибки
        print(colored(f'Ваш результат составил {sum(result)} баллов(а)',
                      color='red', attrs=['bold']))
        print('   * Для повторного тестирования нажмите «Пересдать»')
        print('   * Для сдачи домшней работы нажмите «Зачесть ДЗ»')
        print('Вы можете вернуться и пересдать домашнее задание в любое время')        
        button_retake.on_click(show_question)
        display.display(button_retake)
    else:
        # Если ошибок нет
        print(colored(f'Поздравляем. Вы верно ответили на все вопросы и набрали 10 баллов', 
                      color='green', attrs=['bold']))
    
    # Отображение кнопки «Зачесть ДЗ»
    button_send_homework.on_click(send_homework)
    display.display(button_send_homework)  

def send_homework(self):
    display.clear_output(wait=True)# Список параметров, отправляемых на сервер    
    param = {'hwid': user.HW_ID,
             'questions': json.dumps(questions_id),
             'answers':'',
             'status': 1,
             'user_id': user.id
            }
    # Получение ответов пользователя
    user_answers = [answer_buttons[i].options.index(answer_buttons[i].value) 
                    + 1 if answer_buttons[i].value else 0 for i in range(10)]
    
    # Добавление ответов пользователя в параметры
    param['answers'] = json.dumps(user_answers)
    
    # Проверка ответов пользователя на сервере
    data = requests.get(os.path.join(SERVER, PAGE_CHECK), 
                        params=param)
    print(data.json()['result'])   
    
# Функция визуализации вопросов
def show_question(self):
    param = {'hwid': user.HW_ID} # Параметры запроса (id домашки)
    # Отправка запроса на сервер (получение списка из случайных 10 вопросов)
    questions = requests.get(
        os.path.join(SERVER, PAGE_QUESTION),
        params=param).json()
    variants = ['a','b','c','d'] # Нумерация ответово
    display.clear_output(wait=True) # Очищение экрана
    questions_id.clear() # Очищение списка id-шников вопросов
    answer_buttons.clear()
    # Визуализация вопросов
    for i,q in enumerate(questions):
        answers = q['variants'][1:-1].split("',") # Получение вариантов ответов
        questions_id.append(q['id']) # Сохранение id вопроса
        # Создание кнопок с вариантами ответов
        wt = widgets.ToggleButtons(
            value=None,
            options=variants,        
            disabled=False,
            button_style ='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=answers,
          )
        print()
        print()
        # Печать текста вопроса
        print(colored(f'Вопрос №{i+1}: {q["text"]}:', attrs=['bold']))
        # Печать вариантов ответа
        for i in range(4):
            print(' '*5, variants[i] + ') ' + answers[i].lstrip().replace("'",""))        
        display.display(wt) # Вывод кнопок с ответами
        answer_buttons.append(wt) # Сохранение кнопок
        
    display.display(button_check) # Вывод кнопки «Проверить»    
    button_check.layout.display = 'block' # Отображение кнопки «Проверить»
    button_check.on_click(check_homework) # Добавление обработчика для кнопки
    
# Функция запуска тестирования
def Start(hwid, user_):
    global user
    user = user_
    