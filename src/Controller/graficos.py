import asyncio
import os
import threading
import webbrowser
from multiprocessing import Process
from threading import Timer
from functools import partial
from threading import Thread
import dash
import dash_html_components as html
import dash_core_components as dcc
import networkx as nx
import pandas as pd
import plotly.graph_objects as go  # or plotly.express as px
import igviz as ig
import dash_bootstrap_components as dbc

def open_browser(opcion):
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        if opcion == 1:
            webbrowser.open_new('http://127.0.0.1:8080/')
        if opcion == 2:
            webbrowser.open_new('http://127.0.0.1:8081/')
        if opcion == 3:
            webbrowser.open_new('http://127.0.0.1:8082/')
        if opcion == 4:
            webbrowser.open_new('http://127.0.0.1:8083/')

def reinscripcionSinRelacion(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo):
    app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE],
                    meta_tags=[
                        {
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1, maximum-scale=1",
                        }
                    ], )
    app.title = "Informacion del alumno"
    titulo = html.Div([
        html.H1('Reinscripcion. No Se Encontraron Materias Dependientes, Alumno ' + str(matricula)+ ' Periodo '+str(periodo),
                style={'textAlign': 'center'}),
        html.Br()
    ])
    subtitulo = html.Div([
        html.H5('Escoja una opcion',
                style={'textAlign': 'center'})
    ])
    fig_names = ['Materias Aprobadas', 'Materias Faltantes', 'Materias Abiertas']
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in fig_names],
            value="Materias Faltantes"
        )])
    fig_plot = html.Div(id='fig_plot')

    espacio = html.Div([
        html.Br(),
        html.Br()
    ])

    app.layout = html.Div([titulo,subtitulo,fig_dropdown,espacio,fig_plot])

    @app.callback(
        dash.dependencies.Output('fig_plot', 'children'),
        [dash.dependencies.Input('fig_dropdown', 'value')]
    )
    def update_output(fig_name):
        return name_to_figure(fig_name)

    def name_to_figure(fig_name):
        figure = go.Figure()

        config = {
            'responsive': 'auto',
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan']
        }

        if fig_name == 'Materias Aprobadas':
            figure = materiasAprobadasTable(aprobado)
        elif fig_name == 'Materias Faltantes':
            figure = materiasFaltantesTable(listaMateriasRestantes)
        elif fig_name == 'Materias Abiertas':
            figure = materiasAbren(materiasAbiertas)

        return dcc.Graph(figure=figure, config=config)
    app.run_server(port= 8081, debug=False, use_reloader=False)

def graficoReinscripcion(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula,materiasAbiertas,periodo):
    app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1",
        }
    ],)
    app.title = "Informacion del alumno"
    titulo = html.Div([
        html.H1('Reinscripcion. Alumno ' + str(matricula)+' Periodo '+str(periodo),
                style={'textAlign': 'center'})
    ])
    subtitulo = html.Div([
        html.H5('Escoja una opcion',
                style={'textAlign': 'center'})
    ])
    fig_names = ['Grafico Ruta Critica', 'Grafico Materias Faltantes', 'Materias Aprobadas', 'Materias Reprobadas', 'Materias Faltantes', 'Materias Abiertas']
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in fig_names],
            value = "Grafico Ruta Critica"
        )])

    fig_plot = html.Div(id='fig_plot')

    espacio = html.Div([
        html.Br(),
        html.Br()
    ])

    app.layout = html.Div([titulo,subtitulo,fig_dropdown,espacio,fig_plot])

    @app.callback(
        dash.dependencies.Output('fig_plot', 'children'),
        [dash.dependencies.Input('fig_dropdown', 'value')]
    )
    def update_output(fig_name):
        return name_to_figure(fig_name)

    def name_to_figure(fig_name):
        figure = go.Figure()

        config = {
            'responsive': 'auto',
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan']
        }

        if fig_name == 'Grafico Ruta Critica': #ruta critica del alumno
            figure = rutaCriticaGraph(rutaCritica.get_critical_path())
        elif fig_name == 'Grafico Materias Faltantes': #ruta critica del alumno
            figure = materies_faltantes_graph(relaciones)
        elif fig_name == 'Materias Aprobadas':
            figure = materiasAprobadasTable(materiasAprobadas)
        elif fig_name == 'Materias Reprobadas':
            figure = materiasReprobadasTable(materiasReprobadas)
        elif fig_name == 'Materias Faltantes':
            figure = materiasFaltantesTable(materiasFaltantes)
        elif fig_name == 'Materias Abiertas':
            figure = materiasAbren(materiasAbiertas)

        return dcc.Graph(figure=figure, config=config)

    app.run_server(port= 8080, debug=False, use_reloader=False)

