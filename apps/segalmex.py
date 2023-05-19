from operator import index
from pickle import FALSE

import dash          
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import numpy as np
import pandas as pd
from millify import millify
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from dash_extensions import Download
#from dash_extensions.snippets import send_file
from dash_iconify import DashIconify
import dash_leaflet as dl
from sqlalchemy import create_engine
from app import app
import requests
import random
import json
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from costumFunctions import make_dataframe_state_mun
import sys
import pymysql
import plotly.io as pio
pio.renderers.default = 'firefox'


# CONFIG BASE DATOS (No activo)
#hostname="localhost"
#dbname=["nombre bases separadas por comas"]
#uname="root"
#pwd="myadmin"

# --- Only run on the server
#engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname[0], user=uname, pw=pwd))
#base = pd.read_sql(sql="select * from", con = engine, index_col="Date", parse_dates=True)

# introducir directorio de la carpeta
root = "C:/Users/jcmartinez/Desktop/Dashboard3"

# urls
#repo_est_url = ""
estados_json = open(root + '/datasets/estadosMexico.json')
mx_est_geo = json.load(estados_json)


# base beneficiarios
df_benef = pd.read_excel(root + '/datasets/base_beneficiarios_dashboard_v5.xlsx')
# base centros de acopio
df_centros = pd.read_excel(root + '/datasets/base_centros_inegi.xlsx')
df_centros = df_centros
# base producción agrícola
df_produccion = pd.read_excel(root + '/datasets/base_prodAgricola_con_claves_inegi.xlsx')
df_produccion = df_produccion.dropna()
# georeferenciación de base producción - estados
df_prod_est = pd.read_csv(root + '/datasets/produccion_estados.csv')

# opciones 
list_year = ['2019', '2020', '2021']
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']
list_grado_marginacion = ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto']
list_tamano_productor = ['Pequeño', 'Mediano', 'Grande']
list_states = df_benef['NOM_ENT'].unique()
list_layers = ['Centros de acopio','Nivel de marginación', 'Tamaño del productor']






#------------------------------------------------------------------------------
#                        layout
####################    header
sidebar_header = html.Div([
    dbc.Row([
        #primero
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),
                 
            ],className="card col-12 col-md-2", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6', }),
        # segundo
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/bank.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),
                 
            ],className="card col-12 col-md-2", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6', }),
        # tercero
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/chart-histogram.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),  
            ],className="card col-12 col-md-2", style={'padding':'1rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6', }),
        # Cuarto
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/chart-histogram.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),  
            ],className="card col-12 col-md-2", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6', }),
        # quinto
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/chart-histogram.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),  
            ],className="card col-12 col-md-2", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6', }),
        # sexto
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(id='image', src='../assets/chart-histogram.svg', width="65", height="65"),
                ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                dbc.Col([
                    dbc.Row([html.Center(html.Div([
                    "1,332",
                    ], style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                    )]),
                    dbc.Row([html.Div([
                        dmc.Text("No. Benef.", color='gray', weight=500, align='center', style={"fontSize": 16}),
                        ]),
                    ]),
                ], className="card col-9 border-0 bg-transparent"), 
            ]),  
            ],className="card col-12 col-md-2", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'border-radius': '10px', 'backgroundColor': '#F4F6F6',}),
    ]), 
], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem'})

