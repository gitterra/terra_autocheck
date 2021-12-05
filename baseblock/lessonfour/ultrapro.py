# Homework ID 1753

from IPython import display as dsp
from ... import utils

'''
Здесь Ваши функции автопроверки
'''
# <hide>
###############################################################
# Функция get_cells__ создает массив из ячеек ноутбука для дальнейшей работы
# Возвращает массив cells([code1, output1],...[codeN, outputN]) 
############################################################### 
from google.colab import _message
import re

def get_cells__(logs=False):
  # получаю содержимое ноутбука, включая метаданные с результатами выполнения ячеек в формате json
  nb__ = _message.blocking_request("get_ipynb", request="", timeout_sec=10)
  cells = []
  cellin, cellout = '', ''

  for cell in nb__["ipynb"]["cells"]:
    # ячейки с кодом, которые запускали  
    if cell["cell_type"] == "code" and cell["source"][0] != "# <hide>\n" and 'executionInfo' in cell["metadata"].keys():  
      if cell["metadata"]["executionInfo"]["status"] == "ok":  # проверяем, что ячейка выполнена (присутствует информация о результатах выполнения)
        # удаляем из кода комментарии, обединяем список в строку и передаем в проверочную функцию
        cellin = "".join(list(map(lambda x: x.split("#")[0], cell["source"])))
        cellout = ''
        if cell["outputs"]: # ячейка с выводом
          if cell["outputs"][0]["output_type"] == "stream":
            cellout = "".join(cell["outputs"][0]["text"])
            # if logs:  print(cellout)
        cells.append([cellin, cellout])
  if logs:
      print(*['\nINPUT:\n'+c[0]+['\n\nOUTPUT:\n'+c[1], '\n\nNo OUTPUT\n'][len(c[1])==0] for c in cells], sep='\n')
  return cells

# <hide>
###############################################################
# Функция check_cells__ проверяет наличие признака в ячейке
# Возвращает найденные совпадения matches_in, matches_out 
############################################################### 

def check_cells__(cellin='', cellout='', reg_marker_in='', reg_marker_out='', logs=0):
  matches_in, matches_out = '', ''
  if reg_marker_in: matches_in = re.findall(reg_marker_in, cellin, re.MULTILINE)
  if reg_marker_out: matches_out = re.findall(reg_marker_out, cellout, re.MULTILINE)

  if reg_marker_in and reg_marker_out:
    if logs:  print('два маркера:', reg_marker_in and reg_marker_out)
    if matches_in and matches_out:
      return matches_in, matches_out
  else:
    if matches_in or matches_out:
      if logs:  print('найдено одно совпадение:', matches_in, matches_out)
      return matches_in, matches_out
    if logs:  print(cell["metadata"], cell["source"])
  return '', ''

# функция выводит ячейки, в которых есть совпадение
def show_result__(c, n, cellin='', cellout='',  matches_in='', matches_out=''):
  print('#####################################'+'#'*len(str(n)))
  print(f'###### совпадение {c} в ячейке {n} #######')
  print('#####################################'+'#'*len(str(n)))
  print(f'matches_in: {matches_in}\nmatches_out: {matches_out}')

  print('\nНайдено совпадение в следующих ячейках:\n')
  print('CODE:')
  print(cellin)
  print('\nOUTPUT:')
  print(cellout)

# <hide>
###############################################################
# Функции - 'тестовые юниты' для автопроверки
# Возвращают результат проверки 
# На вход подается сдержимое ячеек и найденные маркеры
############################################################### 

'''
TU1 - проверяет что установлена метрика accuracy
TU2v1 - проверяет наличие функции обучения с тестовой выборкой validation_data= X, Y
TU2v2 - проверяет наличие функции обучения с тестовой выборкой validation_split >= 0.1
TU3 - проверка на достижение необходимой точности на проверочной выборке при обучении сети
'''

