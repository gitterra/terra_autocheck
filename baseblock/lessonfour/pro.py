# Homework ID 1752
from IPython import display as dsp
from ... import utils

'''

Здесь Ваши функции автопроверки

'''
def test():
  global x_data
  from tensorflow.keras.utils import get_file   # инструмент для скачивания и распаковки
  import types, glob, shutil, psutil, gc, os        # работа с путями и проверка соответствия типов
  from sklearn.metrics import accuracy_score    # замер точности
  from PIL import Image
  import numpy as np
  if psutil.virtual_memory()[2] > 85:
    del x_data
    print('Переменная x_data была удалена для освобождения ОЗУ, если проверка не пройдет, Вам придется снова запустить ячейку с созданием массива данных для обучения.')
  gc.collect()
  get_file('bus_test.zip', origin = 'https://drive.google.com/uc?id=1x121oZ9ZYRekXe2ub8HMgTN4oo7r0Qpk', extract=True, cache_dir='.', cache_subdir='.')
  os.remove('bus_test.zip')                     # сразу удаляем тестовый датасет, чтоб не было доступа у студента
  IMAGE_PATH = '/content/bus_test/'
  CLASS_LIST = sorted(os.listdir(IMAGE_PATH))
  data_files = []                               # Cписок путей к файлам картинок
  data_labels = []                              # Список меток классов, соответствующих файлам
  for class_label in range(2):                  # Для всех классов по порядку номеров (их меток)
      class_name = CLASS_LIST[class_label]      # Выборка имени класса из списка имен
      class_path = IMAGE_PATH + class_name      # Формирование полного пути к папке с изображениями класса
      class_files = os.listdir(class_path)      # Получение списка имен файлов с изображениями текущего класса
      data_files += [f'{class_path}/{file_name}' for file_name in class_files]
      data_labels += [class_label] * len(class_files)
  IMG_HEIGHT = 243
  IMG_WIDTH = 162
  data_images = []
  for file_name in data_files:
      img = Image.open(file_name).resize((IMG_WIDTH, IMG_HEIGHT))
      img_np = np.array(img)                    # Перевод в numpy-массив
      data_images.append(img_np)                # Добавление изображения в виде numpy-массива к общему списку
  x_test = np.array(data_images)/255.           # Перевод общего списка изображений в numpy-массив
  y_test = np.array(data_labels)                # Перевод общего списка меток класса в numpy-массив
  shutil.rmtree('/content/bus_test')            # сразу удаляем тестовый датасет, чтоб не было доступа у студента
  del data_images
  accuracy_list = []

  for g in user.content:                           # пробуем перебрать все переменные в поисках рабочих моделей и тестируем их, если их было несколько. Если лучшая модель даст удовл, то тест пройден
    if not str(user.content[g]).startswith('<keras.engine.sequential.Sequential object'):  # ищем только среди интересующих нас объектов.
      continue
    testmodel = user.content[g]
    eval = testmodel.predict(x_test, verbose=0)
    eval = np.squeeze(eval).round().astype(int)
    accuracy = accuracy_score(eval, y_test)
    accuracy_list.append(accuracy)
  gc.collect()
  if accuracy_list:
    if max(accuracy_list) >= 0.93:
      print(f'Максимальная точность составила {max(accuracy_list)}.Задание выполнено.')
      return True
    else:
      print(f'Максимальная точность составила {max(accuracy_list)}. Требуется не менее 0.93. Задание не выполнено.')
      return False
  else:
    print('Моделей класса Sequential не обнаружено')
    return False

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