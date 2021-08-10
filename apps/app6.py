import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app, cache
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go

import requests
import pandas as pd
import io
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFscyI6InByaXZhdGUtZGF0YS1wbGF0Zm9ybS1rZXkgZm9yIGFscGhhIiwiY3JlYXRlZEF0IjoiMjAyMS0wNi0yOFQxODoxNjoyOC4yNThaIiwiaWF0IjoxNjI0OTA0MTg4fQ.ITcG3EO90Uzc9JZYjE6g5mbmh4kkHBDO6QEumQ8ZruQ'
url = "https://endapi.truefeedback.io/dataplatform/survey/"
s = requests.get(url, headers={"auth": token}).content
c = pd.read_json(s)

c['heading'] = c['title']
for i in range(len(c)):
    c['heading'][i] = c['title'][i]['tr']
c = c.dropna()
c['heading'] = c['heading'].replace(['Kentplaza Carrefour Anketi'],'Company A')
c['heading'] = c['heading'].replace(['Konya Elektronik Market Anketi'],'Company B')

l = pd.read_json(s)
l['heading'] = l['title']
for i in range(len(l)):
    l['heading'][i] = l['title'][i]['tr']
l = l.dropna()
l['heading'] = l['heading'].replace(['Kentplaza Carrefour Anketi'],'Company A')
l['heading'] = l['heading'].replace(['Konya Elektronik Market Anketi'],'Company B')
l['totalTfb'] = np.log2(l['totalTfb'])
l["participantLimit"] = np.log2(l["participantLimit"])
l['answerCount'] = np.log2(l['answerCount'])

labels = ['totalTfb', 'participantLimit', 'answerCount']

df = pd.read_csv('./assets/displaydata.csv')
df.set_index('index')
# app = dash.Dash()
years = np.array(['0-20', '20-30', '30-40', '40-50', '50-above'])
genders = np.array(['female', 'male', 'Not Specified'])

cf = pd.read_csv('./assets/displaydata.csv')
cf.set_index('index')
cf['Not Specified']=cf['total']-(cf['male']+cf['female'])
cf = cf.drop(['total', '0-20', '20-30', '30-40', '40-50', '50-above'], axis = 1)
cf = cf.transpose()
cf = cf.set_axis(cf.loc['index'].to_list(), axis=1)
new_df2 = cf.iloc[2:5,:]
country = cf.loc['index'].to_list()