def estatusActualSinRelacion(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo):
    app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE],
                    meta_tags=[
                        {
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1, maximum-scale=1",
                        }
                    ], )
    app.title = "Informacion del alumno"
    titulo = html.Div([
        html.H1('Status Actual. No Se Encontraron Materias Dependientes. Sin Ruta Critica, Alumno ' + str(matricula)+' Periodo '+str(periodo),
                style={'textAlign': 'center'})
    ])
    subtitulo = html.Div([
        html.H5('Escoja una opcion',
                style={'textAlign': 'center'})
    ])

    fig_names = ['Materias Aprobadas', 'Materias Faltantes', 'Materias Abiertas']
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in fig_names],
            value="Materias Faltantes"
        )])
    fig_plot = html.Div(id='fig_plot')

    espacio = html.Div([
        html.Br(),
        html.Br()
    ])

    app.layout = html.Div([titulo,subtitulo,fig_dropdown,espacio,fig_plot])

    @app.callback(
        dash.dependencies.Output('fig_plot', 'children'),
        [dash.dependencies.Input('fig_dropdown', 'value')]
    )
    def update_output(fig_name):
        return name_to_figure(fig_name)

    def name_to_figure(fig_name):
        figure = go.Figure()

        config = {
            'responsive': 'auto',
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan']
        }

        if fig_name == 'Materias Aprobadas':
            figure = materiasAprobadasTable(aprobado)
        elif fig_name == 'Materias Faltantes':
            figure = materiasFaltantesTable(listaMateriasRestantes)
        elif fig_name == 'Materias Abiertas':
            figure = materiasAbren(materiasAbiertas)

        return dcc.Graph(figure=figure, config=config)

    app.run_server(port= 8083, debug=False, use_reloader=False)

def graficoStatusActualidad(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula, materiasAbiertas, periodo):
    app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE],
                    meta_tags=[
                        {
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1, maximum-scale=1",
                        }
                    ], )
    app.title = "Informacion del alumno"
    titulo = html.Div([
        html.H1('Status Actual. Alumno ' + str(matricula) + " Periodo "+str(periodo),
                style={'textAlign': 'center'})
    ])
    subtitulo = html.Div([
        html.H5('Escoja una opcion',
                style={'textAlign': 'center'})
    ])
    fig_names = ['Grafico Ruta Critica', 'Grafico Materias Faltantes', 'Materias Aprobadas', 'Materias Reprobadas', 'Materias Faltantes', 'Materias Abiertas']
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in fig_names],
            value = "Grafico Ruta Critica"
        )])
    fig_plot = html.Div(id='fig_plot')

    espacio = html.Div([
        html.Br(),
        html.Br()
    ])

    app.layout = html.Div([titulo,subtitulo,fig_dropdown,espacio, fig_plot])

    @app.callback(
        dash.dependencies.Output('fig_plot', 'children'),
        [dash.dependencies.Input('fig_dropdown', 'value')]
    )
    def update_output(fig_name):
        return name_to_figure(fig_name)

    def name_to_figure(fig_name):
        figure = go.Figure()

        config = {
            'responsive': 'auto',
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan']
        }

        if fig_name == 'Grafico Ruta Critica': #ruta critica del alumno
            figure = rutaCriticaGraph(rutaCritica.get_critical_path())
        elif fig_name == 'Grafico Materias Faltantes': #ruta critica del alumno
            figure = materies_faltantes_graph(relaciones)
        elif fig_name == 'Materias Aprobadas':
            figure = materiasAprobadasTable(materiasAprobadas)
        elif fig_name == 'Materias Reprobadas':
            figure = materiasReprobadasTable(materiasReprobadas)
        elif fig_name == 'Materias Faltantes':
            figure = materiasFaltantesTable(materiasFaltantes)
        elif fig_name == 'Materias Abiertas':
            figure = materiasAbren(materiasAbiertas)

        return dcc.Graph(figure=figure, config=config)

    app.run_server(port=8082, debug=False, use_reloader=False)

