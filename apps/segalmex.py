from operator import index
from pickle import FALSE

#import dash
#from dash_extensions import Download
#from dash_extensions.enrich import DashProxy, html, Output, Input, dcc
#from dash_extensions.snippets import send_file
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from flask import Flask, render_template
import numpy as np
import pandas as pd
from millify import millify
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback_context, no_update
import dash_lazy_load
import time
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from dash_extensions import Download
#from dash_extensions.snippets import send_file
from dash_iconify import DashIconify
#from dash_extensions.enrich import Dash
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
import reglas_operacion as ro



def get_info(feature=None):
    # Valores por defecto a nivel nacional
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()

    if not feature:
        return [
            html.H4("{}".format("Nacional")),
            dmc.Center(html.Img(id='image', src='../assets/entidades/Nacional.png', width="65", height="65"))]
        # valores a nivel estatal
    return [
            html.H4("{}".format(feature["properties"]["name"])),
            #html.Br(),
            #html.B("Estado"), ": ",
            #html.A("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/entidades/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

def get_info2(feature=None):
    # Valores por defecto a nivel nacional
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()

    if not feature:
        return html.Center([
            dbc.Col(html.Img(src='../assets/entidades/Nacional.png', height="90px")),
            dbc.Col(dmc.Text('Nacional', id='nacional', align="center", weight=700), style={'fontSize':40}),
        ])
    #[
    #        dmc.Center(html.H4("{}".format("Nacional"))),
    #        dmc.Center(html.Img(id='image', src='../assets/Nacional.png', width="65", height="65"))]
    # valores a nivel estatal
    return html.Center([
            dbc.Col(html.Img(id='image', src='../assets/entidades/'+ str(feature["properties"]["name"]) +'.png', width="65", height="90")),
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
#estados_json = open(root + '/datasets/estadosMexico.json')
#mx_est_geo = json.load(estados_json)

json.load(open(root +'/datasets/sample.json'))
data2 = json.load(open(root +'/datasets/sample3.json'))

# bases Beneficiarios estado
base_entidad = pd.read_excel(root + '/datasets/base_entidad.xlsx')
base_entidad_tprod = pd.read_excel(root + '/datasets/base_entidad_tprod.xlsx')
# bases Beneficiarios Municipio
base_municipios = pd.read_excel(root + '/datasets/base_municipio2.xlsx')
base_municipios_tprod = pd.read_excel(root + '/datasets/base_municipio_tprod2.xlsx')
# base productores municipio
base_productores_maiz = pd.read_excel(root + '/datasets/baseTotalProductores_maiz2.xlsx')
# bases de centros de acopio a nivel entidad y municipal
centros_entidad = pd.read_excel(root + '/datasets/centros_entidad.xlsx')
centros_municipio = pd.read_excel(root + '/datasets/centros_municipio2.xlsx')

# sample maps P
# blue style
style = "https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png"
# grey style
style1 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
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
list_states = base_entidad['NOM_ENT'].unique()
list_layers = ['Centros de Acopio','Volumen Producción','Productores','All']
list_beneficiarios_opciones = ['Monto del Apoyo', 'Número de Beneficiarios']


list_capas_marginacion = initial_values = [
    [
        # capas
        #{"value": "Beneficiarios", "label": "Beneficiarios", "group": "Capa"},
        {"value": "Centros de Acopio", "label": "Centros de Acopio", "group": "Capa"},
        {"value": "Productores", "label": "Productores", "group": "Capa"},
        {"value": "Volumen Producción", "label": "Volumen Producción", "group": "Capa"},
        # Grado de marginación
    ],
    [
        {"value": "Beneficiarios", "label": "Beneficiarios", "group": "Capa"},
        {"value": "Muy Bajo", "label": "Muy Bajo", "group": "Nivel Marginación"},
        {"value": "Bajo", "label": "Bajo", "group": "Nivel Marginación"},
        {"value": "Medio", "label": "Medio", "group": "Nivel Marginación"},
        {"value": "Alto", "label": "Alto", "group": "Nivel Marginación"},
        {"value": "Muy Alto", "label": "Muy Alto", "group": "Nivel Marginación"},
    ],
]


list_criterios = ['Marginación', 'Precio']

#------------------------------------------------------------------------------
#                        layout
####################    header

# Filtros principales
main_filters = html.Div([
    #dbc.Row([
        dmc.Center([
            dbc.Row([
                dbc.Col([
                        #dmc.Tooltip(
                            dmc.Select(
                                icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                                label="Seleccione el año",
                                id="anio",
                                data=list_year,
                                value='2020',
                                searchable=True,
                                nothingFound="No options found",
                                 style={"textAlign": "left"}
                            ),
                        # label="Click actualizar año fiscal y producto",
                        # openDelay=500,
                        # ),

                    ], className="col-6 col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px',  'backgroundColor': '#F4F6F6', }),

                dbc.Col([

                        #html.Div([
                            dmc.Select(
                                icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                                label="Seleccione el producto",
                                id="producto",
                                data=list_products,
                                value='Frijol',
                                searchable=True,
                                nothingFound="No options found",
                                style={"textAlign": "left"},
                            ),
                        #]),

                ], className="col-6 col-md-6 border-0 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px',  'backgroundColor': '#F4F6F6', }),

            ], style={'marginBottom':'2rem'}),
         ]),
    # ], className="col-12 bg-transparent", style={'textColor':'white'}),
    dmc.Center(
    dbc.Row([

        dbc.Col([
            html.Div([
                dmc.Button(
                    'Actualizar',
                    id='submit-button',
                    n_clicks=0,
                    #children='Actualizar',
                    color = 'dark'),
                    #className="mb-4 mt-2"),
            ], className='col-12'),

        ], className="col-12 bg-transparent", style={'padding':'.3rem', 'border-radius': '0px', 'textAlign':'center'}),

        ]),
    ),
], className="twelve columns", style={'backgroundColor': '#F2F3F4', 'marginBottom':'3rem'})


####################      sidebar left: Barra de control
sidebar_right = html.Div([
        # Filtros
        #dbc.Row([
            html.Div([

                dmc.Card([

                    dmc.CardSection(
                        children=[
                            dmc.Center(
                                dmc.SimpleGrid(cols=3, children=[
                                    dmc.Text('2020', id='anio_filtro1', size="xl",weight=700, color="#4e203a", align="center"),
                                    dmc.Text(' - ', id='none', size="xl",weight=700, color="#4e203a", align="center"),
                                    dmc.Text('ARROZ', id='producto_filtro1', weight=700, size="xl", color="#4e203a", align="center")
                                ], style={'margin':'0rem', 'padding':'0rem'}),
                            ),
                        ],
                        inheritPadding=False,
                        #pb="md",
                        style={'marginTop':'0rem', 'marginBottom':'0rem'}
                    ),

                ],
                withBorder=True,
                style={'backgroundColor':'#F4F6F6'}),

                
                #dmc.Text("Beneficiarios"),
                # dmc.Text("Seleccione la característica que desee visualizar", size="sm", color="gray"),
                #dmc.ChipGroup(
                #    [dmc.Chip(k, value=k) for k in list_bneficiarios_opciones],
                #    id='beneficiarios-opciones',
                #    multiple=False,
                #    value='Número de Beneficiarios'
                #),
                # dmc.RadioGroup(
                #         [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
                #         id="beneficiarios-opciones",
                #         orientation="horizontal",
                #         #multiple=True,
                #         value="Número de Beneficiarios",
                #         #label="",
                #          mb=10,
                # ),

            ], className='mb-4 mt-2'),
            
            # capas y nivel de marginación
            # html.Div([
            #     dbc.Row([
            #         dbc.Col([
            #             dmc.Text("Seleccione la capa"),
            #             dmc.SegmentedControl(
            #             #dmc.ChipGroup(
            #             #    [dmc.Chip(k, value=k, variant='outline') for k in list_layers],
            #                 orientation="vertical",
            #                 fullWidth=True,
            #                 id='radio-centros',
            #                 data=list_layers,
            #                 color='#4E203A',
            #                 size='xs',
            #                 #multiple=False,
            #                 value='Centros de Acopio',
            #             ),
            #             #dmc.RadioGroup(
            #             #    [dmc.Radio(k, value=k) for k in list_layers],
            #             #    id="radio-centros",
            #             #    orientation="vertical",
            #             #    #multiple=True,
            #             #    value="Centros de acopio",
            #             #    #label="",
            #             #    size="sm",
            #             #    mt=5,
            #             #),
            #             #dmc.Text(id="radio-centros"),
            #         ], className='col-6 mb-2', style={'width': '50%'}),
            #         dbc.Col([
            #             #html.Div([
            #                 #dmc.Text("Nivel de Marginación"),
            #                 #dmc.MultiSelect(
            #                 #    id='grado_marginacion',
            #                 #    value= ['Muy bajo'],
            #                 #    data=list_grado_marginacion,
            #                     #color = '#4E203A',
            #                 #    clearable=True,
            #                 #    style={"width": 350}
            #                 #),
            #                 dmc.CheckboxGroup(
            #                     id="grado_marginacion",
            #                     label="Grado de marginación",
            #                     description="",
            #                     orientation="vertical",
            #                     #withAsterisk=True,
            #                     #offset="xs",
            #                     #gutter="xs",
            #                     #mb=0,
            #                     children=[
            #                         dmc.Checkbox(label="Muy bajo", value="Muy bajo", color="indigo"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Bajo", value="Bajo", color="blue"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Medio", value="Medio", color="green"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Alto", value="Alto", color="orange"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Muy alto", value="Muy alto", color="pink"),
            #                     ],
            #                     value=["Muy bajo", "Bajo","Medio","Alto","Muy alto"],
            #                 style={'height':'0rem', 'margin':'0rem', 'padding':'0rem'}),
            #                 #], className='mb-2'),
            #         ], className="col-6 mt-0", style={'marginBottom':'0rem', 'padding':'0rem'}),
            #     ]),

            # ], className='col-12'),
            # tabs para criterios y capas
            dmc.Tabs([
                dmc.TabsList([
                    dmc.Tooltip(
                        multiline=True,
                        width=200,
                        withArrow=True,
                        transition="fade",
                        position='right',
                        transitionDuration=300,
                        label="Use this button to save this information in your profile,"
                        " after that you will be able to access it any time and share"
                        " it via email.",
                        children=[
                            dmc.Tab("Capas",
                                icon=DashIconify(icon="ic:baseline-edit-location-alt"),
                                value="capas",
                                style={'color':'#4e203a'}
                            )],
                     ),
                    dmc.Tab("Criterios Simulados",
                        #id="tab-criterios",
                        icon=DashIconify(icon="ic:round-window"),
                        value="criterios",
                        style={'color':'#4e203a'}
                    ),
                    ]),
                ],
                id='capas-criterios',
                persistence= True,
                persistence_type = 'session',
                value="capas"),

            dmc.Card([
                    html.Div(
                        id="content-capas-criterios",
                        style={'marginTop':'1rem'}),
                ],
                withBorder=False,
                shadow=0,
                radius="md",
                style={"width": '100%',"padding":'0rem'},

                ),
            # card : criterios simulados
        #]),
        # tablero resumen
        # dmc.Card([
        #         #dmc.CardSection([
        #             dmc.SimpleGrid(cols=2,children=[
        #                 # card1 : centros de acopio
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # card2 : Beneficiarios
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Pob. Beneficiaria", id='resumen_texto_poblacion_beneficiaria', color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # Card 3 : Monto de apoyos
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # Card 4: Vol incentivado promedio
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/porcentaje.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "51%",
        #                             ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
        #             ],
        #             style={"width": 360, "height": 160}
        #             ),
        #         # ],
        #         # inheritPadding=False,
        #         # mt="sm",
        #         # pb="md",),

        # ], style={'marginLeft':'0rem', 'paddingLeft':'0rem'}),

        # dbc.Row([
        #     #primero
        #     dbc.Col([
        #         #html.Div([
        #         dbc.Row([
        #             dbc.Col([
        #                 html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
        #             ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
        #             dbc.Col([
        #                 dbc.Row([html.Center(html.Div([
        #                 "1,332",
        #                 ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
        #                 )]),
        #                 dbc.Row([html.Div([
        #                     dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
        #                     ]),
        #                 ]),
        #             ], className="card col-9 border-0 bg-transparent"),
        #         ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
        #     ],className=" card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),
        #     # segundo
        #     dbc.Col([
        #         dbc.Row([
        #             dbc.Col([
        #                 html.Img(id='image', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
        #             ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
        #             dbc.Col([
        #                 dbc.Row([html.Center(html.Div([
        #                 "1,332",
        #                 ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
        #                 )]),
        #                 dbc.Row([html.Div([
        #                     dmc.Text("Pob. Beneficiaria", color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                     ]),
        #                 ]),
        #             ], className="card col-9 border-0 bg-transparent"),
        #           ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
        #     ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),

        # ], style={'marginTop':'1rem'}),


        # Row three
    #     dbc.Row([
    #     #primero
    #         dbc.Col([
    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
    #                 ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
    #                 dbc.Col([
    #                     dbc.Row([html.Center(html.Div([
    #                     "1,332",
    #                     ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
    #                     )]),
    #                     dbc.Row([html.Div([
    #                         dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
    #                         ]),
    #                     ]),
    #                 ], className="card col-9 border-0 bg-transparent"),
    #             ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
    #         ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),
    #    # segundo
    #         dbc.Col([
    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Img(id='image', src='../assets/porcentaje.png', width="65", height="65"),
    #                 ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
    #                 dbc.Col([
    #                     dbc.Row([html.Center(html.Div([
    #                     "51%",
    #                     ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
    #                     )]),
    #                     dbc.Row([html.Div([
    #                         dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
    #                         ]),
    #                     ]),
    #                 ], className="card col-9 border-0 bg-transparent"),
    #             ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
    #         ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),

    #     ], style={'marginTop':'1rem', 'marginBottom':'1rem'}),

        ], style={'marginLeft':'2rem', 'marginRight':'2rem', 'marginTop':'0.5rem'}
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
            ], className="card col-12 col-md-8", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '10px', 'backgroundColor': '#BFC9CA', }
            ),
            dbc.Col([
                sidebar_right

            ], className="card col-12 col-md-4", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '0px', 'backgroundColor': 'white', }
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
#######################    content3 - gráficos por municipios

content2 = html.Div([
    dmc.Card(children=[
        dmc.CardSection(
            dmc.Group(
                children=[
                    dmc.Text("Review Pictures", weight=500),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                        color="gray",
                        variant="transparent",
                    ),
                ],
                position="apart",
            ),
            withBorder=True,
            inheritPadding=True,
            py="xs",
        ),
        dmc.Text(
            children=[
                dmc.Text(
                    "200+ images uploaded",
                    color="blue",
                    style={"display": "inline"},
                ),
                " since last visit, review them to select which one should be added to your gallery",
            ],
            mt="sm",
            color="dimmed",
            size="sm",
        ),
        dmc.CardSection(
            html.Iframe(id="plot-r1", style={"height": "400px", "width": "1300px"}),
        ),
        dmc.CardSection(children=[
                dmc.SimpleGrid(cols=2, children=[
                    #dbc.Group([
                        # plot 1
                        dmc.Group([
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        dmc.Text("Review Pictures", weight=500),
                                        dmc.ActionIcon(
                                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                                            color="gray",
                                            variant="transparent",
                                        ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=True,
                                py="xs",
                            ),
                            dmc.Text(
                                children=[
                                    dmc.Text(
                                        "200+ images uploaded",
                                        color="blue",
                                        style={"display": "inline"},
                                    ),
                                    " since last visit, review them to select which one should be added to your gallery",
                                ],
                                mt="sm",
                                color="dimmed",
                                size="sm",
                            ),
                            dmc.CardSection(
                                html.Iframe(id="plot-r2", style={"height": "400px", "width": "800px"}),
                            ),
                        ]),
                        # plot 2
                        dmc.Group([
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        dmc.Text("Review Pictures", weight=500),
                                        dmc.ActionIcon(
                                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                                            color="gray",
                                            variant="transparent",
                                        ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=True,
                                py="xs",
                            ),
                            dmc.Text(
                                children=[
                                    dmc.Text(
                                        "200+ images uploaded",
                                        color="blue",
                                        style={"display": "inline"},
                                    ),
                                    " since last visit, review them to select which one should be added to your gallery",
                                ],
                                mt="sm",
                                color="dimmed",
                                size="sm",
                            ),
                            dmc.CardSection(
                                html.Iframe(id="plot-r3", style={"height": "400px", "width": "800px"}),
                            ),
                        ]),
                        #plot3
                        # dmc.Group([
                        #     dmc.CardSection(
                        #         dmc.Group(
                        #             children=[
                        #                 dmc.Text("Review Pictures", weight=500),
                        #                 dmc.ActionIcon(
                        #                     DashIconify(icon="carbon:overflow-menu-horizontal"),
                        #                     color="gray",
                        #                     variant="transparent",
                        #                 ),
                        #             ],
                        #             position="apart",
                        #         ),
                        #         withBorder=True,
                        #         inheritPadding=True,
                        #         py="xs",
                        #     ),
                        #     dmc.Text(
                        #         children=[
                        #             dmc.Text(
                        #                 "200+ images uploaded",
                        #                 color="blue",
                        #                 style={"display": "inline"},
                        #             ),
                        #             " since last visit, review them to select which one should be added to your gallery",
                        #         ],
                        #         mt="sm",
                        #         color="dimmed",
                        #         size="sm",
                        #     ),
                        #     dmc.CardSection(
                        #         html.Iframe(id="plot-r4", style={"height": "400px", "width": "400px"}),
                        #     ),
                        # ]),

                    #], className='col-12'),
                    # html.Iframe(id="plot-r2", style={"height": "300px", "width": "400px"}),
                    # html.Iframe(id="plot-r3", style={"height": "300px", "width": "400px"}),
                    #html.Iframe(id="plot-r4", style={"height": "300px", "width": "400px"}),
                ]),
            ],
            withBorder=True,
            inheritPadding=True,
            mt="sm",
            pb="md",
        ),
        dmc.CardSection(
            dmc.Group(
                children=[
                    dmc.Text("Review Pictures", weight=500),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                        color="gray",
                        variant="transparent",
                    ),
                ],
                position="apart",
            ),
            withBorder=True,
            inheritPadding=True,
            py="xs",
        ),
        dmc.Text(
            children=[
                dmc.Text(
                    "200+ images uploaded",
                    color="blue",
                    style={"display": "inline"},
                ),
                " since last visit, review them to select which one should be added to your gallery",
            ],
            mt="sm",
            color="dimmed",
            size="sm",
        ),
        dmc.CardSection(
            html.Iframe(id="plot-r5", style={"height": "600px", "width": "1300px"}),
        ),



    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="col-12"),
],style={"paddin": '0rem', 'marginLeft':'2rem', 'marginRight':'2rem'})




# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([
        ###  SECCIÓN : BARRA PRINCIPAL
        html.Div([
            dbc.Row([
                dbc.Col([dbc.NavbarBrand("Programa de Precios de Garantía",
                             style={'color':'white', 'font-size': '60px', 'textAlign':'center'}),
                        html.Br(),
                        dbc.NavbarBrand("a Productos Alimentarios Básicos",
                             style={'color':'white', 'font-size': '60px', 'textAlign':'center'})],
                        className="ml-5",  style = {'textAlign':'center', 'color':'white', 'marginBottom':'3rem', 'marginTop':'6rem'} ),
                ],className="col-12"),
        ], style={'opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/maiz-mexico.jpg)','background-size': '1450px 650px','backgroundColor': '#2a3240', 'm':'0px', 'padding':'0px', 'height': '100%'}),

        # SECCIÓN : FILTROS GENERALES
        html.Div([
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    #dmc.Tooltip(
                        dbc.Button(
                            "Resumen Ejecutivo",
                            #href= "/Proyecto.pdf",
                            download="Proyecto.pdf",
                            external_link=False,
                            color="dark",
                            id="btn",
                        ),
                    #     label="Click para descargar el resumen",
                    #     openDelay=500,
                    # ),
                    dcc.Download(id="download"),
                ],  style = {'textAlign':'right', 'paddingRight':'2rem'}),
            ], className="mt-0", ),

            dbc.Row([
                dbc.Col(main_filters, style={'textAlign': 'center'})
            ], style={'paddingRight':'3rem','marginTop':'4rem', 'paddingLeft':'2rem','marginBottom':'4rem'}),

        ], style={'textAlign':'center','backgroundColor':'#F2F3F4','marginRight':'0rem', 'marginTop':'0rem', 'marginBottom':'2rem'}),

        #####  SECCIÓN : REGLAS DE OPERACIÓN
        html.Div([
            html.Div([
                    dmc.Button("Ver Reglas de Operación",
                               id="open",
                               leftIcon=DashIconify(icon="ant-design:read-outlined"),
                               color="dark",
                               n_clicks=0),
                    dbc.Modal([
                            dbc.ModalHeader(dbc.ModalTitle("Reglas de Operación: Trigo - 2020", style={'color':'#4e203a'}), style={'backgroundColor':'white'} ),
                            dbc.ModalBody(html.Div([
                                dmc.Center(ro.ro_2020_trigo)
                                ], style={'paddingLeft':'2.5rem', 'paddingRight':'2.5rem'})
                            , style={'backgroundColor':'#7c90ab'}),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Cerrar", id="close", className="ms-auto", outline=False, color="dark", n_clicks=0
                                ), style={'backgroundColor':'white'}
                            ),
                        ],
                        id="modal",
                        size='xl',
                        is_open=False,

                    ),
                ],
            ),

            ####### SECCION : PIE PLOT
            dmc.Card([
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text("Review Pictures", weight=500),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=True,
                    py="xs",
                ),
                dmc.Text(
                    children=[
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    html.Iframe(id='pie-plot1', srcDoc=open(root + "/graficos/piePlot_2020.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1200px"}),
                ),

            ],
            withBorder=True,
            style={'backgroundColor':'white', 'marginTop':'4rem', 'marginBottom':'2rem'}
            ),
        ], className="flip-card-front", style={'marginLeft':'2rem', 'marginRight':'2rem','backgroundColor':'white', 'm':'0px', 'padding':'0px'}),
        dbc.Row([html.H5(' ')]),

        #####  SECTION: MAPA
        content1,

        #####  SECCIÓN:  BARRA INDICADOR ESTADOS
        dmc.Card([
            dbc.Row([
            #dbc.Col("", style={'marginLeft':'8px'}),
            dbc.Col(get_info2(), id="info2", md=4),
            dbc.Col([dbc.Row(dmc.Text('Año', id='anio_fijo', align="center")), dbc.Row(dmc.Text('2020', id='anio_filtro', align="center", weight=700))], style={'fontSize':40, 'marginTop':'1.2rem'}),
            dbc.Col([dbc.Row(dmc.Text('Producto', id='producto_fijo', align="center")), dbc.Row(dmc.Text('Arroz', id='producto_filtro', align="center", weight=700))], style={'fontSize':40, 'marginTop':'1.2rem'}),
            ]),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={'marginLeft':'1rem','marginRight':'1rem','backgroundColor': '#F4F6F6'}
        ),

        dbc.Row(html.Hr(), style={'paddingLeft':'2rem', 'paddingRight':'2rem', 'marginBottom':'4rem'}),

        #### SECCIÓN : GRAFICOS
        content2,

        # final break
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]),

    ], className="twelve columns", style={'backgroundColor': 'white', 'marginTop': '0rem', 'padding':'0rem'},
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


