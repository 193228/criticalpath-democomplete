import datetime
import os
import random
import sys

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from src.Controller.datosAlumnado import *
from src.Controller.getDependencesByName import getDependencesByName, obtenerRelacionesByName, getMaterias, \
    calcularRutaCritica, getRelation
from src.Controller.reinscripcionCuatri import *
from src.Model.relation_materies import getRelations
from src.View.vistaRutaCritica import Ui_MainWindow as ventanaPrincipal
import warnings
warnings.filterwarnings("ignore")

CLAVE = "004"

class MyApp(QtWidgets.QMainWindow, ventanaPrincipal):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ventanaPrincipal.__init__(self)
        self.setupUi(self)
        acciones(self)

def acciones(ventana):
    cargarLogo(ventana,"./Resources/logoUP.png")
    ventana.statusBotton.clicked.connect(lambda: statusActual(ventana))
    ventana.reinscripcionBotton.clicked.connect(lambda: reinscripcion(ventana))

def cargarLogo(ventana,ruta):
    imagen = QPixmap(ruta)#PyQt5.QPixmap(ruta)
    ventana.photo.setPixmap(imagen)

def mostrarMensajes(ventana,texto):
    msg = QMessageBox()
    msg.setText(texto)
    msg.setWindowTitle("Error")
    msg.setIcon(QMessageBox.Information)
    msg.setStyleSheet("background-color: white;color: rgb(0, 0, 0)")
    msg.exec_()

def statusActual(ventana):
    try:
        pd.options.display.width = 0
        #Obtengo matricula del alumno
        matriculaAlumno = int(ventana.matricula.toPlainText())
        #Obtengo la fecha actual
        dt = datetime.datetime.today().month
        # Obtengo la lista de materias abiertas
        listaMateriasAbiertas = materiasAbiertasActuales(dt, CLAVE)
        #Obtengo datos del alumno
        materiasAlumno, aprobado, reprobado = obtencionDatosAlumno(ventana,matriculaAlumno)
        #Obtengo materias aprobadas por el alumno
        materiasAprobadaAlumno = aprobado['Nombre'].values.tolist()

        print("------------------------------ ESTAS SON MATERIAS DISPONIBLES PARA EL PERIODO ACTUAL "+str(periodoActual(dt))+" ------------------------------------------")
        print(listaMateriasAbiertas)

        print("------------------------------ ESTAS SON MATERIAS QUE HA TOMADO EL ALUMNO "+str(periodoActual(dt))+" ------------------------------------------")
        print(materiasAlumno)

        print("------------------------------ ESTAS SON MATERIAS QUE YA APROBO EL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        print(aprobado)

        print("------------------------------ ESTAS SON MATERIAS QUE DEBE EL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        print(reprobado) #Para el estatus actual solamente

        print("------------------------------ ESTAS SON MATERIAS QUE LE FALTA AL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                print(datos['Nombre'])

        print("------------------------------ ESTA ES LA RUTA CRITICA "+str("193228")+" -------------------------")

        lista = []; lm = []
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                resultado = getDependencesByName(getRelations(), datos['Nombre'])
                lm.append(datos['Nombre'])
                lista.append(resultado)

        relaciones = getRelation(lista)
        listaMaterias = getMaterias()

        if not relaciones.empty:
            b = calcularRutaCritica(relaciones, listaMaterias)
            print(b.get_critical_path())
            print("YA QUEDO ESTATUS ACTUAL")
        else:
            print("No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> "+random.choice(lm))
            print("YA QUEDO ESTATUS ACTUAL")

    except:
        print("ocurrio un error")
        pass

def reinscripcion(ventana):
    lista = []; lm = []
    dt = datetime.datetime.today().month

    matriculaAlumno = int(ventana.matricula.toPlainText())

    listaMaterias = materiasAbiertasReinscripcion(dt, CLAVE)

    materiasAlumno, aprobado, reprobado = obtencionDatosAlumno(ventana, matriculaAlumno)

    # Obtengo materias aprobadas por el alumno
    materiasAprobadaAlumno = aprobado['Nombre'].values.tolist()

    print("------------------------------ ESTAS SON MATERIAS QUE LE FALTA AL ALUMNO CON LA MATRICULA " + str("193228") + " -------------------------")
    for index, datos in listaMaterias.iterrows():
        if datos['Nombre'] not in materiasAprobadaAlumno:
            print(datos['Nombre'])

    inscripcion = materiasReinscribirse(dt, CLAVE, listaMaterias, materiasAprobadaAlumno)

    listaDependencias = getData(inscripcion,periodorReinscripcion(dt))

    if len(listaDependencias) != 0:
        for i in range(len(listaDependencias)):
            resultado = getDependencesByName(getRelations(), listaDependencias[i]['nombreMateria'])
            lm.append(listaDependencias[i]['nombreMateria'])
            lista.append(resultado)

        relaciones = getRelation(lista)
        listaMaterias = getMaterias()

        if not relaciones.empty:
            b = calcularRutaCritica(relaciones, listaMaterias)
            print(b.get_critical_path())
            print("YA QUEDO INSCRIPCION")
        else:
            print( "No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> " + random.choice(lm))
            print("YA QUEDO Inscripcion")

    else:
        df = pd.DataFrame(inscripcion)
        materias = df['materia'].values.flatten().tolist()
        print("No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> " + random.choice(materias))
        print("YA QUEDO Inscripcion")


    '''dt = datetime.datetime.today().month
    #print(dt)
    listaMaterias = materiasAbiertasReinscripcion(dt,CLAVE)
    #print(listaMaterias)
    print("------------------------------ ESTAS SON MATERIAS DISPONIBLES PARA EL SIGUIENTE PERIODO " + str(periodorReinscripcion(dt)) + "-------------------------")

    listaMateriasAbiertasNuevoCuatri = materiasAbiertasReinscripcion(dt, CLAVE)
    print(listaMateriasAbiertasNuevoCuatri)

    #materiasAlumno, aprobado, reprobado = obtencionDatosAlumno(ventana, matriculaAlumno)

    print("------------------------------ ESTAS SON MATERIAS QUE PUEDE TOMAR PARA EL PERIODO " + str(periodorReinscripcion(dt)) + "-------------------------")

    #inscripcion = materiasReinscribirse(dt, CLAVE, listaMateriasAbiertasNuevoCuatri, materiasAprobadaAlumno)
    #print(inscripcion)

    print("----------------------------------- Ruta Critica --------------------------------- ")
    getData(str(periodorReinscripcion(dt)))

    # getData(inscripcion)
    # for i in range(len(inscripcion)):
    # getData(inscripcion[i])

    for i in range(len(materiasCursadaAlumno)):
        if materiasCursadaAlumno[i] in materiasDisponibles:
            print(materiasCursadaAlumno[i])

    # print(aprobado)
    # print(listaMateriasAbiertas)

    # for i in range(len(materiasAlumno)):
    #    print("Nombre: "+str(materiasAlumno['Nombre'][i])+"   Periodo: "+str(materiasAlumno['periodo'][i])+"   Final: "+str(materiasAlumno['Final'][i])+"   Aprobado: "+str(materiasAlumno['Aprobado'][i]))

    # print(materiasAlumno)
    # print(aprobado)
    # print(reprobado)

    for index, datos in reprobado.iterrows():
        if datos['Nombre'] in materiasDisponibles:
            print(datos)'''

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

def criticalPath():
    print()

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # crea un objeto de aplicación (Argumentos de sys)
    window = MyApp()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()