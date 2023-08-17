

######################### Reglas de operación ######################
####################################################################
import dash          
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html



######################################################################
##########################   2019 - Maíz  ############################
######################################################################
ro_2019_maiz = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Maíz-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """Todos los productores de maíz poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal. """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("5,610"), html.Td("20")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                dmc.Text(
                                    """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


##########################   2019 - Frijol  ####################
ro_2019_frijol = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Frijol-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """todos los productores poseedores de una superficie de cultivo 
                                    de hasta 30 hectáreas de temporal o hasta 5 hectáreas de riego. 
                                    Cuando estas superficies excedan hasta en media hectárea, la misma 
                                    será redondeada a la superficie de 30 hectáreas de temporal o 5 hectáreas 
                                    de riego, autorizados para el pago del precio de garantía."""
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("14,500"), html.Td("15 Ton")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                # dmc.Text(
                                #     """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                # , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


############             2019 - Trigo
ro_2019_trigo = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Trigo-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """La totalidad de los productores de trigo con la limitante del volumen máximo por productor. """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("5,790"), html.Td("100Ton")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                # dmc.Text(
                                #     """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                # , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


############             2019 - Arroz
ro_2019_arroz = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Arroz-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """La totalidad de los productores de trigo con la limitante del volumen máximo por productor. """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("6,120"), html.Td("120Ton")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                # dmc.Text(
                                #     """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                # , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


############             2019 - Leche
ro_2019_leche = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Leche-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """Pequeños productores (de 1 a 35 vacas), \n Medianos productos (de 36 a 100 vacas).  """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("8.20/Ltr"), html.Td("15Lts/vaca")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                dmc.Text(
                                    """ *LICONSA podrá comprar leche fluida a productores que rebasen el límite de vacas antes señalado, en tal caso, lo hará a precio de mercado. """
                                , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),

######################################################################
##########################   2020 - Maíz  ############################
######################################################################
ro_2020_maiz = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    dmc.Paper(children=[
                        
                        # Título                                # TÍTULO
                        dmc.Text("Reglas de Operación (Maíz-2020)", color='#2a3240', weight=700, style={'fontSize':24} ),
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
                                    dmc.Text("Pequeños Productores:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                    # Texto principal
                                    dmc.Text(
                                        """Todos los pequeños productores poseedores de una superficie de cultivo de hasta 5 (cinco) hectáreas de temporal. En este límite, las fracciones de hectárea hasta 0.5 se redondearán al número inferior."""
                                    , style={"fontSize": 18}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) *"),
                                                    html.Th("Volumen máximo (Ton)"),])),
                                        html.Tbody([html.Tr([html.Td("5,610"), html.Td("20")])])],
                                        striped=True,
                                        highlightOnHover=True,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True, style={'width':'80%'}),
                                    ),
                                    html.Br(),
                                    # Pie
                                    dmc.Text(
                                        """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    , style={"fontSize": 12}),
                                    html.Br(),
                                    
                                ], style={'marginLeft':'2rem', 'marginRight':'1rem'}),
                                dbc.Col([  
                                    # Subtitulo
                                    dmc.Text("Medianos productores:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                    # Texto principal
                                    # segunda parte medianos productores
                                    dmc.Text(
                                        """Maíz comercializado por medianos productores. Los medianos productores de maíz de riego y los de temporal de más de 5 (cinco) hectáreas, que comercialicen su producción, con hasta 50 hectáreas sembradas."""
                                    , style={"fontSize": 18}),
                                    html.Br(),
                                    # Tabla
                                    html.Center(
                                        dmc.Table(
                                        [html.Thead(html.Tr([
                                                    html.Th("Precio de garantía ($) "),
                                                    html.Th("Volumen máximo (Ton)"),])),
                                        html.Tbody([html.Tr([html.Td("4,150"), html.Td("600")])])],
                                        striped=True,
                                        highlightOnHover=True,
                                        withBorder=True,
                                        horizontalSpacing=4,
                                        withColumnBorders=True, style={'width':'80%'}),
                                    ),
                                    html.Br(),
                                    # Pie
                                    dmc.Text(
                                        """Para los medianos productores de maíz de riego y los de temporal de más de cinco hectáreas, que comercialicen su producción, con hasta 50 (cincuenta) hectáreas sembradas, únicamente se pagará la diferencia entre el Precio de Garantía y un Precio de Mercado de Referencia que establecerá SEGALMEX."""
                                    , style={"fontSize": 18}),
                                ], style={'marginLeft':'1rem', 'marginRight':'2rem'}),
                            ], style={'backgroundColor':'#F8F9F9'}),
                        ]),
                    ],shadow="xs")   
                ], className="col-10", style={'opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/maiz-mexico.jpg)','border-radius': '10px', 'backgroundColor':'#4e203a','marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0.5rem', 'paddingRight':'0rem'}),

##########################   2020 - Frijol  ####################
ro_2020_frijol = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Frijol-2020)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=200,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """Todos los productores poseedores de una superficie de cultivo de hasta 30 (treinta) hectáreas de temporal o 5 (cinco) hectáreas de riego. En estos límites, las fracciones de hectárea hasta 0.5 se redondearán al número inferior."""
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("14,500"), html.Td("15 Ton")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                # dmc.Text(
                                #     """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                # , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


############             2020 - Trigo
ro_2020_trigo = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    
                    dmc.Paper(children=[
                        
                        # Título                                # TÍTULO
                        dmc.Text("Reglas de Operación (Trigo-2020)", color='#2a3240', weight=700, style={'fontSize':24} ),
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
                                    dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                    # Texto principal
                                    dmc.Text(
                                        """La totalidad de los productores que destinen su producción a la industria nacional con la limitante del volumen máximo por productor y otras descritas a continuación."""
                                    , style={"fontSize": 18}),
                                    html.Br(),
                                    # Tabla
                                    dmc.List(
                                        dmc.ListItem([
                                            dmc.Text(
                                                """Apoyos para el trigo panificable. En trigo panificable destinado a la industria molinera nacional y para semilla, el incentivo para alcanzar el Precio de Garantía se aplicará de manera porcentual, como se describe a continuación:"""
                                            , style={"fontSize": 18}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([html.Th(""),
                                                            html.Th("Incentivo para alcanzar el Precio de Garantía")])),
                                                html.Tbody([html.Tr([html.Td("Precio de Garantía"), html.Td("Hasta 100 toneladas por productor elegible, recibirán el incentivo completo (100%), equivalente a la diferencia entre el precio de garantía y un precio de mercado de referencia que establecerá SEGALMEX.")]),
                                                            html.Tr([html.Td("Incentivo por productividad"), html.Td("Hasta 200 toneladas adicionales a las primeras 100 por productor, recibirán el 50% del incentivo completo.")]),
                                                            html.Tr([html.Td("Precio de mercado de referencia"), html.Td("El precio de mercado de referencia será definido para cada región y su cálculo se efectuará considerando el promedio de los precios del trigo en el Mercado de Físicos de la Bolsa de Comercio de Chicago (CBOT) y el promedio del tipo de cambio, más las bases fijadas por SEGALMEX, durante los primeros 15 días en que se generalice el periodo de la cosecha en cada región.")])])],
                                                highlightOnHover=True,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, style={'width':'100%'}),
                                            ),        
                                              
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                    # Pie
                                    # dmc.Text(
                                    #     """*Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                    # , style={"fontSize": 12}),
                                    # html.Br(),
                                    
                                ], style={'marginLeft':'2rem', 'marginRight':'1rem'}),
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
                                            , style={"fontSize": 18}),
                                            html.Br(),
                                            # table
                                            html.Center(
                                                dmc.Table(
                                                [html.Thead(html.Tr([
                                                            html.Th("Precio de garantía ($) "),
                                                            html.Th("Volumen máximo (Ton)"),])),
                                                html.Tbody([html.Tr([html.Td("5,790"), html.Td("100 Ton")])])],
                                                striped=True,
                                                highlightOnHover=True,
                                                withBorder=True,
                                                horizontalSpacing=4,
                                                withColumnBorders=True, style={'width':'80%'}),
                                            ),          
                                        ]),
                                    ),
                                    
                                    html.Br(),
                                ], style={'marginLeft':'1rem', 'marginRight':'2rem'}),
                            ], style={'backgroundColor':'#F8F9F9'}),
                        ]),
                    ],shadow="xs")   
                ], className="col-10", style={'opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/maiz-mexico.jpg)','border-radius': '10px', 'backgroundColor':'#4e203a','marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0.3rem', 'paddingRight':'0rem'}),

