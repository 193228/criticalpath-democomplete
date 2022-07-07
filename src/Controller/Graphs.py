import pandas as pd
from src.Services.dbConnect import conexionBd
import warnings
warnings.filterwarnings("ignore")
from criticalpath import Node
import datetime

def graphReinscripcion(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasPerperiodo):
    print(" --------------------------- ESTE GRAFO SERA EL DE LA REINSCRIPCION ----------------------------------- ")
    print(aprobado)
    print(reprobado)
    print(listaMateriasRestantes)
    print(relaciones)
    print(materiasPerperiodo)

def graphStatusActual(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasPerperiodo):
    print(" --------------------------- ESTE GRAFO SERA EL DEL STATUS ACTUAL  ----------------------------------- ")
    print(aprobado)
    print(reprobado)
    print(listaMateriasRestantes)
    print(relaciones)
    print(materiasPerperiodo)

