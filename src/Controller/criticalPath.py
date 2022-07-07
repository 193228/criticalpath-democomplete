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
            "materiaDependiente": materiaDependiente,
            "duracion": int(df["TotalHoras"]) / int(df["HorasSemana"])
        }
        listaMaterias.append(diccionario)
    return listaMaterias