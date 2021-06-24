import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
from distributed import Client, LocalCluster

from app import app, cache

import plotly.express as px
from dynamic import loader

import plotly.graph_objs as go

import os

PAGE_SIZE = 5

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


@cache.memoize()
def datas():
    import modin.pandas as pd
    # Dask Local Cluster
    print("my present cwd  ", os.getcwd(),)
    cluster = LocalCluster()
    client = Client(cluster)
    df = pd.read_csv("./assets/displaydata.csv", index_col=[0])
    #df = px.data.iris()

    return df


# storage
caches = {"col": ['country names', 'female', 'male', 'no gender info', 'total', '10-20', '20-30',
                  '30-40', '40-50', '50-above', 'no age info']}


def layout3():

    # layoutdis=
    layoutdis = html.Div(
        className="row",
        children=[
            html.H1("Survey Participants Analytics", style={
                'textAlign': 'center',
                'color': colors['background'],
                'width': '100vw'
            }),
            html.Div(
                className='six columns',
                style={'height': 750, 'overflowY': 'scroll', 'width': '100vw'},
                children=[
                    html.Link(href='./assets/GUI.css', rel='stylesheet'),

                    dash_table.DataTable(
                        id='table-paging-with-graph',

                        columns=[
                            {"name": i, "id": i} for i in caches["col"]
                        ],
                        page_current=0,
                        page_size=20,
                        page_action='custom',

                        filter_action='custom',
                        filter_query='',
                        style_cell=dict(
                            textAlign='center', font_family="cursive", font_size='16px'),
                        style_header=dict(
                            backgroundColor="#97D987", font_family='sans-serif', font_size='20px'),
                        style_data=dict(backgroundColor="#F3EDE0"),
                        style_table=dict(width="auto", height="auto", marginLeft=19.8, marginRight=19.8
                                         ),

                        sort_action='custom',
                        sort_mode='multi',
                        sort_by=[],

                        # fill_width=False,
                    ),


                ]),
            html.Div(
                id='table-paging-with-graph-container',
                className="five columns"
            )
        ]
    )
    return layoutdis


# @app.callback(
#     Output("scatter-plot3", "figure"),
#     [Input("range-slider3", "value")])
# def update_bar_chart(slider_range):
#     low, high = slider_range
#     df = datas()
#     #dff  = loader.data()
#     print(df.head(),flush=True)
#     mask = (df['petal_width'] > low) & (df['petal_width'] < high)
#     fig = px.scatter(
#         df[mask], x="sepal_width", y="sepal_length",
#         color="species", size='petal_length',
#         hover_data=['petal_width'])
#     return fig


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query")])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = datas()
    dff.columns = caches["col"]
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)

    return html.Div(
        [
            dcc.Graph(
                id=column,
                style={'display': 'inline-block', 'text-align': 'center'},
                figure={
                    "data": [

                        # "x": dff[caches["col"][0]],
                        # "y": dff[column] if column in dff else [],
                        # "type": "pie",
                        # "marker": {"color": "#0074D9"},
                        # "color":dff["male"],
                        # 'line_color':'red',#dict(color='purple')
                        # "name": dff["countryNames"]

                        go.Pie(
                            labels=dff[caches["col"][0]],
                            values=dff[column] if column in dff else [],
                            #name= dff["country names"]
                        ),

                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 650,
                        "width": 650,
                        "margin": {"t": 30, "l": 30, "r": 30},
                        'title': column + " plot per country"
                        # "color":"female"
                    },
                },
            )
            for column in ["male", "female", "total"]
        ]
    )


# import dash_table_experiments as dt
# import datetime

# from app import app,cache

# @cache.memoize()
# def get_market_df(date):

#     df=pd.read_excel('fields_df.xls',encoding='utf-8')
#     #меняем пустые строки на 0
#     df=df.fillna(0)
#     df=df[df.department!=0]
#     return df

# @cache.memoize()
# def get_case_ifl_df(date):

#     df=pd.read_excel('ifl_case.xls',encoding='utf-8')
#     #меняем пустые строки на 0
#     df=df.fillna(0)
#     df=df[df.department!=0]
#     return df


# @cache.memoize()
# def get_df(date):

#     df=pd.read_excel('main_df.xls',encoding='utf-8')
#     #меняем пустые строки на 0
#     df=df.fillna(0)
#     df=df[df.quantity!=0]
#     df=df[df.department!=0]
#     return df


# @cache.memoize()
# def get_agents_df(date):

#     df=pd.read_excel('agents_df.xls',encoding='utf-8')
#     #меняем пустые строки на 0
#     df=df.fillna(0)
#     return df

# def layout():


#     load_time=str(datetime.datetime.now())
#     load_time=load_time[:15]

#     main_df=get_df(load_time)
#     fields_df=get_market_df(load_time)