# Filtros proncipales
main_filters = html.Div([

    dbc.Row([
        dbc.Col([            
            ], className="card col-4 border-0 bg-transparent"),
        dbc.Col([ 
            dbc.Row([
                dbc.Col([
                    
                    html.Div([
                        dmc.Select(
                            icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                            label="Seleccione el año",
                            id="anio",
                            data=list_year,
                            value='2020',
                            searchable=True,
                            nothingFound="No options found",
                            #style={"width": 250},
                        ), 
                    ]),
                    ], className="card col-12 col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px',  'backgroundColor': '#F4F6F6', }
                ),
                
                dbc.Col([
                    html.Div([
                        dmc.Select(
                            icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                            label="Seleccione el producto",
                            id="producto",
                            data=list_products,
                            value='Frijol',
                            searchable=True,
                            nothingFound="No options found",
                            #style={"width": 250},
                        ),
                    ]),
                ], className="card col-12 col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px',  'backgroundColor': '#F4F6F6', }
            ),
            ]),
        ], className="card col-8 bg-transparent", style={'textColor':'white'}),
        
    ]),
   
    dbc.Row([
        dbc.Col([ 
            ], className="card col-4 border-0 bg-transparent"),
        dbc.Col([
            dbc.Row([
                dbc.Col([            
                    html.Div([
        
                    ]),
                    ], className="card col-12 col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px',  'backgroundColor': '#F4F6F6', }
                ),
                
                dbc.Col([
                    html.Div([
                        dbc.Button(id='submit-button',
                            n_clicks=0,
                            children='Actualizar',
                            color = 'dark',    
                            className="mb-4 mt-2"),
                    ], style={"width": "120%", 'marginLeft':'1.5rem', 'marginRight':'1.5rem'}
                    ), 
    
                ], className="card col-12  col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px', 'textAlign':'left', 'backgroundColor': 'black', }
            ),
            ]),
            
                
        ], className="card col-8 m-auto bg-transparent", style={'border-radius':'3px'}),
        
    ], className="eight colums bg-transparent"),

], className="eight columns", style={'backgroundColor': '#F4F6F6'})