############             2020 - Arroz
ro_2020_arroz = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Arroz-2020)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """La totalidad de los productores de trigo con la limitante del volumen máximo por productor. """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("6,120"), html.Td("120Ton")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                # dmc.Text(
                                #     """ *Adicional $150 (CIENTO CINCUENTA PESOS 00/100 M.N.) por tonelada, sin exceder el costo de traslado de 20 toneladas por ciclo. """
                                # , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),


############             2019 - Leche
ro_2020_leche = html.Div([
                    #dmc.Accordion(id="accordion-uno"),
                    #dmc.Text(id="accordion-text-uno", mt=10),
                    dmc.Paper(children=[
                            # TÍTULO
                            dmc.Text("Reglas de Operación (Leche-2019)", color='#2a3240', weight=700, style={'fontSize':24} ),
                            html.Br(),
                            # spoiler (text)
                            dmc.Spoiler(
                            showLabel="Continuar leyendo",
                            hideLabel="Ocultar",
                            maxHeight=50,
                            children=[  
                                # Subtitulo
                                dmc.Text("Posibles beneficiarios:", color='#4e203a', weight=700, style={'fontSize':20} ),
                                # Texto principal
                                dmc.Text(
                                    """Pequeños productores (de 1 a 35 vacas), \n Medianos productos (de 36 a 100 vacas).  """
                                , style={"fontSize": 18}),
                                html.Br(),
                                # Tabla
                                html.Center(
                                    dmc.Table(
                                    [html.Thead(html.Tr([
                                                html.Th("Precio de garantía ($) "),
                                                html.Th("Volumen máximo (Ton)"),])),
                                    html.Tbody([html.Tr([html.Td("8.20/Ltr"), html.Td("15Lts/vaca")])])],
                                    striped=True,
                                    highlightOnHover=True,
                                    withBorder=True,
                                    horizontalSpacing=4,
                                    withColumnBorders=True, style={'width':'50%'}),
                                ),
                                html.Br(),
                                # Pie
                                dmc.Text(
                                    """ *LICONSA podrá comprar leche fluida a productores que rebasen el límite de vacas antes señalado, en tal caso, lo hará a precio de mercado. """
                                , style={"fontSize": 12}),
                            ]),
                    ],shadow="xs")   
                #     ]),
                # ]),
            ], className="col-10", style={'marginTop':'4rem','marginBottom':'2rem','paddingLeft':'0rem', 'paddingRight':'0rem'}),



