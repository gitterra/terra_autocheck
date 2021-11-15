import ipywidgets as widgets
#SERVER = 'http://127.0.0.1:8000/'              # Адрес сервера
SERVER = 'https://aiu-check-homework.herokuapp.com/'
PAGE_CHECK = 'app_check/api-v0/check'          # Страница проверки ответов пользователя
PAGE_QUESTION = 'app_check/api-v0/questions'   # Страница получения вопросов
PAGE_LOGIN = 'app_check/api-v0/autorization'   # Страница получения вопросов

# Тексты на кнопках
BUTTONS_TEXT = ['Проверить',
                'Пересдать',
                ' Зачесть ДЗ',
                'Приступить']

answer_buttons = []                            # Список кнопок с ответами на вопросы
questions_id = []                              # Список id вопросов

# Создание кнопки «Проверить»
button_check = widgets.Button(
    description=BUTTONS_TEXT[0],
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip=BUTTONS_TEXT[0],
    icon='search' # (FontAwesome names without the `fa-` prefix)
)

 # Создание кнопки «Пересдать»
button_retake = widgets.Button(
    description=BUTTONS_TEXT[1],
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    tooltip=BUTTONS_TEXT[1],
    icon='refresh' # (FontAwesome names without the `fa-` prefix)
)

# Создание кнопки «Зачесть ДЗ»
button_send_homework = widgets.Button(
    description=BUTTONS_TEXT[2],
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip=BUTTONS_TEXT[2],
    icon='check-circle'
)   
 
# Создание кнопки «Приступить»
button_start = widgets.Button(
    description=BUTTONS_TEXT[3],
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip=BUTTONS_TEXT[0],
    icon='pencil' # (FontAwesome names without the `fa-` prefix)
)

# Создание поля ввода логина
login_text= widgets.Text(
    value='',
    placeholder='login@login.com',
    description='Введите ваш логин (email) на учебной платформе:',
    disabled=False,
    layout=widgets.Layout(width='600px'),
    style={'description_width': 'initial'},
)