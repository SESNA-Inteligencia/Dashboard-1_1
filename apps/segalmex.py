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
from dash_extensions.enrich import Dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function, assign
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




#import plotly.io as pio
#pio.renderers.default = 'firefox'


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

# diccionario nombre columnas {base: new}
names = {
    'B_ANIO': 'Anio',
    'B_PRODUCTO': 'Producto2',
    'B_CVE_ENT': 'CVE_ENT',
    'B_NOM_ENT': 'NOM_ENT',
    'B_CVE_MUN': 'CVE_MUN',
    'B_NOM_MUN': 'NOM_MUN',
    'B_CVE_LOC': 'CVE_LOC',
    'B_NOM_LOC': 'NOM_LOC',
    'B_TAMPROD': 'TAMPROD',
    'C_IMM': 'IML',
    'C_GMM': 'GML',
    'B_MONTO DE APOYO TOTAL $': 'MONTO_APOYO_TOTAL',
    'C_Produccion': 'Volumenproduccion',
    'C_LAT_DECIMAL': 'LAT_DECIMAL',
    'C_LON_DECIMAL': 'LON_DECIMAL'
}

# base beneficiarios
products = {
    'ARROZ':'Arroz',
    'FRIJOL':'Frijol',
    'MAIZ':'Maíz',
    'LECHE':'Leche',
    'TRIGO':'Trigo'
}

#base = pd.read_excel(root + '/datasets/base_beneficiarios_dashboard_v5.xlsx')
df_2019 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2019.xlsx', sheet_name='Data')
df_2020 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2020.xlsx', sheet_name='Data')
df_2021 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2021.xlsx', sheet_name='Data')

base1 = pd.read_excel(root + '/datasets/base1.xlsx')
base_entidad = pd.read_excel(root + '/datasets/base_entidad.xlsx')

centros = pd.read_excel(root + '/datasets/centros.xlsx')

# read datasets
df = pd.concat([df_2019, df_2020, df_2021], axis=0).reset_index()
usecols = [*names.keys()]
base = df[usecols].copy()
base.columns = [*names.values()]
# base2
data2 = json.load(open(root +'/datasets/sample.json'))
# change 
base['Producto'] = base['Producto2'].map(products)

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
list_states = base['NOM_ENT'].unique()
list_layers = ['Centros de acopio','Volumen Produccion']
list_bneficiarios_opciones = ['Monto del Apoyo', 'Número de Beneficiarios']


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


####################      sidebar left: Barra de control
sidebar_right = html.Div([
        # Filtros
        dbc.Row([
            html.Div([
                dmc.Text("Beneficiarios"),
                dmc.Text("Seleccione la característica que desee visualizar", size="sm", color="gray"),
                dmc.ChipGroup(
                    [dmc.Chip(k, value=k) for k in list_bneficiarios_opciones],
                    id='beneficiarios-opciones',
                    value='Número de Beneficiarios'
                ),
                ], className='mb-4 mt-2'),
            html.Hr(),
            html.Div([
                    dmc.Text("Seleccione la capa que desee visualizar"),
                    dmc.RadioGroup(
                        [dmc.Radio(k, value=k) for k in list_layers],
                        id="radiogroup-simple",
                        orientation="vertical",
                        value="Centros de acopio",
                        #label="",
                        size="sm",
                        mt=5,
                    ),
                    dmc.Text(id="radio-centros"),
                ], className='mb-4'),
     
            html.Div([
                dmc.Text("Nivel de Marginación"),
                dmc.MultiSelect(
                    id='grado_marginacion', 
                    value= ['Muy bajo'],
                    data=list_grado_marginacion,
                    clearable=True,
                    style={"width": 350}  
                ),       
                
                ], className='mb-2'),
            html.Div([
                dmc.Text("Tamaño del Productor"),
                dmc.MultiSelect(
                    id='tamanio_productor', 
                    value= ['Pequeño'],
                    data=list_tamano_productor,
                    clearable=True,
                    style={"width": 350}  
                ),       
                ]),

        ], className="mt-2", style={'marginBottom':'1rem'}),
    
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

#######################    content - Mapa interactivo 
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


#######################    content3 - gráficos principales
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

#######################    content4 - gráficos principales
content4 = html.Div([
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
        
        # accordeon
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                            dmc.Accordion(id="accordion-dos"),
                            dmc.Text(id="accordion-text-dos", mt=10),
                    ]),
                ]),
            ], className="col-8", style={'marginTop':'2rem','marginBottom':'1rem','marginLeft':'1rem', 'marginRight':'1rem'}),
        
        ], className="eight columns", style={'backgroundColor':'#F4F6F6', 'm':'0px', 'padding':'0px'}),
        # second row: graficos
        dbc.Row([
                dbc.Col(content3, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem'}),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
                ]
        ),
        # accordeon
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                            dmc.Accordion(id="accordion-tres"),
                            dmc.Text(id="accordion-text-tres", mt=10),
                    ]),
                ]),
            ], className="col-8", style={'marginTop':'2rem','marginBottom':'1rem','marginLeft':'1rem', 'marginRight':'1rem'}),
        
        ], className="eight columns", style={'backgroundColor':'#F4F6F6', 'm':'0px', 'padding':'0px'}),
    
        # third row: graficos
        dbc.Row([
                dbc.Col(content2, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem'}),
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


#-------------------------------------------------------------------------------
#                              Resumen cards
#-------------------------------------------------------------------------------
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
    
    data = base[base['Anio'] == int(sel_anio)]
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
    
    data = base[base['Anio'] == int(sel_anio)]
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
    
##########################################################################################
# SECCIÓN I :  mapa
##########################################################################################
# grafica mapa

tab1_mapa_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="mapa")
    ], style={'height': '100vh'})