#########      CARD 1 : Regresa estado  ################
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

#########      CALL : Regresa año  ################
@app.callback(# 'click_feature
        Output('anio_filtro1', 'children'),
        Output('anio_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def anio(clicks, sel_producto, sel_anio):


    return sel_anio, sel_anio

#########      CALL : Regresa producto  ################
@app.callback(# 'click_feature
        Output('producto_filtro1', 'children'),
        Output('producto_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def producto(clicks, sel_producto, sel_anio):

    return sel_producto, sel_producto

#########      CALL : Reglas de operación  ################
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#########      CALL : Pie Plot  ################
@app.callback(# 'click_feature
        Output('pie-plot1', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True
    )
def pie_plo1(clicks, sel_producto, sel_anio):
    #time.sleep(1)
    return open(root + f"./graficos/piePlot_{str(2020)}.html", 'r', encoding = 'utf-8').read()

# @app.callback(Output("loading-output-1", "children"),
#           Input("loading-input-1", "value"))
# def input_triggers_spinner(value):
#     time.sleep(2)
#     return value



#########    CALL : Indicador estado (MAPA)  ################
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



#########      CALL : Cuenta centros de acopio  ################
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

#########   CALL : Imagen Población beneficiaria / Monto Apoyo  ################
@app.callback(# 'click_feature
        Output('image-poblacion_beneficiaria', 'src'),
        Input('beneficiarios-opciones', 'value'),
    )
def resumen_benef_textImage(beneficiarios):

    # condición
    if beneficiarios == 'Número de Beneficiarios':
        #texto = "Pob. Beneficiaria"
        return '../assets/poblacionBeneficiaria.png'
    else:
        #texto = "Monto del Apoyo"
        return '../assets/dollar.svg'

#########   CALL : Regresa texto Población Benef / Monto del apoyo  ################
@app.callback(# 'click_feature
        Output('resumen_texto_poblacion_beneficiaria', 'children'),
        Input('beneficiarios-opciones', 'value'),
    )
def resumen_benef_textImag2(beneficiarios):

    # condición
    if beneficiarios == 'Número de Beneficiarios':
        texto = "Pob. Beneficiaria"
    else:
        texto = "Monto del Apoyo"

    return texto

#########  CALL : Regresa Cantidad Población Beneficiaria  ################
@app.callback(
        Output('resumen-poblacion_beneficiaria', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        Input('beneficiarios-opciones', 'value'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def resumen_pablacion_beneficiaria(clicks, feature, beneficiario, sel_producto, sel_anio):

    data = base_entidad.copy()
    data['MONTO_APOYO_TOTALsum'] = data['MONTO_APOYO_TOTALsum'].astype('float')
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]

    # Condición
    if beneficiario == 'Número de Beneficiarios':
        if not feature:
            result = np.sum(data['NUM_BENEFsize'])
        else:
            # filtro de estado
            data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
            # Sin dato nombre de dato faltante
            result = np.sum(data_filt['NUM_BENEFsize'])

        return "{:,}".format(result)
    else:
        if not feature:
            result = np.sum(data['MONTO_APOYO_TOTALsum'])
        else:
            # filtro de estado
            data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
            # Sin dato nombre de dato faltante
            result = np.sum(data_filt['MONTO_APOYO_TOTALsum'].astype('float'))

        return millify(result, precision=1)



#                      CARD 3 : Monto apoyos total
# @app.callback(
#         Output('resumen-monto_apoyos_total', 'children'),
#         Input('submit-button', 'n_clicks'),
#         Input("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )
# def resumen_monto_apoyos_total(clicks, feature, sel_producto, sel_anio):

#     data = base_entidad.copy()
#     # filtros
#     data = data[data['Anio'] == int(sel_anio)]
#     data = data[data['Producto'] == sel_producto]

#     # Condición
#     if not feature:
#         result = np.sum(data['MONTO_APOYO_TOTALsum'])
#     else:
#         # filtro de estado
#         data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
#         # Sin dato nombre de dato faltante
#         result = np.sum(data_filt['MONTO_APOYO_TOTALsum'])
#     # millify(monto_apoyos, precision=2)
#     return millify(result, precision=1)

#                      CARD 4 : Monto apoyos promedio
# @app.callback(
#         Output('resumen_monto_apoyos_prom', 'children'),
#         Input('submit-button', 'n_clicks'),
#         Input("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )
# def resumen_monto_apoyos_promedio(clicks, feature, sel_producto, sel_anio):

#     data = base_entidad.copy()
#     # filtros
#     data = data[data['Anio'] == int(sel_anio)]
#     data = data[data['Producto'] == sel_producto]

#     # Condición
#     if not feature:
#         result = np.mean(data['MONTO_APOYO_TOTALsum'])
#     else:
#         # filtro de estado
#         data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
#         # Sin dato nombre de dato faltante
#         result = np.mean(data_filt['MONTO_APOYO_TOTALmean'])

#     # millify(monto_apoyos, precision=2)
#     return millify(result, precision=1)

#########  CALL : Regresa Monto Volumne Incentivado  ################
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

#########  CALL : Regresa Monto Volumen Incentivado Promedio  ################
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
#########       CALL : Transfer list  ################

# opción Capas
tab1_capas_criterios = html.Div([
    dmc.Text("Seleccione la característica que desee visualizar", size="sm", color="gray"),
    dmc.RadioGroup(
            [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
            id="beneficiarios-opciones",
            orientation="horizontal",
            #multiple=True,
            value="Número de Beneficiarios",
            #label="",
            style={'marginBottom':'1rem'}
    ),
    dmc.Text("Seleccione la característica que desee visualizar", size="sm", color="gray", style={'marginBottom':'1rem'}),
    dmc.TransferList(
        id="transfer-list-simple",
        value=list_capas_marginacion,
        searchPlaceholder=['Agregar...', 'Remover...'],
        nothingFound=['Cannot find item to add', 'Cannot find item to remove'],
        placeholder=['No item left to add', 'No item left ro remove'],
        style={'fontSize':'10px','marginBottom':'1rem'}
    ),
    # Tablero resumen
    dmc.Card([
        #dmc.CardSection([
            dmc.SimpleGrid(cols=2,children=[
                # card1 : centros de acopio
                dmc.Card([
                    dbc.Row([
                        dbc.Col([
                            html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
                        ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
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
                    ], style={'border-radius': '5px', 'paddin':'0rem'}),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                # card2 : Beneficiarios
                dmc.Card([
                    dbc.Row([
                        dbc.Col([
                            html.Img(id='image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
                        ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
                        dbc.Col([
                            dbc.Row([html.Center(html.Div([
                            "1,332",
                            ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                            )]),
                            dbc.Row([html.Div([
                                dmc.Text("Pob. Beneficiaria", id='resumen_texto_poblacion_beneficiaria', color='grey', weight=500, align='center', style={"fontSize": 11}),
                                ]),
                            ]),
                        ], className="card col-9 border-0 bg-transparent"),
                    ], style={'border-radius': '5px', 'paddin':'0rem'}),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                # Card 3 : Monto de apoyos
                dmc.Card([
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
                    ], style={'border-radius': '5px', 'paddin':'0rem'}),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                # Card 4: Vol incentivado promedio
                dmc.Card([
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
                    ], style={'border-radius': '5px', 'paddin':'0rem'}),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
            ],style={"width": 360, "height": 160}
        ),
    ], style={'marginLeft':'0rem', 'paddingLeft':'0rem'}),

])

#  Pestaña de opciones (Transfer list - Criterios simulados)
tab2_capas_criterios = html.Div([
    dmc.Card([
        dmc.SimpleGrid(cols=2, children=[
            dmc.Select(
                label='Criterios simulados',
                id='criterios1',
                searchable=True,
                dropdownPosition='bottom',
                value= ['Criterio de Marginación'],
                data=list_criterios,
                nothingFound="No options found",
                style={"width": '100%'}
            ),

            dmc.Select(
                label='Otro selector',
                id='criterios2',
                value= ['Criterio de Marginación'],
                data=list_criterios,
                nothingFound="No options found",
                style={"width": '100%'}
            ),
        ], style={'marginBottom':'4rem'}),
        
        dmc.Center([
            dmc.Button(
            "Ver Metodología",
            id='btn_metodo_pdf',
            variant="subtle",
            rightIcon=DashIconify(icon="ic:baseline-download"),
            color="blue",
            ),
            dcc.Download(id="download"),

        ]),
        
    ], style={'padding':'0rem', 'marginBottom':'4rem'}),
    
    
])
        



######### CALL : Regresa PDF de sección criterios simulados  ################
@app.callback(Output("download", "data"),
              [Input("btn_metodo_pdf", "n_clicks")],
              prevent_initial_call=True)
def func(n_clicks):
    return dcc.send_file("C:/Users/jcmartinez/Desktop/Dashboard3/Proyecto.pdf")

#########  CALL : Regresa opciones capas / criterios  ################
@app.callback(Output("content-capas-criterios", "children"),
             [Input("capas-criterios", "value")],
             PreventUpdate=False)
def switch_tab(active):
    if active == "capas":
        return tab1_capas_criterios
    elif active == "criterios":
        return tab2_capas_criterios

    return html.P("This shouldn't ever be displayed...")


#########  CALL : Regresa actualización del MAPA  ################
# declaración de parámetros para color y leyendas
classes = [0, 1000,3000,5000,10000, 100000, 1000000, 3000000]
colorscale = ['#fef9e7','#D5F5E3', '#ABEBC6', '#82E0AA', '#58D68D', '#2ECC71', '#239B56', '#1D8348'] # '#0B5345'
#
# fillOpacity : transparencia de color de relleno
style = dict(weight=1, opacity=0.9, color='#2e4053', dashArray='1', fillOpacity=0.9)
# estilo centros de acopio
#  color: color de fondo
style2 = dict(weight=1, opacity=0.9 ,color='#2e4053', dashArray='1', fillOpacity=0.01)
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

#info2 = html.Div(children=get_info2(), id="info2", className="info2",
#                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})


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

##   CALLBACK : MAPA
@app.callback(
        Output('mapa2', 'children'),
        Input('submit-button', 'n_clicks'),
        #Input('t_productor', 'value'),
        #Input('grado_marginacion', 'value'),
        Input("beneficiarios-opciones", "value"),
        #Input("radio-centros", "value"),
        Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
    )

# def actualizar_mapa2(clicks, margin_sel, benef_sel,capas_sel, transfer_sel, producto_sel, anio_sel):
def actualizar_mapa2(clicks, benef_sel, transfer_sel, producto_sel, anio_sel):


    # capas
    capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
    margin = [item['label'] for item in transfer_sel[1] if item['group']=='Nivel Marginación']

    # if isinstance(capas_sel, str):
    #     capas = [capas_sel]
    # else:
    #     capas = capas_sel
    # nivel de marginación
    # if isinstance(margin_sel, str):
    #     margin = [margin_sel]
    # else:
    #     margin = margin_sel

    productores_maiz = base_productores_maiz.copy()
    centros = centros_municipio.copy()
    centros = centros_municipio[centros_municipio['GM_2020'].isin(margin)].dropna(axis=0)
    benef_filter = base_municipios[base_municipios['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['GMMmode'].isin(margin)].dropna(axis=0)


    # # opción de beneficiarios
    # if benef_sel=='Número de Beneficiarios':
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
    # else:
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])


    # # opción centros de acopio y de producción
    # if capas_sel == ['Beneficiarios']:
    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                          options=dict(style=style_handle),  # how to style each polygon
    #                          zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                          zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                          # color : color del perimetro del hover
    #                          # dashArray : tipo de linea
    #                          hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                          hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                          id='states'),
    #             benef_option,
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])

    # elif capas_sel == ['Centros de Acopio']:
    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         # color : color del perimetro del hover
    #                         # dashArray : tipo de linea
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                         id='states'),
    #             #benef_option,
    #             dl.Pane([dl.Circle(center=[lat, lon], radius=2, color='red', children=[
    #                             dl.Popup("Municipio: {}".format(mun))
    #                             ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # elif capas_sel == ['Productores']:

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         # color : color del perimetro del hover
    #                         # dashArray : tipo de linea
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                         id='states'),
    #             #benef_option,
    #             dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), color='black', children=[
    #                             dl.Popup("Municipio: {}".format(mun))
    #                             ]) for lat, lon, mun, radio in zip(productores_maiz['LAT_DECIMAL'],productores_maiz['LON_DECIMAL'], productores_maiz['NOM_MUN'], productores_maiz['TotalProductores'])]),
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # elif capas_sel == ['Volumen Producción']:
    #     # Si el producto es del año 2019 y Leche, grafica fondo blanco
    #     #   en caso contrario fondo en verde degradado.
    #     #   Valor de cero para anio-producto dibuja fondo declarado en hoverStyle

    #     # opciones para anio:2019 y producto Leche, ya que no existen datos
    #     if int(anio_sel) == 2019 and producto_sel == 'Leche':
    #         colorprop = 1
    #         estilo = style2
    #     else:
    #         colorprop = f'{anio_sel}-{producto_sel}'
    #         estilo = style

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
    #                         id='states'),
    #             #benef_option,           #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # else:
    #     # opciones para anio:2019 y producto Leche, ya que no existen datos
    #     if int(anio_sel) == 2019 and producto_sel == 'Leche':
    #         colorprop = 1
    #         estilo = style2
    #     else:
    #         colorprop = f'{anio_sel}-{producto_sel}'
    #         estilo = style2

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop),
    #                         id='states'),
    #             # benef_option,
    #             # dl.Pane([dl.Circle(center=[lat, lon], radius=6, color='red', children=[
    #             #                 dl.Popup("Municipio: {}".format(mun))
    #             #                 ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),
    #             # #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])

    # Base
    base = dl.GeoJSON(data=data2,  # url to geojson file  #283747
                    options=dict(style=style_handle),  # how to style each polygon
                    zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                    zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                    # color : color del perimetro del hover
                    # dashArray : tipo de linea 
                    # #154360
                    hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
                    hoverStyle=arrow_function(dict(weight=4, fillColor='#4e203a', color='#4e203a',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
                    id='states')

    # opción de beneficiarios
    def benef_choice(benef_sel):
        if benef_sel=='Número de Beneficiarios':
            benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio),fillOpacity=1,fillColor=color, color=color, children=[
                dl.Popup("Municipio: {}".format(mun))
                ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
        else:
            benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio), color=color, children=[
                dl.Popup("Municipio: {}".format(mun))
                ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])

        return benef_option

    # capa de beneficiarios
    beneficiarios = benef_choice(benef_sel)

    # Centro de acopio
    centros = dl.Pane([dl.Circle(center=[lat, lon], radius=2, color='red', children=[
                                    dl.Popup("Municipio: {}".format(mun))
                                    ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])])

    # Productores
    productores = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), color='black', children=[
        dl.Popup("Municipio: {}".format(mun))
        ]) for lat, lon, mun, radio in zip(productores_maiz['LAT_DECIMAL'],productores_maiz['LON_DECIMAL'], productores_maiz['NOM_MUN'], productores_maiz['TotalProductores'])])

    # volumen producción
    def volumenProduccion_choice(producto, anio):
        anio_sel = anio
        producto_sel = producto
        # condition for year
        if int(anio_sel) == 2019 and producto_sel == 'Leche':
            colorprop = 1
            estilo = style2
        else:
            colorprop = f'{anio_sel}-{producto_sel}'
            estilo = style
        # layer
        volumen_produccion = dl.GeoJSON(data=data2,  # url to geojson file
                                    options=dict(style=style_handle),  # how to style each polygon
                                    zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                                    zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                                    hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop), #2e4053
                                    hoverStyle=arrow_function(dict(weight=4, fillColor='#4e203a', color='#4e203a',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
                                    id='states')

        return volumen_produccion

    volumen_produccion = volumenProduccion_choice(producto_sel, anio_sel)

    # diccionarios de capas
    layers = {
        #'Base': base,
        'Beneficiarios': beneficiarios,
        'Productores': productores,
        'Centros de Acopio': centros,
        'Volumen Producción': volumen_produccion
    }

    # class MAP
    class Map():
        # constructor
        def __init__(self, background_style):
            self.base_layer = [dl.TileLayer(url=background_style),
                                colorbar,
                                info,
                                base]
        # function
        def add(self, features):
            # add layers
            for feature in features:
                self.base_layer.append(layers[feature])

            return self.base_layer
    # background style del mapa
    children_layer = Map(background_style=style1).add(capas_sel)

    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5, children=children_layer
           ,style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
        #html.Div(id="state"), html.Div(id="info2")
    ])

    return tab2_mapa_content
############################################################################################
# SECTION II :
############################################################################################

# Tabs actualization
# tab1_r2c1_content = html.Div([
#     html.Iframe(srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
# ])

# tab2_r2c1_content = html.Div([
#     dcc.Graph(id="plot2-r2c1")
#     #dcc.Graph(id="tabla-r2c1")
# ])
# @app.callback(Output("content-r2c1", "children"),
#               [Input("tabs-r2c1", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c1-1":
#         return tab1_r2c1_content
#     elif at == "tab-r2c1-2":
#         return tab2_r2c1_content
#     return html.P("This shouldn't ever be displayed...")

# #----------------------------------------------------------------------------------
# #                     Actializa Gráfico 1:
# #----------------------------------------------------------------------------------
# @app.callback(
#         Output('plot1-r2c1', 'figure'),
#         Input('submit-button', 'n_clicks'),
#         #Input('estados', 'value'),
#         Input('anio', 'value')
#     )

# def actualizar_plot1_r2c1(clicks, anio_sel):


#     return

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 2:
#----------------------------------------------------------------------------------

# tab1_r2c2_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         html.Iframe(id='plot1-r2c2', srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
#     ]),

# tab2_r2c2_content = html.Div([
#     dt.DataTable(id="plot2-r2c2")
# ])

# #  Actualiza tabs - mapa
# @app.callback(Output("content-r2c2", "children"),
#               [Input("tabs-r2c2", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c2-1":
#         return tab1_r2c2_content
#     elif at == "tab-r2c2-2":
#         return tab2_r2c2_content
#     return html.P("This shouldn't ever be displayed...")

#########  CALL : Actualiza gráfico cantidad/Monto productores  ################
@app.callback(
        Output('plot-r3c1', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r3c1(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]

    if feature == None:
        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 3:
#----------------------------------------------------------------------------------

# tab1_r2c2_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         html.Iframe(id='plot1-r2c2', srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
#     ]),

# tab2_r2c2_content = html.Div([
#     dt.DataTable(id="plot2-r2c2")
# ])

# #  Actualiza tabs - mapa
# @app.callback(Output("content-r2c2", "children"),
#               [Input("tabs-r2c2", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c2-1":
#         return tab1_r2c2_content
#     elif at == "tab-r2c2-2":
#         return tab2_r2c2_content
#     return html.P("This shouldn't ever be displayed...")

# --------------------------------------------
@app.callback(
        Output('plot-r3c2', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r3c2(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


    if feature == None:
        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()



#########################################################################################
#  SECTION III - grafico Barras por municipio
##########################################################################################
# tab1_r3c1_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         dcc.Graph(id="plot1-r3c1")
#     ]),

# tab2_r3c1_content = html.Div([
#      #dcc.Graph(id="plot2-r3c1")
#      html.Iframe(id='plot2-r3c1', srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1300px"})
# ], style={'height':'60vh'})



#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row3-col1 Grafico qqplot
#--------------------------------------------------------------------------------------
@app.callback(
        Output('plot-r1', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r1(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


    if feature == None:
        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


@app.callback(
        Output('plot-r2', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r2(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


    if feature == None:
        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


@app.callback(
        Output('plot-r3', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r3(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


    if feature == None:
        return open(root + f"/graficos/sunburstPlot2.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/sunburstPlot2.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


@app.callback(
        Output('plot-r4', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r4(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


    if feature == None:
        return open(root + f"/graficos/sunburstPlot3.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/sunburstPlot3.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})

@app.callback(
        Output('plot-r5', 'srcDoc'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r5(clicks, feature, producto_sel, anio_sel):
    # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
    # dist_plot = base[base['Anio'] == int(anio_sel)]
    # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]

    if feature == None:
        return open(root + f"/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
    else:
        entidad = feature["properties"]["name"]

        return open(root + f"/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read()
        #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})





