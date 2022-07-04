import pandas as pd
from src.Services.dbConnect import conexionBd
import warnings
warnings.filterwarnings("ignore")
from criticalpath import Node
import datetime

def getDicc(periodo):
    periodo = str(int(periodo)+1)
    conexion = conexionBd()
    #dataframe = pd.read_sql("select * from d_materia where periodo = 2 and planEstudiosID = 28 or TipoPrerequisito = 'PM' and Periodo = "+periodo+ " and planEstudiosID = 28", con=conexion)
    dataframe = pd.read_sql('select * from d_materia where TipoPrerequisito = "PM" and Periodo = ' + periodo,con=conexion)
    listaMaterias = []
    for index, df in dataframe.iterrows():
        try:
            preRequisito = df['Prerequisito'].split("|")
            preRequisito = sorted([i for i in preRequisito if i])
            sql_list = str(tuple([key for key in preRequisito])).replace(',)', ')')
            consulta = pd.read_sql("""SELECT Nombre FROM d_materia WHERE MateriaID IN {sql_list}""".format(sql_list=sql_list),con=conexion).values.flatten().tolist()
            materiaDependiente = (','.join(consulta))
        except:
            preRequisito = None
            materiaDependiente = None

        diccionario = {
            "idMateria": df['MateriaID'],
            "idPlanEstudios": df['PlanEstudiosID'],
            "nombre": df['Nombre'],
            "creditos": df['Creditos'],
            "horasSemana": df['HorasSemana'],
            "totalHoras": df['TotalHoras'],
            "preRequisito": preRequisito,
            "periodo": df['Periodo'],
            #"dependencias": (df['Nombre'],materiaDependiente),
            "materiaDependiente": materiaDependiente,
            "duracion": int(df["TotalHoras"]) / int(df["HorasSemana"])
            #"dependencias": (df['Nombre'],consulta)
        }
        listaMaterias.append(diccionario)
    return listaMaterias

'''def getRelations(diccionario):
    l = []
    for i in range(len(diccionario)):
        dicc = {
            "nombreMateria":diccionario[i]['nombre'],
            "materiaDepende":diccionario[i]['materiaDependiente'],
            "duracion":int(diccionario[i]["totalHoras"])/int(diccionario[i]["horasSemana"])
        }
        l.append(dicc)
    df = pd.DataFrame(l)
    return df'''

def getCriticalPath(datos):
    # Crear el proyecto "p"
    p = Node('proyecto')
    '''tarea = [("A", {"duracion": 3}),
              ("B", {"duracion": 2}),
              ("C", {"duracion": 4}),
              ("D", {"duracion": 3}),
              ("E", {"duracion": 2}),
              ("F", {"duracion": 4}),
              ("G", {"duracion": 2}),
              ("H", {"duracion": 1}),
              ("I", {"duracion": 2}),
              ("J", {"duracion": 4})]

    dependencia = [("A", "E"),
                    ("B", "E"),
                    ("E", "F"),
                    ("F", "G"),
                    ("G", "I"),
                    ("I", "J"),
                    ("C", "J"),
                    ("H", "I"),
                    ("D", "H")]


    print(tarea)
    print(dependencia)'''

    tareas = []

    for i in range(len(datos)):
        x = (datos[i]['nombre'],{"duracion": int(datos[i]['duracion'])})
        tareas.append(x)

    dependencias = []

    for i in range(len(datos)):
        y = (datos[i]['nombre'],datos[i]['materiaDependiente'])
        dependencias.append(y)

    print(tareas)
    print(dependencias)


    # Cargar al proyecto las tareas y sus duraciones
    for i in tareas:
        p.add(Node(i[0], duration=i[1]["duracion"]))

    # Cargar al proyecto sus dependencias (secuencias)
    for j in dependencias:
        p.link(j[0], j[1])

    # Actualizar el proyecto:
    p.update_all()

    print(p.get_critical_path())
    print(p.duration)