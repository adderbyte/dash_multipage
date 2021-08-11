import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import requests
import pandas as pd
import io
from PIL import Image
from app import app, cache

final_nlp = pd.read_csv("./assets/finaldf.csv")
Turkishnlp = pd.read_csv("./assets/Turkishnlp.csv")
Englishnlp = pd.read_csv("./assets/Englishnlp.csv")

labels = ['Turkish', 'English']
english = ['POSITIVE', 'NEGATIVE', 'undetermined']
turkish = ['positive', 'negative', 'undetermined']



def bubble_chart():
    fig = px.scatter(final_nlp, x="Count", y="Languages",size="Count", color="Languages",hover_name="Languages", size_max=80, log_x=True)
    return fig
def word_cloud_1():
    complaints_text = list(Turkishnlp["trProcessed"].dropna().values)
    if len(complaints_text) < 1:
        return {}, {}, {}
    text = " ".join(list(complaints_text))

    mask = np.array(Image.open('./assets/turkey1.jpg'))
    wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
    wc.generate(text)
    fig = px.imshow(wc)
    return fig

def word_cloud_2():
    complaints_text = list(Englishnlp["enProcessed"].dropna().values)
    if len(complaints_text) < 1:
        return {}, {}, {}
    text = " ".join(list(complaints_text))

    mask = np.array(Image.open('./assets/world_map-2.jpg'))
    wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
    wc.generate(text)
    fig = px.imshow(wc)
    return fig

BODY = dbc.Container(html.Div([html.H1("NLP", style={
    'textAlign': 'center',
    "font-family": "'Fredoka One', cursive",
    "font-size": "48px",
    "margin-bottom": "35px",
}), dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Count by Language", style={'text-align': 'center', 'font-weight': 800}), style={
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
                #html.P("Country:"),
                # dcc.Dropdown(
                #     id='country-id', 
                #     value='Turkey', 
                #     options=[{'value': x, 'label': x} 
                #             for x in country],
                #     clearable=False
                # ),
                dcc.Graph(figure = bubble_chart(), config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),
            
            html.Br(), html.Br(),
            dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Sentiments for Language", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='values',
                    options=[{'label': i, 'value': i} for i in labels],
                    value='Turkish',
                    placeholder='Filter by region...'
                ),
                
                dcc.Graph(id= 'pie-chart-1', config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),

                html.Br(), html.Br(),
                dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Word Cloud - Turkish", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='words2',
                    options=[{'label': i, 'value': i} for i in turkish],
                    value='positive',
                    placeholder='Filter by region...'
                ),
                # dcc.Dropdown(
                #     id='years-id',
                #     options=[{'label': i, 'value': i}
                #             for i in genders],
                #     value=['total'],
                #     multi=True, placeholder='Filter by sex ...'
                # ),
                #html.P("Country:"),
                # dcc.Dropdown(
                #     id='country-id', 
                #     value='Turkey', 
                #     options=[{'value': x, 'label': x} 
                #             for x in country],
                #     clearable=False
                # ),
                dcc.Graph(id = "turkishcloud", config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),

                html.Br(), html.Br(),
                dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Word Response - Turkish", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='words2-1',
                    options=[{'label': i, 'value': i} for i in turkish],
                    value='positive',
                    placeholder='Filter by sentiment...'
                ),
                dcc.Dropdown(
                    id='word2-id',
                    options=[{'label': i, 'value': i}
                            for i in Turkishnlp.trProcessed.unique()],
                    value='twitter üzerinden reklamlar devam ederse başarılı olacağını düşünüyorum',
                    placeholder='Filter by words ...'
                ),
                # html.P("Country:"),
                # dcc.Dropdown(
                #     id='country-id', 
                #     value='Turkey', 
                #     options=[{'value': x, 'label': x} 
                #             for x in country],
                #     clearable=False
                # ),
                dcc.Graph(id ='table-2', config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),

                html.Br(), html.Br(),
                dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Word Cloud - English", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='words',
                    options=[{'label': i, 'value': i} for i in english],
                    value='POSITIVE',
                    placeholder='Filter by sentiment...'
                ),
                # dcc.Dropdown(
                #     id='years-id',
                #     options=[{'label': i, 'value': i}
                #             for i in genders],
                #     value=['total'],
                #     multi=True, placeholder='Filter by sex ...'
                # ),
                # html.P("Country:"),
                # dcc.Dropdown(
                #     id='country-id', 
                #     value='Turkey', 
                #     options=[{'value': x, 'label': x} 
                #             for x in country],
                #     clearable=False
                # ),
                dcc.Graph(id ='word-1', config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),

                html.Br(), html.Br(),
                dbc.CardBody(html.Div([ dbc.CardHeader(html.H4("Word Response - English", style={'text-align': 'center', 'font-weight': 800}), style={
                   "border-radius": "20px 20px 0px 0px"}),
                dcc.Dropdown(
                    id='words-1',
                    options=[{'label': i, 'value': i} for i in english],
                    value='POSITIVE',
                    placeholder='Filter by sentiment...'
                ),
                dcc.Dropdown(
                    id='word-id',
                    options=[{'label': i, 'value': i}
                            for i in Englishnlp.enProcessed.unique()],
                    value='super',
                    placeholder='Filter by words ...'
                ),
                # html.P("Country:"),
                # dcc.Dropdown(
                #     id='country-id', 
                #     value='Turkey', 
                #     options=[{'value': x, 'label': x} 
                #             for x in country],
                #     clearable=False
                # ),
                dcc.Graph(id ='table-1', config={
        "displaylogo": False
    },
                    ),
                
            ]),
                style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","margin-bottom": "30px", "margin-top": "30px","padding":"1%"}),
]))

