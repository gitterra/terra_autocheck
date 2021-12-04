# Homework ID 1744
from IPython import display as dsp
from ... import utils
import numpy as np
import sys
from shutil import rmtree
from os import mkdir
from IPython.display import clear_output
from tqdm import tqdm
import re
import importlib

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

def check_patt(pat, t):
  ret1 = {}
  for name in t.keys():
    ret1[name] = pat - set([p for p in pat if re.search(p, t[name])])
  return ret1

def Start(usr):
  sys.path.append('/content/tmp')
  mkdir('/content/tmp')
  tasks = [{
      'alias': {r'rnd_array\s*=': 'my_array',
                r'str_array\s*=': 'str_array'},
      'func': task1,
      'result': False,
      'error': set()
  }, {
      'alias': {r'def\s+first_monday\s*\(': 'first_monday'},
      'func': task2,
      'result': False,
      'error': set()
  }, {
      'alias': {r'def\s+sort_bubble\s*\(': 'sort_bubble'},
      'func': task3,
      'result': False,
      'error': set()
  }, {
      'alias': {r'x\s*=': 'x',
                r'y\s*=': 'y',
                r'\.scatter\s*\(\s*x\s*,\s*y': 'plt.scatter'},
      'func': task4,
      'result': False,
      'error': set()
  }, {
      'alias': {r'val_x\s*=': 'val_x',
                r'val_y\s*=': 'val_y',
                r'\.plot\s*\(\s*val_x\s*,\s*val_y': 'plt.plot',
                r'\.scatter\s*\(\s*val_x\s*,\s*val_y': 'plt.scatter',
                r'figsize\s*=\s*\(\s*6\s*,\s*3\s*\)': '\nНеправильный размер рисунка',
                r'\.grid\(': '\nОтсутствие сетки на рисунке - не использован метод grid',
                r"\.xlabel\(\s*\'": "\nНет подписи оси - не использован метод xlabel",
                r"\.ylabel\(\s*\'": "\nНет подписи оси - не использован метод ylabel",
                r"\.title\(\s*['\"]Самолет": '\nГрафик не подписан - не использован метод title'},
      'func': task5,
      'result': False,
      'error': set()
  }
  ]
  # flag = False
  t = save_cells(usr.content)
  res = [check_task(t, op) for op in tasks]  # , check_task2(t), check_task3(t), check_task4(t), check_task5(t)]
  clear_output()
  num = 0
  for i in tqdm(res, desc='Задание ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}',
                colour='red' if not all(res) else 'green'):
      # print(tasks)
      num += 1
      print('\n\n', f'Задание {num}', 'выполнено' if i else 'сделано неправильно')
      if not i:
          print(', '.join(tasks[num - 1]['error']))
  print('\n')
  print('ДЗ выполнено' if all(res) else 'Исправьте ошибки и попробуйте снова')
  rmtree('/content/tmp')
  user.content['In'].clear()

def task1(tmp, text=None):
   assert tmp.rnd_array.shape == (3, 4) or tmp.rnd_array.dtype == np.int or (tmp.rnd_array.max() >=38 and tmp.rnd_array.min() <= 15), 'Неправильный размер массива или содержание массива'
   a1 = np.select([tmp.rnd_array < 20, tmp.rnd_array > 30], ['small', 'large'], default='medium')
   assert (tmp.str_array == a1).all(), 'Неправильный результат'

def task2(tmp, text=None):
  t1 = np.busday_offset('2015', 0, roll='forward', weekmask='Mon')
  t2 = np.busday_offset('2000', 0, roll='forward', weekmask='Mon')
  t3 = np.busday_offset('2020', 0, roll='forward', weekmask='Mon')
  assert tmp.first_monday('2015') == t1, 'Неправильное определение понедельника 2015'
  assert tmp.first_monday('2000') == t2, 'Неправильное определение понедельника 2000'
  assert tmp.first_monday('2020') == t3, 'Неправильное определение понедельника 2020'

def task3(tmp, text=None):
  checks = (([3, 2, 1], [1, 2, 3]), ([2, -2, 5], [-2, 2, 5]))
  for check, res in checks:
    assert tmp.sort_bubble(check) == res, 'Неправильный результат'
  # print('>>>', text[f'{tmp.__name__}.py'])
  assert not re.search(r'\.sort\s*\(|sorted\s*\(', text), "Использование запрещенных функций"

