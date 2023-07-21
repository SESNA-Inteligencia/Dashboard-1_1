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

def get_info(feature=None):
    # Valores por defecto a nivel nacional 
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()
    
    if not feature:
        return [
            html.H4("{}".format("Nacional")),
            dmc.Center(html.Img(id='image', src='../assets/Nacional.png', width="65", height="65"))]
        # valores a nivel estatal
    return [
            html.H4("{}".format(feature["properties"]["name"])),
            #html.Br(),
            #html.B("Estado"), ": ",
            #html.A("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

def get_info2(feature=None):
    # Valores por defecto a nivel nacional 
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()
    
    if not feature:
        return html.Center([
            dbc.Col(html.Img(src='../assets/Nacional.png', height="90px")),
            dbc.Col(html.H1("Nacional")),
        ])
    #[
    #        dmc.Center(html.H4("{}".format("Nacional"))),
    #        dmc.Center(html.Img(id='image', src='../assets/Nacional.png', width="65", height="65"))]
    # valores a nivel estatal
    return html.Center([
            dbc.Col(html.Img(id='image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="90")),
            dbc.Col(html.H1("{}".format(feature["properties"]["name"]))),
        ])
    
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
df = pd.concat([df_2019, df_2020, df_2021], axis=0).reset_index()

usecols = [*names.keys()]
base = df[usecols].copy()
base.columns = [*names.values()]
base['Producto'] = base['Producto2'].map(products)
# base2 : georeferencia (contornos) a nivel estatal
#data2 = json.load(open(root +'/datasets/sample.json'))
data2 = json.load(open(root +'/datasets/sample3.json'))

# bases OK
base1 = pd.read_excel(root + '/datasets/base1.xlsx')
# bases de beneficiarios a nivel estatal y municipal para tamaño de productor y sin tamaño de productor
base_entidad = pd.read_excel(root + '/datasets/base_entidad.xlsx')
base_entidad_tprod = pd.read_excel(root + '/datasets/base_entidad_tprod.xlsx')
base_municipios = pd.read_excel(root + '/datasets/base_municipio.xlsx')
base_municipios_tprod = pd.read_excel(root + '/datasets/base_municipio_tprod.xlsx')
# bases de centrros de acopio a nivel entidad y municipal
centros_entidad = pd.read_excel(root + '/datasets/centros_entidad.xlsx')
centros_municipio = pd.read_excel(root + '/datasets/centros_municipio.xlsx')

# sample maps 
# blue style
style1 = "https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png"
# grey style
style2 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
# black style
style3 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
# base centros de acopio
#df_centros = pd.read_excel(root + '/datasets/base_centros_inegi.xlsx')
#df_centros = df_centros

# base producción agrícola
#df_produccion = pd.read_excel(root + '/datasets/base_prodAgricola_con_claves_inegi.xlsx')
#df_produccion = df_produccion.dropna()
# georeferenciación de base producción - estados
#df_prod_est = pd.read_csv(root + '/datasets/produccion_estados.csv')

# opciones 
list_year = ['2019', '2020', '2021']
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']
list_grado_marginacion = [['Muy bajo', 'blue'], 
                          ['Bajo','indigo'], 
                          ['Medio', 'green'], 
                          ['Alto', 'red'], 
                          ['Muy alto', 'orange']]

list_tamano_productor = ['Pequeño', 'Mediano', 'Grande']
list_states = base['NOM_ENT'].unique()
list_layers = ['Centros de Acopio','Volumen Producción', 'All']
list_beneficiarios_opciones = ['Monto del Apoyo', 'Número de Beneficiarios']

#------------------------------------------------------------------------------
#                        layout
####################    header
sidebar_header = html.Div([
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
                ],className="card col-12 col-md-2", style={'boxShadow': '#e3e3e3 4px 4px 1px','marginLeft':'2rem', 'marginRight':'2rem', "height": '6rem', 'padding':'.2rem', 'border-radius': '5px', 'backgroundColor': '#EBF5FB', }),
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
                    
            ],className="card col-12 col-md-2", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'marginRight':'2rem', "height": '6rem', 'padding':'.2rem', 'border-radius': '5px', 'backgroundColor': '#EBF5FB', }),
            # tercero
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
                    
                ],className="card col-12 col-md-2", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'marginRight':'2rem', "height": '6rem', 'padding':'.2rem', 'border-radius': '5px', 'backgroundColor': '#EBF5FB', }),
            # cuarto
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
                    
            ],className="card col-12 col-md-2", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'marginRight':'2rem', "height": '6rem', 'padding':'.2rem', 'border-radius': '5px', 'backgroundColor': '#EBF5FB', }),
            # quinto
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
                ],className="card col-12 col-md-2", style={'boxShadow': '#e3e3e3 4px 4px 1px', 'marginRight':'0rem', "height": '6rem', 'padding':'.2rem', 'border-radius': '5px', 'backgroundColor': '#EBF5FB', }),
            # sexto
            
    ], style={'marginTop':'4rem'}), 
], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem', 'marginBottom':'2rem'})

