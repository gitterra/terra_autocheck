# Homework ID 1755


from typing import KeysView
from IPython import display as dsp
from ... import utils

def check(task): 
  if task == 1:                                                                 # для варианта из нескольких задач
    goodAnswer = 0                                                              # базовый коэффициент исполнения задачи
    i = 0                                                                       # стандартная переменная перебора
    koefA = 0                                                                   # Вспомогательная переменная подсчета                  
    koefB = 0                                                                   # Вспомогательная переменная подсчета  
    koefC = 0                                                                   # Вспомогательная переменная подсчета
    plentyGlobals = set(user.content.keys())                                    # Множество глобальных параметров
    badNetAnswer = 'Внимание! Не все заданные слои присутсвуют в моделе!'       # Плохой ответ
    badNumberAnswer = 'Внимание! Количество слоев модели задано не верно!'      # Плохой ответ
    badButch = 'Внимание! Параметры обучения указаны не верно!'                 # Плохой ответ
    badCompile = 'Внимание! Параметры компиляции указаны не верно!'             # Плохой ответ
    badAccuracy = 'Внимание! Изображение обучения оформленно некоректно!'       # Плохой ответ
    
    plentyNetParametrs = set([r'Sequential', r'Dense', r'model', r'BatchNormalization', r'Conv2D', r'MaxPooling2D', r'Flatten', r'Dropout']) # создание множества верных элементов параметров сети
    if plentyNetParametrs.issubset(plentyGlobals):                              # проверка наличия всех елементов множества верных слоев в глобальном множестве параметров
      goodAnswer +=1                                                            # добавляем положительный ответ
    else:                                                                       # если совпадают не все слои загружаем отрицательный ответ
      print(badNetAnswer)                                                       # отрицательный ответ
    
    if len(model.layers) == 9:                                                  # проверка количества слоев сети
      goodAnswer +=1                                                            # положительный ответ
    else:                                                                       # если не совпадает количество слоев загружаем отрицательный ответ
      print(badNumberAnswer)                                                    # отрицательный ответ
    
    for i in range(len(content['In'])):                                         # проходим по элементам запущенных ячеек
      if 'batch_size=128' and 'epochs=15' in user.content['In'][i]:             # если батч 128 и эпох 15 есть в ячейке, то указываем это (должен найти 4 элемента с учетом этой ячейки)
        koefA +=1                                                               # складываем количество найденных значений
    if koefA > 0:                                                               # если коэффициент больше нуля то ок
      goodAnswer +=1                                                            # положительный ответ
    else:                                                                       # иначе
      print(badButch)                                                           # отрицательный ответ
    
    for i in range(len(content['In'])):                                         # проходим по элементам запущенных ячеек
      if 'categorical_crossentropy' and 'Adam(learning_rate=0.001)' in user.content['In'][i]:   # если кросэнтропия и адам ячейке, то указываем это (должен найти 4 элемента с учетом этой ячейки)
        koefB +=1                                                               # складываем количество найденных значений                                              
    if koefB > 0:                                                               # если коэффициент больше нуля то ок
      goodAnswer +=1                                                            # положительный ответ
    else:                                                                       # иначе
      print(badCompile)                                                         # отрицательный ответ

    for i in range(len(content['In'])):                                         # проходим по элементам запущенных ячеек
      if 'accuracy' and 'val_accuracy' in user.content['In'][i]:                # если чтоности в ячейке, то указываем это (должен найти 4 элемента с учетом этой ячейки)
        koefC +=1                                                               # складываем количество найденных значений                                              
    if koefB > 0:                                                               # если коэффициент больше нуля то ок
      goodAnswer +=1                                                            # положительный ответ
    else:                                                                       # иначе
      print(badAccuracy)                                                        # отрицательный ответ
    
    if goodAnswer == 5:                                                         # если все условия выполнены, задача решена верно
      print('Отличено! Задание выполнено верно!')
    user.content['In'].clear()


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