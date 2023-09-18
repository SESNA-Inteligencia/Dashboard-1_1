

######################### Reglas de operación ######################
####################################################################
import dash          
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html



######################################################################
##########################   2019 - Maíz  ############################
######################################################################
ro_2019_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los productores de maíz poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                    html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                        html.Tbody([html.Tr([html.Td("5,610"), html.Td("20 Ton")])])],
                                        striped=False,
                                        highlightOnHover=False,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True,
                                        
                                        style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'1rem'}),
                                    ), 
                                    dmc.Text(
                                        """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo."""
                                    , color='white',  style={"fontSize": 11, 'padding':'1rem'}),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                    
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    # dmc.List(
                                    #     dmc.ListItem([
                                    #         dmc.Text(
                                    #             """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                    #         , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                    #         html.Br(),
                                    #         # table
                                    #         html.Center(
                                    #             dmc.Table(
                                    #             [html.Thead(html.Tr([
                                    #                         html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                    #                         html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                    #             html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                    #             striped=False,
                                    #             highlightOnHover=False,
                                    #             withBorder=True,
                                    #             horizontalSpacing=4,
                                    #             withColumnBorders=True,
                                                
                                    #             style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                    #         ),          
                                    #     ]),
                                    # ),
                                    html.Br(),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                    ], style={'paddingLeft':'1rem'}),
                            
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

##########################   2019 - Frijol  ####################
ro_2019_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Trigo
ro_2019_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Arroz
ro_2019_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Leche
ro_2019_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

######################################################################
##########################   2020 - Maíz  ############################
######################################################################
ro_2020_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

##########################   2020 - Frijol  ####################
ro_2020_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2020 - Trigo
ro_2020_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),  
                #], className="col-12"),

############             2020 - Arroz
ro_2020_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Leche
ro_2020_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),
######################################################################
##########################   2021 - Maíz  ############################
######################################################################
ro_2021_maiz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),
##########################   2020 - Frijol  ####################
ro_2021_frijol = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2020 - Trigo
ro_2021_trigo = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Posibles beneficiarios:  La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía",  style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ",  style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton)",  style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white'}),
                                            ),          
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),   
                #], className="col-12"),

############             2020 - Arroz
ro_2021_arroz = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),

############             2019 - Leche
ro_2021_leche = html.Div(
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    #dmc.BackgroundImage(
                        
                    #    src="/assets/maiz-mexico.jpg",
                        children=[
                        
                        # Título                                # TÍTULO
                        #dmc.Text("Reglas de Operación (Trigo-2020)", color='white', weight=700, style={'fontSize':24} ),
                        html.Br(),
                            # spoiler (text)
                        dmc.Spoiler(
                        showLabel="Continuar leyendo",
                        hideLabel="Ocultar",

                        maxHeight=200,
                        children=[
                            dbc.Row([
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Posibles beneficiarios:", color='#7c90ab', weight=700, style={'fontSize':20, 'padding':'1rem'} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , color='white',  style={"fontSize": 18, 'padding':'1rem'}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía", style={'color':'white'})])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, 
                                                style={'padding':'1rem','width':'80%','color':'white' }),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ],),
                                dbc.Col([  
                                    # Subtitulo
                                    # dmc.Text(
                                    #     """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    # , style={"fontSize": 18}),
                                    #html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo cristalino. Para el trigo cristalino destinado a la industria molinera nacional, se apoyarán hasta 50 (cincuenta) toneladas por productor con un incentivo del 40% del otorgado para trigo panificable descrito en la tabla anterior como “precio de garantía”. Este apoyo sólo se aplicará en Baja California, en Sonora y en el Bajío."""
                                            , color='white', style={"fontSize": 18, 'padding':'1rem'}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) ", style={'color':'white'}),
                                                            html.Th("Volumen máximo (Ton) ", style={'color':'white'}),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=False,
                                                highlightOnHover=False,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True,
                                                
                                                style={'width':'80%', 'padding':'1rem', 'color':'white', 'marginBottom':'8rem'}),
                                            ),          
                                        ]),
                                    ),
                                    html.Div([
                                        dmc.Text("""Fuente: """, color='white', style={"fontSize": 18}),
                                        html.A("Reglas de Operación del Programa de Precios de Garantía a Productos Alimentarios Básicos", 
                                            href='https://www.dof.gob.mx/nota_detalle.php?codigo=5609037&fecha=28/12/2020#gsc.tab=0', 
                                            target="_blank", 
                                            style={'color':'#07B8F1'}),
                                        
                                        ], style={'paddingLeft':'1rem'}),
                                  html.Br(),
                                    
                                ],),
                            ],),
                        ], ),
                    ],style={'opacity':'0.75'}),
#####################################################################

def resumen_reglas_operacion(Anio, Producto):
    '''
    Función para retornar el resumen de las reglas de operación
        dados el año y el tipo de producto
        
    Input : 
        Anio     : (int) Año correspondiente a las reglas de operación
                   2019, 2020, 2021
        Producto : (str) Producto considerado; Maíz, Frijol, Trigo,
                   Arroz, y leche.
    Outputs:
        Div : Texto html con el resumen de las reglas de operación  
    '''
    
    #############         Año 2019          ###################
    if Anio == '2019' and Producto == 'Maíz':
        result = ro_2019_maiz
    elif Anio == '2019' and Producto == 'Frijol':
        result = ro_2019_frijol
    elif Anio == '2019' and Producto == 'Trigo':
        result = ro_2019_trigo
    elif Anio == '2019' and Producto == 'Arroz':
        result = ro_2019_arroz
    elif Anio == '2019' and Producto == 'Leche':
        result = ro_2019_leche
    #############         Año 2020          ###################
    elif Anio == '2020' and Producto == 'Maíz':
        result = ro_2020_maiz
    elif Anio == '2020' and Producto == 'Frijol':
        result = ro_2020_frijol
    elif Anio == '2020' and Producto == 'Trigo':
        result = ro_2020_trigo
    elif Anio == '2020' and Producto == 'Arroz':
        result = ro_2020_arroz
    elif Anio == '2020' and Producto == 'Leche':
        result = ro_2020_leche
    #############         Año 2020          ###################
    elif Anio == '2021' and Producto == 'Maíz':
        result = ro_2021_maiz
    elif Anio == '2021' and Producto == 'Frijol':
        result = ro_2021_frijol
    elif Anio == '2021' and Producto == 'Trigo':
        result = ro_2021_trigo
    elif Anio == '2021' and Producto == 'Arroz':
        result = ro_2021_arroz
    elif Anio == '2021' and Producto == 'Leche':
        result = ro_2021_leche
    else:
        result = "No information"
    
    return result