# Filtros principales
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
                #dmc.ChipGroup(
                #    [dmc.Chip(k, value=k) for k in list_bneficiarios_opciones],
                #    id='beneficiarios-opciones',
                #    multiple=False,
                #    value='Número de Beneficiarios'
                #),
                dmc.RadioGroup(
                        [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
                        id="beneficiarios-opciones",
                        orientation="horizontal",
                        #multiple=True,
                        value="Número de Beneficiarios",
                        #label="",
                         mb=10,
                ),
                ], className='mb-4 mt-2'),
            html.Hr(),
            html.Div([
                    dmc.Text("Seleccione la capa que desee visualizar"),
                    dmc.SegmentedControl(
                    #dmc.ChipGroup(
                    #    [dmc.Chip(k, value=k, variant='outline') for k in list_layers],
                        orientation="horizontal",
                        fullWidth=True,
                        id='radio-centros',
                        data=list_layers,
                        color='#4E203A',
                        #multiple=False,
                        value='Volumen Producción',
                    ),
                    #dmc.RadioGroup(
                    #    [dmc.Radio(k, value=k) for k in list_layers],
                    #    id="radio-centros",
                    #    orientation="vertical",
                    #    #multiple=True,
                    #    value="Centros de acopio",
                    #    #label="",
                    #    size="sm",
                    #    mt=5,
                    #),
                    #dmc.Text(id="radio-centros"),
                ], className='mb-4'),
     
            html.Div([
                dmc.Text("Nivel de Marginación"),
                #dmc.MultiSelect(
                #    id='grado_marginacion', 
                #    value= ['Muy bajo'],
                #    data=list_grado_marginacion,
                    #color = '#4E203A',
                #    clearable=True,
                #    style={"width": 350}  
                #),  
                dmc.CheckboxGroup(
                    id="grado_marginacion",
                    label="Grado de marginación",
                    description="",
                    orientation="horizontal",
                    withAsterisk=True,
                    offset="md",
                    mb=12,
                    children=[
                        dmc.Checkbox(label="Muy bajo", value="Muy bajo", color="indigo"),
                        dmc.Checkbox(label="Bajo", value="Bajo", color="blue"),
                        dmc.Checkbox(label="Medio", value="Medio", color="green"),
                        dmc.Checkbox(label="Alto", value="Alto", color="orange"),
                        dmc.Checkbox(label="Muy alto", value="Muy alto", color="pink"),
                    ],
                    value=["Muy bajo", "Bajo","Medio","Alto","Muy alto"],
                ),      
                ], className='mb-2'),

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
                            dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
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
                            dmc.Text("Pob. Beneficiaria", color='grey', weight=500, align='center', style={"fontSize": 11}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem', 'border-radius': '5px', 'backgroundColor': '#7C90AB', }),  #'#F4F6F6'

        ], style={'marginTop':'1rem'}), 

  
        # Row three
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
                        ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
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
                        ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
                        )]),
                        dbc.Row([html.Div([
                            dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
                            ]),
                        ]),
                    ], className="card col-9 border-0 bg-transparent"), 
                ]),
                    
                ],className="card col-12 col-md-6", style={'padding':'.3rem','border-radius': '5px', 'backgroundColor': '#F4F6F6', }),

        ], style={'marginTop':'1rem', 'marginBottom':'1rem'}),

        ], style={'marginLeft':'2rem', 'marginRight':'2rem', 'marginTop':'1rem'}
    )