tab2_mapa_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dl.Map(id="mapa2")
    ], style={'height': '100vh'})


# Función para encabezados
def get_info(feature=None):
    # Valores por defecto a nivel nacional 
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()
    
    if not feature:
        return [
            html.H4("{}".format("Nacional")),
            html.Br(),
            html.B("Monto Apoyo"), ": {} \n".format(100),
            html.Br(),
            html.B("Monto Promedio Apoyo"), ": {} \n".format(100),
            html.Br(),
            html.B("Total Beneficiarios"), ": {} \n".format(1278),
            html.Br(),
            html.B("Total Centros Acopio"), ": {} \n".format(1278),
            html.Br()]
        # valores a nivel estatal
    return [
            html.H4("{}".format(feature["properties"]["name"])),
            #html.Br(),
            #html.B("Estado"), ": ",
            #html.A("{}".format(feature["properties"]["name"])),
            html.Br(),
            html.B("Monto Apoyo"), ": {} \n".format(np.round(np.sum(base1[base1['NOM_ENT'] == feature["properties"]["name"]]['MONTO_APOYO_TOTAL']),2)),
            html.Br(),
            html.B("Monto Promedio Apoyo"), ": {} \n".format(np.round(np.mean(base1[base1['NOM_ENT'] == feature["properties"]["name"]]['MONTO_APOYO_TOTAL']),2)),
            html.Br(),
            html.B("Total Beneficiarios"), ": {} \n".format(1278),
            html.Br(),
            html.B("Total Centros Acopio"), ": {} \n".format(1278),
            html.Br()]