def materiasAbren(materias):
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(["MateriaID", "Nombre De La Materia", "Cuatrimestre"]),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[materias.materiaid, materias.Nombre, materias.Periodo],
                   fill_color='lavender',
                   align='center'))
    ])
    return figure

def materiasAprobadasTable(dataframe):
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(["Nombre De La Materia","ID Materia","Cuatrimestre","Promedio Final"]),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[dataframe.Nombre, dataframe.materiaid, dataframe.periodo, dataframe.Final],
                   fill_color='lavender',
                   align='center'))
    ])
    return figure

def materiasFaltantesTable(dataframe):
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(["Nombre De La Materia", "Cuatrimestre"]),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[dataframe.nombre, dataframe.periodo],
                   fill_color='lavender',
                   align='center'))
    ])
    return figure

def materiasReprobadasTable(dataframe):
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(["Nombre De La Materia","ID Materia","Cuatrimestre","Promedio Final"]),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[dataframe.Nombre, dataframe.materiaid, dataframe.periodo, dataframe.Final],
                   fill_color='lavender',
                   align='center'))
    ])
    return figure


def materies_faltantes_graph(materias):
    frm = materias['from'].values.tolist()
    to = materias['to'].values.tolist()
    resultList = list(set(frm) | set(to))
    node_ruta = dict(zip(resultList, resultList))
    relationships = pd.DataFrame(materias)
    G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.DiGraph())
    nx.set_node_attributes(G, node_ruta, "propiedad")

    figure = ig.plot(
        G,
        title="Materias Faltantes A Cursar",
        node_label="propiedad",  # Display the "prop" attribute as a label on the node
        node_text=["propiedad"],
        node_label_position="top center",  # Display the node label directly above the node
        layout="spring",
        titlefont_size=20,
        color_method="blue",
        size_method="static",
    )

    return figure

def rutaCriticaGraph(rutaCritica):
    for i in range(len(rutaCritica)): rutaCritica[i]=str(rutaCritica[i])
    node_ruta = dict(zip(rutaCritica, rutaCritica))
    crit_path = [str(n) for n in rutaCritica]  # rutaCritica.get_critical_path()]
    crit_edges = [(n, crit_path[i + 1]) for i, n in enumerate(crit_path[:-1])]
    crit_edges_df = pd.DataFrame(crit_edges)
    crit_edges_df.columns = ["from", "to"]
    relationships = pd.DataFrame(crit_edges_df)
    G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.DiGraph())
    nx.set_node_attributes(G, node_ruta, "propiedad")

    figure = ig.plot(
        G,
        title="Ruta Critica",
        node_label="propiedad",  # Display the "prop" attribute as a label on the node
        node_text=["propiedad"],
        node_label_position="top center",  # Display the node label directly above the node
        layout="spectral",
        titlefont_size=20,
        color_method="red",
        size_method="static",
        annotation_text="Ruta Critica Recomendada es: "+str(rutaCritica)
    )

    return figure

#reinscripcion
def llamadaReinscripcion(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula,materiasAbiertas,periodo):
    Thread(target=graficoReinscripcion, args=(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula,materiasAbiertas,periodo), daemon=True).start()
    Timer(1, open_browser(1)).start()

#reinscripcion sin relaciones
def llamadaReinscripcionSinRelaciones(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo):
    Thread(target=reinscripcionSinRelacion, args=(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo), daemon=True).start()
    Timer(1, open_browser(2)).start()

#status actual
def llamadaStatusActual(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula,materiasAbiertas,periodo):
    Thread(target=graficoStatusActualidad, args=(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes,matricula,materiasAbiertas,periodo), daemon=True).start()
    Timer(1, open_browser(3)).start()

#status actual sin relaciones
def llamadaStatusActualSinRelaciones(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo):
    Thread(target=estatusActualSinRelacion, args=(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo), daemon=True).start()
    Timer(1, open_browser(4)).start()