#     sales_channels=main_df.sales_channel.unique().tolist()
#     sales_channels.append('Все')
#     insurance_types=main_df.insurance_type.unique().tolist()
#     insurance_types.append('ИФЛ')

#     return html.Div([

#     html.Div([html.H3('Sales analitics' )],style={'text-align':'center'}),
#     html.Div(id='stored_data',children=load_time,style={'display':'none'}),
#     html.Div([
#          html.Div([dcc.Dropdown(id='drop_sales_channel',options=[{'label' : i, 'value' : i } for i in sales_channels],value='Агенты')],style={'width':'49%','display':'inline-block'})
#         ,html.Div([dcc.Dropdown(id='drop_insurance_type',options=[{'label' : i, 'value' : i } for i in insurance_types],value='ИФЛ')],style={'width':'49%','display':'inline-block'})
#     ]),
#     html.Div([dcc.Graph(id='total_view')
#                         ], style={'width': '100%', 'display': 'inline-block'}),
#     html.Div([
#     html.Div([dcc.Graph(id='department_markets')],style={'width': '49%', 'display': 'inline-block'}),
#     html.Div([dt.DataTable(rows=[{}],
#         # optional - sets the order of columns
#         columns=['вид страхования','продающих агентов','всего агентов','договоров','сборы'],

#         row_selectable=False,
#         filterable=False,
#         sortable=False,
#         editable=False,
#         id='department_agents_info')],style={'width': '49%', 'display': 'inline-block'})
#     ]),

#     html.Div([dt.DataTable(rows=[{}],
#         # optional - sets the order of columns
#         columns=['ФИО','статус','возраст','стаж','вид страхования','договоров','сборы'],
#         row_selectable=False,
#         filterable=True,
#         sortable=True,
#         editable=False,
#         id='agents_sales_info'
#         )],style={'width': '100%', 'display': 'inline-block'})

#     ,
#     html.Div([dcc.Graph(id='case_ifl')],style={'width': '49%', 'display': 'inline-block'})

#     ])


# @app.callback(
# dash.dependencies.Output('total_view','figure'),
# [dash.dependencies.Input('stored_data','children'),
# dash.dependencies.Input('drop_sales_channel','value'),
# dash.dependencies.Input('drop_insurance_type','value')
# ])

# def update_total_view(stored_data,sales_channel,insurance_type):
#     main_df=get_df(stored_data)
#     fields_df=get_market_df(stored_data)

#     if sales_channel!='Все':
#         main_df=main_df[(main_df.sales_channel== sales_channel)]

#     if insurance_type=='ИФЛ':
#         main_df=main_df[(main_df.insurance_type=='Строения') | (main_df.insurance_type=='Квартиры')]
#         fields_df=fields_df[(fields_df.insurance_type=='Строения') | (fields_df.insurance_type=='Квартиры') ]
#     else:
#         main_df=main_df[(main_df.insurance_type==insurance_type)]
#         fields_df=fields_df[fields_df.insurance_type==insurance_type]


#     departments=main_df.department.unique()

#     market_impact=[]

#     for department in departments:

#         quantity=main_df[main_df.department==department]
#         market=fields_df[fields_df.department==department]


#         if market.market_quantity.sum()!=0:
#             market_impact.append(float("{0:.2f}".format((quantity.quantity.sum()/market.market_quantity.sum())*100)))
#         else:
#             market_impact.append(0)
#     data= dict(zip(departments, market_impact))


#     return {
#                         'data':[
#                         {'x': sorted(data, key=data.get), 'y': sorted(data.values()) , 'type' : 'bar' ,'name' : 'охват рынка'}]
#                         ,'layout':{'title' : '% охвата рынка ','hovermode' : 'closest'}
#                         }


# @app.callback(
# dash.dependencies.Output('department_markets','figure'),
# [dash.dependencies.Input('stored_data','children'),
# dash.dependencies.Input('drop_sales_channel','value'),
# dash.dependencies.Input('total_view','clickData')
# ])

# def update_department_markets(stored_data,sales_channel,department_click):

#     main_df=get_df(stored_data)
#     fields_df=get_market_df(stored_data)

#     insurance_types=main_df.insurance_type.unique()

#     #Фильтруем по отделу
#     try:
#         department=department_click['points'][0]['x']
#     except TypeError:
#         department='Донецк'


#     if sales_channel!='Все':
#         main_df=main_df[(main_df.sales_channel== sales_channel)]

#     main_df=main_df[(main_df.department==department)]
#     fields_df=fields_df[fields_df.department==department]


#     typed_market_impact=[]

#     for insurance_type in insurance_types :
#         quantity=main_df[main_df.insurance_type==insurance_type]
#         market=fields_df[fields_df.insurance_type==insurance_type]
#         if market.market_quantity.sum()!=0:
#             typed_market_impact.append(float("{0:.2f}".format((quantity.quantity.sum()/market.market_quantity.sum())*100)))
#         else:
#             typed_market_impact.append(0)

