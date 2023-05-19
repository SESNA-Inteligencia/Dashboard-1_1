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

list_ramos = ['uno', 'dos', 'tres']
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
            dbc.Col(html.Div([
                dmc.Text("Programas sociales", color='black', weight=500, align='center', style={"fontSize": 50}),
                ], style={"text-aling":"center"}),
            ),
    ],  className="col-12 mb-4"),
    # first row 
    html.Center([
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Select(
                        id='ramos', 
                        data=list_ramos,
                        value= "uno",
                        clearable=True,
                        #style={"width": 600}  
                        ),       
                    ]),
            className="col-12 col-md-6 mt-4", style={'marginLeft':'2rem'}),   
            dbc.Col(html.Div([
                    dmc.Text("Ramo", color='black', weight=500, align='left', style={"fontSize": 20}),
                ]),
           md=4, className="mt-4"), 
            #dbc.Col(md=2),
            #dbc.Col(html.Div([
            #        dbc.Button("", color="dark",
            #                   outline=True, href="#"),
            #    ]),
            #md=2),
    ], className="col-12 col-md-7 mb-0 ml-4 mt-4 p-3 text-black rounded-0", style={'boxShadow': '#e3e3e3 4px 4px 0px', 'backgroundColor':'#FFFFFF'}),
    
    # second row organismo
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Select(
                        id='organismos', 
                        data=list_ramos,
                        value= "uno",
                        clearable=True,
                        #style={"width": 600}  
                        ),       
                    ]),
            className="col-12 col-md-6 mt-1", style={'marginLeft':'2rem'}),   
            dbc.Col(html.Div([
                    dmc.Text("Organismo", color='black', weight=500, align='left', style={"fontSize": 20}),
                ]),
           md=4, className="mt-1"), 
            #dbc.Col(html.Div([
            #        dbc.Button("", color="dark",
            #                   outline=True, href="#"),
            #    ]),
            #md=2),
    ], className="col-12 col-md-7 mb-0 p-3 text-black rounded-0", style={'boxShadow': '#e3e3e3 4px 4px 0px', 'backgroundColor':'#FFFFFF'}),
    
    # third row : Programa social
    dbc.Row([
            dbc.Col(html.Div([
                    dmc.Select(
                        id='progama_social', 
                        data=list_ramos,
                        value= "uno",
                        clearable=True,
                        #style={"width": 600}  
                        ),       
                    ]),
            className="col-12 col-md-6 mt-1", style={'marginLeft':'2rem'}),   
            dbc.Col(html.Div([
                    dmc.Text("Programa social", color='black', weight=500, align='left', style={"fontSize": 20}),
                ]),
           md=4, className="mt-1"), 
            
    ], className="col-12 col-md-7 mb-0 p-3 text-black rounded-0 text-center", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'}),
  
    # fourd row : bottom
    dbc.Row([
            dbc.Col(html.Div([
                dbc.Button("Ver", 
                           id ="submit-home",
                           color="dark", 
                           #size="lg",
                           className="me-1",
                           #outline=True, 
                           href="/segalmex"),
     
            ], className="d-grid gap-2 col-6 mx-auto", style={'marginLeft':'2rem',"text-aling":"center"}),     
            md=6),
            dbc.Col(html.Div([
                    dmc.Text("", color='black', weight=500, align='left', style={"fontSize": 20}),
                ]),
            md=6), 
        ], justify='center', className="col-12 col-md-7 mb-4 p-3 text-black rounded-0", style={'marginBottom':'4rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'backgroundColor':'#FFFFFF'}),
    
    
    
    ]),
    

    html.Br(),
    html.Br(),
    html.Br(),
     

])
