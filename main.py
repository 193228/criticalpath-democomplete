import datetime
import os
import random
import sys
from multiprocessing import Process
from threading import Thread

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QRunnable, Qt, QThreadPool, QThread

from fastest import run_dash
from src.Controller.Graphs import graphStatusActual, graphReinscripcion
from src.Controller.datosAlumnado import *
from src.Controller.getDependencesByName import getDependencesByName, getMaterias, \
    calcularRutaCritica, getRelation
from src.Controller.graficos import graficoReinscripcion
from src.Controller.reinscripcionCuatri import *
from src.Model.relation_materies import getRelations
from src.View.vistaRutaCritica import Ui_MainWindow as ventanaPrincipal
import warnings
warnings.filterwarnings("ignore")
CLAVE = "004"

relaciones = ""

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
        materiasFaltantes = []

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

        '''print("------------------------------ ESTAS SON MATERIAS QUE HA TOMADO EL ALUMNO "+str(periodoActual(dt))+" ------------------------------------------")
        print(materiasAlumno)'''

        print("------------------------------ ESTAS SON MATERIAS QUE YA APROBO EL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        print(aprobado)

        '''print("------------------------------ ESTAS SON MATERIAS QUE DEBE EL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        print(reprobado) #Para el estatus actual solamente'''

        print("------------------------------ ESTAS SON MATERIAS QUE LE FALTA AL ALUMNO CON LA MATRICULA "+str("193228")+" -------------------------")
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                print(datos)
                faltantes = {
                    "nombre": datos['Nombre'],
                    "periodo": datos['Periodo']
                }
                materiasFaltantes.append(faltantes)
        listaMateriasFaltantes = pd.DataFrame(materiasFaltantes)

        print("------------------------------ ESTA ES LA RUTA CRITICA "+str("193228")+" -------------------------")

        lista = []; lm = []
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                resultado = getDependencesByName(getRelations(), datos['Nombre'])
                lm.append(datos['Nombre'])
                lista.append(resultado)

        relaciones = getRelation(lista)

        if not relaciones.empty:
            #b = calcularRutaCritica(relaciones, listaMaterias)
            #print(b.get_critical_path())
            print("YA QUEDO ESTATUS ACTUAL")
            graphStatusActual(aprobado, reprobado, listaMateriasFaltantes, relaciones, listaMateriasAbiertas, matriculaAlumno, periodoActual(dt))
        else:
            print("No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> "+random.choice(lm))
            print("YA QUEDO ESTATUS ACTUAL")
            graphStatusActual(aprobado, reprobado, listaMateriasFaltantes,relaciones,listaMateriasAbiertas, matriculaAlumno, periodoActual(dt))

    except:
        print("ocurrio un error")
        pass

def reinscripcion(ventana):
    try:
        lista = []; lm = [];  materiasFaltantes = []
        dt = datetime.datetime.today().month

        matriculaAlumno = int(ventana.matricula.toPlainText())

        listaMateriasAbiertas = materiasAbiertasReinscripcion(dt, CLAVE)

        materiasAlumno, aprobado, reprobado = obtencionDatosAlumno(ventana, matriculaAlumno)

        # Obtengo materias aprobadas por el alumno
        materiasAprobadaAlumno = aprobado['Nombre'].values.tolist()

        print("------------------------------ ESTAS SON MATERIAS QUE LE FALTA AL ALUMNO CON LA MATRICULA " + str("193228") + " -------------------------")
        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                faltantes = {
                    "nombre": datos['Nombre'],
                    "periodo": datos['Periodo']
                }
                materiasFaltantes.append(faltantes)

        listaMateriasFaltantes = pd.DataFrame(materiasFaltantes)

        inscripcion = materiasReinscribirse(dt, CLAVE, listaMateriasAbiertas, materiasAprobadaAlumno)
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
                graphReinscripcion(aprobado,reprobado,listaMateriasFaltantes, relaciones, listaMateriasAbiertas,matriculaAlumno, periodorReinscripcion(dt))
            else:
                print( "No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> " + random.choice(lm))
                print("YA QUEDO Inscripcion")
                graphReinscripcion(aprobado,reprobado,listaMateriasFaltantes, relaciones, listaMateriasAbiertas,matriculaAlumno,periodorReinscripcion(dt))

        else:
            df = pd.DataFrame(inscripcion)
            materias = df['materia'].values.flatten().tolist()
            print("No se registro ninguna materia dependiente. No existe ruta Critica. Agarre cualquier materia que le falte -> " + random.choice(materias))
            graphReinscripcion(aprobado, reprobado, listaMateriasFaltantes, pd.DataFrame(), listaMateriasAbiertas, matriculaAlumno, periodorReinscripcion(dt))

    except:
        print("Ocurrio un error")
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # crea un objeto de aplicación (Argumentos de sys)
    window = MyApp()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()