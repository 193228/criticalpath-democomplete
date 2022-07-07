from src.Controller.aperturaMaterias import *
from src.Model.relation_materies import getRelations


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

def getData(diccionario,periodo):
    lista = []
    print("Periodo para ruta critica "+periodo)

    materiasDependencias = getRelations()
    df = pd.DataFrame(materiasDependencias)
    materia = df['materia'].values.flatten().tolist()

    enero_abril = [1, 2, 4, 5, 7, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    for i in range(len(diccionario)):
        if diccionario[i]['materia'] in materia:
            print(diccionario[i])
            if diccionario[i]['Periodo'] == 'Septiembre-Diciembre':
                x = getName(diccionario[i],df)
                for i in range(len(x)):
                    if x[i]['cuatrimestreObjetivo'] in enero_abril:
                        lista.append(x[i])
                    else:
                        print("no esta porque en el periodo de enero-abril no puede tomar materias de "+str(x[i]['cuatrimestreObjetivo'])+" Cuatrimestre")
                        lista.append(x[i])

            if diccionario[i]['Periodo'] == 'Enero-Abril':
                x = getName(diccionario[i],df)
                for i in range(len(x)):
                    if x[i]['cuatrimestreObjetivo'] in mayo_agosto:
                        lista.append(x[i])
                    else:
                        print("no esta porque en el periodo de enero-abril no puede tomar materias de "+str(x[i]['cuatrimestreObjetivo'])+" Cuatrimestre")
                        print(x[i])

            if diccionario[i]['Periodo'] == 'Mayo-Agosto':
                x = getName(diccionario[i],df)
                for i in range(len(x)):
                    if x[i]['cuatrimestreObjetivo'] in septiembre_diciembre:
                        lista.append(x[i])
                    else:
                        print("no esta porque en el periodo de enero-abril no puede tomar materias de "+str(x[i]['cuatrimestreObjetivo'])+" Cuatrimestre")
                        print(x[i])

        else:
            print("no esta en las que puede tomar")

    return lista

def getName(diccionario,df):
    l = []
    for i in range(len(df)):
        if diccionario['materia'] in df['materia'][i]:
            x = {
                "nombreMateria":df['materia'][i],
                "dependeDe":df['depende'][i],
                "cuatrimestreObjetivo":df['cuatrimestreObjetivo'][i],
                "duracion":15
            }
            l.append(x)
    print(l)
    return l


