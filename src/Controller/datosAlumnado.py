import pandas as pd

from main import mostrarMensajes
from src.Services.dbConnect import conexionBd
from src.Services.querys import queryDatosAlumno


def obtencionDatosAlumno(ventana,matricula):
    materiasAlumno = pd.read_sql(queryDatosAlumno(matricula), con=conexionBd())
    if materiasAlumno.empty:
        mostrarMensajes(ventana,"Error. Matricula no registrada")
    else:
        listaMaterias = materiasAlumno.drop_duplicates(subset='Nombre', keep="last")
        lista_materias_aprobadas = listaMaterias.query("Aprobado == 2")
        lista_materias_reprobadas = listaMaterias.query("Aprobado == 1")
        return materiasAlumno, lista_materias_aprobadas, lista_materias_reprobadas