def task4(tmp, text=None):
  assert len(tmp.x.shape) == len(tmp.y.shape) == 1, 'Неправильный размер массивов'
  assert tmp.x.shape[0] == tmp.y.shape[0], 'Массивы не равны друг другу'

def task5(tmp, text=None):
  assert text.count('.plot') > 1, 'Не выведен график методом plot. Их должно быть два'

def check_task(text, context):
  # flag = False
  print(context)
  if context['alias']:
    patterns = set(context['alias'].keys())
    n_pat = len(patterns)
    ret = check_patt(patterns, text)
  else:
    ret = {name: set() for name in text.keys()}
  # print(ret)
  error = context['error']
  for name in tqdm(text.keys(), desc='Проверка ячеек ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}'):
    jump = True
    print(ret[name])
    try:
      print(f'\nЯчейка \n\n{text[name]}')
      tmp_imp = importlib.import_module(name[:-3])
      if not ret[name]:
        try:
          context['func'](tmp_imp, text[name])
          # print('\n Это правильное решение')
          context['result'] = True
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
          error.add('\n\nНе использована необходимая функция '+f'{", ".join([context["alias"][key] for key in ret[name]])}')
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
    except AttributeError:
      error.add(f'\n\nИспользован неизвестный метод')
      jump = False
    if jump:
      del sys.modules[tmp_imp.__name__]
    print()
  print('\n\nЗадание выполнено' if context['result'] else '\n\n Задание не выполнено. Попробуйте снова')
  return context['result']

def check_homework(self):
    dsp.clear_output(wait=True)
    global user
    keywords = utils.Keywords(user.content)
    keywords.check()
    sys.path.append('/content/tmp')
    mkdir('/content/tmp')
    tasks = [{
              'alias':{r'rnd_array\s*=': 'my_array',
                      r'str_array\s*=': 'str_array'},
              'func': task1,
              'result': False,
              'error': set()
          }, {
              'alias':{r'def\s+first_monday\s*\(': 'first_monday'},
              'func': task2,
              'result': False,
              'error': set()
          }, {
              'alias':{r'def\s+sort_bubble\s*\(': 'sort_bubble'},
              'func': task3,
              'result': False,
              'error': set()
          }, {
              'alias': {r'x\s*=': 'x',
                r'y\s*=': 'y',
                r'\.scatter\s*\(\s*x\s*,\s*y': 'plt.scatter'},
              'func': task4,
              'result': False,
              'error': set()
          }, {
              'alias': {r'val_x\s*=': 'val_x',
                  r'val_y\s*=': 'val_y',
                  r'\.plot\s*\(\s*val_x\s*,\s*val_y': 'plt.plot',
                  r'\.scatter\s*\(\s*val_x\s*,\s*val_y': 'plt.scatter',
                  r'figsize\s*=\s*\(\s*6\s*,\s*3\s*\)': '\nНеправильный размер рисунка',
                  r'\.grid\(': '\nОтсутствие сетки на рисунке - не использован метод grid',
                  r"\.xlabel\(\s*\'": "\nНет подписи оси - не использован метод xlabel",
                  r"\.ylabel\(\s*\'": "\nНет подписи оси - не использован метод ylabel",
                  r"\.title\(\s*['\"]Самолет": '\nГрафик не подписан - не использован метод title'},
              'func': task5,
              'result': False,
              'error': set()
          }]
	  # flag = False
    t = save_cells(user.content['In'])
    res = [check_task(t, op) for op in tasks]#, check_task2(t), check_task3(t), check_task4(t), check_task5(t)]
    clear_output()
    num = 0
    for i in tqdm(res, desc='Задание ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}', colour='red' if not all(res) else 'green'):
	    # print(tasks)
	    num += 1
	    print('\n\n', f'Задание {num}', 'выполнено' if i else 'сделано неправильно')
	    if not i:
	      print(', '.join(tasks[num-1]['error']))
    print('\n')
    print('ДЗ выполнено' if all(res) else 'Исправьте ошибки и попробуйте снова')
    rmtree('/content/tmp')
    user.content['In'].clear()


def Start(_user):
    global user
    user = _user
    check_homework(None)