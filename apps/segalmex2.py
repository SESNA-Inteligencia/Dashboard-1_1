from operator import index
from pickle import FALSE

import dash          
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
#import dash_leaflet as dl
from sqlalchemy import create_engine
from app import app
import requests
import random
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from costumFunctions import make_dataframe_state_mun
import sys
import pymysql

# CONFIG BASE DATOS AMERICANO
hostname="localhost"
dbname=["nombre bases separadas por comas"]
uname="root"
pwd="myadmin"

# --- Only run on the server
#engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname[0], user=uname, pw=pwd))
#base = pd.read_sql(sql="select * from close_price where Date > '2020-01-01'", con = engine, index_col="Date", parse_dates=True)

# urls
repo_est_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json' 
repo_mun_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/MunicipiosMexico.json'

# read 
mx_est_geo = requests.get(repo_est_url).json()
mx_mun_geo = requests.get(repo_mun_url).json()


# base beneficiarios
df_benef= pd.read_excel('C:/Users/jcmartinez/Desktop/Dashboard/datasets/base_beneficiarios_dashboard.xlsx')
# base centros de acopio
df_centros = pd.read_excel('C:/Users/jcmartinez/Desktop/Dashboard/datasets/base_centros_inegi.xlsx')
df_centros = df_centros.dropna()
# base producción agrícola
df_produccion = pd.read_excel('C:/Users/jcmartinez/Desktop/Dashboard/datasets/base_prodAgricola_con_claves_inegi.xlsx')
df_produccion = df_produccion.dropna()

# georeferenciación de base producción - estados
df_prod_est = pd.read_csv('C:/Users/jcmartinez/Desktop/Dashboard/datasets/produccion_estados.csv')

# opciones 
list_year = [2019, 2020, 2021]
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']
list_grado_marginacion = ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto']
list_tamano_productor = ['Pequeño', 'Mediano']

'''
all_options = {
    'Americano': df_benef[df_benef['Anio'] == 'Americano']['simbolo'].unique(),
    'Europeo': base[base['mercado'] == 'Europeo']['simbolo'].unique(),
    'Mexicano': base[base['mercado'] == 'Mexicano']['simbolo'].unique()
}
'''

