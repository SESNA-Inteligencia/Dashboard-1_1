import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from sqlalchemy import create_engine
import sys
import pymysql
from datetime import date, datetime, timedelta


# change to app.layout if running as single page app instead
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Carousel(
                items=[
                    {"key": "1", "src": "../assets/logo.svg", "header": "With header ","caption": "SESNA"},
                    {"key": "2", "src": "../assets/logo.svg", "header": "With header ","caption": "SESNA"},
                    {"key": "3", "src": "../assets/logo.svg", "header": "With header ","caption": "SESNA"},
                ],
                controls=True,
                indicators=False,
                interval=2000,
                ride="carousel",
            ), className="mb-5 mt-5", style={'color':'black'},
            #html.Img(src="../assets/logo.svg", style={
            #                                            "width": "100%",
            #                                            "margin-bottom": "10px",
            #                                        })
        )
    ]),
    dbc.Row([
            dbc.Col(html.H1(" ... ",
                    className="text-center"), className="mb-5 mt-5")
            ]),
    
    # first row 
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Text("SEGALMEX", color='blue', weight=500, style={"fontSize": 30}),
                ]),
           md=8),   
            dbc.Col(html.Div([
                    dbc.Button("Ver", color="dark",
                               outline=True, href="/segalmex"),
                ]),
            md=2),
            #dbc.Col(html.Div([
            #        dbc.Button("", color="dark",
            #                   outline=True, href="#"),
            #    ]),
            #md=2),
    ], className="mb-1 p-3 text-black rounded-3 ", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'}),
    # second row
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Text("LICONSA", color='blue', weight=500, style={"fontSize": 30}),
                ]),
           md=8),   
            dbc.Col(html.Div([
                    dbc.Button("Ver", color="dark",
                               outline=True, href="/segalmex"),
                ]),
            md=2),
            #dbc.Col(html.Div([
            #        dbc.Button("Descarga", color="dark",
            #                   outline=True, href="#"),
            #    ]),
            #md=2),
    ], className="mb-1 p-3 text-black rounded-3 ", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'}),
  
    # third row 
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Text("SEGALMEX", color='blue', weight=500, style={"fontSize": 30}),
                ]),
           md=8),   
            dbc.Col(html.Div([
                    dbc.Button("Ver", color="dark",
                               outline=True, href="/segalmex"),
                ]),
            md=2),
            #dbc.Col(html.Div([
            #        dbc.Button("Descarga", color="dark",
            #                   outline=True, href="#"),
            #    ]),
            #md=2),
    ], className="mb-1 p-3 text-black rounded-3 ", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'}),
  
    #        dbc.Col(html.Div(
    #            [
    #                #html.Div("DICONSA", className="display-6",
    #                #        style={'color': 'black'}),
    #                dmc.Text("DICONSA", color='blue', weight=500, style={"fontSize": 45}),
    #                html.Hr(className="my-2",style={'borderColor': 'black'}),
    #                html.P(
    #                    '''
    #            En esta sección se presenta ...
    #            '''
    #                ),
    #                dbc.Button("Ver", color="dark",
    #                           outline=True, href="/page3"),
    #            ],
    #            className="h-100 p-5 text-black rounded-3 ", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'},
    #        ),
    #            md=4, className="mb-3"),
            
    #        ], className="mb-10")

    html.Br(),
    html.Br(),
    html.Br(),
     

])