#######################    content - Mapa interactivo ##############
content1 = html.Div([
        dbc.Row([
            dbc.Col([
                    html.Div([
                        #dbc.Tabs([
                        #        dbc.Tab(label="Mapa", tab_id="tab-1", label_style={"backgroundColor":"#2a3240","color": "white"}),
                        #        
                        #        #dbc.Tab(label="Tabla", tab_id="tab-2",  label_style={"color": "#00AEF9"}),
                        #    ],
                        #    id="tabs-mapa",
                        #    active_tab="tab-1",
                        #    style={'backgroundColor':'#BFC9CA', 'padding':'.0rem'},
                        #),
                        dl.Map(id="mapa2"),
                     ], style={"width": "100%"}
                    ),   # style={'height':'100vh'}               
            ], className="card col-12 col-md-8", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': '#BFC9CA', }
            ), 
            dbc.Col([
                sidebar_right
                
            ], className="card col-12 col-md-4", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '0px', 'backgroundColor': 'white', }
            )
        ]),
        # Barra de control
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem', 'marginRight': '2rem','marginBottom': '4rem'}
    )
# backgroundColor': '#F4F6F6'
#############################################################
###            content2 - graficos barras
###    - Gráfico1 : Tamaño productor por estado
###    - Gráfico2 : Nivel de marginación por estado
############################################################# 
content2 = html.Div([
        dbc.Row([
            dbc.Col([
                    #html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 1", tab_id="tab-r2c1-1", label_style={"color": "white", 'backgroundColor': '#2a3240'}),
                                #dbc.Tab(label="Tabla 1", tab_id="tab-r2c1-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r2c1",
                            active_tab="tab-r2c1-1",
                            style={'backgroundColor': '#F2F4F4'}
                        ),
                        html.Div(id="content-r2c1"),
                    # ], style={'backgroundColor': '#F2F4F4',"width": "100%"}
                    #),                  
                ], className="card col-4 col-md-4", style={'backgroundColor': '#F2F4F4','padding':'.0rem', 'marginTop':'0rem', 'marginRight':'1rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', }
                ), 
            dbc.Col([], className="card col-3", style={'backgroundColor': '#F2F4F4'}),
            dbc.Col([
                    #html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 2", tab_id="tab-r2c2-1", label_style={"color": "#F2F4F4", 'backgroundColor': '#2a3240'}),
                                
                                #dbc.Tab(label="Tabla 2", tab_id="tab-r2c2-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r2c2",
                            active_tab="tab-r2c2-1",
                            style={'backgroundColor': '#F2F4F4'}
                        ),
                        html.Div(id="content-r2c2"),
                     #], style={'backgroundColor': '#F2F4F4', "width": "100%"}
                    #),                  
                ], className="card col-4 col-md-4", style={'padding':'.0rem', 'marginTop':'0rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': '#F2F4F4', }
                ), 
        ]),
        
    ], className="twelve columns", style={'backgroundColor': '#F2F4F4', 'marginLeft': '0rem','marginRight': '0rem','marginTop': '0rem','marginBottom': '4rem'}

    )

