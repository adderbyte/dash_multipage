import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app
from apps import app1, app2, app3, app4, app5, app6, app7, app8
from apps.dask_dash_app3 import app_sm

# import dash_table_experiments as dt
import base64
import os
from flask import send_from_directory


server = app.server

# after

app.layout = html.Div([html.Link(
    rel='stylesheet',
    href='/assets/custom.css'),

    dcc.Location(id='url', refresh=False),
    # html.Nav(id='nav',
    #          className='navbar navbar-default', children=html.Div(className='container-fluid', children=[html.Div(
    #              className='navbar-header', children=html.Div(className="navbar-brand", children='Analytics App')
    #          ),
    #              html.Ul(className='nav navbar-nav', children=[
    #                  html.Li(children=html.A(
    #                      href="/apps/app1", children="Home")),
    #                  html.Li(children=html.A(
    #                      href="/apps/app3", children="Visualization")),
    #                  html.Li(children=html.A(href="/assets/searchTermsColor.html",
    #                                          children="Natural Language Processing")),
    #                  # html.Li(children=html.A(href="/apps/app4",children="app4")),
    #                  # html.Li(children=html.A(href="/apps/app5",children="app5")),
    #                  html.Li(children=html.A(href="/apps/dask_dash_app3/app_sm",
    #                                          children="Statistical models")),
    #                  #html.Li(children=html.A(href="/apps/app7",children="HelpDesk stats")),
    #                  html.Li(children=html.A(href="/apps/app6",
    #                                          children="Machine Learning"))
    #              ]),
    #              html.P(className='text-right vertical-center', children=html.A(className='text-muted',
    #                     href="https://plot.ly/products/dash/", children='Created using Dash by Plotly'))
    #          ])),
    html.Div(
    [
        html.Link(href='https://fonts.googleapis.com', rel='preconnect'),
        html.Link(href='https://fonts.gstatic.com', rel='preconnect'),
        html.Link(
            href='https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap', rel='stylesheet'),
        dbc.Nav(dbc.Row(
            [
                dbc.Col(dbc.NavLink(
                    "Analytics App", active=True, href="#", className="navbar-brand vertical-center"), width="auto"),
                dbc.Col(dbc.NavLink("Home", href="/apps/app1",
                                    className="text-right vertical-center"), width="auto"),
                dbc.Col(dbc.NavLink("Visualization", href="/apps/app6",
                                    className="text-right vertical-center"), width="auto"),
                dbc.Col(dbc.NavLink("Natural Language Processing",
                                    href="/apps/app4", className="text-right vertical-center", external_link=True,), width="auto"),
                dbc.Col(dbc.NavLink("Statistical Models",
                                    href="/apps/dask_dash_app3/app_sm", className="text-right vertical-center"), width="auto"),
                dbc.Col(dbc.NavLink("Survey Streams", href="/apps/app6",
                                    className="text-right vertical-center"), width="auto"),
            ]
        ), style={"font-family": "'Fredoka One', cursive", "color": "black"}),
        html.Br(),
        html.P(id="button-clicks"),
    ]),
    html.Div(id='page-content')])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout()
    elif pathname == '/apps/app6':
        return app6.layout6()
    elif pathname == '/apps/app4':
        return app4.layout4()
    elif pathname == '/apps/dask_dash_app3/app_sm':
        return app_sm.layout()
    elif pathname == '/apps/app7':
        return app7.layout7()
    elif pathname == '/apps/app8':
        return app8.layout8()
    else:
        return app1.layout()


@ app.server.route('/dynamic/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'dynamic')
    return send_from_directory(dynamic, path)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False, port='8050')
