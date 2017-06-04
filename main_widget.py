from ipywidgets import IntSlider, Box, Layout, Label, Dropdown, Button
from IPython.display import display, HTML, clear_output
from core.whose_cpp_code import classify_authors
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
import time


init_notebook_mode(connected=True)
warnings.filterwarnings("ignore")


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


# loops = IntSlider(min=1, max=10)
data = Dropdown(options={'students': './matricies/students/',
                         'GoogleCodeJam': './matricies/GoogleCodeJam/',
                         'GitHub': './matricies/GitHub_short/',
                         'user_data': './data/matricies'})
classifier = Dropdown(options={'RandomForest': 'RandomForestClassifier',
                               'ExtraTrees': 'ExtraTreesClassifier',
                               'AdaBoost': 'AdaBoostClassifier'})


def make_metrics_bar(metrics, loops_num):

    trace0 = go.Bar(
        x=list(range(1, loops_num + 1)),
        y=metrics['f1_score'],
        name='F1-score',
        marker=dict(
            color='rgb(136, 142, 150)'
        )
    )
    trace1 = go.Bar(
        x=list(range(1, loops_num + 1)),
        y=metrics['precision'],
        name='Precision',
        marker=dict(
            color='rgb(204,204,204)',
        )
    )
    trace2 = go.Bar(
        x=list(range(1, loops_num + 1)),
        y=metrics['recall'],
        name='Recall',
        marker=dict(
            color='rgb(144, 177, 229)',
        )
    )
    trace3 = go.Bar(
        x=list(range(1, loops_num + 1)),
        y=metrics['accuracy'],
        name='Accuracy',
        marker=dict(
            color='rgb(49,130,189)',
        )
    )

    data = [trace0, trace1, trace2, trace3]
    layout = go.Layout(
        xaxis=dict(
            tickangle=-45,
            title='Number of experiment',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='Value, %',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        barmode='group',
        title='Classification metrics',
    )

    fig = go.Figure(data=data, layout=layout)
    iplot(fig, filename='metrics-bar')


def make_pie(mean_accuracy):
    fig = {
        "data": [
          {
              "values": [1 - mean_accuracy, mean_accuracy],
              "labels": ['Wrong predicted samples, %', 'True predictes samples, %'],
              "type": "pie",
              "text": "Accuracy",
              "textposition":"inside",
              "hole": .4,
              #       "domain": {"x": [.52, 1]},
          }],
        "layout": {
            "title": 'Total mean accuracy',

            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Accuracy",
                }
            ]
        }
    }
    iplot(fig)


loops = IntSlider(min=1, max=10)

form_items = [
    Box([Label(value='Циклов:'), loops], layout=form_item_layout),
    Box([Label(value='Данные:'), data], layout=form_item_layout),
    Box([Label(value='Алгоритм:'), classifier], layout=form_item_layout),
]


def classify_mul(b):
    clear_output()
    accuracy, precision, recall, f1_score = [], [], [], []
    start_time = time.time()
    for loop in range(loops.value):
        print('Цикл ', loop + 1, ': Пожалуйста, ожидайте...')
        report = classify_authors(data.value, classifier.value)
        df = pd.DataFrame(report)
        accuracy.append(np.mean(df['accuracy'].tolist()))
        precision.append(np.mean(df['precision'].tolist()))
        recall.append(np.mean(df['recall'].tolist()))
        f1_score.append(np.mean(df['f1_score'].tolist()))

    run_time = round(time.time() - start_time, 2)
    print('Время работы, сек.: ', run_time)

    metrics = {'f1_score': f1_score,
               'precision': precision,
               'recall': recall,
               'accuracy': accuracy
               }
    make_metrics_bar(metrics, loops.value)

    mean_accuracy = np.mean(accuracy)
    make_pie(mean_accuracy)

    # saving results to csv
    metrics.update({'classifier': classifier.value})
    result_df = pd.DataFrame(metrics)
    result_df.to_csv('./results/results.csv', mode='a')


def display_main_form():
    form = Box(form_items, layout=form_layout)
    classify_mul_btn = Button(description='Классифицировать', tooltip='Click me',
                              icon='check', button_style='success')
    classify_mul_btn.on_click(classify_mul)
    display(form, classify_mul_btn)
