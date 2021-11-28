# Homework ID 1749
from IPython import display as dsp
from ... import utils

'''

Здесь Ваши функции автопроверки

'''


def test():
    from tensorflow.keras.utils import get_file  # инструмент для скачивания и распаковки
    import glob, os, types, glob  # работа с путями и проверка соответствия типов

    def link_find(In, func):
        extentions = ['png', 'jpg', 'jpeg', 'tif', 'tiff', 'bmp']
        for i in In:
            if i.startswith(func):
                b = i.split(".")
                for i in b:
                    if i.startswith(tuple(extentions)):
                        return True
        return False

    get_file('digits.zip', origin='https://storage.googleapis.com/datasets_ai/Bas%D0%B5Unit/1_intro/hw_upro.zip',
             extract=True, cache_dir='.', cache_subdir='.')  ## качаем тестовый датасет
    imgs = sorted(glob.glob('/content/digits/*'))  ## Формируем пары Х У для проверки качества
    labels = [int(os.path.basename(im)[:-4]) for im in imgs]
    func_search = 0  ## флаг обнаружения функции с интересующим названием

    try:
        if not isinstance(predict_image, types.FunctionType):  ## проверка типа переменной
            print('predict_image должна быть функцией.')
            return False
    except NameError:  ## проверка есть ли переменная
        print("Функция predict_image не обнаружена. Тест проходит в режиме проверки всех функций в текущей сессии.\n")
        func_search = 1

    if func_search:  ## берем словарь глобальных переменных для поиска функций, если не была обнаружена predict_image
        globalsdict = user.content
    else:
        globalsdict = {'predict_image': '<function'}  ## иначе создаем свой словарь с одной переменной

    for fun in globalsdict:  ## идем по словарю
        if str(user.content[fun]).startswith('<function') and fun != 'test':  ## оставляем только функции
            test_pred = user.content[fun]
            predsfinal = []  ### хранение всех точностей всех моделей
            flag_ret_No_int = 0  ## флажки, значение в конце в принтах
            flag_input_No_str_and_model = 0
            flag_input_No_path = 0
            flag_No_models = 0
            flag_No_accuracy = 0
            flag_Pass_accuracy = 1
            flag_No_selftested_function = 1

            if link_find(user.content['In'], fun):
                flag_No_selftested_function = 0

            for g in user.content:  ## пробуем перебрать все переменные в поисках рабочих моделей и тестируем их, если их было несколько. Если лучшая модель даст удовл, то тест пройден
                if not str(user.content[g]).startswith(
                        '<keras.engine.sequential.Sequential object'):  ## ищем только среди интересующих нас объектов.
                    continue
                preds = []  ## предикты, выданные данной переменной, если это модель
                testmodel = user.content[g]
                for i, l in zip(imgs,
                                labels):  ## предиктим тестовый датасет и записываем булевый результат верно/неверно
                    try:
                        pred = test_pred(i, testmodel)
                        if isinstance(pred, tuple) or not type(
                                pred) == int:  ## проверка, что функция возвращает только одно число
                            flag_ret_No_int = 1

                        predbool = pred == l
                        preds.append(predbool)
                    except TypeError:
                        flag_input_No_str_and_model = 1

                    except IsADirectoryError:
                        flag_input_No_path = 1

                predsfinal.append(sum(preds) / 10)  ## отправляем аккураси модели в общий список

            if predsfinal == []:  ## если предиктов не было, то модели, которая бы могла их делать, не было))
                flag_No_models = 1

            if max(predsfinal) > 0.5:  ## если точность любой модели больше 50, то тест пройден
                flag_Pass_accuracy = 0

            if max(predsfinal) < 0.5 and not flag_ret_No_int:  ## если возврат был верного типа, но точности мало, то так и отвечаем
                flag_No_accuracy = 1

            if sum([flag_ret_No_int, flag_input_No_str_and_model, flag_input_No_path, flag_No_models, flag_No_accuracy,
                    flag_Pass_accuracy, flag_No_selftested_function]) == 0:  ## если все флаги погашены, то проходим
                print(f'Проверка функции {fun}')
                print('-' * 20)
                print(f'Функция {fun} прошла тест.')
                return True

            print(f'Проверка функции {fun}')
            print('-' * 20)
            print('Следующие тесты не пройдены:')
            if flag_No_selftested_function:
                print('-Проверьте работоспособность своей функции на собственном изображении.')
            if flag_ret_No_int:
                print("-Функция должна возвращать число, а именно: предсказанную цифру (типа int)")
            if flag_input_No_str_and_model:
                print(
                    '-Проверьте, что функция принимает 1 аргументом путь к изображению типа "str", а 2 аргументом модель.')
            if flag_input_No_path:
                print('-Проверьте, что функция ожидиает путь именно к картинке')
            if flag_No_models:
                print('-Модель не обнаружена')
            if flag_No_accuracy:
                print(f'-Модель не обучена, точность лучшей модели составляет {max(predsfinal)}, требуется минимум 0.5')
            print('-' * 20)
            print()
    print('Ни одна из обнаруженных функций не прошла тест.')
    return False

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
    test()

def Start(_user):
    global user
    user = _user
    check_homework(None)