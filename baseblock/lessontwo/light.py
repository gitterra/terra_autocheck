import re
from shutil import rmtree
import sys
from os import mkdir
import sys
import importlib
import numpy as np
from IPython.display import clear_output


def save_cells(content):
  text = {}
  ad = len(content[:-1])
  i = False
  s = 'import matplotlib.pyplot as plt\nimport numpy as np\n\n'
  for num, item in enumerate(content[:-1]):
    if item == '':
      continue
    text[f'tmp{num}.py'] = item
    with open(f'/content/tmp/tmp{num}.py', mode='w', encoding='utf8') as f:
      f.write('\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n' + item)
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
  flag = False
  t = save_cells(usr.content)
  res = [check_task1(t), check_task2(t), check_task3(t), check_task4(t), check_task5(t)]
  clear_output()
  for num, i in enumerate(res):
    print(f'Задание {num+1}', 'выполнено' if i else 'сделано не правильно') 
  print('ДЗ выполнено' if all(res) else 'Исправьте ошибки и попробуйте снова')
  rmtree('/content/tmp')
  In.clear()

def check_task1(text):
  a1 = np.random.randint(1, 11, size=10)
  a2 = np.random.randint(1, 11, size=4)
  result = np.in1d(a1, a2)
  flag = False
  ret = check_patt(set(['check_arrays']), text)
  print(ret)
  for name in text.keys():
    jump = True
    try:
      # print(f'Ячейка \n\n{text[name]}')
      tmp = importlib.import_module(name[:-3])
      if not ret[name]:
        try:
          assert tmp.check_arrays(a1, a2).all() == result.all(), 'Неправильный результат'
          assert len(tmp.check_arrays(a1, a2)) == 10, 'Неправильная длина результата'
          print('\n Это правильное решение')
          flag = True
        except ValueError as v:
          print(f'\n\nПопытка подачи неправильного значения {v}')
        except UnboundLocalError:
          print(f'\n\nИспользование переменной перед приравниванием')
        except TypeError:
          print(f'\n\nНеправильное использование типов данных')
        except NameError:
          # er = sys.exc_info()
          print(f'\n\nИспользование неправильного идентификатора')
        except AssertionError as a:
          print(f'\n\nОшибка кода: {a}')
        except Exception as e:
          print(e)
      else:
        print('\n\nНе использована необходимая функция check_arrays')
    except IndentationError:
      print(f'\n\nНеправильный отступ')
      jump = False
    except NameError:
      jump = False
      print(f'\n\nЯчейка не содержит определения функции get_max')
    except AttributeError:
      print(f'\n\nИспользован неизвестный метод')
      jump = False
    if jump:
      del sys.modules[tmp.__name__]
    print()
  print('\n\nЗадание 1 выполнено' if flag else '\n\n Задание 1 не выполнено. Попробуйте снова')
  return flag

def check_task2(text):
  a1 = (2, 6)
  a2 = (-2, 6)
  result1 = (6.324555320336759, 1.2490457723982544)
  result2 = (6.324555320336759, 1.8925468811915387)
  flag = False
  ret = check_patt(set(['find_angle']), text)
  print(ret)
  for name in text.keys():
    jump = True
    try:
      # print(f'Ячейка \n\n{text[name]}')
      tmp = importlib.import_module(name[:-3])
      if not ret[name]:
        try:
          assert tmp.find_angle(a1) == result1, 'Неправильный результат'
          assert tmp.find_angle(a2) == result2, 'Неправильный результат'
          assert len(tmp.find_angle(a1)) == 2, 'Неправильная длина результата'
          print('\n Это правильное решение')
          flag = True
        except ValueError as v:
          print(f'\n\nПопытка подачи неправильного значения {v}')
        except UnboundLocalError:
          print(f'\n\nИспользование переменной перед приравниванием')
        except TypeError:
          print(f'\n\nНеправильное использование типов данных')
        except NameError:
          # er = sys.exc_info()
          print(f'\n\nИспользование неправильного идентификатора')
        except AssertionError as a:
          print(f'\n\nОшибка кода: {a}')
        except AttributeError:
          print('\n\nНе использована необходимая функция')
        except Exception as e:
          print(e, type(e))
      else:
        print('\n\nНе использована необходимая функция')
    except IndentationError:
      print(f'\n\nНеправильный отступ')
      jump = False
    except NameError:
      jump = False
      print(f'\n\nЯчейка не содержит определения функции')
    except SyntaxError:
      jump = False
      print(f'\n\nНеправильный синтаксис')
    except AttributeError:
      print(f'\n\nИспользован неизвестный метод')
      jump = False
    if jump:
      del sys.modules[tmp.__name__]
    print()
  print('\n\nЗадание 2 выполнено' if flag else '\n\n Задание 2 не выполнено. Попробуйте снова')
  return flag

