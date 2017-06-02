from core.sample_matrix import get_sample_matrix

from ipywidgets import Button
from IPython.display import display, clear_output


# Путь к данным
path = './data/'
outpath = './data/matricies/'


def display_matrix_widget(path, outpath):
    matrix_btn = Button(description='Получить матрицу', tooltip='Click me',
                        icon='check', button_style='success')

    def matrix_btn_click(b):
        print('Пожалуйста, подождите...')
        clear_output()
        get_sample_matrix(path, outpath)
        print('Готово.')

    matrix_btn.on_click(matrix_btn_click)
    display(matrix_btn)