#######################    content3 - gráficos por municipios
content3 = html.Div([
        dbc.Row([
            dbc.Col([
                    
                    html.Div([
                        dbc.Tabs([
                                #dbc.Tab(label="Gráfico 3", tab_id="tab-r3c1-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Municipios", tab_id="tab-r3c1-2",  label_style={"color": "#4e203a", 'backgroundColor': '#F2F4F4'}),
                            ],
                            id="tabs-r3c1",
                            active_tab="tab-r3c1-2",
                            style={"backgroundColor":'#F2F4F4'}
                        ),
                        html.Div(id="content-r3c1"),
                     ], style={"backgroundColor":'#F2F4F4',"width": "100%"}
                    ),                  
                ], className="col-12", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
        ]),
    ], className="ten columns", style={'backgroundColor': '#F2F4F4', 'marginLeft': '4rem','marginRight': '4rem','marginTop': '0rem'}

    )

# Content 4
content4 = html.Div([
        dbc.Row([
            dbc.Col([
                    #html.Div([
                        
                        html.Div(id="content-r4_1"),
                    # ], style={'backgroundColor': '#F2F4F4',"width": "100%"}
                    #),                  
                ], className="card col-4 col-md-4", style={'backgroundColor': '#F2F4F4','padding':'.0rem', 'marginTop':'0rem', 'marginRight':'1rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', }
                ), 
            dbc.Col([], className="card col-3", style={'backgroundColor': '#F2F4F4'}),
            dbc.Col([
                    #html.Div([
                        html.Div(id="content-r4_2"),
                     #], style={'backgroundColor': '#F2F4F4', "width": "100%"}
                    #),                  
                ], className="card col-4 col-md-4", style={'padding':'.0rem', 'marginTop':'0rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': '#F2F4F4', }
                ), 
        ]),
        
    ], className="twelve columns", style={'backgroundColor': '#F2F4F4', 'marginLeft': '0rem','marginRight': '0rem','marginTop': '0rem'}

    )



# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([

        html.Div([
            html.Br(),
            html.Br(),
            dbc.Row([
            dbc.Col(html.Img(src="assets/segalmex3.jpg", height="80px"), style = {'textAlign':'center', 'marginRight':'10px'} ),
            ],
            className="g-0 m-0, p-0",
        ),
        
        dbc.Row([
            dbc.Col(html.H1("SEGALMEX"),  className="ml-5",  style = {'textAlign':'center', 'color':'white'} ),
            ],
            className="g-0 m-0 p-0",
        ),
        html.Br(),
        ], style={'background-image': 'url(/assets/maiz_image.jpg)','background-size': '150px 150px','backgroundColor':'#E5E8E8', 'm':'0px', 'padding':'0px'}),    
        
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
                            #dmc.Accordion(id="accordion-uno"),
                            #dmc.Text(id="accordion-text-uno", mt=10),
                            dmc.Spoiler(
                                showLabel="Show more",
                                hideLabel="Hide",
                                maxHeight=50,
                                children=[
                                    dmc.Text(
                                        """We Butter the Bread with Butter was founded in 2007 by Marcel Neumann, who was originally guitarist 
                                        for Martin Kesici's band, and Tobias Schultka. The band was originally meant as a joke, but progressed 
                                        into being a more serious musical duo. The name for the band has no particular meaning, although its 
                                        origins were suggested from when the two original members were driving in a car operated by Marcel 
                                        Neumann and an accident almost occurred. Neumann found Schultka "so funny that he briefly lost control of 
                                        the vehicle." Many of their songs from this point were covers of German folk tales and nursery rhymes. """
                                    )
                                ],
                            )
                    ]),
                ]),
            ], className="col-8", style={'marginTop':'2rem','marginBottom':'2rem','marginLeft':'1rem', 'marginRight':'1rem'}),
            
            # pie plot for products
            dbc.Row([
                html.Br(),
                html.Iframe(id='plot2-r3c1', srcDoc=open(root + "/graficos/piePlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1300px"})
            ], className="col-10", style={'backgroundColor':'#F2F3F4','marginTop':'4rem', 'marginBottom':'2rem', 'marginLeft':'6rem', 'marginRight':'4rem'}),
            
        ], className="eight columns", style={'backgroundColor':'#F4F6F6', 'm':'0px', 'padding':'0px'}),
            
        dbc.Row([html.H5(' ')]),
        # first row: filtros y mapa
        #dbc.Row([
        #    dbc.Col(sidebar_header, className="col-12 mb-4"),
        #    ]),
        dbc.Row([
                dbc.Col(content1, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6'}),
                #dbc.Col(sidebar_right, className="col-12 col-md-4"),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
                ]
        ),
        # Indicador de estado
        dbc.Row([
            #dbc.Col("", style={'marginLeft':'8px'}),
            dbc.Col(get_info2(), id="info2", md=4),
            #dbc.Col("", style={'marginRight':'8px'})
            ], style={'backgroundColor': '#F4F6F6','marginLeft':'2px','marginRight':'2px', 'marginBottom':'4px', 'backgroundColor': '#F4F6F6'}),

            # third row: graficos
        dbc.Row([
                dbc.Col(content2, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem', 'marginLeft':'2rem', 'marginRight':'2rem'}),
                #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
        ], className='mb-0', style={'marginLeft':'2rem', 'marginRight':'2rem'}),  
        
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
        
        dbc.Row([
                dbc.Col(content4, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem'}),
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
        #dbc.Row([
        #        dbc.Col(content2, className="col-12 col-md-12", style={'backgroundColor': '#F4F6F6', 'marginTop': '1rem', 'marginLeft':'2rem', 'marginRight':'2rem'}),
        #        #dbc.Col(sidebar_vol_right, width=3, className='bg-light')
        #], className='mb-0', style={'marginLeft':'2rem', 'marginRight':'2rem'}),  
        
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]),       
        
    ], style={'backgroundColor': '#F4F6F6', 'marginTop': '0rem', 'padding':'0rem'},
    fluid=True
    )
    # #EBF5FB
    # #F4F6F6
#########################################################################################
############################            Call backs         ##############################
#########################################################################################

#-------------------------------------------------------------------------------
#                              Resumen cards
#-------------------------------------------------------------------------------
#                      CARD 1 : Regresa estado
@app.callback(# 'click_feature
        Output('state01', 'children'),
        Input("states", "click_feature")
    )
def get_state(clicks, feature):
    
    # condición
    if not feature:
        state = 'Nacional'
    else: 
        # filtro de estado
        state = feature["properties"]["name"]

    return state

#           CARD 2 : Indicador de estado

@app.callback(# 'click_feature
        Output('state_label', 'children'),
        Input("states", "click_feature")
    )
def get_state(clicks, feature):
    
    # condición
    if not feature:
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str("Nacional") +'.png', width="65", height="65")),
          ]    
    else: 
        # filtro de estado
        state = feature["properties"]["name"]
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]



