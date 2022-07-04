import datetime
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from src.Controller.datosAlumnado import *
from src.Controller.reinscripcionCuatri import *
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
    #Index(['Matricula', 'Nombre', 'materiaid', 'fechaperiodoid', 'periodo','Final', 'Aprobado'], #ruta critica
    try:
        pd.options.display.width = 0
        matriculaAlumno = int(ventana.matricula.toPlainText())
        dt = datetime.datetime.today().month
        listaMateriasAbiertas = materiasAbiertasActuales(dt, CLAVE)
        materiasAlumno, aprobado, reprobado = obtencionDatosAlumno(ventana,matriculaAlumno)
        materiasDisponibles = listaMateriasAbiertas['Nombre'].values.tolist()
        materiasAprobadaAlumno = aprobado['Nombre'].values.tolist()

        print("------------------------------ ESTAS SON MATERIAS DISPONIBLES PARA EL PERIODO ACTUAL "+str(periodoActual(dt))+" ------------------------------------------")
        print(listaMateriasAbiertas)
        print("------------------------------ ESTAS SON MATERIAS QUE YA APROBO EL ALUMNO CON LA MATRICULA "+str(matriculaAlumno)+" -------------------------")
        print(aprobado)
        print("------------------------------ ESTAS SON MATERIAS QUE DEBE EL ALUMNO CON LA MATRICULA "+str(matriculaAlumno)+" -------------------------")
        print(reprobado) #Para el estatus actual solamente

        print("------------------------------ ESTAS SON MATERIAS QUE LE FALTA AL ALUMNO CON LA MATRICULA "+str(matriculaAlumno)+" -------------------------")

        for index, datos in listaMateriasAbiertas.iterrows():
            if datos['Nombre'] not in materiasAprobadaAlumno:
                print("IDMATERIA: " + str(datos['materiaid']) + "    Nombre: " + str(datos['Nombre']) + "    Periodo: " + str(datos['Periodo']))

        print("------------------------------ ESTAS SON MATERIAS DISPONIBLES PARA EL SIGUIENTE PERIODO "+str(periodorReinscripcion(dt))+"-------------------------")

        listaMateriasAbiertasNuevoCuatri = materiasAbiertasReinscripcion(dt, CLAVE)
        print(listaMateriasAbiertasNuevoCuatri)

        print("------------------------------ ESTAS SON MATERIAS QUE PUEDE TOMAR PARA EL PERIODO "+str(periodorReinscripcion(dt))+"-------------------------")

        inscripcion = materiasReinscribirse(dt,CLAVE,listaMateriasAbiertas,materiasAprobadaAlumno)
        print(inscripcion)

        '''for i in range(len(materiasCursadaAlumno)):
            if materiasCursadaAlumno[i] in materiasDisponibles:
                print(materiasCursadaAlumno[i])'''

        #print(aprobado)
        #print(listaMateriasAbiertas)

        #for i in range(len(materiasAlumno)):
        #    print("Nombre: "+str(materiasAlumno['Nombre'][i])+"   Periodo: "+str(materiasAlumno['periodo'][i])+"   Final: "+str(materiasAlumno['Final'][i])+"   Aprobado: "+str(materiasAlumno['Aprobado'][i]))

        #print(materiasAlumno)
        #print(aprobado)
        #print(reprobado)

        '''for index, datos in reprobado.iterrows():
            if datos['Nombre'] in materiasDisponibles:
                print(datos)'''

    except:
        print("ocurrio un error")
        pass

def reinscripcion(ventana):
    dt = datetime.datetime.today().month
    #print(dt)
    listaMaterias = materiasAbiertasReinscripcion(dt,CLAVE)
    #print(listaMaterias)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # crea un objeto de aplicación (Argumentos de sys)
    window = MyApp()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()