####################### TEST UNIT 1 ############################
def test_unit_1(cellin, cellout, matches_in='', matches_out='', pred_test='', logs=0):  # pred_test - результаты из предыдущего теста
 # print('ok1', matches_in, matches_out)
  test_unit_num = [test_units__[i].__name__ for i in range(len(test_units__))].index('test_unit_1') # индекс текущей функции в списке функций
  pred_test__[1] = pred_test__[2] = matches_in[0][0]  # записываем название модели для следующих функций
  test_flags__[test_unit_num] = 1 # ставим отметку, что первая проверка пройдена
  test_results__[test_unit_num] = '1/Компиляция модели с метрикой точности accuracy обнаружена'


####################### TEST UNIT 2v1 ############################
# TU2v1 - проверяет наличие функции обучения с тестовой выборкой validation_data= X, Y
def test_unit_2v1(cellin, cellout, matches_in='', matches_out='', pred_test='', logs=0):  # pred_test - результаты из прошлых тестов, передаются при необходимости
  # print('ok2v1', matches_in, matches_out)

  if matches_in[0][0] == pred_test:
    test_flags__[1]=1 # ставим флаг, что условие c разделением данных выполнено
    test_flags__[2]=0 # обнуляем флаг в тесте 2v2
    test_results__[1] = f'2/Подходящая модель ({matches_in[0][0]}) и обучающие данные обнаружены'
   
  elif test_flags__[1]:
    pass
  else:
    test_results__[1] = f'Для обучаемой модели ({matches_in[0][0]}) не обнаружена компиляция с метрикой точности accuracy'

####################### TEST UNIT 2v2 ############################
def test_unit_2v2(cellin, cellout, matches_in='', matches_out='', pred_test='', logs=1):  # pred_test - результаты из предыдущего теста
  # print('ok2v2', 'in', matches_in, 'out', matches_out, pred_test)
  # предлагаю использовать model.history
  # hist_tmp = eval(pred_test__[1]+'.history.history["val_accuracy"]')
  # print('выводим history', hist_tmp)

  if matches_in[0][0] == pred_test:
    test_flags__[2]=1 # ставим флаг, что условие c разделением данных выполнено
    test_flags__[1]=0 # обнуляем флаг в тесте 2v1
    test_results__[1] = f'2/Подходящая модель ({matches_in[0][0]}) и обучающие данные обнаружены'

  if matches_in[0][-1]>=0.1:
    print(f'Для получения точности на проверочной выборке данные поделены с помощью validation_split = {matches_in[0][-1]}')
  else:
    print('Для правильного выполнения задания необходимо взять для проверочной выборки validation_split >= 0.1')


###################### TEST UNIT 3 ############################
# В этой функции важно проверить что точность данных растёт с увеличением эпохи
# Точность возрастает на последних эпохах

def test_unit_3(cellin, cellout, matches_in='', matches_out='', pred_test='', logs=1):
  # print('ok3', 'in', matches_in, 'out', matches_out, pred_test)
  
  # print('(test_flags__[1] or test_flags__[2]) and matches_in==".fit" =', test_flags__, matches_in, (test_flags__[1] or test_flags__[2]) and matches_in=='.fit')
  if (test_flags__[1] or test_flags__[2]) and matches_in[0]=='.fit':  # проверяем, если пройдена проверка в тестах 2v1 или 2v2

    list_val_acc = [] # список точностей на проверочной выборке по каждой эпохе
    for acc, val_acc in matches_out: # Пример: ('accuracy: 0.8446', 'val_accuracy: 0.8442')'
      for v in val_acc.split(':'):
        if v != 'val_accuracy':
          list_val_acc.append(float(v))
    # print('list_val_acc',list_val_acc)

    # проверяем точность
    count_v_acc = 0 # счётчик эпох с достигнутой нужной точностью
    for v_acc in list_val_acc[-min(10,len(list_val_acc)):]:
      mean_acc = sum(list_val_acc)/len(list_val_acc) # среднее заначение точностей
      if v_acc > 0.85 and v_acc > mean_acc: # проверяем на достижение необходимой точности на последних эпохах и рост точности
        count_v_acc = count_v_acc + 1
    print('count_v_acc', count_v_acc)
    if count_v_acc > 3:
      test_flags__[3] = 1
      test_results__[2] = f'3/На последних {min(10,len(list_val_acc))} эпохах достигнута необходимая точность на проверочной выборке'
    else:
      test_results__[2] = f'3/Для данного задания достигнутой точности и роста точности на последних {min(10,len(list_val_acc))} эпохах не достаточно. \nПопробуйте изменить модель или дообучить на большем количестве эпох.'
  else:
    print('Модель не обучалась')
  # print(f'Лучшая точность на {list_val_acc.index(max(list_val_acc))+1} эпохе - {round(max(list_val_acc)*100, 2)}%')

  
