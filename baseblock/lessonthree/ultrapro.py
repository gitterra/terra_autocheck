
# from utils import Keywords
import numpy as np
import sys
from shutil import rmtree
from os import mkdir
from IPython.display import clear_output
from tqdm import tqdm
from re import search
import importlib

class Task:
  def __init__(self, alias):
    self.alias = alias
    self.result = False
    self.error = set()
  
  def check_patt(self, pat, t):
    ret1 = {}
    for name in t.keys():
      ret1[name] = pat - set([p for p in pat if search(p, t[name])])
    return ret1

  def check_task(self, text):
    # flag = False
    # print(context)
    if self.alias:
      patterns = set(self.alias.keys())
      n_pat = len(patterns)
      ret = self.check_patt(patterns, text)
    else:
      ret = {name: set() for name in text.keys()}
    # print(ret)
    error = self.error
    for name in tqdm(text.keys(), desc='Проверка ячеек ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}'):
      jump = True
      print(ret[name])
      try:
        print(f'\nЯчейка \n\n{text[name]}')
        tmp_imp = importlib.import_module(name[:-3])
        # words = Keywords(tmp_imp.__dir__())
        # assert words.check(), 'Переопределение стандартной функции'
        if not ret[name]:
          try:
            self.run(tmp_imp, text[name])
            # print('\n Это правильное решение')
            self.result = True
          except ValueError as v:
            error.add(f'\n\nПопытка подачи неправильного значения {v}')
          except UnboundLocalError:
            error.add(f'\n\nИспользование переменной перед приравниванием')
          except TypeError as t:
            error.add(f'\n\nНеправильное использование типов данных: \n{t}')
          except NameError as n:
            # er = sys.exc_info()
            error.add(f'\n\nИспользование неправильного идентификатора: \n{n}')
          except AssertionError as a:
            error.add(f'\n\nОшибка кода: {a}')
          except Exception as e:
            error.add(str(e)+str(type(e)))
        else:
            error.add('\n\nНе использована необходимая функция '+f'{", ".join([self.alias[key] for key in ret[name]])}')
      except IndentationError:
        error.add(f'\n\nНеправильный отступ')
        jump = False
      except NameError as n1:
        jump = False
        error.add(f'\n\nЯчейка не содержит определения необходимой функции: \n{n1}')
      except AssertionError as a:
        error.add(f'\n\nОшибка кода: {a}')
        jump = False
      except SyntaxError:
        error.add(f'\n\nСинтаксическая ошибка')
        jump = False
      except ValueError:
        error.add(f'\n\nИспользовано неправильное значение')
        jump = False
      except AttributeError:
        error.add(f'\n\nИспользован неизвестный метод')
        jump = False
      if jump:
        del sys.modules[tmp_imp.__name__]
      print()
      print(self.error)
    print('\n\nЗадание выполнено' if self.result else '\n\n Задание не выполнено. Попробуйте снова')
    return self.result

class Task1(Task):
  def run(self, tmp, text):
    m1 = np.random.randint(1, 12, size=(4, 3))
    m2 = np.random.randint(12, 24, size=(3, 4))
    m3 = np.random.randint(24, 46, size=(4, 2))
    assert (tmp.prod_matrix_3(m1, m2, m3) == m1@m2@m3).all(), "Неправильный результат"
    assert not search(r'@|\.dot\s*\(', text), 'Использованы запрещенные методы'

class Task2(Task):
  def run(self, tmp, text):
    m3 = [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    m7 = [[1, 2, 3, 4, 5, 6, 7],
          [24, 25, 26, 27, 28, 29, 8],
          [23, 40, 41, 42, 43, 30, 9],
          [22, 39, 48, 49, 44, 31, 10],
          [21, 38, 47, 46, 45, 32, 11],
          [20, 37, 36, 35, 34, 33, 12],
          [19, 18, 17, 16, 15, 14, 13]]
    m6 = [[1, 2, 3, 4, 5, 6],
          [20, 21, 22, 23, 24, 7],
          [19, 32, 33, 34, 25, 8],
          [18, 31, 36, 35, 26, 9],
          [17, 30, 29, 28, 27, 10],
          [16, 15, 14, 13, 12, 11]]
    assert tmp.whirligig(3) == m3, "Неправильный результат на матрице 3х3"
    assert tmp.whirligig(7) == m7, "Неправильный результат на матрице 7х7"
    assert tmp.whirligig(6) == m6, "Неправильный результат на матрице 6х6"

class Task3(Task):
  def run(self, tmp, text):
    assert tmp.work_days('2015-02', '2015-03') == 20, "Неправильный результат для февраля 2015"
    assert tmp.work_days('2019-03', '2019-04') == 21, "Неправильный результат для марта 2019"
    assert tmp.work_days('2021-03', '2021-04') == 23, "Неправильный результат для марта 2021"

class Task4(Task):
  def run(self, tmp, text):
    assert search(r'\.bar\s*\(.+hatch\s*=', text), 'Неправильный метод построения гистограммы'

class Task5(Task):
  def run(self, tmp, text):
    assert len(tmp.x) == len(tmp.y) == len(tmp.colors) == len(tmp.areas), 'Несоответвествие размеров параметров'
    assert search(r'\.scatter\s*\(\s*x\s*,\s*y\s*,\s*s\s*=\s*areas\s*,\s*c\s*=\s*colors', text), 'Использование неправильного метода или параметров'

def save_cells(cnt):
  text = {}
  ad = len(cnt[:-1])
  i = False
  s = 'import matplotlib.pyplot as plt\nimport numpy as np\n\n'
  for num, item in enumerate(cnt[:-1]):
    if item == '':
      continue
    text[f'tmp{num}.py'] = item
    with open(f'/content/tmp/tmp{num}.py', mode='w', encoding='utf8') as f:
      f.write('import matplotlib.pyplot as plt\nimport numpy as np\n\n' + item)
      s += text[f'tmp{num}.py'] + '\n'
      if i:
        with open(f'/content/tmp/tmp{num+ad}.py', mode='w', encoding='utf8') as f:
          f.write(s)
        text[f'tmp{num+ad}.py'] = s
      i = True
  return text

def Start(usr):
  sys.path.append('/content/tmp')
  mkdir('/content/tmp')
  # flag = False
  t = save_cells()#(usr.content)
  tasks = [Task1(alias={r'def\s+prod_matrix_3\s*\(': 'prod_matrix_3'}),
           Task2(alias={r'def\s+whirligig\s*\(': 'whirligig'}),
           Task3(alias={r'def\s+work_days\s*\(': 'work_days'}),
           Task4(alias={r'patterns\s*=\s*': 'patterns'}),
           Task5(alias={r'x\s*=\s*': 'x',
                        r'y\s*=\s*': 'y',
                        r'colors\s*=\s*': 'colors',
                        r'areas\s*=\s*': 'areas'})]
  res = [op.check_task(t) for op in tasks]
  num = 0 
  for i in tqdm(res, desc='Задание ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}', colour='red' if not all(res) else 'green'):
    # print(tasks)
    num += 1
    print('\n\n', f'Задание {num}', 'выполнено' if i else 'сделано неправильно')
    if not i:
      print(', '.join(tasks[num-1].error))
  print('\n') 
  print('ДЗ выполнено' if all(res) else 'Исправьте ошибки и попробуйте снова')
  rmtree('/content/tmp')
  In.clear()
  