def check_task3(text):
  res = np.array([[1, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 1, 0, 1, 0],
                  [0, 0, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 0, 0],
                  [0, 1, 0, 1, 0, 1, 0],
                  [1, 0, 0, 1, 0, 0, 1]])
  alias = {r'my_array\s*=': 'my_array',
           r'plt\.imshow\(': 'plt.imshow'}
  flag = False
  patterns =set(alias.keys())
  ret = check_patt(patterns, text)
  for name in ret.keys():
      jump = True
      try:
        # print(f'Ячейка \n\n{text[name]}')
        tmp = importlib.import_module(name[:-3])
        if not ret[name]:
          try:
            assert (tmp.my_array == res).all(), 'Неправильный результат'
            print('\n Это правильное решение')
            flag = True
          except ValueError as v:
            print(f'\n\nПопытка подачи неправильного значения {v}')
          except UnboundLocalError:
            print(f'\n\nИспользование переменной перед приравниванием')
          except TypeError:
            print(f'\n\nНеправильное использование типов данных')
          except NameError:
            # er = sys.exc_info()
            print(f'\n\nИспользование неправильного идентификатора')
          except AssertionError as a:
            print(f'\n\nОшибка кода: {a}')
          except AttributeError:
            print('\n\nНе использована необходимая функция')
          except Exception as e:
            print(e, type(e))
        else:
          print('\n\nНе использована необходимая функция или переменная\n')
          print('\n'.join([alias[n] for n in ret[name]]))
      except IndentationError:
        print(f'\n\nНеправильный отступ')
        jump = False
      except NameError:
        jump = False
        print(f'\n\nЯчейка содержит неизвестный идентификатор')
      except SyntaxError:
        jump = False
        print(f'\n\nНеправильный синтаксис')
      except AttributeError:
        print(f'\n\nИспользован неизвестный метод')
        jump = False
      if jump:
        del sys.modules[tmp.__name__]
      print()
  print('\n\nЗадание 3 выполнено' if flag else '\n\n Задание 3 не выполнено. Попробуйте снова')
  return flag