#     data= dict(zip(insurance_types, typed_market_impact))

#     title=department + ' % охвата рынка по видам страхования'


#     return {
#                         'data':[
#                         {'x': sorted(data, key=data.get), 'y': sorted(data.values()) , 'type' : 'bar' ,'name' : 'охват зынка'}]
#                         ,'layout':{'title' : title,'hovermode' : 'closest'}
#                         }

# @app.callback(
# dash.dependencies.Output('department_agents_info','rows'),
# [dash.dependencies.Input('stored_data','children'),
# dash.dependencies.Input('drop_sales_channel','value'),
# dash.dependencies.Input('total_view','clickData')
# ])

# def update_agent_info_table(stored_data,sales_channel,department_click):

#     main_df=get_df(stored_data)
#     agents_df=get_agents_df(stored_data)

#     insurance_types=main_df.insurance_type.unique()

#     #Фильтруем по отделу
#     try:
#         department=department_click['points'][0]['x']
#     except TypeError:
#         department='Донецк'

#     if sales_channel!='Все':
#         main_df=main_df[(main_df.sales_channel== sales_channel)]

#     main_df=main_df[(main_df.department==department)]
#     agents_df=agents_df[agents_df.department==department]

#     table_df=main_df[['insurance_type','agent']]
#     table_df.columns=['insurance type','agents with sales']
#     table_df=table_df.pivot_table(index='insurance type',values=['agents with sales'], aggfunc=len, fill_value=0)
#     table_df=pd.DataFrame(table_df.to_records())

#     quantity_df=main_df[['insurance_type','quantity','value']]
#     quantity_df=quantity_df.pivot_table(index='insurance_type',values=['quantity','value'], aggfunc=sum)
#     quantity_df=pd.DataFrame(quantity_df.to_records())

#     if sales_channel=='Агенты':
#         total_agents=agents_df.agents.sum()
#     elif sales_channel=='МРП':
#         total_agents=agents_df.mrp.sum()
#     else:
#         total_agents=agents_df.mrp.sum()+agents_df.agents.sum()


#     table_df['agents total']=total_agents
#     try:
#         table_df['quantity']=quantity_df['quantity']
#         table_df['value']=quantity_df['value']
#         table_df['value']=table_df['value'].map("{:,.0f}".format)
#         table_df['quantity']=table_df['quantity'].map("{:,.0f}".format)
#         table_df.columns=['вид страхования','продающих агентов','всего агентов','договоров','сборы']
#     except KeyError:
#         pass

#     try:
#         return   table_df.to_dict('records')
#     except AttributeError:
#         return [{}]


# @app.callback(
# dash.dependencies.Output('agents_sales_info','rows'),
# [dash.dependencies.Input('stored_data','children'),
# dash.dependencies.Input('drop_sales_channel','value'),
# dash.dependencies.Input('total_view','clickData')
# ])

# def update_agent_sales_info_table(stored_data,sales_channel,department_click):

#     main_df=get_df(stored_data)

#     insurance_types=main_df.insurance_type.unique()

#     #Фильтруем по отделу
#     try:
#         department=department_click['points'][0]['x']
#     except TypeError:
#         department='Донецк'

#     if sales_channel!='Все':
#         main_df=main_df[(main_df.sales_channel== sales_channel)]

#     main_df=main_df[(main_df.department==department)]

#     table_df=main_df[['agent','status','age','standing','insurance_type','quantity','value']]


#     table_df['quantity']=table_df['quantity'].map("{:,.0f}".format)
#     table_df['value']=table_df['value'].map("{:,.0f}".format)
#     table_df.columns=['ФИО','статус','возраст','стаж','вид страхования','договоров','сборы']


#     try:
#         return   table_df.to_dict('records')
#     except AttributeError:
#         return [{}]


# @app.callback(
# dash.dependencies.Output('case_ifl','figure'),
# [dash.dependencies.Input('stored_data','children'),
# dash.dependencies.Input('total_view','clickData')
# ])

# def update_agent_info_table(stored_data,department_click):

#     main_df=get_case_ifl_df(stored_data)


#     #Фильтруем по отделу
#     try:
#         department=department_click['points'][0]['x']
#     except TypeError:
#         department='Донецк'

#     main_df=main_df[(main_df.department==department)]

#     categories=[]
#     values=[]

#     for category in main_df.category.unique():
#         categories.append(category)
#         df=main_df[main_df.category==category]
#         values.append(df.quantity.sum())


#     try:
#         return   {
#                 'data' : [go.Pie(labels=categories,values=values,

#                 hoverinfo='label+value+percent',
#                 textinfo='none' )], 'layout' : {'title' : 'соотношение стоимости застрахованных объектов ИФЛ'}
#                 }
#     except AttributeError:
#         return {}