# Pie Chart Callback
@app.callback(
    Output("pie-chart-1", "figure"),
    [Input("values", "value")])
def generate_chart(values):
    fig = go.Figure()
    if values == "Turkish":
        count = Turkishnlp["sentimentAnalysis"].value_counts().index[:3].tolist()
        a = Turkishnlp["sentimentAnalysis"].value_counts()
        a.tolist()
        colors = ['#05ed18', '#ff241c', '#0066ff']
        fig = go.Figure(data=[go.Pie(labels=count, values=a)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                    marker=dict(colors=colors))
        #fig.show()
    elif values == "English":
        count = Englishnlp["sentimentAnalysis"].value_counts().index[:3].tolist()
        a = Englishnlp["sentimentAnalysis"].value_counts()
        a.tolist()
        colors = ['#05ed18', '#ff241c', '#0066ff']
        fig = go.Figure(data=[go.Pie(labels=count, values=a)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                    marker=dict(colors=colors))
        #fig.show()
    return fig

###English wordcloud    
@app.callback(
    Output("word-1", "figure"),
    [Input("words", "value")])
def generate_cloud(words):
    fig = go.Figure()
    if words == "POSITIVE":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'NEGATIVE') & (Englishnlp.sentimentAnalysis != 'undetermined')]
        complaints_text = list(Englishnlp1["enProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/world_map-2.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    elif words == "NEGATIVE":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'POSITIVE') & (Englishnlp.sentimentAnalysis != 'undetermined')]
        complaints_text = list(Englishnlp1["enProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/world_map-2.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    elif words == "undetermined":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'POSITIVE') & (Englishnlp.sentimentAnalysis != 'NEGATIVE')]
        complaints_text = list(Englishnlp1["enProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/world_map-2.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    return fig

###Turkish Word cloud
@app.callback(
    Output("turkishcloud", "figure"),
    [Input("words2", "value")])
def generate_cloud(words):
    fig = go.Figure()
    if words == "positive":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'negative') & (Turkishnlp.sentimentAnalysis != 'undetermined')]
        complaints_text = list(Turkishnlp1["trProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/turkey1.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    elif words == "negative":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'positive') & (Turkishnlp.sentimentAnalysis != 'undetermined')]
        complaints_text = list(Turkishnlp1["trProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/turkey1.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    elif words == "undetermined":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'positive') & (Turkishnlp.sentimentAnalysis != 'negative')]
        complaints_text = list(Turkishnlp1["trProcessed"].dropna().values)
        if len(complaints_text) < 1:
            return {}, {}, {}
        text = " ".join(list(complaints_text))

        mask = np.array(Image.open('./assets/turkey1.jpg'))
        wc = WordCloud(stopwords=STOPWORDS,
               mask=mask, background_color="white",
               max_words=2000, max_font_size=256,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0])
        wc.generate(text)
        fig = px.imshow(wc)
        #fig.show()
    return fig

@app.callback(
    Output("table-1", "figure"),
    [Input("words-1", "value"), Input("word-id", "value")])
def generate_cloud(words_1, word_id):
    fig = go.Figure()
    if words_1 == "POSITIVE":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'NEGATIVE') & (Englishnlp.sentimentAnalysis != 'undetermined')]
        Englishnlp2 = Englishnlp1[(Englishnlp1.enProcessed == word_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Englishnlp2['enProcessed'], # 1st column
                       Englishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])       
        #fig.show()
    elif words_1 == "NEGATIVE":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'POSITIVE') & (Englishnlp.sentimentAnalysis != 'undetermined')]
        Englishnlp2 = Englishnlp1[(Englishnlp1.enProcessed == word_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Englishnlp2['enProcessed'], # 1st column
                       Englishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])       

        #fig.show()
    elif words_1 == "undetermined":
        Englishnlp1 = Englishnlp[(Englishnlp.sentimentAnalysis != 'POSITIVE') & (Englishnlp.sentimentAnalysis != 'NEGATIVE')]
        Englishnlp2 = Englishnlp1[(Englishnlp1.enProcessed == word_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Englishnlp2['enProcessed'], # 1st column
                       Englishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
]) 
        #fig.show()
    return fig

@app.callback(
    Output("table-2", "figure"),
    [Input("words2-1", "value"), Input("word2-id", "value")])
def generate_cloud(words2_1, word2_id):
    fig = go.Figure()
    if words2_1 == "positive":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'negative') & (Turkishnlp.sentimentAnalysis != 'undetermined')]
        Turkishnlp2 = Turkishnlp1[(Turkishnlp1.trProcessed == word2_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Turkishnlp2['trProcessed'], # 1st column
                       Turkishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])       
        #fig.show()
    elif words2_1 == "negative":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'positive') & (Turkishnlp.sentimentAnalysis != 'undetermined')]
        Turkishnlp2 = Turkishnlp1[(Turkishnlp1.trProcessed == word2_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Turkishnlp2['trProcessed'], # 1st column
                       Turkishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])       

        #fig.show()
    elif words2_1 == "undetermined":
        Turkishnlp1 = Turkishnlp[(Turkishnlp.sentimentAnalysis != 'positive') & (Turkishnlp.sentimentAnalysis != 'negative')]
        Turkishnlp2 = Turkishnlp1[(Turkishnlp1.enProcessed == word2_id)]
        fig = go.Figure(data=[go.Table(
        header=dict(values=['Word Selected', 'Response'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
        cells=dict(values=[Turkishnlp2['trProcessed'], # 1st column
                       Turkishnlp2['10']], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
]) 
        #fig.show()
    return fig
# # Bar Chart Callback


# @app.callback(
#     Output("bar-chart", "figure"),
#     [Input("dropdown", "value"), Input("crossfilter-yaxis-type", "value")])
# def update_bar_chart(label, yaxis_type):
#     if yaxis_type == 'Linear':
#         fig = px.bar(c, x='heading', y=label, labels={
#                         "heading": "Survey"
#                     },)
#         fig = fig.update_traces(marker_color='#7F3C8D')
#         fig = fig.update_layout(plot_bgcolor='rgb(255,255,255)')
#     else:
#         fig = px.bar(l, x='heading', y=label, labels={
#                         "heading": "Survey"
#                     },)
#     # fig = fig.update_yaxes(type='linear' if yaxis_type == 'Linear' else 'log')
#         fig = fig.update_traces(marker_color='#7F3C8D')
#     # fig = fig.update_yaxes(type='log')
#         fig = fig.update_layout(plot_bgcolor='rgb(255,255,255)')
#         # l[label] = c[label]

#     return fig


# app.run_server(debug=True)

# def layout6():
#     return html.Div(children=[BODY])

# if __name__ == '__main__':
#     app.run_server(debug=True)

def layout4():
    return html.Div(children=[BODY])
