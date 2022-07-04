from src.Controller.aperturaMaterias import *


def materiasReinscribirse(mes_reinscribirse,CLAVE,listaMateriasAbiertas,materiasAprobadaAlumno):
    reinscribirse = []

    if 1 <= mes_reinscribirse <= 4:
        mayo_agosto = materiasAbiertasReinscripcion(mes_reinscribirse, CLAVE)['Nombre'].values.tolist()
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                if datos['Nombre'] in mayo_agosto:
                    dicc = {"Periodo": "Mayo-Agosto","materia": datos['Nombre'],"idmateria": datos['materiaid'],"numeroCuatrimestre": datos['Periodo']}
                    reinscribirse.append(dicc)
        return reinscribirse

    if 5 <= mes_reinscribirse <= 8:
        septiembre_diciembre = materiasAbiertasReinscripcion(mes_reinscribirse, CLAVE)['Nombre'].values.tolist()
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                if datos['Nombre'] in septiembre_diciembre:
                    dicc = {"Periodo": "Septiembre-Diciembre","materia": datos['Nombre'],"idmateria": datos['materiaid'],"numeroCuatrimestre": datos['Periodo']}
                    reinscribirse.append(dicc)
        return reinscribirse

    if 9 <= mes_reinscribirse <= 12:
        enero_abril = materiasAbiertasReinscripcion(mes_reinscribirse, CLAVE)['Nombre'].values.tolist()
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                if datos['Nombre'] in enero_abril:
                    dicc = {"Periodo": "Enero-Abril","materia": datos['Nombre'],"idmateria": datos['materiaid'],"numeroCuatrimestre": datos['Periodo']}
                    reinscribirse.append(dicc)
        return reinscribirse

def periodoActual(mes):
    if 1 <= mes <= 4:
        resultado = "Enero-Abril"

    if 5 <= mes <= 8:
        resultado = "Mayo-Agosto"

    if 9 <= mes <= 12:
        resultado = "Septiembre-Diciembre"

    return resultado

def periodorReinscripcion(mes):
    if 1 <= mes <= 4:
        resultado = "Mayo-Agosto"

    if 5 <= mes <= 8:
        resultado = "Septiembre-Diciembre"

    if 9 <= mes <= 12:
        resultado = "Enero-Abril"

    return resultado


