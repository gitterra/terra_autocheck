# Homework ID 1755



from typing import KeysView
from IPython import display as dsp
from ... import utils
############################
from google.colab import _message

class NotebookCheck():
  def __init__(self, debug=0, ncell=0):
    self.checkLayers = {'Conv2D': 2, 'Dense': 1, 'MaxPooling2D': 1, 'BatchNormalization': 1, 'Dropout': 1}
    self.chekParams = {'loss': 'categorical_crossentropy', 'optimizer': 'Adam', 'learning_rate': 0.001,
                       'batch_size': 128, 'epochs': 15, 'verbose': 1}

    nb = _message.blocking_request('get_ipynb', timeout_sec=10)
    cellin = cellout = ''
    self.cells = {}
    self.NoteCode = ''

    for cell in nb['ipynb']['cells']:
      if cell['cell_type'] == 'code' and cell['execution_count'] != None:
        if cell['metadata']['executionInfo']['status'] == 'ok':
          cellin = ''.join(list(map(lambda x: x.split('#')[0] + '\n', cell['source'])))
          if 'NotebookCheck' in cellin:
            continue
          cellout = ''
          if cell['outputs']:
            if cell['outputs'][0]['output_type'] == 'stream':
              cellout = ''.join(cell['outputs'][0]['text'])
            elif cell['outputs'][0]['output_type'] == 'display_data':
              cellout = 'image/png\n' + ''.join(cell['outputs'][0]['data']['text/plain'])
            elif cell['outputs'][0]['output_type'] == 'execute_result':
              cellout = ''.join(cell['outputs'][0]['data']['text/plain'])
            elif cell['outputs'][0]['output_type'] == 'error':
              cellout = cell['outputs'][0]['ename'] + '\n' + ''.join(cell['outputs'][0]['traceback'])

        self.cells[cell['execution_count']] = [cellin, cellout]

        self.NoteCodeToText()

        if debug == 1:
          print(
            'Ячейка № {}\n INPUT: {}\n OUTPUT: {}\n\n'.format(cell['execution_count'], cell['source'], cell['outputs']))
        elif debug == 2:
          print(cell)

        if cell['execution_count'] == ncell:
          print(cell)

  def getcells(self):
    return self.cells

  def check(self):
    answer = 0
    loadMnist = self.getLoadBase()
    if loadMnist['load mnist'] == 1:
      print('База рукописных цыфр загружена')
      answer += 1
    else:
      self.cPrint('Не найдена загрузка базы рукописных цыфр', 'red')

    if len(loadMnist['reshape']) == 2:
      print('Преобразование размерности набора данных для подачи в нейросеть выполнено.')
      answer += 1
    elif len(loadMnist['reshape']) == 1:
      print('Преобразование размерности набора данных для подачи в нейросеть выполнено только для набора',
            loadMnist['reshape'][0])
    else:
      self.cPrint('Преобразование размерности набора данных для подачи в нейросеть не выполнено', 'red')

    if len(loadMnist['to_categorical']) == 2:
      print('Преобразование выборки с ответами в OHE выполнено.')
      answer += 1
    elif len(loadMnist['to_categorical']) == 1:
      print('Преобразование выборки с ответами в OHE выполнено только для набора', loadMnist['reshape'][0])
    else:
      self.cPrint('Преобразование выборки с ответами в OHE не выполнено', 'red')

    if len(loadMnist['norm']) == 2:
      print('Нормирование данных выполнено.')
      answer += 1
    elif len(loadMnist['norm']) == 1:
      print('Нормирование данных выполнено только для набора', loadMnist['reshape'][0])
    else:
      cPprint('Нормирование данных не выполнено')

    dictModels = self.getModelLayers()

    if len(dictModels) > 0:
      print('Найдено обученных можелей:', len(dictModels))
      answer += 1
    else:
      self.cPrint('Не найдено ни одной обученной модели.', 'red')
    for key in dictModels:
      print(dictModels[key]['model name'], ':')
      for keyL in self.checkLayers:
        if sum(keyL in x for x in dictModels[key]['layers']) >= self.checkLayers[keyL]:
          print('Количество слоев {} удовлетворяет условию'.format(keyL))
          answer += 1
        else:
          self.cPrint('Количество слоев {} не удовлетворяет условию'.format(keyL), 'red')

      for keyP in self.chekParams:

        if keyP in dictModels[key]['params'].keys():
          if dictModels[key]['params'][keyP] == self.chekParams[keyP]:
            print('Значение {} удовлетворяет условию'.format(keyP))
            answer += 1
          else:
            self.cPrint('Значение {} не удовлетворяет условию'.format(keyP), 'red')
        else:
          cPrint('Параметр {} не найден'.format(keyP), 'red')

      pl = self.getPlot(dictModels[key]['history'])
      if pl['show'] == 1:
        if pl['accuracy'] == 1:
          print('График доли верных ответов на обучающей выборке найден')
          answer += 1
        else:
          self.cPrint('График доли верных ответов на обучающей выборке не найден', 'red')

        if pl['val_accuracy'] == 1:
          print('График доли верных ответов на проверочной выборке найден')
          answer += 1
        else:
          self.cPrint('График доли верных ответов на проверочной выборке не найден', 'red')

        print('Гарфик нарисован')
        answer += 1
      else:
        self.cPrint('График не найден. Выедите график доли верных ответов на обучающей и проверочной выборке', 'red')

    if answer == 19:
      print('\n\nПоздравляем! Все условия выполненны. Задание принято.')
    elif 0 < answer < 19:
      print('\n\nВыполнены не все условия. Задание не принято. Исправьте ошибки и запустите проверку повторно.')
    else:
      print('Задание не выполненно. Проверки не пройдены. Попробуйте еще раз.')

  def cPrint(self, text='', colorPrint='black'):
    colorMap = {'red': '\x1b[1;31m', 'black': '\x1b[0m'}
    clr = colorPrint
    if colorPrint not in colorMap.keys():
      printStr = colorMap['red'] + f'Цвет {clr} не определен для вывода print' + colorMap['black']
      clr = 'black'
      print(printStr)
    print(colorMap[clr] + text + colorMap['black'])

  def NoteCodeToText(self):
    open_key = 0
    t = ''
    self.NoteCode = ''
    for key in self.cells:
      for st in self.cells[key][0].split('\n'):
        t += st
        for i in st:
          if i == '(' or i == '[':
            open_key += 1
          elif i == ')' or i == ']':
            open_key -= 1
        if open_key == 0:
          self.NoteCode += t + '\n'
          t = ''

  def getLoadBase(self):
    base = {'load mnist': 0, 'reshape': [], 'to_categorical': [], 'norm': []}
    train_test = []
    for st in self.NoteCode.split('\n'):

      if 'mnist.load_data()' in st:
        base['load mnist'] = 1
        for i in self.getParams('(' + st.split('=')[0] + ')'):
          train_test.extend(self.getParams(i))

      if len(train_test) == 4:
        if train_test[0] + '.reshape' in st and '1' in st.split(',')[-1]:
          base['reshape'].append('x_train')
          train_test[0] = st.split('=')[0].strip()

        if train_test[2] + '.reshape' in st and '1' in st.split(',')[-1]:
          base['reshape'].append('x_test')
          train_test[2] = st.split('=')[0].strip()

        if train_test[1] in st and 'to_categorical(' in st and '10' in st.split(',')[-1]:
          base['to_categorical'].append('y_train')
          train_test[1] = st.split('=')[0].strip()

        if train_test[3] in st and 'to_categorical(' in st and '10' in st.split(',')[-1]:
          base['to_categorical'].append('y_test')
          train_test[3] = st.split('=')[0].strip()

        if train_test[0] in st.split('=')[-1] and '255' == st.split('/')[-1].strip():
          base['norm'].append('x_train')
          train_test[0] = st.split('=')[0].strip()

        if train_test[2] in st.split('=')[-1] and '255' == st.split('/')[-1].strip():
          base['norm'].append('x_test')
          train_test[2] = st.split('=')[0].strip()

    return base

  def getPlot(self, histName):
    checkPl = {'accuracy': 0, 'val_accuracy': 0, 'show': 0}
    for st in self.NoteCode.split('\n'):
      if '.plot(' in st:
        if histName + ".history" in st and 'accuracy' in st:
          checkPl['accuracy'] = 1
        if histName + ".history" in st and 'val_accuracy' in st:
          checkPl['val_accuracy'] = 1
      if '.show(' in st:
        checkPl['show'] = 1
    return checkPl

  def getModelLayers(self):
    func = ['']
    listLayers = []
    giper_params = {}
    fName = ''
    tName = ''
    n = 0
    dictModels = {}
    text = ''

    for st in self.NoteCode.split('\n'):
      if 'def' in st:
        func.append(st.split(' ')[1][:-3])
      if 'return' in st:
        func.pop()

      # Проверяем создание модели Sequential()
      if 'Sequential(' in st:
        tName = st.split('=')[0].strip()
        if len(func) > 1 and st[:2] == '  ':
          fName = func[-1]
        elif st[:2] != '  ':
          if len(func) > 1:
            func.pop()
          fName = ''

      # собираем слои найденной модели
      if tName != '' and tName + '.add' in st:
        listLayers.append(st[st.find('(') + 1:st.rfind(')')])

      if fName != '' and fName in st and st.find('=') > 0:
        tName = st.split('=')[0].strip()

      # Гиперпараметры модели
      if tName != '' and tName + '.compile' in st:
        args = self.getParams(st)
        for arg in args:
          val_arg = arg[arg.find('=') + 1:].replace("'", "").replace("[", "").replace("]", "")
          if val_arg.find('(') > 0 and val_arg.find('=') > 0:
            giper_params[arg[:arg.find('=')].strip()] = self.try_number(val_arg[:val_arg.find('(')].strip())
            giper_params[val_arg[val_arg.find('(') + 1:val_arg.find('=')].strip()] = self.try_number(
              val_arg[val_arg.find('=') + 1:val_arg.rfind(')')].replace("'", "").replace("[", "").replace("]", ""))
          else:
            giper_params[arg[:arg.find('=')].strip()] = self.try_number(val_arg.strip())

      if tName != '' and tName + '.fit' in st:
        args = self.getParams(st)

        for arg in args:
          if arg.find('=') > 0:
            giper_params[arg[:arg.find('=')].strip()] = self.try_number(
              arg[arg.find('=') + 1:].replace("'", "").replace("[", "").replace("]", ""))

        hist = st[:st.find('=')].strip()

        dictModels[n] = {'model name': tName, 'layers': listLayers, 'params': giper_params, 'func': fName,
                         'history': hist}
        n += 1

    return dictModels

  def getParams(self, params):
    p = params[params.find('(') + 1:params.rfind(')')]
    list_params = []
    k = 0
    j = 0
    for i in range(len(p)):
      if p[i] == '(' or p[i] == '[':
        k += 1
      if p[i] == ')' or p[i] == ']':
        k -= 1
      if (k == 0 and p[i] == ','):
        list_params.append(p[j:i].strip())
        j = i + 1
      if i == len(p) - 1:
        list_params.append(p[j:].strip())

    return list_params

  def try_number(self, x):
    try:
      return int(x)
    except ValueError:
      try:
        return float(x)
      except:
        return x

#
# ОБЯЗАТЕЛЬНЫЙ БЛОК
#

def check_homework(self):
    dsp.clear_output(wait=True)
    global user

    '''
    Здесь код вызова функций автопроверки ДЗ
    '''
    nc = NotebookCheck()
    nc.check()

    # Проверка на пересечение имён
    # Пока оформляем это в качестве рекомендации (НЕ ОШИБКА)
    # Просто оставляйте этот код здесь
    keywords = utils.Keywords(user.content)
    keywords.check()

def Start(_user):
    global user
    user = _user
    check_homework(None)