#------------------------------------------------------------------------------
#                        layout
####################      sidebar left: control bar
sidebar_1eft = html.Div([
    # filtro año
        dbc.Row([
                html.H6('Año', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'3rem'})
                ],
            style={ 'marginBottom':'0.2rem'},
            ),
        dbc.Row([
            html.Div([
                dcc.Dropdown(id='anio', options=[
                    {'label': i, 'value': i} for i in list_year], value=list_year[0], multi=False, 
                             ),
                dbc.Popover(
                    dbc.PopoverBody("Selecciona el año "),
                    target="anio",
                    trigger="focus",
                    placement="top",
                    className="text-center"
                ),
            ], style={"color": "grey", "width": "80%", 'marginLeft':'1.5rem', 'marginTop':'0.1rem', 'marginRight':'1.5rem'}),
            
            ], className="mt-0"),
        # filtro producto
        dbc.Row([
                html.H6('Producto', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'2rem'})
                ],
            style={'marginBottom':'0.2rem'},
            ),
        dbc.Row([
            html.Div([
                dcc.Dropdown(id='producto', options=[
                    {'label': i, 'value': i} for i in list_products], value=list_products[0], multi=False, 
                             ),
                dbc.Popover(
                    dbc.PopoverBody("Selecciona el producto "),
                    target="producto",
                    trigger="focus",
                    placement="top",
                    className="text-center"
                ),
            ], style={"color": "grey", "width": "80%", 'marginLeft':'1.5rem', 'marginTop':'0.1rem', 'marginRight':'1.5rem'}),
            

            ], className="mt-0"),
        
        # filtro Grado de marginacion
        dbc.Row([
                html.H6('Grado de marginación', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'2rem'})
                ],
            style={'marginBottom':'0.2rem'},
            ),
        dbc.Row([
            html.Div([
                dcc.Dropdown(id='grado_marginacion', options=[
                    {'label': i, 'value': i} for i in list_grado_marginacion], value=list_grado_marginacion[0], multi=False, 
                             ),
                dbc.Popover(
                    dbc.PopoverBody("Selecciona el grado de marginación"),
                    target="grado_marginacion",
                    trigger="focus",
                    placement="top",
                    className="text-center"
                ),
            ], style={"color": "grey", "width": "80%", 'marginLeft':'1.5rem', 'marginTop':'0.1rem', 'marginRight':'1.5rem'}),
            

            ], className="mt-0"),
        
        # filtro Tamaño del productor
        dbc.Row([
                html.H6('Tamaño del productor', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'2rem'})
                ],
            style={'marginBottom':'0.2rem'},
            ),
        dbc.Row([
            html.Div([
                dcc.Dropdown(id='t_productor', options=[
                    {'label': i, 'value': i} for i in list_tamano_productor], value=list_tamano_productor[0], multi=False, 
                             ),
                dbc.Popover(
                    dbc.PopoverBody("Selecciona el tamaño del productor"),
                    target="t_productor",
                    trigger="focus",
                    placement="top",
                    className="text-center"
                ),
            ], style={"color": "grey", "width": "80%", 'marginLeft':'1.5rem', 'marginTop':'0.1rem', 'marginRight':'1.5rem'}),
            

            ], className="mt-0"),
        
    
        dbc.Row([
            html.Div([
            
                dbc.Button(id='submit-button',
                    n_clicks=0,
                    children='Actualizar',
                    color = 'dark',    
                    className="mb-5 mt-5"),
            ], style={"width": "80%", "color":"grey", "align":"center", 'marginLeft':'1.5rem', 'marginRight':'1.5rem'}
            ),
            
        ]),
        
        
        ], className='col-10 col-md-12', style={'backgroundColor': '#EAEDED', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'marginLeft': '2rem', 'marginBottom': '2rem', 'marginRight':'1rem', 'marginTop': '0rem'}
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
                ], className="card col-12", style={'height':'84vh', 'padding':'.3rem', 'marginTop':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
        ]),
        
        
    ], className="seven columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '1rem','marginRight': '2rem','marginTop': '0rem'}

    )

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


#######################    content2 - gráficos
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
                ], className="card col-12 col-md-6", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
            dbc.Col([
                    html.Div([
                        dbc.Tabs([
                                dbc.Tab(label="Gráfico 4", tab_id="tab-r3c2-1", label_style={"color": "#00AEF9"}),
                                
                                dbc.Tab(label="Tabla 4", tab_id="tab-r3c2-2",  label_style={"color": "#00AEF9"}),
                            ],
                            id="tabs-r3c2",
                            active_tab="tab-r3c2-1",
                        ),
                        html.Div(id="content-r3c2"),
                     ], style={"width": "100%"}
                    ),                 
                ], className="card col-12 col-md-6 ", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
            
        ]),
         
        
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem'}

    )


# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([
         
        #dbc.Row([
        #    dbc.Col([
        #    html.Br(),
        #    html.H1('SEGALMEX', id='titulo', className="text-center", style={'color':'blue'}),
        #    html.Br(),
        #    ]
        #    )
        #], className='m-5 mt-0'),
        
        #html.A(
            
        dbc.Row([
            dbc.Col([
                html.Br()
            ]),
        ]),    
            
        dbc.Row([
            dbc.Col(html.Img(src="assets/segalmex3.jpg", height="60px"), style = {'textAlign':'right', 'marginRight':'10px'} ),
            dbc.Col(html.H1("SEGALMEX"),  className="ml-5",  style = {'textAlign':'left', 'color':'blue'} ),
            ],
            align="center",
            className="g-0 m-0",
        ),
        
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]), 
        
        
        dbc.Row([html.H5(' ')]),
        # first row: filtros y mapa
        dbc.Row([
                dbc.Col(sidebar_1eft, className="col-12 col-md-3"),
                dbc.Col(content1, className="col-12 col-md-9", style={'backgroundColor': '#F4F6F6', 'margin': '0rem'}),
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
        
    ], style={'backgroundColor': '#F4F6F6', 'margin': '0rem'},
    fluid=True
    )


