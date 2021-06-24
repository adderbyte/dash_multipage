import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from distributed import Client, LocalCluster
from app import app,cache

import pandas as pd
from loader import *


@cache.memoize()
def datas():

    df = px.data.iris()
    return df

def layoutAl():
    return  html.Div([
    dcc.Graph(id="scatter-plotall"),
    html.P("Petal Width:"),
    dcc.RangeSlider(
        id='range-sliderall',
        min=0, max=2.5, step=0.1,
        marks={0: '0', 2.5: '2.5'},
        value=[0.5, 2]
    ),
])

@app.callback(
    Output("scatter-plotall", "figure"), 
    [Input("range-sliderall", "value")])
def update_bar_chart(slider_range):
    low, high = slider_range
    df = datas()
    print(df.head(),flush=True)
    mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(
        df[mask], x="sepal_width", y="sepal_length", 
        color="species", size='petal_length', 
        hover_data=['petal_width'])
    return fig



#df  = data() 
# @cache.memoize()
# def datas():
#     df = pd.read_csv("/assets/displaydata.csv",index_col=[0])
#     return df


# print("jkhgfdsfzghjkl;",df.head(),flush=True)

# PAGE_SIZE = 5

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# def layoutAll():

#     layoutdis= html.Div(
#     className="row",
#     children=[
#         html.H1("Users Interactive Plot", style={
#             'textAlign': 'center',
#             'color': colors['background']
#         }),
#         # html.Div(
#         #     html.Link(href='/assets/GUI.css', rel='stylesheet'),
            
#         #     dash_table.DataTable(
#         #         id='table-paging-with-graph',
#         #         columns=[
#         #             {"name": i, "id": i} for i in df.columns
#         #         ],
#         #         page_current=0,
#         #         page_size=20,
#         #         page_action='custom',

#         #         filter_action='custom',
#         #         filter_query='',
#         #         style_cell=dict(textAlign='center', font_family = "cursive",font_size= '16px'),
#         #         style_header=dict(backgroundColor="#97D987",font_family='sans-serif',
#         #         font_size= '20px'),
#         #         style_data=dict(backgroundColor="#EBF9D7"),

#         #         sort_action='custom',
#         #         sort_mode='multi',
#         #         sort_by=[]
#         #     ),
#         #     style={'height': 750, 'overflowY': 'scroll'},
#         #     className='six columns'
#         # ),
#         # html.Div(
#         #     id='table-paging-with-graph-container',
#         #     className="five columns"
#         # )
#     ]
# )
#     return layoutdis

# operators = [['ge ', '>='],
#              ['le ', '<='],
#              ['lt ', '<'],
#              ['gt ', '>'],
#              ['ne ', '!='],
#              ['eq ', '='],
#              ['contains '],
#              ['datestartswith ']]


# def split_filter_part(filter_part):
#     for operator_type in operators:
#         for operator in operator_type:
#             if operator in filter_part:
#                 name_part, value_part = filter_part.split(operator, 1)
#                 name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

#                 value_part = value_part.strip()
#                 v0 = value_part[0]
#                 if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
#                     value = value_part[1: -1].replace('\\' + v0, v0)
#                 else:
#                     try:
#                         value = float(value_part)
#                     except ValueError:
#                         value = value_part

#                 # word operators need spaces after them in the filter string,
#                 # but we don't want these later
#                 return name, operator_type[0].strip(), value

#     return [None] * 3


# @app.callback(
#     Output('table-paging-with-graph', "data"),
#     Input('table-paging-with-graph', "page_current"),
#     Input('table-paging-with-graph', "page_size"),
#     Input('table-paging-with-graph', "sort_by"),
#     Input('table-paging-with-graph', "filter_query"))
# def update_table(page_current, page_size, sort_by, filter):
#     filtering_expressions = filter.split(' && ')
#     dff = datas()
#     for filter_part in filtering_expressions:
#         col_name, operator, filter_value = split_filter_part(filter_part)

#         if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
#             # these operators match pandas series operator method names
#             dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
#         elif operator == 'contains':
#             dff = dff.loc[dff[col_name].str.contains(filter_value)]
#         elif operator == 'datestartswith':
#             # this is a simplification of the front-end filtering logic,
#             # only works with complete fields in standard format
#             dff = dff.loc[dff[col_name].str.startswith(filter_value)]

#     if len(sort_by):
#         dff = dff.sort_values(
#             [col['column_id'] for col in sort_by],
#             ascending=[
#                 col['direction'] == 'asc'
#                 for col in sort_by
#             ],
#             inplace=False
#         )

#     return dff.iloc[
#         page_current*page_size: (page_current + 1)*page_size
#     ].to_dict('records')


# @app.callback(
#     Output('table-paging-with-graph-container', "children"),
#     Input('table-paging-with-graph', "data"))
# def update_graph(rows):
#     dff = pd.DataFrame(rows)
#     return html.Div(
#         [
#             dcc.Graph(
#                 id=column,
#                 figure={
#                     "data": [
#                         {
#                             "x": dff["countryNames"],
#                             "y": dff[column] if column in dff else [],
#                             "type": "bar",
#                             "marker": {"color": "#0074D9"},
#                             "color":dff["male"],
#                             'line_color':'red',#dict(color='purple')
#                             #"name": dff["countryNames"]
#                         }
#                     ],
#                     "layout": {
#                         "xaxis": {"automargin": True},
#                         "yaxis": {"automargin": True},
#                         "height": 250,
#                         "margin": {"t": 30, "l": 10, "r": 30},
#                         'title': column + " plot per country"
#                         #"color":"female"
#                     },
#                 },
#             )
#             for column in ["total"]
#         ]
#     )

