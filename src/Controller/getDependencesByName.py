from criticalpath import Node
import pandas as pd
from src.Model.relation_materies import getRelations
import networkx as nx

from src.Services.dbConnect import conexionBd

def getRelation(lista):
    dataframe = []

    lista = list(filter(None, lista))
    listaDependencia = [ele for ele in lista if ele != []]

    if len(listaDependencia) == 0:
        return pd.DataFrame()

    for i in listaDependencia:
        for dependencias in i:
            dicc = {"from": dependencias['from'],"to": dependencias['to']}
            dataframe.append(dicc)

    relaciones = pd.DataFrame(dataframe)
    return relaciones


def getMaterias():
    materias = pd.read_sql('select Nombre from d_materia where planestudiosid=28',con=conexionBd()).values.flatten().tolist()
    return materias

def obtenerRelacionesByName(lista):
    edges = pd.DataFrame.from_dict(lista)
    return edges

def getDependencesByName(diccionario,nombre):
    dicc = pd.DataFrame(diccionario)
    lista = []
    G = nx.from_pandas_edgelist(dicc,source='materia',target='depende', edge_attr=None,create_using=nx.DiGraph())
    sucesores = nx.bfs_successors(G, nombre)

    try:
        for i in sucesores:
            for j in i[1]:
                lista.append({"from": i[0], "to": j})
        return lista

    except:
        return lista.append({"from": nombre, "to": nombre})

def calcularRutaCritica(relaciones,materias):
    #creo una lista de tareas y dependencias
    tareas = []; dependencias = []
    # Crear el proyecto "p"
    p = Node('proyecto')
    #creo una lista de tareas
    for i in range(len(materias)):
        tareas.append((materias[i], {"duracion": 15}))
    #creo una lista de dependencias
    for i in range(len(relaciones)):
        dependencias.append((relaciones['from'][i],relaciones['to'][i]))

    # Cargar al proyecto las tareas y sus duraciones
    for i in tareas:
        p.add(Node(i[0], duration=i[1]["duracion"]))

    # Cargar al proyecto sus dependencias (secuencias)
    for j in dependencias:
        p.link(j[0], j[1])

    # Actualizar el proyecto:
    p.update_all()
    return p


'''if __name__ == '__main__':
    lista = getDependencesByName(getRelations(),"Algoritmos")
    relaciones = obtenerRelacionesByName(lista)
    listaMaterias = getMaterias()
    calcularRutaCritica(relaciones, listaMaterias)'''
