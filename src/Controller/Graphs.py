from src.Controller.getDependencesByName import calcularRutaCritica, getMaterias
from src.Services.dbConnect import conexionBd
import warnings
warnings.filterwarnings("ignore")

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go  # or plotly.express as px
import pandas as pd
import networkx as nx
import igviz as ig
from pyvis.network import Network
from IPython.core.display import display, HTML


def graphReinscripcion(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasAbiertas,matricula):
    print(" --------------------------- ESTE GRAFO SERA EL DE LA REINSCRIPCION ----------------------------------- ")
    if len(relaciones) == 0:
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__)
        app.title = "Informacion del alumno"
        titulo = html.Div([
            html.H1('No Se Encontraron Materias Dependientes. Sin Ruta Critica, Alumno '+matricula, style={'textAlign': 'center'})
        ])

        fig_names = ['Materias Aprobadas','Materias Faltantes']
        fig_dropdown = html.Div([
            dcc.Dropdown(
                id='fig_dropdown',
                options=[{'label': x, 'value': x} for x in fig_names],
                value="Materias Faltantes"
            )])
        fig_plot = html.Div(id='fig_plot')
        app.layout = html.Div([titulo, fig_dropdown, fig_plot])

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

            return dcc.Graph(figure=figure, config=config)

        app.run_server(debug=False, use_reloader=False)
        #print(listaMateriasRestantes['nombre'])
    else:
        rutaCritica = calcularRutaCritica(relaciones, getMaterias())
        graficoReinscripcion(relaciones,rutaCritica,aprobado,reprobado,listaMateriasRestantes)

def graphStatusActual(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasAbiertas):
    print(" --------------------------- ESTE GRAFO SERA EL DEL STATUS ACTUAL  ----------------------------------- ")
    if len(relaciones) == 0:
        print(listaMateriasRestantes['nombre'])
    else:
        rutaCritica = calcularRutaCritica(relaciones, getMaterias())
        print(aprobado)
        print(reprobado)
        print(listaMateriasRestantes)
        print(relaciones)
        print(materiasAbiertas)
        print(rutaCritica)
        graficoStatusActual(relaciones,rutaCritica)


def graficoReinscripcion(relaciones,rutaCritica,materiasAprobadas,materiasReprobadas,materiasFaltantes):
    app = dash.Dash()
    fig_names = ['Grafico Ruta Critica', 'Grafico Materias Faltantes', 'Materias Aprobadas', 'Materias Reprobadas', 'Materias Faltantes']
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in fig_names],
            value = "Grafico Ruta Critica"
        )])
    fig_plot = html.Div(id='fig_plot')
    app.layout = html.Div([fig_dropdown, fig_plot])

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

        return dcc.Graph(figure=figure, config=config)
    app.run_server(debug=False, use_reloader=False)


def graficoStatusActual(grafo,rutaCritica):
    app = dash.Dash()
    relationships = pd.DataFrame({ 'from': ['A','A','A'], 'to': ['B','C','D']})
    G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.DiGraph())

    fig = ig.plot(
        G,
        #colorbar_title="#23A8F2",
        title="Ruta Critica",
        annotation_text= "Camino Sugerido ",#+str(rutaCritica.get_critical_path()),
        layout="spring",
        size_method="static",
    )

    fig.show()
    app.run_server(debug=False, use_reloader=False)


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
    print(dataframe)
    figure = go.Figure(data=[go.Table(
        header=dict(values=list(["Nombre De La Materia", "Cuatrimestre"]),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[dataframe.nombre, dataframe.periodo],
                   fill_color='lavender',
                   align='center'))
    ])
    return figure

def materiasAbiertasActuales(dataframe):
    print("")

def materiasReprobadasTable(dataframe):
    print(dataframe)

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
        node_label="propiedad",  # Display the "prop" attribute as a label on the node
        node_text=["propiedad"],
        node_label_position="top center",  # Display the node label directly above the node
        layout="spiral",
        titlefont_size=20,
        color_method="blue",
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
        node_label="propiedad",  # Display the "prop" attribute as a label on the node
        node_text=["propiedad"],
        node_label_position="top center",  # Display the node label directly above the node
        layout="spiral",
        titlefont_size=20,
        color_method="red"
    )

    return figure