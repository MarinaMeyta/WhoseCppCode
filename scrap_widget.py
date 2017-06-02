from ipywidgets import Text, IntSlider, Box, Layout, Label, Dropdown, Textarea, Button
from IPython.display import display, HTML, clear_output

from core.github_scrapper import scrap
from core.encoder import correctEncoding
from core.whose_cpp_code import get_filenames
import re


def display_scrapping_form():
    form_layout = Layout(
        display='flex',
        flex_flow='column',
        align_items='stretch',
        width='50%'
    )

    form_item_layout = Layout(
        display='flex',
        flex_flow='row',
        justify_content='space-between'
    )

    username = Text()
    password = Text()
    userlist_field = Textarea(placeholder='Список пользователей')

    scrap_form_items = [
        Box([Label(value='Логин:'), username], layout=form_item_layout),
        Box([Label(value='Пароль:'), password], layout=form_item_layout),
        Box([Label(value='Найти:'), userlist_field], layout=form_item_layout),
    ]

    def get_userlist():
        userlist_raw = userlist_field.value
        userlist = re.findall('[^\n\.\,\s]+', userlist_raw)
        return userlist

    def scrap_github(b):
        clear_output()
        if username.value and password.value:
            print('Идет сбор файлов, пожалуйста, подождите...\n')
            userlist = get_userlist()
            scrap(userlist, username.value, password.value)
            filenames, authors = get_filenames('./data/')
            [correctEncoding(filename) for filename in filenames]
            print('Готово. Данные расположены в корне проекта в папке data.\n\nЕсли данные не были загружены, проверьте правильность ввода логина, пароля, а также имен пользователей.')
        else:
            print('Пожалуйста, введите данные для аутентификации на сайте www.github.com.')

    scrap_form = Box(scrap_form_items, layout=form_layout)
    scrap_button = Button(description='Получить данные', tooltip='Click me',
                          icon='check', button_style='success')
    scrap_button.on_click(scrap_github)
    display(scrap_form, scrap_button)
