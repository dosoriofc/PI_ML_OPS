from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import pandas as pd
import numpy as np  

#import pyarrow.parquet as pq

#from pydantic import BaseModel
#from dateutil import parser
#from typing import List
#import os

app = FastAPI()



# Endpoint de la función PlayTimeGenre 
@app.get('/PlayTimeGenre')
def PlayTimeGenre(genero: str):

    df_api1_merged = pd.read_parquet("df_api1.parquet")
    
    '''
    Esta funcion debe devolver año con mas horas jugadas para un género especificado. 

    Args
        genero (str): Nombre del genero de interes.
    
    Returns:
        Año con mas horas jugadas para dicho género. 
        Ejemplo de retorno: "Año de lanzamiento con más horas jugadas para Género X": 2013
    '''

    # Se cambia a letra minuscula el valor de genero ingresado
    genero = genero.lower()

    # Filtramos el dataframe con solo las filas que contengan el genero buscado (que est dentro de una lista en la columna genres)
    def buscar_genero(genres_lista, genero_buscar):
        return genero_buscar in genres_lista

    df_api1_genres = df_api1_merged[df_api1_merged['genres'].apply(buscar_genero, genero_buscar=genero)]
    
    # Agrupar por año y sumar las horas jugadas
    df_api1_grouped = df_api1_genres.groupby('year')['playtime_forever'].sum()
    
    # Encontrar el año con la suma máxima de horas jugadas
    anio_max_horas_jugadas = df_api1_grouped.idxmax()

    resultado=f"Año de lanzamiento con más horas jugadas para Género {genero} es: {anio_max_horas_jugadas}"
        
    return resultado