BODY = dbc.Container(html.Div([html.H1("Visualization", style={
    'textAlign': 'center',
    "font-family": "'Fredoka One', cursive",
    "font-size": "48px",
    "margin-bottom": "35px",
}), dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("User Count by Gender", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                # dcc.Dropdown(
                #     id='state-id',
                #     options=[{'label': i, 'value': i} for i in df.countryNames.unique()], multi=True,
                #     value=['Turkey'],
                #     placeholder='Filter by region...'
                # ),
                # dcc.Dropdown(
                #     id='years-id',
                #     options=[{'label': i, 'value': i}
                #             for i in genders],
                #     value=['total'],
                #     multi=True, placeholder='Filter by sex ...'
                # ),
                html.P("Country:"),
                dcc.Dropdown(
                    id='country-id', 
                    value='Turkey', 
                    options=[{'value': x, 'label': x} 
                            for x in country],
                    clearable=False
                ),
                dcc.Graph(id='indicator', config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),
            
            html.Br(), html.Br(),
            dbc.CardBody(html.Div([dbc.CardHeader(html.H4("User Count by Age Distribution", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='state1-id',
                    options=[{'label': i, 'value': i} for i in df.countryNames.unique()], multi=True,
                    value=['Turkey'],
                    placeholder='Filter by region...'
                ),
                dcc.Dropdown(
                    id='age-id',
                    options=[{'label': i, 'value': i}
                            for i in years],
                    value=['20-30'],
                    multi=True, placeholder='Filter by age group ...'
                ),
                
                dcc.Graph(id='indicator-1', config={
        "displaylogo": False
    },),
                
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","padding":"1%", "margin-bottom": "30px"}),
            
            html.Br(), html.Br(),
    dbc.CardBody(html.Div([dbc.CardHeader(html.H4("Survey Count ", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in labels],
            value=labels[0],
            clearable=False,
        ),
        dcc.RadioItems(
            id='crossfilter-yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block', 'marginTop': '5px'}
        ),
        dcc.Graph(id="bar-chart", config={
        "displaylogo": False
    },),
    ]), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
               "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"}),
    html.Br(), html.Br(), html.Br(),
    dbc.CardBody(html.Div([dbc.CardHeader(html.H4("Survey Percentage ", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
        dcc.Dropdown(
            id='values',
            value='totalTfb',
            options=[{'value': x, 'label': x}
                     for x in labels],
            clearable=False
        ),
        dcc.Graph(id="pie-chart", config={
        "displaylogo": False
    },),
    ]), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
               "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8", "margin-bottom": "50px"}
), ]))



@app.callback(
    Output('indicator-1', 'figure'),
    [Input('state1-id', 'value'), Input('age-id', 'value')])
def update_bar_graph(state_1, age_id):

    # print(dff.head())
    data = []
    for state in state_1:
        for age in age_id:
            # for indicator_id in indicator_ids:
            dff = df.loc[(df['countryNames'] == state)]
            trace = go.Bar(
                x=[age],
                y=dff[age],
                name=state + ' Age Group: ' + age + ' User Count',

            )
            data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'Age Group'},
            yaxis={'title': 'User Count by Age distribution'},
            barmode='group'
        )
    }



@app.callback(
    Output('indicator', 'figure'),
    [Input('country-id', 'value')])
# def update_time_series(country_id):
def generate_chart(country_id):
    labels = ['female','male','Not Specified']
    values = new_df2[country_id].to_list()
    fig = px.pie(cf, values=values, names=labels)
    fig.show()
    return fig

    # print(dff.head())
    # data = []
    # for state in state_id:
    #     for year in years_id:
    #         # for indicator_id in indicator_ids:
    #         dff = df.loc[(df['countryNames'] == state)]
    #         trace = go.Bar(
    #             x=[year],
    #             y=dff[year],
    #             name=state + ' ' + year + ' User Count',
    #         )
    #         data.append(trace)

    # return {
    #     'data': data,
    #     'layout': go.Layout(
    #         xaxis={'title': 'Gender'},
    #         yaxis={'title': 'User Count By Gender'},
    #         barmode='group'
    #     )
    #}



# Pie Chart Callback
@app.callback(
    Output("pie-chart", "figure"),
    [Input("values", "value")])
def generate_chart(values):
    fig = px.pie(c, values=values, names='heading')
    return fig

# Bar Chart Callback


@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value"), Input("crossfilter-yaxis-type", "value")])
def update_bar_chart(label, yaxis_type):
    if yaxis_type == 'Linear':
        fig = px.bar(c, x='heading', y=label, labels={
                        "heading": "Survey"
                    },)
        fig = fig.update_traces(marker_color='#7F3C8D')
        fig = fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    else:
        fig = px.bar(l, x='heading', y=label, labels={
                        "heading": "Survey"
                    },)
    # fig = fig.update_yaxes(type='linear' if yaxis_type == 'Linear' else 'log')
        fig = fig.update_traces(marker_color='#7F3C8D')
    # fig = fig.update_yaxes(type='log')
        fig = fig.update_layout(plot_bgcolor='rgb(255,255,255)')
        # l[label] = c[label]

    return fig


# app.run_server(debug=True)

def layout6():
    return html.Div(children=[BODY])


# # -*- coding: utf-8 -*-
# """
# Module doc string
# """
# import pathlib
# import re
# import json
# from datetime import datetime
# import flask
# import dash
# import dash_table
# import matplotlib.colors as mcolors
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import plotly.express as px
# import pandas as pd
# import numpy as np
# from apps.dask_dash_app3.precomputing import add_stopwords
# from dash.dependencies import Output, Input, State
# from dateutil import relativedelta
# from wordcloud import WordCloud, STOPWORDS
# #from ldacomplaints import lda_analysis
# from sklearn.manifold import TSNE
# from app import app, cache
# import io
# import requests
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFscyI6InByaXZhdGUtZGF0YS1wbGF0Zm9ybS1rZXkgZm9yIGFscGhhIiwiY3JlYXRlZEF0IjoiMjAyMS0wNi0yOFQxODoxNjoyOC4yNThaIiwiaWF0IjoxNjI0OTA0MTg4fQ.ITcG3EO90Uzc9JZYjE6g5mbmh4kkHBDO6QEumQ8ZruQ'
# url = "https://endapi.truefeedback.io/dataplatform/survey/"
# s = requests.get(url, headers={"auth": token}).content
# c = pd.read_json(s)

# c['heading'] = c['title']
# for i in range(len(c)):
#     c['heading'][i] = c['title'][i]['tr']
# c = c.dropna()

# EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# #FILENAME = "data/trufeed.csv"
# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# #GLOBAL_DF = pd.read_csv(DATA_PATH.joinpath(FILENAME), header=0)


# LDA_PLOT = dcc.Loading(
#     id="loading-lda-plot", children=[dcc.Graph(id="tsne-lda")], type="default"
# )
# df = px.data.tips()
# days = df.day.unique()

# app = dash.Dash(__name__)

# BAR_GRAPH = [
#     html.Div([
#         dcc.Dropdown(
#             id="dropdown",
#             options=[{"label": x, "value": x} for x in days],
#             value=days[0],
#             clearable=False,
#         ),
#         dcc.Graph(id="bar-chart"),
#     ])
# ]


# BODY = dbc.Container(
#     [html.H1("Statistical Models", style={
#         'textAlign': 'center',
#         # 'color': colors['background'],
#         # 'width': '100vw',
#         "font-family": "'Fredoka One', cursive",
#         "font-size": "48px",
#         "margin-bottom": "35px",
#         # "margin-right": "50px"
#     }),
#         dbc.Row([dbc.Col(dbc.Card(BAR_GRAPH, style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
#                                                     "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"}))],
#                 style={"marginTop": 30}),
#         #     dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_PLOT, style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
#         #                                                       "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"})), ],
#         #             style={"marginTop": 30}),
#         #     dbc.Row(
#         #         [
#         #             dbc.Col(LEFT_COLUMN, md=4, align="center"),
#         #             dbc.Col(dbc.Card(TOP_BANKS_PLOT, style={
#         #                     "border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
#         #                     "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"}), md=8),
#         #         ],
#         #         style={"marginTop": 30},
#         # ),
#         # dbc.Card(WORDCLOUD_PLOTS, style={
#         #     "border-radius": "20px", "border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
#         #     "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"}),
#         # dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS, style={
#         #         "border-radius": "20px", "border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
#         #         "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8"})])], style={"marginTop": 50, "marginBottom": 100}),
#     ],
#     className="mt-12",
# )

# app.layout = BAR_GRAPH


# def layout():
#     return html.Div(children=[BODY])


# @app.callback(
#     Output("bar-chart", "figure"),
#     [Input("dropdown", "value")])
# def update_bar_chart(day):
#     mask = df["day"] == day
#     fig = px.bar(df[mask], x="sex", y="total_bill",
#                  color="smoker", barmode="group")
#     return fig