# declaración de parámetros para color y leyendas        
classes = [0, 5, 10, 20, 40, 60, 80, 100]
colorscale = ['#D5F5E3', '#ABEBC6', '#82E0AA', '#58D68D', '#2ECC71', '#28B463', '#239B56', '#1D8348']
style = dict(weight=2, opacity=1, color='#ECF0F1', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")

# Information
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})


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
    #base = base.copy()
    #base = base.dropna()
    benef_filter = base[base['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    #benef_filter = benef_filter[benef_filter['GM_2020'].isin(gmarg)]
    #benef_filter = benef_filter[benef_filter['Tamanio_productor'].isin(tprod)]
    max_benef = benef_filter['MONTO_APOYO_TOTAL'].max()    
        
    #est_color = df_prod_est[df_prod_est['Anio']==int(anio_sel)]
    #est_color = est_color [est_color['Producto']==producto_sel]
    
    #if isinstance(ticker_sel, str):
    #    stks = [ticker_sel]
    #else:
    #    stks = ticker_sel
    # MAPA
    fig = go.Figure()
    # Traza areas de producción
    fig.add_trace(go.Choroplethmapbox(name='Mexico', geojson=mx_est_geo, ids=benef_filter['NOM_ENT'], z=benef_filter['Volumenproduccion'],
                                        locations=benef_filter['NOM_ENT'], featureidkey='properties.name', colorscale='greens',
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
    
    #
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
#@app.callback(
#        Output('mapa2', 'figure'),
#        Input('submit-button', 'n_clicks'),
#        State('producto', 'value'),
#        State('anio', 'value')
#    )
# actualiza infor en mapa
@app.callback(Output("info", "children"), [Input("states", "hover_feature")])
def info_hover(feature):
    return get_info(feature)

@app.callback(
        Output('mapa2', 'children'),
        Input('submit-button', 'n_clicks'),
        #Input('t_productor', 'value'),
        #Input('grado_marginacion', 'value'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_mapa2(clicks, producto_sel, anio_sel):
    
    benef_filter = base1[base1['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    
    
    tab2_mapa_content = html.Div([
            dl.Map(center=[22.76, -102.58], zoom=5, children=[
                dl.TileLayer(),
                colorbar,
                info, 
                dl.GeoJSON(data=data2,  # url to geojson file
                            options=dict(style=style_handle),  # how to style each polygon
                            zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                            zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                            hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='7')),  # style applied on hover
                            hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),
                            id="states"),  
                dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color='blue', children=[
                                dl.Popup("Municipio: {}".format(mun))
                                ]) for mun, lat, lon, radio, color in zip(base1['NOM_MUN'], base1['LAT_DECIMAL'], base1['LON_DECIMAL'], base1['radio'], base1['color'])]),
                dl.Pane([dl.Circle(center=[lat, lon], radius=6, color='red', children=[
                                dl.Popup("Municipio: {}".format(mun))
                                ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),               
                #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
                #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
                #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
        ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
            #html.Div(id="state"), html.Div(id="info2")
        ])
    return tab2_mapa_content
############################################################################################
# SECTION II : 
############################################################################################

# Tabs actualization
tab1_r2c1_content = html.Div([             
    dcc.Graph(id="plot1-r2c1")
])

tab2_r2c1_content = html.Div([
    dcc.Graph(id="plot2-r2c1")
    #dcc.Graph(id="tabla-r2c1")
])
@app.callback(Output("content-r2c1", "children"), [Input("tabs-r2c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c1-1":
        return tab1_r2c1_content
    elif at == "tab-r2c1-2":
        return tab2_r2c1_content
    return html.P("This shouldn't ever be displayed...")

#----------------------------------------------------------------------------------
#                     Actializa Tab 1: row2 - col1
#----------------------------------------------------------------------------------
@app.callback(
        Output('plot1-r2c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('estados', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot1_r2c1(clicks, anio_sel):
    #
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}   
    
    # 
    base2 = base[base['Anio'] == int(anio_sel)]
    #base = dist_plot[dist_plot['PRODUCTO2']== producto]

    base2 = base2.groupby(['Producto'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    #milli = [millify(element, precision=2) for element in base['MONTO_APOYO_TOTAL']]
    #print(milli)

    fig = go.Figure()
    productos = base2['Producto'].unique()
    # all traces
    for producto in productos:
        base_prod = base2[base2['Producto']==producto]
        fig.add_trace(go.Bar(
                    x=base_prod['Producto'].to_list(),
                    y=base_prod['MONTO_APOYO_TOTAL'].to_list(),
                    text=millify(base_prod['MONTO_APOYO_TOTAL'],2),
                    name=producto,
                    width=0.98,
                    ))
    
    fig.update_layout(
            showlegend=True,
            autosize=False,
            #width=900,
            height=350,
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
            yaxis_title="Monto apoyo otorgado",
            legend_title="Producto:",
            font=dict(
                #family="Courier New, monospace",
                size=12,
                color="Black"
                ))

    fig.update_xaxes(tickangle=0)

    
    return fig

#----------------------------------------------------------------------------------------
#                        Actualización Tab 2 : row2 - col1
#--------------------------------------------------------------------------------------- 
@app.callback(
        Output('plot2-r2c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('estados', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot2_r2c1(clicks, anio_sel):
        
  
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}   
    
    productos = base['Producto'].unique()
    anios = base['Anio'].unique()
    base2 = base.groupby(['Producto','Anio'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    #milli = [millify(element, precision=2) for element in base['MONTO_APOYO_TOTAL']]
    #print(milli)

    fig = go.Figure()
    for producto in productos:
    #for anio in anios:
        base_i = base2[base2['Producto'] == producto].sort_values('Anio', ascending=True)
        milli = [millify(ele, precision=2) for ele in base_i['MONTO_APOYO_TOTAL']]
    #  base_i = base_i[base_i['ANIO'] == anio]
        # all traces
        #print(base_i['MONTO_APOYO_TOTAL'])
        fig.add_trace(go.Scatter(
                x= base_i['Anio'].astype('str'),
                y= base_i['MONTO_APOYO_TOTAL'].to_list(),
                text= milli,
                mode="lines+markers+text",
                name= producto,
                textposition="top right"
                ))

    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

    fig.update_layout(
                showlegend=True,
                autosize=False,
                #width=900,
                height=350,
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
                yaxis_title="Monto Apoyo Otorgado ($)",
                legend_title="",
                font=dict(
                    #family="Courier New, monospace",
                    size=12,
                    color="Black"
                    ))

    fig.update_xaxes(tickangle=0)
    
    
    return fig

#   Actualización row2 - col2
tab1_r2c2_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot1-r2c2")
    ]),

tab2_r2c2_content = html.Div([
    dt.DataTable(id="plot2-r2c2")
])

#  Actualiza tabs - mapa
@app.callback(Output("content-r2c2", "children"), [Input("tabs-r2c2", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c2-1":
        return tab1_r2c2_content
    elif at == "tab-r2c2-2":
        return tab2_r2c2_content
    return html.P("This shouldn't ever be displayed...")

#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row2-col2
#--------------------------------------------------------------------------------------
@app.callback(
        Output('plot1-r2c2', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('municipios', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot_r2c2(clicks, anio_sel):
    

    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}
    # Total de productos
    
    productos = base['Producto'].unique()
    anios = base['Anio'].unique()
    base2 = base.groupby(['Producto','Anio'])['MONTO_APOYO_TOTAL'].sum().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    #milli = [millify(element, precision=2) for element in base['MONTO_APOYO_TOTAL']]
    #print(milli)

    fig = go.Figure()
    for producto in productos:
    #for anio in anios:
        base_i = base2[base2['Producto'] == producto].sort_values('Anio', ascending=True)
        milli = [millify(ele, precision=2) for ele in base_i['MONTO_APOYO_TOTAL']]
    #  base_i = base_i[base_i['ANIO'] == anio]
        # all traces
        #print(base_i['MONTO_APOYO_TOTAL'])
        fig.add_trace(go.Scatter(
                x= base_i['Anio'].astype('str'),
                y= base_i['MONTO_APOYO_TOTAL'].to_list(),
                text= milli,
                mode="lines+markers+text",
                name= producto,
                textposition="top right"
                ))

    fig.update_layout(legend=dict(
            orientation="v",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

    fig.update_layout(
                showlegend=True,
                autosize=False,
                #width=900,
                height=350,
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
                yaxis_title="Monto Apoyo Otorgado ($)",
                legend_title="",
                font=dict(
                    #family="Courier New, monospace",
                    size=12,
                    color="Black"
                    ))

    fig.update_xaxes(tickangle=0)
    
    
    return fig

#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row2-col2
#--------------------------------------------------------------------------------------
@app.callback(
        Output('plot2-r2c2', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('municipios', 'value'),
        #Input('anio', 'value')
    )

def actualizar_plot2_r2c2(clicks):
    
    colors = {'Arroz': 'orange', 
          'Maíz': 'yellow',
          'Frijol': 'brown',
          'Leche': 'blue',
          'Trigo': 'green'}
    # Total de productos
    base2 = base.copy()
    labels = base2['Anio'].unique()
    widths = np.array([33.3,33.3,33.3])

    # diccionario con key: producto y value=monto por año
    data = {product:np.round(np.divide([base2[(base2['Producto'] == product) & (base2['Anio'] == anio)]['MONTO_APOYO_TOTAL'].sum() for anio in np.sort(base2['Anio'].unique())],[base2[base2['Anio'] == anio]['MONTO_APOYO_TOTAL'].sum() for anio in np.sort(base2['Anio'].unique())]),4)*100 for product in base2['Producto'].unique()}
    data_monto = {product:[base2[(base2['Producto'] == product) & (base2['Anio'] == anio)]['MONTO_APOYO_TOTAL'].sum() for anio in np.sort(base2['Anio'].unique())] for product in base2['Producto'].unique()}

    fig = go.Figure()
    for key in data:
    #if key == product:
        fig.add_trace(go.Bar(
            name=key,
            y=data[key],
            x=np.cumsum(widths)-widths,
            width=widths,
            offset=0,
            opacity=0.8,
            customdata= [millify(element,2) for element in data_monto[key]],
            texttemplate=" %{y}% <br> %{customdata}",
            textposition="inside",
            textangle=0,
            textfont_color="white",
            hovertemplate="<br>".join([
                "Porcentaje: %{y}%",
                "Monto: %{customdata}",
            ])
        ))
 
    fig.update_xaxes(
        tickvals=np.cumsum(widths)-widths/2,
        ticktext= ["%s<br>" % l for l in labels]
    )

    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))
    fig.update_layout(
                showlegend=True,
                autosize=False,
                width=700,
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

    fig.update_xaxes(range=[0,100])
    fig.update_yaxes(range=[0,100], visible=False)
    #ig.update.layout(xaxis_visible=False, yaxis_visible=False, xaxis2_visible=False, yaxis2_visible=False)
    fig.update_layout(
        title_text="",
        barmode="stack",
        uniformtext=dict(mode="hide", minsize=10),
    )
    #fig.show(config={"displayModeBar": False})
    
    return fig




#########################################################################################
# SECTION II - grafico r2 :  
##########################################################################################
tab1_r3c1_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot1-r3c1")
    ]),

tab2_r3c1_content = html.Div([
     dcc.Graph(id="plot2-r3c1")
])

@app.callback(Output("content-r3c1", "children"), [Input("tabs-r3c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r3c1-1":
        return tab1_r3c1_content
    elif at == "tab-r3c1-2":
        return tab2_r3c1_content
    return html.P("This shouldn't ever be displayed...")


#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row3-col1  --> Grafico monto y producto vs estado
#--------------------------------------------------------------------------------------
@app.callback(
        Output('plot1-r3c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('producto', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot1_r3c1(clicks, anio_sel):
    
    # filtro de año
    #base = base.copy()
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


#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row3-col1 Grafico qqplot
#--------------------------------------------------------------------------------------

@app.callback(
        Output('plot2-r3c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        Input('producto', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot2_r3c1(clicks, producto_sel, anio_sel):
    
    dist_plot = base[base['Anio'] == int(anio_sel)]
    dist_plot = dist_plot[dist_plot['Producto']== producto_sel]

    idx = dist_plot.groupby(['NOM_ENT'])['MONTO_APOYO_TOTAL'].mean().reset_index().sort_values('MONTO_APOYO_TOTAL', ascending=False)
    #dist_plot = dist_plot.iloc[idx]
    monto_promedio = dist_plot['MONTO_APOYO_TOTAL'].mean()

    estados = idx['NOM_ENT'].unique()
    colores = [f'rgba({26+i*3},{45+i*5},{96+i*8},0.8)' for i in range(len(estados))]
    
    fig = go.Figure()
    for estado, cls in zip(estados, colores):
        serie = dist_plot[dist_plot['NOM_ENT'] == estado]
        #print(serie)
        fig.add_trace(
                    go.Box(
                        y=serie['MONTO_APOYO_TOTAL'], 
                        orientation='v',
                        name=estado,
                        #boxpoints='all',
                        #jitter=0.5,
                        whiskerwidth=0.1,
                        marker_color=cls,
                        fillcolor=cls,
                        marker=dict(
                            size=0.1,
                            #color='rgb(0, 0, 0)'
                        )
                        ))
    fig.add_hline(y=monto_promedio, line_width=0.3, line_dash="dash", line_color="blue", opacity=0.2)
    #Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=1)
    fig.update_layout(paper_bgcolor='white',
                        plot_bgcolor='white',)
        

    fig.update_layout(showlegend=False)
        
    fig.update_layout(
            autosize=False,
            #width=1020,
            height=350,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0),
            #paper_bgcolor="Lightblue",
            )

    return fig

###########################################################################################
#                                   SECTION III
###########################################################################################
# funcion para accordion label
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
# funcion para accordion content
def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))

# acordeon uno callbacks
@app.callback(
    Output("accordion-text-uno", "children"), 
    Input("accordion-uno", "value"))
def show_state(value):
    # text
    characters_list = [
        {
            "id": "bender",
            "image": "/assets/chart-histogram.png",
            "label": "Punto número uno",
            "description": "Descripción punto uno",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        },
        {
            "id": "carol",
            "image": "/assets/chart-line-up.png",
            "label": "Punto número dos",
            "description": "Descripción punto dos",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        },
        
    ]
    # resultado
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


# acordeon dos callbacks
@app.callback(
    Output("accordion-text-dos", "children"), 
    Input("accordion-dos", "value"))
def show_state(value):
    # text
    characters_list = [
        {
            "id": "bender",
            "image": "/assets/chart-histogram.png",
            "label": "Punto número uno",
            "description": "Descripción punto uno",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        },
        
        
    ]
    # resultado
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

# acordeon tres callbacks
@app.callback(
    Output("accordion-text-tres", "children"), 
    Input("accordion-tres", "value"))
def show_state(value):
    # text
    characters_list = [
        {
            "id": "carol",
            "image": "/assets/chart-line-up.png",
            "label": "Punto número dos",
            "description": "Descripción punto dos",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        },
        
    ]
    # resultado
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