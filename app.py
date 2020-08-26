# Import required libraries
import os

import pandas as pd
import numpy as np
import base64
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bio

try:
    from layout_helper import run_standalone_app
except ModuleNotFoundError:
    from .layout_helper import run_standalone_app


DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

COUNTRIES = {   #'VALUE': 'LABEL'
    'US': 'United States',
    'CA': 'Canada'
}

YEARS = [1,3,5]

DATASETS = {  #'VALUE': ['LABEL', header?]
    'plot': ['Plot', False],
    'table': ['Table', True]
}

IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'maxresdefault.jpg')
IMG = base64.b64encode(open(IMG_PATH, 'rb').read()).decode()

SHOW = {'display': 'block'}
HIDE = {'display': 'none'}


def description():
    return 'Interactively identify clinically meaningful markers in genomic \
    experiments with this volcano plot.'


def header_colors():
    return {
        'bg_color': '#19d3f3',
        'font_color': 'white',
        'light_logo': True
    }


def layout():
    return html.Div(id='vp-page-content', className='app-body', children=[
        html.Div(
            id='vp-graph-div',
            children=[
                html.Div(id='dropdown-area', children=[
                    html.Div(id='dropdown-wrapper', children=[
                        dcc.Dropdown(
                            id='header-dropdown',
                            options=[
                                {
                                    'label': str(year)+'-year stat',
                                    'value': year
                                }
                                for year in YEARS
                            ],
                            value=YEARS[0],
                        ),                        
                    ]),
                    html.Div(id='dropdown-wrapper2', children=[
                        dcc.Dropdown(
                            id='header-dropdow2',
                            options=[
                                {
                                    'label': str(year)+'-year stat2',
                                    'value': year
                                }
                                for year in YEARS
                            ],
                            value=YEARS[0],
                        ),      
                        dcc.Dropdown(
                            id='header-dropdow3',
                            options=[
                                {
                                    'label': str(year)+'-year stat3',
                                    'value': year
                                }
                                for year in YEARS
                            ],
                            value=YEARS[0],
                        ),                           
                    ]),                    
                ]),
                html.Img(id='startup_img', src='data:image/png;base64,{}'.format(IMG)),
                dcc.Graph(
                    id='vp-graph'
            )],
        ),
        html.Div(id='vp-control-tabs', className='control-tabs', children=[
            dcc.Tabs(id='vp-tabs', value='what-is', children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children='What is Volcano Plot?'),
                        html.P(
                            'You can use Volcano Plot to interactively '
                            'identify clinically meaningful markers in '
                            'genomic experiments, i.e., markers that are '
                            'statistically significant and have an effect '
                            'size greater than some threshold. '
                            'Specifically, volcano plots depict the negative '
                            'log-base-10 p-values plotted against their '
                            'effect size.'
                        ),
                        html.P(
                            'In the "Data" tab, you can select a dataset '
                            'to view on the plot. In the "View" tab, you '
                            'can control the color of the highlighted '
                            'points, as well as the threshold lines that '
                            'define which values are significant. You can '
                            'also access metadata from hovering and '
                            'clicking on the graph.'
                        )
                    ])
                ),
                dcc.Tab(
                    label='Data',
                    value='data',
                    children=html.Div(className='control-tab', children=[
                        html.Div(className='app-controls-block', children=[
                            html.Div(
                                className='app-controls-name',
                                children='Country: '
                            ),
                            dcc.Dropdown(
                                id='vp-dataset-dropdown1',
                                options=[
                                    {
                                        'label': COUNTRIES[country],
                                        'value': country
                                    }
                                    for country in COUNTRIES
                                ],
                            ),
                            html.Div(
                                className='app-controls-name',
                                children='Dataset:'
                            ),                            
                            dcc.Dropdown(
                                id='vp-dataset-dropdown2',
                                options=[
                                    {
                                        'label': DATASETS[dataset][0],
                                        'value': dataset
                                    }
                                    for dataset in DATASETS
                                ],
                            )                            
                        ])
                    ])
                ),
            ])
        ])
    ])


def callbacks(_app):
    @_app.callback(
        [
            Output('dropdown-wrapper', 'style'),
        ],
        [
            Input('vp-dataset-dropdown2', 'value'),
        ]
    )
    def update_header(drop2):
        if drop2 in DATASETS and DATASETS[drop2][1]:
            return [SHOW]
        else:
            return [HIDE]
        
    @_app.callback(
        [
            Output('startup_img', 'style'),
            Output('vp-graph', 'style'),
            Output('vp-graph', 'figure'),
        ],
        [
            Input('vp-dataset-dropdown1', 'value'),
            Input('vp-dataset-dropdown2', 'value'),
            Input('header-dropdown', 'value'),
        ]
    )
    def update_figure(country, dataset, year):
        if country in COUNTRIES and dataset in DATASETS:
            if not DATASETS[dataset][1] or year in YEARS:
                figure = {}
                if country == 'US':
                    if dataset == 'plot':
                        figure = {}
                    else:
                        # table
                        figure = {}
                else:
                    if dataset == 'plot':
                        figure = {}
                    elif year == 1:
                        figure = {}
                    elif year == 3:
                        figure = {}
                    else:
                        figure = {}
                return HIDE, SHOW, figure
        return SHOW, HIDE, {}
    
    
# only declare app/server if the file is being run directly
if 'DEMO_STANDALONE' not in os.environ:
    app = run_standalone_app(layout, callbacks, header_colors, __file__)
    server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
