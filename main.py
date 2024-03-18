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

    #Leemos el mismo archivo con los datos requeridos para esta funcion
    df_api1_merged = pd.read_parquet("./data/df_api1.parquet")
    
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


# Endpoint de la función UserForGenre 
@app.get('/UserForGenre')
def UserForGenre(genero: str):

    #Leemos el mismo archivo con los datos requeridos para esta funcion
    df_api2_merged = pd.read_parquet("./data/df_api2.parquet")

    '''
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

    Args:
        genero (str): Nombre del genero de interes.
    
    Returns:
        Ejemplo de retorno: Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}]} 
    '''

    # Se cambia a letra minuscula el valor de genero ingresado
    genero = genero.lower()

    # Filtramos el dataframe con solo las filas que contengan el genero buscado (que est dentro de una lista en la columna genres)
    def buscar_genero(genres_lista, genero_buscar):
        return genero_buscar in genres_lista

    df_api2_genres = df_api2_merged[df_api2_merged['genres'].apply(buscar_genero, genero_buscar=genero)]
    #print(df_api2_genres['genres'].value_counts())

    # Calculamos las horas jugadas por usuario
    horas_por_usuario = df_api2_genres.groupby('user_id')['playtime_forever'].sum()/60
    #print(horas_por_usuario)
    
    # Encontramos el usuario con más horas jugadas
    usuario_mas_horas = horas_por_usuario.idxmax()
    max_horas = horas_por_usuario.max()
    #print(usuario_mas_horas, max_horas)

    # Obtenemos las horas jugadas por año
    horas_por_ano_usuario_mas_horas = df_api2_genres[df_api2_genres['user_id'] == usuario_mas_horas].groupby('year')['playtime_forever'].sum()/60
    #print(horas_por_ano_usuario_mas_horas)

    # Convertir las horas jugadas por año a un formato de lista de diccionarios
    horas_por_ano_usuario_mas_horas = horas_por_ano_usuario_mas_horas.reset_index().to_dict(orient='records')
    #print(horas_por_ano_usuario_mas_horas)

    # Para presentar el resultado en el formato solicitado 
    horas_por_ano_str = ", ".join([f"{{Año: {registro['year']}, Horas: {int(registro['playtime_forever'])}}}" for registro in horas_por_ano_usuario_mas_horas if int(registro['playtime_forever']) != 0])

    # Imprimir el resultado
    resultado = f"Usuario con más horas jugadas para Género {genero} es: {usuario_mas_horas}, \"Horas jugadas\":[{horas_por_ano_str}]"

    return resultado


# Endpoint de la función UsersRecommend 
@app.get('/UsersRecommend')
def UsersRecommend(año: int):

    #Leemos el mismo archivo con los datos requeridos para esta funcion
    df_api3_merged = pd.read_parquet("./data/df_api3.parquet")

    '''
    Debe devolver Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

    Args:
        año (int): Año de interes.
    
    Returns:
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''

    # Filtramos los datos por el año indicado
    df_api3_merged = df_api3_merged[df_api3_merged['year'] == año]

    # Calculamos la suma de sentimientos por juego
    sentimiento_por_juego = df_api3_merged.groupby('title')['sentimiento_etiqueta'].sum()

    # Seleccionamos los tres juegos con los puntajes más altos (ordenados de mayor a menor)
    top_juegos = sentimiento_por_juego.nlargest(3)

    # Obtenemos los nombres de los juegos
    nombres_top_juegos = top_juegos.index.tolist()

    # Imprimir el resultado en el formato solicitado
    resultado = [{"Puesto {}: {}".format(i+1, juego)} for i, juego in enumerate(nombres_top_juegos)]

    return resultado


# Endpoint de la función UsersNoRecommend 
@app.get('/UsersNotRecommend')
def UsersNotRecommend(año: int):

    #Leemos el mismo archivo generado para la funcion anterior ya que contine la informacion requerida para esta funcion
    df_api4_merged = pd.read_parquet("./data/df_api3.parquet")

    '''
    Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.

    Args:
        año (int): Año de interes.
    
    Returns:
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''
    # Filtramos los datos por el año indicado
    df_api4_merged = df_api4_merged[df_api4_merged['year'] == año]

    # Calculamos el número de veces que la columna 'sentimiento_etiqueta' tiene un valor de cero
    puntaje_cero_por_juego = df_api4_merged.groupby('title')['sentimiento_etiqueta'].apply(lambda x: (x == 0).sum())

    # Seleccionamos los tres juegos con menos recomendacion 
    last_juegos = puntaje_cero_por_juego.nlargest(3)
    #print(last_juegos)

    # Obtenemos los nombres de los juegos
    nombres_last_juegos = last_juegos.index.tolist()

    # Imprimir el resultado en el formato solicitado
    resultado = [{"Puesto {}: {}".format(i+1, juego)} for i, juego in enumerate(nombres_last_juegos)]

    return resultado


# Endpoint de la función UsersRecommend3 
@app.get('/sentiment')
def sentiment(año: int):

    #Leemos el mismo archivo con los datos requeridos para esta funcion
    df_api5_merged = pd.read_parquet("./data/df_api5.parquet")

    # Filtramos los datos por el año indicado
    df_api5_merged = df_api5_merged[df_api5_merged['year'] == año]

    # Contamos el número de veces que se repiten los valores en la columna 'sentimiento_etiqueta'
    # conteo_valores = df_api5_merged['sentimiento_etiqueta'].value_counts()
    conteo_valores = df_api5_merged['sentimiento_etiqueta'].value_counts().to_dict()

    # Creamos la lista con el formato deseado
    # resultado = {'Negative': conteo_valores.get(0, 0), 'Neutral': conteo_valores.get(1, 0), 'Positive': conteo_valores.get(2, 0)}
    resultado = {'Valor {}'.format(k): conteo_valores.get(k, 0) for k in range(3)}

    #resultado = 'hola2'

    return resultado

