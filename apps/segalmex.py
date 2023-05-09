from operator import index
from pickle import FALSE

import dash          
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#import dash_leaflet as dl
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
df_centros = df_centros.dropna()
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
                #dcc.Dropdown(id='anio', options=[
                #    {'label': i, 'value': i} for i in list_year], value=list_year[0], multi=False, 
                #             ),
                #dmc.RadioGroup(
                #    [dmc.Radio(x, value=x) for x in list_year],
                #    id="anio",
                #    value='2020',
                #),
                #dcc.RadioItems(
                #    id='anio',
                #    options=[{'label': i, 'value': i} for i in list_year],
                #    value=2020,
                #    labelStyle={'display': 'inline-block', "font-size": "20px"},
                #),
                
                #html.Div([
                dmc.ChipGroup(
                    [dmc.Chip(k, value=k) for k in list_year],
                    id='anio',
                    value='2020',
                ),
                #]),
                
                #dbc.Popover(
                #    dbc.PopoverBody("Selecciona el año "),
                #    target="anio",
                #    trigger="focus",
                #    placement="top",
                #    className="text-center"
                #),
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
                #dcc.Dropdown(id='producto', options=[
                #    {'label': i, 'value': i} for i in list_products], value=list_products[0], multi=False, 
                #             ),
                
                dmc.Select(
                    id="producto",
                    data=list_products,
                    value='Frijol',
                    searchable=True,
                    nothingFound="No options found",
                    style={"width": 250},
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
                #dcc.Dropdown(id='grado_marginacion',  options=[
                #    {'label': i, 'value': i} for i in list_grado_marginacion], value=list_grado_marginacion[0], multi=True, searchable=True,
                #             ),
                dmc.MultiSelect(
                    id='grado_marginacion', 
                    value= ['Muy bajo','Bajo','Medio','Alto','Muy alto'],
                    data=list_grado_marginacion,
                    clearable=True,
                    style={"width": 250}  
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
                #dcc.Dropdown(id='t_productor', options=[
                #    {'label': i, 'value': i} for i in list_tamano_productor], value=list_tamano_productor[0], multi=True, searchable=True,
                #             ),
                dmc.MultiSelect(
                    id='t_productor', 
                    data=list_tamano_productor,
                    value= ["Pequeño","Mediano","Grande"],
                    clearable=True,
                    style={"width": 250}  
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
                ], className="card col-12", style={'height':'84vh', 'padding':'.3rem', 'marginTop':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', } # white
                ), 
            
        ]),
        
        
    ], className="seven columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '1rem','marginRight': '2rem','marginTop': '0rem'}

    )
# backgroundColor': '#F4F6F6'
#######################    content2 - gráficos
content2 = html.Div([

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6('Estado', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'1rem'})
                    ],
                    style={'marginBottom':'0.2rem'},
                ),
                html.Div([

                    dmc.MultiSelect(
                        id='estados', 
                        data=list_states,
                        value= ["Aguascalientes"],
                        clearable=True,
                        #style={"width": 600}  
                    ),       

                ]),
    
                
                ], className="card col-12 col-md-6", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
            ),
            
            dbc.Col([
                html.Div([
                    html.H6('Municipio', style={'color':'#2C3E50', 'marginLeft':'1.5rem', 'marginRight':'1.5rem', 'marginTop':'1rem'})
                    ],
                    style={'marginBottom':'0.2rem'},
                ),
                html.Div([

                    dmc.MultiSelect(
                        id='municipios', 
                        data=list_states,
                        value= ["Aguascalientes"],
                        clearable=True,
                        #style={"width": 600}  
                    ),       

                ]),
    
                
                ], className="card col-12 col-md-6", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
            ),
        
        
        ]),
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
                ], className="card col-12", style={'padding':'.3rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
                ), 
            
            #dbc.Col([
            #        html.Div([
            #            dbc.Tabs([
            #                    dbc.Tab(label="Gráfico 4", tab_id="tab-r3c2-1", label_style={"color": "#00AEF9"}),
            #                    
            #                    dbc.Tab(label="Tabla 4", tab_id="tab-r3c2-2",  label_style={"color": "#00AEF9"}),
            #                ],
            #                id="tabs-r3c2",
            #                active_tab="tab-r3c2-1",
            #            ),
            #            html.Div(id="content-r3c2"),
            #         ], style={"width": "100%"}
            #        ),                 
            #    ], className="card col-12 col-md-6 ", style={'padding':'.3rem', 'marginTop':'0rem', 'marginLeft':'0rem', 'boxShadow': '#e3e3e3 4px 4px 1px', 'border-radius': '10px', 'backgroundColor': 'white', }
            #    ), 
            
            
        ]),
         
        
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem','marginRight': '2rem','marginTop': '0rem'}

    )


# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([
         
   
            
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
        State('t_productor', 'value'),
        State('grado_marginacion', 'value'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def actualizar_mapa(clicks, tproductor_sel, gmarginacion_sel, producto_sel, anio_sel):
    
    
    if tproductor_sel is None:
        raise PreventUpdate
    
    if producto_sel is None:
        raise PreventUpdate
    
    if gmarginacion_sel is None:
        raise PreventUpdate
    
    # Para selecciones múltiples: si es valor único creamos la lista, si no es valor único es una lista
    if isinstance(tproductor_sel, str):
        tprod = [tproductor_sel]
    else:
        tprod = tproductor_sel
            
    # selección múltiple grado de marginación
    if isinstance(gmarginacion_sel, str):
        gmarg = [gmarginacion_sel]
    else:
        gmarg = gmarginacion_sel
        
    # filtros
    base = df_benef.copy()
    #base = base.dropna()
    benef_filter = base[base['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['GM_2020'].isin(gmarg)]
    benef_filter = benef_filter[benef_filter['Tamanio_productor'].isin(tprod)]
    max_benef = benef_filter['MONTO_APOYO_TOTAL'].max()    
        
    est_color = df_prod_est[df_prod_est['Anio']==int(anio_sel)]
    est_color = est_color [est_color['Producto']==producto_sel]
    
    
    max_vol_prods =  {'Arroz': 50000000, 
                                     'Frijol':100000000, 
                                     'Leche':600000000, 
                                     'Maíz':4700000000000, 
                                     'Trigo':1200000000000}
    
    max_vol_prod = max_vol_prods[producto_sel]
    
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