# <hide>
# глобальная функция тестирования
def test(logs=0):
  global pred_test__, test_flags__, test_results__, test_units__  # pred_test - результаты, которые надо передавать в следующий тест
  global matches_in, matches_out, cellin, cellout

  reg_marker_in = [r'(\w+?)\.compile.*\(.+? *[\s\w\n=,()]*metrics.+(accuracy)', # проверка наличия accuracy
                   r'(\w+?)\.fit.*\( *(.+?) *,[\s\n]*(.+?) *,[\s\w\n=,()]*validation_data[ =]*\( *(.+?) *,[\s\n]*(.+?)\)',
                   r'(\w+?)\.fit.*\( *(.+?) *,[\s\n]*(.+?) *,[\s\w\n=,()]*validation_split[\s\w\n=]*(\d.*?\d)',
                   r'\.fit']

  reg_marker_out = ['',
                    r'Epoch \d.+\n.+?(accuracy: \d\.\d+).+(val_accuracy: .+)', #находит последнюю эпоху в выводе. Возвращает номер эпохи, accuracy и val_accuracy
                    r'Epoch \d.+\n.+?(accuracy: \d\.\d+).+(val_accuracy: .+)',
                    r'Epoch \d.+\n.+?(accuracy: \d\.\d+).+(val_accuracy: .+)']  # достижение нужной точности val_accuracy

  test_flags__ = [0,0,0,0]
  test_results__ = ['','','','']
  test_units__ = [test_unit_1, test_unit_2v1, test_unit_2v2, test_unit_3]

  # получаем содержимое ноутбука в виде списка ячеек
  cells__ = get_cells__(logs=0)
  pred_test__ = {i: '' for i in range(len(test_units__))} # создаём пустой словарь

  c = 1 # для подсчета совпадений
  n = 0 # для подсчета ячеек
  for cellin, cellout in cells__:
    for i in range(len(test_flags__)):
      matches_in, matches_out = check_cells__(cellin, cellout, reg_marker_in = reg_marker_in[i], reg_marker_out = reg_marker_out[i], logs=0)
      if matches_in or matches_out:
        test_units__[i](cellin, cellout, matches_in=matches_in, matches_out=matches_out, pred_test=pred_test__[i]) # num - порядковый номер теста
        if logs==2: show_result__(c, n, cellin=cellin, cellout=cellout, matches_in=matches_in, matches_out=matches_out)
        c += 1
    n +=1
  
  print('\nРезультаты проверки:')
  for res in test_results__:
    print(res)
  if sum(test_flags__)==3:
    print('\nПоздравляем! Необходимая точность достигнута. Задание принято.')
  else:
    print('\nПроверки не все пройдены. Попробуйте еще раз. Задание не принято.')


    
    
def myTest():
    print('тестовый вывод')

#
# ОБЯЗАТЕЛЬНЫЙ БЛОК
#

def check_homework(self):
    dsp.clear_output(wait=True)
    global user

    '''
    Здесь код вызова функций автопроверки ДЗ

    '''
    test()

    # Проверка на пересечение имён
    # Пока оформляем это в качестве рекомендации (НЕ ОШИБКА)
    # Просто оставляйте этот код здесь
    keywords = utils.Keywords(user.content)
    keywords.check()


def Start(_user):
    global user
    user = _user
    check_homework(None)