############################            Call backs         ##############################
# tabs - mapa
# grafica mapa
tab1_mapa_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="mapa")
    ]),

tab2_mapa_content = html.Div([
    dcc.Graph(id="tabla-mapa")
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
        State('producto', 'value'),
        State('anio', 'value')
    )
def actualizar_mapa(clicks, producto_sel, anio_sel):
    
    
    benef_filter = df_benef[df_benef['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == anio_sel]
    
    
    est_color = df_prod_est[df_prod_est['Anio']==anio_sel]
    est_color = est_color [est_color ['Producto']==producto_sel]
    #if isinstance(ticker_sel, str):
    #    stks = [ticker_sel]
    #else:
    #    stks = ticker_sel
    
    # MAPA
    fig = go.Figure()

    # Traza areas de producción
    fig.add_trace(go.Choroplethmapbox(name='Mexico', geojson=mx_est_geo, ids=est_color['Entidad'], z=est_color['Volumenproduccion'],
                                    locations=est_color['Entidad'], featureidkey='properties.name', colorscale='greens',
                                    marker=dict(line=dict(color='black'), opacity=0.6)))
    
    # centros de acopio aparecen para el caso del maíz y frijol
    if producto_sel == 'Frijol' or producto_sel == 'Maíz':
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
            lat=benef_filter['Lat'],
            lon=benef_filter['Lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=6,
                color='blue'
            ),
            text=benef_filter['Valor'],
        ))
    
    fig.add_trace(go.Densitymapbox(
            lat=benef_filter['Lat'], 
            lon=benef_filter['Lon'], 
            z=benef_filter['Valor'], 
            radius=30))
    
    
    fig.update_layout(mapbox_style= "open-street-map", #'open-street-map',
                    mapbox_zoom=4, 
                    mapbox_center = {'lat': 25, 'lon': -99}
                    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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
    
    benef_filter = df_benef[df_benef['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == anio_sel]

    est_color = df_prod_est[df_prod_est['Anio']==anio_sel]
    est_color = est_color [est_color ['Producto']==producto_sel]
    
    # MAPA
    fig = go.Figure()

    # Traza areas de producción
    fig.add_trace(go.Choroplethmapbox(name='Mexico', geojson=mx_est_geo, ids=est_color['Entidad'], z=est_color['Volumenproduccion'],
                                    locations=est_color['Entidad'], featureidkey='properties.name', colorscale='greens',
                                    marker=dict(line=dict(color='black'), opacity=0.1)))

    # Traza de centros de acopio
    fig.add_trace(go.Scattermapbox(
            lat=df_centros['LAT_DECIMAL'],
            lon=df_centros['LON_DECIMAL'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                color='red'
            ),
            text='Centro de acopio: ' + df_centros['NOM_MUN'],
        ))
    # Traza de beneficiarios 
    fig.add_trace(go.Scattermapbox(
            lat=benef_filter['Lat'],
            lon=benef_filter['Lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=15,
                color='blue'
            ),
            text='Beneficio Total: ' + benef_filter['Valor'],
        ))
    

    fig.update_layout(mapbox_style='open-street-map',
                    mapbox_zoom=4, 
                    mapbox_center = {'lat': 25, 'lon': -99}
                    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


###############        tabs - grafico r2
tab1_r2c1_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r2c1")
    ]),

tab2_r2c1_content = html.Div([
    dcc.Graph(id="tabla-r2c1")
])

@app.callback(Output("content-r2c1", "children"), [Input("tabs-r2c1", "active_tab")])
def switch_tab(at):
    if at == "tab-r2c1-1":
        return tab1_r2c1_content
    elif at == "tab-r2c1-2":
        return tab2_r2c1_content
    return html.P("This shouldn't ever be displayed...")

@app.callback(
        Output('plot-r2c1', 'figure'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r2c1(clicks, producto_sel, anio_sel):
    
    # Map 
    df_benef_state = df_benef[['Estado', 'Valor']].groupby('Estado').sum().sort_values('Valor', ascending=False)
    df_benef_state_mean = df_benef_state.mean()
    df_benef_state_mean.Valor


    fig = go.Figure()
    # 
    fig.add_trace(go.Bar(
        x=df_benef_state.index.to_list(),
        y=df_benef_state.Valor.to_list()))

    fig.add_hline(y=df_benef_state_mean.Valor, line_dash="dot", row=3, col="all",
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
            #paper_bgcolor="White",
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


###   Gráfico row2 - col2
tab1_r2c2_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r2c2")
    ]),

tab2_r2c2_content = html.Div([
    dcc.Graph(id="tabla-r2c2")
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
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r2c2(clicks, producto_sel, anio_sel):
    
    # Map 
    df_benef_state = df_benef[['Estado', 'Valor']].groupby('Estado').sum().sort_values('Valor', ascending=False)
    df_benef_state_mean = df_benef_state.mean()
    df_benef_state_mean.Valor


    fig = go.Figure()
    # frontera eficiente
    fig.add_trace(go.Bar(
        x=df_benef_state.index.to_list(),
        y=df_benef_state.Valor.to_list()))

    fig.add_hline(y=df_benef_state_mean.Valor, line_dash="dot", row=3, col="all",
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
            #paper_bgcolor="White",
            )

    fig.update_traces(marker_color='red', marker_line_color='red',
                marker_line_width=1.5, opacity=0.6)
    
    fig.update_layout(
        title="Monto Apoyo Total",
        xaxis_title="Monto Apoyo Total",
        yaxis_title="Monto Apoyo Total",
        legend_title="",
        font=dict(
            #   family="Courier New, monospace",
            size=8,
            color="Red"
            ))

    fig.update_xaxes(tickangle=80)

    return fig


###############       tabs - grafico r3
tab1_r3c1_content = html.Div([
        #dcc.Graph(id="mapa", mathjax=True)
        dcc.Graph(id="plot-r3c1")
    ]),

tab2_r3c1_content = html.Div([
    dcc.Graph(id="tabla-r3c1")
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
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )

def actualizar_plot_r3c1(clicks, producto_sel, anio_sel):
    
    # Map 
    df_benef_state = df_benef[['Estado', 'Valor']].groupby('Estado').sum().sort_values('Valor', ascending=False)
    df_benef_state_mean = df_benef_state.mean()
    df_benef_state_mean.Valor


    fig = go.Figure()
    # frontera eficiente
    fig.add_trace(go.Bar(
        x=df_benef_state.index.to_list(),
        y=df_benef_state.Valor.to_list()))

    fig.add_hline(y=df_benef_state_mean.Valor, line_dash="dot", row=3, col="all",
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
            #paper_bgcolor="White",
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
    df_benef_state = df_benef[['Estado', 'Valor']].groupby('Estado').sum().sort_values('Valor', ascending=False)
    df_benef_state_mean = df_benef_state.mean()
    df_benef_state_mean.Valor


    fig = go.Figure()
    # frontera eficiente
    fig.add_trace(go.Bar(
        x=df_benef_state.index.to_list(),
        y=df_benef_state.Valor.to_list()))

    fig.add_hline(y=df_benef_state_mean.Valor, line_dash="dot", row=3, col="all",
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
            #paper_bgcolor="White",
            )

    fig.update_traces(marker_color='green', marker_line_color='green',
                  marker_line_width=1.5, opacity=0.6)
    
    
    fig.update_layout(
        title="Monto Apoyo Total",
        xaxis_title="Monto Apoyo Total",
        yaxis_title="Monto Apoyo Total",
        legend_title="",
        font=dict(
            #   family="Courier New, monospace",
            size=8,
            color="Green"
            ))

    fig.update_xaxes(tickangle=80)

    return fig
