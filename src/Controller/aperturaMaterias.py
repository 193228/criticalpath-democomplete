import pandas as pd
from src.Services.dbConnect import conexionBd
from src.Services.querys import queryAperturaMaterias

def materiasAbiertasActuales(mes,clave):
    enero_abril = [1, 2, 4, 5, 6, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if 1 <= mes  <= 4:
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril,clave), con=conexionBd())

    if 5 <= mes <= 8:
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto,clave), con=conexionBd())

    if 9 <= mes <= 12:
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre,clave), con=conexionBd())

    return resultado

def materiasAbiertasReinscripcion(mes,clave):
    enero_abril = [1, 2, 4, 5, 6, 8, 10]
    mayo_agosto = [2, 3, 5, 6, 8, 9]
    septiembre_diciembre = [1, 3, 4, 6, 7, 9, 10]

    if 1 <= mes  <= 4:
        resultado = pd.read_sql(queryAperturaMaterias(mayo_agosto,clave), con=conexionBd())

    if 5 <= mes <= 8:
        resultado = pd.read_sql(queryAperturaMaterias(septiembre_diciembre,clave), con=conexionBd())

    if 9 <= mes <= 12:
        resultado = pd.read_sql(queryAperturaMaterias(enero_abril,clave), con=conexionBd())

    return resultado