#                      CARD 1 : Cuenta centros de acopio
@app.callback(# 'click_feature
        Output('resumen-centros_acopio', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_centros_acopio(clicks, feature, sel_producto, sel_anio):
    
    # estado: feature["properties"]["name"]
    data = centros_entidad.copy()
    # condición
    if not feature:
        cuenta_registros = np.sum(data['NUM_CENTROS'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        cuenta_registros = data_filt['NUM_CENTROS']

    return cuenta_registros

#                      CARD 2 : Población beneficiaria
@app.callback(
        Output('resumen-poblacion_beneficiaria', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def resumen_pablacion_beneficiaria(clicks, feature, sel_producto, sel_anio):
    
    data = base_entidad.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Condición
    if not feature:
        result = np.sum(data['NUM_BENEFsize'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        result = np.sum(data_filt['NUM_BENEFsize'])

    return "{:,}".format(result)
    
#                      CARD 3 : Monto apoyos total
@app.callback(
        Output('resumen-monto_apoyos_total', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_monto_apoyos_total(clicks, feature, sel_producto, sel_anio):
    
    data = base_entidad.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Condición
    if not feature:
        result = np.sum(data['MONTO_APOYO_TOTALsum'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        result = np.sum(data_filt['MONTO_APOYO_TOTALsum'])
    # millify(monto_apoyos, precision=2)
    return millify(result, precision=1)

#                      CARD 4 : Monto apoyos promedio
@app.callback(
        Output('resumen_monto_apoyos_prom', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_monto_apoyos_promedio(clicks, feature, sel_producto, sel_anio):
    
    data = base_entidad.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Condición
    if not feature:
        result = np.mean(data['MONTO_APOYO_TOTALsum'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        result = np.mean(data_filt['MONTO_APOYO_TOTALmean'])

    # millify(monto_apoyos, precision=2)
    return millify(result, precision=1)

#                 CARD 5 : Volumen incentivado total
@app.callback(
        Output('resumen-volumen_incentivado_total', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_volumen_incentivado_total(clicks, feature, sel_producto, sel_anio):
    
    data = base_entidad.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    
    # Condición
    if not feature:
        result = np.sum(data['VolumenIncentivadosum'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        result = np.sum(data_filt['VolumenIncentivadosum'])
    # millify(monto_apoyos, precision=2)
    return millify(result, precision=1)

#                CARD 6 : Volumen Incentivado promedio
@app.callback(
        Output('resumen-volumen_incentivado_promedio', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )
def resumen_volumen_incentivado_promedio(clicks, feature, sel_producto, sel_anio):
    
    data = base_entidad.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    # Condición
    if not feature:
        result = np.sum(data['VolumenIncentivadomean'])
    else: 
        # filtro de estado
        data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
        # Sin dato nombre de dato faltante
        result = np.sum(data_filt['VolumenIncentivadomean'])
    # millify(monto_apoyos, precision=2)
    return millify(result, precision=1)

# Descarga de resumen ejecutivo  
#@app.callback(
#    Output("download", "data"), 
#    Input("btn", "n_clicks"))
#def func(n_clicks):
#    return dcc.send_file("C:/Users/jcmartinez/Desktop/Dashboard3/Proyecto.pdf")
    
##########################################################################################
# SECCIÓN I :  mapa
##########################################################################################
# gráfica mapa
tab1_mapa_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dl.Map(id="mapa2")
    ], style={'height': '100vh'})

tab2_mapa_content = html.Div([  
        #dcc.Graph(id="mapa", mathjax=True)
        html.Iframe(id='map', srcDoc=open('PieMap.html', 'r').read(), style={"height": "1200px", "width": "900px"})
    ], style={'height': '100vh', 'width': '100vh'})


    

# declaración de parámetros para color y leyendas        
classes = [0, 1000,3000,5000,10000, 100000, 1000000, 3000000]
colorscale = ['#D5F5E3', '#ABEBC6', '#82E0AA', '#58D68D', '#2ECC71', '#239B56', '#1D8348', '#0B5345']
style = dict(weight=1, opacity=0.9, color='#2e4053', dashArray='1', fillOpacity=1)
# estilo centros de acopio
style2 = dict(weight=1, opacity=0.9, color='#2e4053', dashArray='1', fillOpacity=1)
# Create colorbar.
ctg = ["{}+".format(millify(cls), classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(millify(classes[-1]))]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside
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
@app.callback(Output("content-mapa", "children"), 
              [Input("tabs-mapa", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_mapa_content
    elif at == "tab-2":
        return tab2_mapa_content
    return html.P("This shouldn't ever be displayed...")

####   actualiza tabla-Mapa
# actualiza infor en mapa
@app.callback(Output("info", "children"), 
              Input("states", "click_feature"))
              #State('producto', 'value'),
              #State('anio', 'value'))
def info_hover(feature):
    return get_info(feature)

@app.callback(Output("info2", "children"), 
              Input("states", "click_feature"))
              #State('producto', 'value'),
              #State('anio', 'value'))
def info_hover(feature):
    return get_info2(feature)


@app.callback(
        Output('mapa2', 'children'),
        Input('submit-button', 'n_clicks'),
        #Input('t_productor', 'value'),
        Input('grado_marginacion', 'value'),
        Input("beneficiarios-opciones", "value"),
        Input("radio-centros", "value"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_mapa2(clicks, margin_sel, benef_sel,capas_sel, producto_sel, anio_sel):
    
    # capas
    if isinstance(capas_sel, str):
        capas = [capas_sel]
    else:
        capas = capas_sel
    # nivel de marginación     
    if isinstance(margin_sel, str):
        margin = [margin_sel]
    else:
        margin = margin_sel
    
        
    centros = centros_municipio.copy()
    benef_filter = base_municipios[base_municipios['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['GMMmode'].isin(margin)]
    
    # opción de beneficiarios
    if benef_sel=='Número de Beneficiarios':
        benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
            dl.Popup("Municipio: {}".format(mun))
            ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
    else:
        benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color=color, children=[
            dl.Popup("Municipio: {}".format(mun))
            ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])
 
    # opción centros de acopio y de producción
    if capas_sel == 'Centros de Acopio':
        tab2_mapa_content = html.Div([
            dl.Map(center=[22.76, -102.58], zoom=5, children=[
                dl.TileLayer(url=style1),
                info,  
                 dl.GeoJSON(data=data2,  # url to geojson file
                            options=dict(style=style_handle),  # how to style each polygon
                            zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                            zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                            hoverStyle=arrow_function(dict(weight=4, color='white', dashArray='2')),  # style applied on hover
                            hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp="#2e4053"),
                            id="states"),  
                benef_option,
                dl.Pane([dl.Circle(center=[lat, lon], radius=6, color='red', children=[
                                dl.Popup("Municipio: {}".format(mun))
                                ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),               
                #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
                #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
                #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
                ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
                #html.Div(id="state"), html.Div(id="info2")
            ])
    elif capas_sel == 'Volumen Producción':
        tab2_mapa_content = html.Div([
            dl.Map(center=[22.76, -102.58], zoom=5, children=[
                dl.TileLayer(url=style1),
                colorbar,
                info, 
                dl.GeoJSON(data=data2,  # url to geojson file
                            options=dict(style=style_handle),  # how to style each polygon
                            zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                            zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                            hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp=f'{anio_sel}-{producto_sel}'),
                            hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
                            id="states"),  
                benef_option,           #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
                #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
                #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
                ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
                #html.Div(id="state"), html.Div(id="info2")
            ])
    else:
        tab2_mapa_content = html.Div([
            dl.Map(center=[22.76, -102.58], zoom=5, children=[
                dl.TileLayer(url=style1),
                colorbar,
                info, 
                dl.GeoJSON(data=data2,  # url to geojson file
                            options=dict(style=style_handle),  # how to style each polygon
                            zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                            zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                            hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
                            hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp=f'{anio_sel}-{producto_sel}'),
                            id="states"),  
                benef_option,
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
    html.Iframe(srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
])

tab2_r2c1_content = html.Div([
    dcc.Graph(id="plot2-r2c1")
    #dcc.Graph(id="tabla-r2c1")
])
@app.callback(Output("content-r2c1", "children"), 
              [Input("tabs-r2c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c1-1":
        return tab1_r2c1_content
    elif at == "tab-r2c1-2":
        return tab2_r2c1_content
    return html.P("This shouldn't ever be displayed...")

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 1:
#----------------------------------------------------------------------------------
@app.callback(
        Output('plot1-r2c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('estados', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot1_r2c1(clicks, anio_sel):
  
    
    return 

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 2:
#----------------------------------------------------------------------------------

tab1_r2c2_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        html.Iframe(id='plot1-r2c2', srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
    ]),

tab2_r2c2_content = html.Div([
    dt.DataTable(id="plot2-r2c2")
])

#  Actualiza tabs - mapa
@app.callback(Output("content-r2c2", "children"), 
              [Input("tabs-r2c2", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c2-1":
        return tab1_r2c2_content
    elif at == "tab-r2c2-2":
        return tab2_r2c2_content
    return html.P("This shouldn't ever be displayed...")

# --------------------------------------------
@app.callback(
        Output('plot1-r2c2', 'figure'),
        Input('submit-button', 'n_clicks'),
        #Input('municipios', 'value'),
        Input('anio', 'value')
    )

def actualizar_plot1_r2c2(clicks, anio_sel):
  
    return

#########################################################################################
#  SECTION III - grafico Barras por municipio  
##########################################################################################
tab1_r3c1_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot1-r3c1")
    ]),

tab2_r3c1_content = html.Div([
     #dcc.Graph(id="plot2-r3c1")
     html.Iframe(id='plot2-r3c1', srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1300px"})
], style={'height':'60vh'})

@app.callback(Output("content-r3c1", "children"), 
              [Input("tabs-r3c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r3c1-1":
        return tab1_r3c1_content
    elif at == "tab-r3c1-2":
        return tab2_r3c1_content
    return html.P("This shouldn't ever be displayed...")


#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row3-col1 Grafico qqplot
#--------------------------------------------------------------------------------------
@app.callback(
        Output('plot2-r3c1', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot2_r3c1(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    dist_plot = base[base['Anio'] == int(anio_sel)]
    dist_plot = dist_plot[dist_plot['Producto']== producto_sel]
    
    
    if feature == None:
        return open(root + f"/graficos/g1_barras/2020-Maíz-Veracruz de Ignacio de la Llave.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]
    
        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
  

###########################################################################################
#                                S E C T I O N  IV
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
            "content": html.Div([dmc.Text("Posibles beneficiarios:"),
                                 dmc.Text("todos los productores de maíz poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal.", color="black"),
                                 ]),
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



# creación de una tabla
def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table