def check_task4(text):
  lang_list = ['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
  alias = {r'programmingLanguages\s*=': 'programmingLanguages',
           r'popuratity\s*=': 'popuratity',
           r'colors\s*=': 'colors',
           r'plt.pie\s*\(': 'plt.pie'}
  flag = False
  patterns =set(alias.keys())
  ret = check_patt(patterns, text)
  for name in ret.keys():
      jump = True
      try:
        # print(f'Ячейка \n\n{text[name]}')
        tmp = importlib.import_module(name[:-3])
        if not ret[name]:
          try:
            assert tmp.programmingLanguages == lang_list, 'Неправильный список языков'
            assert len(tmp.popuratity) == 6, 'Неверная длина списка значений'
            assert len(tmp.colors) == 6, "Неверная длина списков цветов"
            print('\n Это правильное решение')
            flag = True
          except ValueError as v:
            print(f'\n\nПопытка подачи неправильного значения {v}')
          except UnboundLocalError:
            print(f'\n\nИспользование переменной перед приравниванием')
          except TypeError:
            print(f'\n\nНеправильное использование типов данных')
          except NameError as n:
            # er = sys.exc_info()
            print(f'\n\nИспользование неправильного идентификатора \n {n}')
          except AssertionError as a:
            print(f'\n\nОшибка кода: {a}')
          except AttributeError as a1:
            print(f'\n\nНе использована необходимая функция. \n {a1}')
          except Exception as e:
            print(e, type(e))
        else:
          print('\n\nНе использована необходимая функция или переменная\n')
          print('\n'.join([alias[n] for n in ret[name]]))
      except IndentationError:
        print(f'\n\nНеправильный отступ')
        jump = False
      except NameError:
        jump = False
        print(f'\n\nЯчейка содержит неизвестный идентификатор')
      except SyntaxError:
        jump = False
        print(f'\n\nНеправильный синтаксис')
      except AttributeError:
        print(f'\n\nИспользован неизвестный метод')
        jump = False
      except ValueError:
        print(f'\n\nИспользовано неизвестное значение')
        jump = False
      if jump:
        del sys.modules[tmp.__name__]
      print()
  print('\n\nЗадание 4 выполнено' if flag else '\n\n Задание 4 не выполнено. Попробуйте снова')
  return flag

def check_task5(text):
  alias = {r'x\s*=': 'x',
           r'\.plot\(.*=?x.*linestyle\s*=.*label\s*=': 'plt.plot(x, y, linestyle="...", label="...")',
           r'\.xlabel\([\'"]x[\'"]\)': 'plt.xlabel',
           r'\.ylabel\([\'"]y[\'"]\)': 'plt.ylabel',
           r'\.legend\(\)': 'plt.legend'}
  flag = False
  patterns =set(alias.keys())
  ret = check_patt(patterns, text)
  for name in ret.keys():
      jump = True
      try:
        # print(f'Ячейка \n\n{text[name]}')
        tmp = importlib.import_module(name[:-3])
        if not ret[name]:
          try:
            assert tmp.x.max() < 101 or tmp.x.min() > -101, 'Неправильный отрезок значений'
            assert re.findall(r'\.plot\(.*=?x.*linestyle\s*=.*label\s*=', text[name]) != 2, 'Неправильное число графиков'
            print('\n Это правильное решение')
            flag = True
          except ValueError as v:
            print(f'\n\nПопытка подачи неправильного значения {v}')
          except UnboundLocalError:
            print(f'\n\nИспользование переменной перед приравниванием')
          except TypeError:
            print(f'\n\nНеправильное использование типов данных')
          except NameError as n:
            # er = sys.exc_info()
            print(f'\n\nИспользование неправильного идентификатора \n {n}')
          except AssertionError as a:
            print(f'\n\nОшибка кода: {a}')
          except AttributeError as a1:
            print(f'\n\nНе использована необходимая функция. \n {a1}')
          except Exception as e:
            print(e, type(e))
        else:
          print('\n\nНе использована необходимая функция или переменная\n')
          print('\n'.join([alias[n] for n in ret[name]]))
      except IndentationError:
        print(f'\n\nНеправильный отступ')
        jump = False
      except NameError:
        jump = False
        print(f'\n\nЯчейка содержит неизвестный идентификатор')
      except SyntaxError:
        jump = False
        print(f'\n\nНеправильный синтаксис')
      except AttributeError:
        print(f'\n\nИспользован неизвестный метод')
        jump = False
      except ValueError:
        print(f'\n\nИспользовано неизвестное значение')
        jump = False
      if jump:
        del sys.modules[tmp.__name__]
      print()
  print('\n\nЗадание 5 выполнено' if flag else '\n\n Задание 5 не выполнено. Попробуйте снова')
  return flag
