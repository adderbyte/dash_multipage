from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from flask import url_for

from app import app


def layout():
    return html.Div([
        html.Link(href='https://fonts.googleapis.com', rel='preconnect'),
        html.Link(href='https://fonts.gstatic.com', rel='preconnect'),
        html.Link(
            href='https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap', rel='stylesheet'),
        html.Div(className='Row', children=[
            html.Div(className='col-lg-6', children=[
                html.Div(className='Row', children=[html.Div(className='col-lg-12', children=[
                    html.H1(className='text-center', style={"font-family": "'Fredoka One', cursive", "font-size": "4rem"}, children=['ANALYTICS PLATFORM', html.Br(), 'TRUEFEEDBACK'])])]),
                html.Div(className='Row', style={"text-align": "center"}, children=[html.Div(className='col-lg-12', children=[
                    html.Div(className='col-lg-2'),
                    html.Div(className='col-lg-4', children=[
                        html.Br(), html.Br(),
                        html.A([html.Img(className='img-responsive', src=app.get_asset_url(
                            'plotly(8).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 12px 8px #cccccc",
                                                     "-webkit-box-shadow": "0px 0px 12px 8px #cccccc"})], href="/apps/app6"),
                        html.Br(), html.Br(),
                        html.A(children=[html.Img(
                            className='img-responsive', src=app.get_asset_url('plotly(10).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 12px 8px #cccccc",
                                                                                                        "-webkit-box-shadow": "0px 0px 12px 8px #cccccc"})], href="/apps/app4"),
                    ]),
                    html.Div(className='col-lg-4', children=[
                        html.Br(), html.Br(),
                        html.A([html.Img(className='img-responsive',
                                         src=app.get_asset_url('plotly(9).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 12px 8px #cccccc",
                                                                                        "-webkit-box-shadow": "0px 0px 12px 8px #cccccc"})],  href="/apps/dask_dash_app3/app_sm"),
                        html.Br(), html.Br(),
                        html.A([html.Img(className='img-responsive',
                                         src=app.get_asset_url('plotly(12).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 12px 8px #cccccc",
                                                                                         "-webkit-box-shadow": "0px 0px 12px 8px #cccccc"})], href="/apps/app6"),
                    ]),
                    html.Div(className='col-lg-2'),
                ])])
            ]),


            html.Div(className='col-lg-6', children=[
                html.Div(className='col-lg-11', children=[
                    html.A([html.Img(className='img-responsive',
                                     src=app.get_asset_url('6.png'))]),
                ])]),
            html.Div(className='col-lg-1')
        ]),
        # html.Div(className='Row', children=[
        #     html.Div(className='col-lg-1'),
        #     html.Div(className='col-lg-10', children=[
        #         html.Div(className='col-lg-3', children=[
        #             html.A([html.Img(className='img-responsive', src=app.get_asset_url(
        #                 'plotly(8).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #969696",
        #                                          "-webkit-box-shadow": "0px 0px 8px 8px #969696"})], href="/apps/app3"),
        #         ]),
        #         html.Div(className='col-lg-3', children=[
        #             html.A(children=[html.Img(
        #                 className='img-responsive', src=app.get_asset_url('plotly(10).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #969696",
        #                                                                                             "-webkit-box-shadow": "0px 0px 8px 8px #969696"})], href="/assets/searchTermsColor.html"),
        #         ]),
        #         html.Div(className='col-lg-3', children=[
        #             html.A([html.Img(className='img-responsive',
        #                    src=app.get_asset_url('plotly(9).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #969696",
        #                                                                   "-webkit-box-shadow": "0px 0px 8px 8px #969696"})],  href="/apps/dask_dash_app3/app_sm")
        #         ]),
        #         html.Div(className='col-lg-3', children=[
        #             html.A([html.Img(className='img-responsive',
        #                    src=app.get_asset_url('plotly(12).png'), style={"border-radius": "20px", "box-shadow": "0px 0px 8px 8px #969696",
        #                                                                    "-webkit-box-shadow": "0px 0px 8px 8px #969696"})], href="/apps/app6"),
        #         ]),
        #     ]),
        #     html.Div(className='col-lg-1')
        # ])
    ])