####################      sidebar left: control bar
sidebar_right = html.Div([

        # Filtros
        dbc.Row([
            html.Div([
                    dmc.RadioGroup(
                        [dmc.Radio(k, value=k) for k in list_layers],
                        id="radiogroup-simple",
                        orientation="vertical",
                        value="Centros de acopio",
                        label="Select la capa que desee visualizar",
                        size="sm",
                        mt=10,
                    ),
                    dmc.Text(id="radio-output"),
                ])

        ], className="mt-2", style={'marginBottom':'4rem'}),
        
        # tablero resumen
        dbc.Row([
        #primero
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                    dbc.Col([
                        dbc.Row([html.Center(html.Div([
                        "1,332",
                        ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 12}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem', 'border-radius': '5px', 'backgroundColor': '#F4F6F6', }),
            # segundo
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                    dbc.Col([
                        dbc.Row([html.Center(html.Div([
                        "1,332",
                        ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Pob. Beneficiaria", color='grey', weight=500, align='center', style={"fontSize": 12}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem', 'border-radius': '5px', 'backgroundColor': '#F4F6F6', }),

        ], style={'marginTop':'4rem'}), 

        dbc.Row([
        #primero
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                    dbc.Col([
                        dbc.Row([html.Center(html.Div([
                        "1,332",
                        ], id='resumen-monto_apoyos', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Monto Apoyos", color='grey', weight=500, align='center', style={"fontSize": 12}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem', 'border-radius': '5px', 'backgroundColor': '#F4F6F6', }),
            # segundo
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image', src='../assets/porcentaje.png', width="65", height="65"),
                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                    dbc.Col([
                        dbc.Row([html.Center(html.Div([
                        "51%",
                        ], id='resumen-porcentaje_faltante', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Datos faltantes (%)", color='gray', weight=500, align='center', style={"fontSize": 12}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem','border-radius': '5px', 'backgroundColor': '#F4F6F6', }),

        ], style={'marginTop':'1rem', 'marginBottom':'2rem'}),

        
        
        ], style={'marginLeft':'2rem', 'marginRight':'2rem', 'marginTop':'2rem'}
    )

#######################    content - mapa
content1 = html.Div([
        dbc.Row([
            dbc.Col([
                    html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Mapa", tab_id="tab-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Tabla", tab_id="tab-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-mapa",
                            active_tab="tab-1",
                        ),
                        html.Div(id="content-mapa"),
                     ], style={"width": "100%"}
                    ),   # style={'height':'100vh'}               
            ], className="card col-12 col-md-8", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
            ), 
            dbc.Col([
                sidebar_right
                
            ], className="card col-12 col-md-4", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '0px', 'backgroundColor': 'white', }
            )
        ]),
        # Barra de control
        
    
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem', 'marginRight': '2rem','marginTop': '0rem'}
    )
# backgroundColor': '#F4F6F6'
#######################    content2 - gráficos
content2 = html.Div([
        dbc.Row([
            
            dbc.Col([
                    
                    html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 1", tab_id="tab-r2c1-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Tabla 1", tab_id="tab-r2c1-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r2c1",
                            active_tab="tab-r2c1-1",
                        ),
                        html.Div(id="content-r2c1"),
                     ], style={"width": "100%"}
                    ),                  
                ], className="card col-12 col-md-6", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
            dbc.Col([
                    html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 2", tab_id="tab-r2c2-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Tabla 2", tab_id="tab-r2c2-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r2c2",
                            active_tab="tab-r2c2-1",
                        ),
                        html.Div(id="content-r2c2"),
                     ], style={"width": "100%"}
                    ),                  
                ], className="card col-12 col-md-6", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
            
        ]),
         
        
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem'}

    )


#######################    content2 - gráficos principales
content3 = html.Div([
        dbc.Row([
            dbc.Col([
                    
                    html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 3", tab_id="tab-r3c1-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Tabla 3", tab_id="tab-r3c1-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r3c1",
                            active_tab="tab-r3c1-1",
                        ),
                        html.Div(id="content-r3c1"),
                     ], style={"width": "100%"}
                    ),                  
                ], className="card col-12", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
        ]),
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem'}

    )


# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([

 
        html.Div([
            html.Br(),
            html.Br(),
            dbc.Row([
            dbc.Col(html.Img(src="assets/segalmex3.jpg", height="60px"), style = {'textAlign':'center', 'marginRight':'10px'} ),
            ],
            className="g-0 m-0, p-0",
        ),
        
        dbc.Row([
            dbc.Col(html.H1("SEGALMEX"),  className="ml-5",  style = {'textAlign':'center', 'color':'black'} ),
            ],
            className="g-0 m-0 p-0",
        ),
        html.Br(),
        ], style={'backgroundColor':'#E5E8E8', 'm':'0px', 'padding':'0px'}),    
        
        # horizontal line
        html.Hr(),
        
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "Resumen Ejecutivo",
                    #href= "/Proyecto.pdf",
                    download="Proyecto.pdf",
                    external_link=False,
                    color="dark",
                    id="btn",
                ),   
                dcc.Download(id="download"),
                
            ],  style = {'textAlign':'right', 'color':'black', 'marginRight':'3rem'}),
        ], className="g-0 m-0"),
        
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]), 
        
        #dbc.Row([
        #    dbc.Col(sidebar_header, className="col-12 mb-4"),
        #    ]),
        #html.Div([
            dbc.Row([
                dbc.Col(main_filters, 
                        className="col-8 mb-4")
            ]),
        #], style={'backgroundColor':'#E5E8E8', 'm':'0px', 'padding':'0px'}),
        
        # accordeon
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                            dmc.Accordion(id="accordion-uno"),
                            dmc.Text(id="accordion-text-uno", mt=10),
                    ]),
                ]),
            ], className="col-8", style={'marginTop':'2rem','marginBottom':'2rem','marginLeft':'1rem', 'marginRight':'1rem'}),
        
        ], className="eight columns", style={'backgroundColor':'#F4F6F6', 'm':'0px', 'padding':'0px'}),
            
        
        
        dbc.Row([html.H5(' ')]),
        # first row: filtros y mapa
        dbc.Row([
                dbc.Col(content1, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6'}),
                #dbc.Col(sidebar_right, className="col-12 col-md-4"),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
                ]
        ),
        # second row: graficos
        dbc.Row([
                dbc.Col(content2, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem'}),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
                ]
        ),
        # third row: graficos
        dbc.Row([
                dbc.Col(content3, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem'}),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
        ], className='mb-0'),  
        
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]),       
        
    ], style={'backgroundColor': '#F4F6F6', 'marginTop': '0rem', 'padding':'0rem'},
    fluid=True
    )

#########################################################################################
############################            Call backs         ##############################
#########################################################################################

######    Resumen cards
# cuenta centros de acopio
@app.callback(
        Output('resumen-centros_acopio', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_centros_acopio(clicks, sel_producto, sel_anio):
    
    data = df_centros
    # Sin dato nombre de dato faltante
    cuenta_registros = len(data['NUM'])

    return cuenta_registros
# cuenta población beneficiaria
@app.callback(
        Output('resumen-poblacion_beneficiaria', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_pablacion_beneficiaria(clicks, sel_producto, sel_anio):
    
    data = df_benef[df_benef['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Sin dato nombre de dato faltante
    cuenta_registros = len(data['NOM_LOC'])

    return "{:,}".format(cuenta_registros)
    
# Monto apoyos
@app.callback(
        Output('resumen-monto_apoyos', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_monto_apoyos(clicks, sel_producto, sel_anio):
    
    data = df_benef[df_benef['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Sin dato nombre de dato faltante
    monto_apoyos = data['MONTO_APOYO_TOTAL'].sum()
    # millify(monto_apoyos, precision=2)
    return millify(monto_apoyos, precision=2)

# Descarga de resumen ejecutivo  
#@app.callback(
#    Output("download", "data"), 
#    Input("btn", "n_clicks"))
#def func(n_clicks):
#    return dcc.send_file("C:/Users/jcmartinez/Desktop/Dashboard3/Proyecto.pdf")
    

# tabs - mapa
# grafica mapa
tab1_mapa_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="mapa")
    ]),

tab2_mapa_content = html.Div([
    dt.DataTable(id="tabla-mapa")
])

#  Actualiza tabs - mapa
@app.callback(Output("content-mapa", "children"), [Input("tabs-mapa", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_mapa_content
    elif at == "tab-2":
        return tab2_mapa_content
    return html.P("This shouldn't ever be displayed...")

# actualiza MAPA
@app.callback(
        Output('mapa', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('t_productor', 'value'),
        #Input('grado_marginacion', 'value'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def actualizar_mapa(clicks, producto_sel, anio_sel):
    
    
    #if tproductor_sel is None:
    #    raise PreventUpdate
    
    if producto_sel is None:
        raise PreventUpdate
    
    #if gmarginacion_sel is None:
    #    raise PreventUpdate
    
    # Para selecciones múltiples: si es valor único creamos la lista, si no es valor único es una lista
    #if isinstance(tproductor_sel, str):
    #    tprod = [tproductor_sel]
    #else:
    #    tprod = tproductor_sel
            
    # selección múltiple grado de marginación
    #if isinstance(gmarginacion_sel, str):
    #    gmarg = [gmarginacion_sel]
    #else:
    #    gmarg = gmarginacion_sel
        
    # filtros
    base = df_benef.copy()
    #base = base.dropna()
    benef_filter = base[base['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    #benef_filter = benef_filter[benef_filter['GM_2020'].isin(gmarg)]
    #benef_filter = benef_filter[benef_filter['Tamanio_productor'].isin(tprod)]
    max_benef = benef_filter['MONTO_APOYO_TOTAL'].max()    
        
    est_color = df_prod_est[df_prod_est['Anio']==int(anio_sel)]
    est_color = est_color [est_color['Producto']==producto_sel]
    
    #if isinstance(ticker_sel, str):
    #    stks = [ticker_sel]
    #else:
    #    stks = ticker_sel
    # MAPA
    fig = go.Figure()
    # Traza areas de producción
    fig.add_trace(go.Choroplethmapbox(name='Mexico', geojson=mx_est_geo, ids=est_color['Entidad'], z=est_color['Volumenproduccion'],
                                        locations=est_color['Entidad'], featureidkey='properties.name', colorscale='greens',
                                        zmin=0, zmax=max_benef, 
                                        marker=dict(line=dict(color='black'), opacity=0.6)))
    # Traza de centros de acopio
    fig.add_trace(go.Scattermapbox(
            lat=df_centros['LAT_DECIMAL'],
            lon=df_centros['LON_DECIMAL'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                color='red'
            ),
            text=df_centros['NOM_MUN'],
        ))
    # Traza de beneficiarios 
    fig.add_trace(go.Scattermapbox(
            lat=benef_filter['LAT_DECIMAL'],
            lon=benef_filter['LON_DECIMAL'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                color='blue'
            ),
            text=benef_filter['MONTO_APOYO_TOTAL'],
        ))
    # Áreas de densidad (heatmap)
    fig.add_trace(go.Densitymapbox(
            lat=benef_filter['LAT_DECIMAL'], 
            lon=benef_filter['LON_DECIMAL'], 
            z=benef_filter['MONTO_APOYO_TOTAL'], 
            zmin=0, zmax=max_benef,
            colorscale='YlOrRd',
            opacity=0.8,
            radius=12))
        
    #fig.update_layout(mapbox_style="dark", mapbox_accesstoken='some_token')
    fig.update_layout(mapbox_style="open-street-map", #mapbox_style= "open-street-map", #'open-street-map',
                    mapbox_zoom=4, 
                    mapbox_center = {'lat': 25, 'lon': -99},
                    paper_bgcolor='white',
                    plot_bgcolor='white')

    fig.update_layout(legend_title_text='', margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_traces(colorbar_orientation='v',
                    colorbar_x=-0.1,
                    selector=dict(type='densitymapbox'))
        
    return fig

####   actualiza tabla-Mapa
@app.callback(
        Output('tabla-mapa', 'figure'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_tabla_mapa(clicks, producto_sel, anio_sel):
    
    
    return 


###############        tabs - grafico r2
tab1_r2c1_content = html.Div([             
    dcc.Graph(id="plot-r2c1")
])

tab2_r2c1_content = html.Div([
    html.Div(id="tabla-r2c1")
    #dcc.Graph(id="tabla-r2c1")
])

@app.callback(Output("content-r2c1", "children"), [Input("tabs-r2c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c1-1":
        return tab1_r2c1_content
    elif at == "tab-r2c1-2":
        return tab2_r2c1_content
    return html.P("This shouldn't ever be displayed...")

# actializa gráfico r2-c1 
@app.callback(
        Output('plot-r2c1', 'figure'),
        #Input('submit-button', 'n_clicks'),
        Input('estados', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot_r2c1(estado_sel, anio_sel):
    #
    if isinstance(estado_sel, str):
        state_sel = [estado_sel]
    else:
        state_sel = estado_sel
     
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}   
    
    # Map 
    base = df_benef.copy()
     # filtro de estado
    base_filt = base[base['NOM_ENT'].isin(state_sel)]
    # filtro de año
    base_filt = base_filt[base_filt['Anio']==int(anio_sel)]
    # agrupamiento
    base_filt = base_filt[['Producto', 'MONTO_APOYO_TOTAL']].groupby(['Producto'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
   
   
    productos = base_filt['Producto'].unique()
    
    fig = go.Figure()
    # all traces
    for producto in productos:
        base_prod = base_filt[base_filt['Producto']==producto]
        fig.add_trace(go.Bar(
                x=base_prod['Producto'].to_list(),
                y=base_prod['MONTO_APOYO_TOTAL'].to_list(),
                #mode='markers',
                name= producto))

    fig.update_layout(
        showlegend=False,
        autosize=False,
        #width=900,
        height=400,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor= "White",
            )

    fig.update_layout(
        title="",
        xaxis_title="Producto",
        yaxis_title="Monto Apoyo",
        legend_title="",
        font=dict(
            #   family="Courier New, monospace",
            size=13,
            color="Black"
            ))

    fig.update_xaxes(tickangle=0)
    
    fig.update_layout(barmode='stack')
    return fig

# actializa tabla r2-c1 
@app.callback(
        Output('tabla-r2c1', 'children'),
        #Input('submit-button', 'n_clicks'),
        Input('estados', 'value'),
        Input('anio', 'value')
    )

def actualizar_tabla_r2c1(estado_sel, anio_sel):
        
    if isinstance(estado_sel, str):
        state_sel = [estado_sel]
    else:
        state_sel = estado_sel
     
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}   
    
    # Map 
    base = df_benef.copy()
     # filtro de estado
    base_filt = base[base['NOM_ENT'].isin(state_sel)]
    # filtro de año
    base_filt = base_filt[base_filt['Anio']==int(anio_sel)]
    # agrupamiento
    base_filt = base_filt[['Producto', 'MONTO_APOYO_TOTAL']].groupby(['Producto'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
   
    table = dt.DataTable(
        columns=[
            {"name": "Entidad", "id": "entidad" },
            {"name": "Arroz", "id": "arroz", "deletable": [False, True], "renamable": True, "hideable": "last"},
            {"name": "Frijol", "id": "frijol", "deletable": [False, True], "renamable": True, "hideable": "last"},
            {"name": "Leche", "id": "leche", "deletable": [False, True], "renamable": True, "hideable": "last"},
            {"name": "Maíz", "id": "maiz", "deletable": [False, True], "renamable": True, "hideable": "last"},
            {"name": "Trigo", "id": "trigo", "deletable": [False, True], "renamable": True, "hideable": "last"},
        ],
        data=[
            {
                "entidad": i,
                "arroz": i * 10,
                "frijol": i * 100,
                "leche": i * -1,
                "maiz": i * -10,
                "trigo": i * -100,
            }
            for i in range(100)
        ],
        export_format='csv', # | 'xlsx'
        export_headers='display',
        #merge_duplicate_headers=True
        page_size=10,
    )
    return table


###   Gráfico row2 - col2
tab1_r2c2_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r2c2")
    ]),

tab2_r2c2_content = html.Div([
    dt.DataTable(id="tabla-r2c2")
])

#  Actualiza tabs - mapa
@app.callback(Output("content-r2c2", "children"), [Input("tabs-r2c2", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c2-1":
        return tab1_r2c2_content
    elif at == "tab-r2c2-2":
        return tab2_r2c2_content
    return html.P("This shouldn't ever be displayed...")


@app.callback(
        Output('plot-r2c2', 'figure'),
        #Input('submit-button', 'n_clicks'),
        Input('estados', 'value'),
        #Input('municipios', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot_r2c2(estado_sel, anio_sel):
    
    
    if isinstance(estado_sel, str):
        state_sel = [estado_sel]
    else:
        state_sel = estado_sel
    
    
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}
    # Total de productos
    
    # filtro de año
    base_filt = df_benef[df_benef['Anio'] == int(anio_sel)]
    
    base_filt = base_filt[base_filt['NOM_ENT'].isin(state_sel)]
    
    productos = base_filt['Producto'].unique()
    
    
    fig = go.Figure()
  
    # all traces
    for producto in productos:
        base_prod = base_filt[base_filt['Producto']==producto]
        fig.add_trace(go.Scatter(
                x=base_prod['IMN_2020'].to_list(),
                y=base_prod['MONTO_APOYO_TOTAL'].to_list(),
                mode='markers',
                name= producto,
                marker=dict(size=8,
                        color=colors[producto])))
    
    fig.update_layout(
            showlegend=True,
            autosize=False,
            #width=900,
            height=400,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0),
                #plot_bgcolor='rgba(0, 0, 0, 0)',
                #paper_bgcolor= "White",
                )

    fig.update_layout(
            title="",
            xaxis_title="Grado de Marginación",
            yaxis_title="Monto Apoyo",
            legend_title="Producto:",
            font=dict(
                #family="Courier New, monospace",
                size=13,
                color="Black"
                ))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    ))

    fig.update_xaxes(tickangle=80)

    return fig


###############       tabs - grafico r3
tab1_r3c1_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r3c1")
    ]),

tab2_r3c1_content = html.Div([
    dt.DataTable(id="tabla-r3c1")
])

@app.callback(Output("content-r3c1", "children"), [Input("tabs-r3c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r3c1-1":
        return tab1_r3c1_content
    elif at == "tab-r3c1-2":
        return tab2_r3c1_content
    return html.P("This shouldn't ever be displayed...")


@app.callback(
        Output('plot-r3c1', 'figure'),
        #Input('submit-button', 'n_clicks'),
        #Input('producto', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot_r3c1(anio_sel):
    
   
    # filtro de año
    base = df_benef.copy()
    base_filt = base[base['Anio'] == int(anio_sel)]
    
    # Map 
    base_filt = base_filt[['NOM_ENT', 'Producto','MONTO_APOYO_TOTAL']].groupby(['NOM_ENT', 'Producto'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    base_filt_mean = base_filt['MONTO_APOYO_TOTAL'].mean()
    # 
    productos = base_filt['Producto'].unique()
    
    fig = go.Figure()
    
    for producto in productos:
        fig.add_trace(
                go.Bar(name= producto, 
                x=base_filt[base_filt['Producto']==producto]['NOM_ENT'].to_list(),
                y=base_filt[base_filt['Producto']==producto]['MONTO_APOYO_TOTAL'].to_list()
                )
        ),

    fig.update_layout(barmode='stack')
    
    fig.add_hline(y=base_filt_mean, line_dash="dot", row=3, col="all",
                annotation_text="Promedio", 
                annotation_position="bottom right")
    
    fig.update_layout(
        showlegend=False,
        autosize=False,
        #width=900,
        height=400,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor= "White",
            )

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Monto Apoyo",
        legend_title="",
        font=dict(
            #   family="Courier New, monospace",
            size=8,
            color="Black"
            ))

    fig.update_xaxes(tickangle=80)

    return fig



###   Actualiza grafico row4 - col2
tab1_r3c2_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r3c2")
    ]),

tab2_r3c2_content = html.Div([
    dcc.Graph(id="tabla-r3c2")
])


@app.callback(Output("content-r3c2", "children"), [Input("tabs-r3c2", "active_tab")])
def switch_tab(at):
    if at == "tab-r3c2-1":
        return tab1_r3c2_content
    elif at == "tab-r3c2-2":
        return tab2_r3c2_content
    return html.P("This shouldn't ever be displayed...")


@app.callback(
        Output('plot-r3c2', 'figure'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r3c2(clicks, producto_sel, anio_sel):
    
    # Map 
    df_benef_state = df_benef[['NOM_ENT', 'MONTO_APOYO_TOTAL']].groupby('NOM_ENT').sum().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    df_benef_state_mean = df_benef_state.mean()[:10]
    
    fig = go.Figure()
    # 
    fig.add_trace(go.Bar(
        x=df_benef_state.index.to_list(),
        y=df_benef_state['MONTO_APOYO_TOTAL'].to_list()))

    fig.add_hline(y=df_benef_state_mean['MONTO_APOYO_TOTAL'], line_dash="dot", row=3, col="all",
                annotation_text="Promedio", 
                annotation_position="bottom right")
    
    fig.update_layout(
        showlegend=False,
        autosize=False,
        #width=900,
        height=400,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor= "White",
            )

    fig.update_layout(
        title="Monto Apoyo Total",
        xaxis_title="Monto Apoyo Total",
        yaxis_title="Monto Apoyo Total",
        legend_title="",
        font=dict(
            #   family="Courier New, monospace",
            size=8,
            color="RebeccaPurple"
            ))

    fig.update_xaxes(tickangle=80)

    return fig


# acordion - uno
characters_list = [
    {
        "id": "bender",
        "image": "/assets/chart-histogram.png",
        "label": "Punto número uno",
        "description": "Fascinated with cooking, though has no sense of taste",
        "content": "Bender Bending Rodríguez, (born September 4, 2996), designated Bending Unit 22, and commonly "
        "known as Bender, is a bending unit created by a division of MomCorp in Tijuana, Mexico, "
        "and his serial number is 2716057. His mugshot id number is 01473. He is Fry's best friend.",
    },
    {
        "id": "carol",
        "image": "/assets/chart-line-up.png",
        "label": "Punto número dos",
        "description": "One of the richest people on Earth",
        "content": "Carol Miller (born January 30, 2880), better known as Mom, is the evil chief executive officer "
        "and shareholder of 99.7% of Momcorp, one of the largest industrial conglomerates in the universe "
        "and the source of most of Earth's robots. She is also one of the main antagonists of the Futurama "
        "series.",
    },
    
]

def create_accordion_label(label, image, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                dmc.Avatar(src=image, radius="xl", size="lg"),
                html.Div([
                        dmc.Text(label),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),
                    ]),
            ]
        )
    )


def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))


@app.callback(
    Output("accordion-text-uno", "children"), 
    Input("accordion-uno", "value"))
def show_state(value):
    result = dmc.Accordion(
    chevronPosition="right",
    variant="contained",
    children=[
        dmc.AccordionItem(
            [
                create_accordion_label(
                    character["label"], character["image"], character["description"]
                ),
                create_accordion_content(character["content"]),
            ],
            value=character["id"],
        )
        for character in characters_list
    ],
    )
    return result