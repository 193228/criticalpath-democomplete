from src.Controller.getDependencesByName import calcularRutaCritica, getMaterias
from src.Controller.graficos import *
import warnings
warnings.filterwarnings("ignore")


def graphReinscripcion(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasAbiertas,matricula,periodo):
    print(" --------------------------- ESTE GRAFO SERA EL DE LA REINSCRIPCION ----------------------------------- ")
    if len(relaciones) == 0:
        llamadaReinscripcionSinRelaciones(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo)
    else:
        rutaCritica = calcularRutaCritica(relaciones, getMaterias())
        llamadaReinscripcion(relaciones,rutaCritica,aprobado,reprobado,listaMateriasRestantes,matricula,materiasAbiertas,periodo)

def graphStatusActual(aprobado,reprobado,listaMateriasRestantes,relaciones,materiasAbiertas,matricula,periodo):
    print(" --------------------------- ESTE GRAFO SERA EL DEL STATUS ACTUAL  ----------------------------------- ")
    if len(relaciones) == 0:
        llamadaStatusActualSinRelaciones(aprobado,listaMateriasRestantes,materiasAbiertas,matricula,periodo)
    else:
        rutaCritica = calcularRutaCritica(relaciones, getMaterias())
        llamadaStatusActual(relaciones,rutaCritica,aprobado,reprobado,listaMateriasRestantes,matricula,materiasAbiertas,periodo)
        #graficoStatusActualidad(relaciones,rutaCritica,aprobado,reprobado,listaMateriasRestantes,matricula,materiasAbiertas,periodo)