# @cache.memoize()
# def displayall():
#     import modin.pandas as pd
#     # Dask Local Cluster 
#     cluster = LocalCluster()
#     client = Client(cluster)
#     app = dash.Dash(__name__)


#     df = pd.read_csv("../data/displaydata.csv",index_col=[0])
#     #df.columns = ['Countries','Gender','Age group','Size Count']



#     PAGE_SIZE = 5

#     colors = {
#         'background': '#302f2f',
#         'text': '#7FDBFF'
#     }

#     app.layout = html.Div(style={
#                 'background-color': '#302f2f'},
#         className="row",
#         children=[
#             html.H1("TRUEFEEDBACKCHAIN ANALYTICS PLATFORM", style={
#                 'textAlign': 'center',
#                 'color': '#ffc72e',
#                 'font-weight': 1000,
#                 'background-color': '#302f2f'
#             }),
#             html.Div(
#                 dash_table.DataTable(
#                     id='table-paging-with-graph',
#                     columns=[
#                         {"name": i, "id": i} for i in df.columns
#                     ],
#                     page_current=0,
#                     page_size=20,
#                     page_action='custom',

#                     filter_action='custom',
#                     filter_query='',
#                     style_cell=dict(textAlign='center', font_family = "Helvetica",font_size= '16px'),
#                     style_header=dict(backgroundColor="#ff9233",font_family='sans-serif',
#                     font_size= '20px'),
#                     style_data=dict(backgroundColor="#ffc72e"),

#                     sort_action='custom',
#                     sort_mode='multi',
#                     sort_by=[]
#                 ),
#                 style={'height': 750, 'overflowY': 'scroll'},
#                 className='six columns'
#             ),
#             html.Div(
#                 id='table-paging-with-graph-container',
#                 className="five columns"
#             )
#         ]
#     )

#     operators = [['ge ', '>='],
#                 ['le ', '<='],
#                 ['lt ', '<'],
#                 ['gt ', '>'],
#                 ['ne ', '!='],
#                 ['eq ', '='],
#                 ['contains '],
#                 ['datestartswith ']]


#     def split_filter_part(filter_part):
#         for operator_type in operators:
#             for operator in operator_type:
#                 if operator in filter_part:
#                     name_part, value_part = filter_part.split(operator, 1)
#                     name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

#                     value_part = value_part.strip()
#                     v0 = value_part[0]
#                     if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
#                         value = value_part[1: -1].replace('\\' + v0, v0)
#                     else:
#                         try:
#                             value = float(value_part)
#                         except ValueError:
#                             value = value_part

#                     # word operators need spaces after them in the filter string,
#                     # but we don't want these later
#                     return name, operator_type[0].strip(), value

#         return [None] * 3


#     @app.callback(
#         Output('table-paging-with-graph', "data"),
#         Input('table-paging-with-graph', "page_current"),
#         Input('table-paging-with-graph', "page_size"),
#         Input('table-paging-with-graph', "sort_by"),
#         Input('table-paging-with-graph', "filter_query"))
#     def update_table(page_current, page_size, sort_by, filter):
#         filtering_expressions = filter.split(' && ')
#         dff = df
#         for filter_part in filtering_expressions:
#             col_name, operator, filter_value = split_filter_part(filter_part)

#             if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
#                 # these operators match pandas series operator method names
#                 dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
#             elif operator == 'contains':
#                 dff = dff.loc[dff[col_name].str.contains(filter_value)]
#             elif operator == 'datestartswith':
#                 # this is a simplification of the front-end filtering logic,
#                 # only works with complete fields in standard format
#                 dff = dff.loc[dff[col_name].str.startswith(filter_value)]

#         if len(sort_by):
#             dff = dff.sort_values(
#                 [col['column_id'] for col in sort_by],
#                 ascending=[
#                     col['direction'] == 'asc'
#                     for col in sort_by
#                 ],
#                 inplace=False
#             )

#         return dff.iloc[
#             page_current*page_size: (page_current + 1)*page_size
#         ].to_dict('records')


#     @app.callback(
#         Output('table-paging-with-graph-container', "children"),
#         Input('table-paging-with-graph', "data"))
#     def update_graph(rows):
#         dff = pd.DataFrame(rows)
#         return html.Div(
#             [
#                 dcc.Graph(
#                     id=column,
#                     figure={
#                         "data": [
#                             {
#                                 "x": dff["countryNames"],
#                                 "y": dff[column] if column in dff else [],
#                                 "type": "bar",
#                                 "marker": {"color": "#ffbb00"},
#                                 "color":dff["male"],
#                                 'line_color':'red',#dict(color='purple')
#                                 #"name": dff["countryNames"]
#                             }
#                         ],
#                         "layout": {
#                             "xaxis": {"automargin": True},
#                             "yaxis": {"automargin": True},
#                             "height": 250,
#                             "plot_bgcolor":colors['background'],
#                             "margin": {"t": 30, "l": 10, "r": 30},
#                             'title': column + " plot per country"
#                             #"color":"female"
#                         },
#                     },
#                 )
#                 for column in ["total"]
#             ]
#         )
#     app.run_server(debug=True,host='0.0.0.0',port='8050')

# if __name__ == '__main__':
#     main()
