# Proyecto MLOps: Sistema de Recomendación de Videojuegos para Usuarios de Steam


## Descripción del Proyecto
- Teniendo como entrada 3 archivos JSON suministrados por la plataforma multinacional de videojuegos Steam con informacion acerca de videjuegos, jugadores y las reseñas de estos sobre los juegos
- Se genero un Producto Mínimo Viable que muestra una API deployada en un servicio en la nube y la aplicación de un modelo de Machine Learning que permiten realizar consultas sobre información relevante acerca de los videojuegos
- Se realizo un análisis de sentimientos sobre los comentarios de los usuarios de los juegos y, por otro lado, la recomendación de juegos similares a partir de dar el nombre de un juego

## Herramientas usadas
- Visual Studio Code como editor de codigo
- Python como lenguaje de programacion
- GitHub como repositorio del proyecto
- FastAPI como framework
- Render para hacer el deploy  y publicar en la web

## Etapas del Proyecto

### 1. ETL
En esta etapa de ingenieria de datos se realizo un proceso de ETL a partir de 3 archivos JSON con informacion acerca de los videjuegos, los jugadores y las reseñas de estos:

- australian_user_reviews.json: Contiene las reseñas de juegos realizadas por usuarios 
- output_steam_games.json: Este archivo proporciona información detallada sobre los juegos disponibles en la plataforma Steam. Incluye datos como géneros, etiquetas, especificaciones, desarrolladores, año de lanzamiento, precio y otros atributos relevantes de cada juego
- australian_users_items.json:  contiene información sobre los ítems relacionados con usuarios

Ver notebook: [Proceso de ETL y Resultado](https://github.com/dosoriofc/PI_ML_OPS/blob/main/ETL.ipynb)

### 2. EDA

Con los 3 archivos recibidos en formato JSON se comienza el proyecto realizando un analisis explotatorio en los Dataset para ver que decisiones tenemos que tomar para luego en el ETL hacer las transformacion necesarias para realizar las consultas y optimizar tanto el rendimiento de la API como el entrenamiento del modelo.

Para esto se utilizó la librería Pandas para la manipulación de los datos y las librerías Matplotlib para la visualización.

Ver notebook: [Proceso de EDA y Resultado](https://github.com/dosoriofc/PI_ML_OPS/blob/main/EDA.ipynb)

### 3. Feature Engineering
En el dataset user_reviews se incluyen reseñas de juegos hechos por distintos usuarios.  Se creo la columna sentiment_analysis aplicando análisis de sentimiento a las reseñas de los usuarios. Se utilizo la biblioteca NLTK (Natural Language Toolkit) con el analizador de sentimientos de Vader, que proporciona una puntuación compuesta que puede ser utilizada para clasificar la polaridad de las reseñas en negativas (valor '0'), neutrales (valor '1') o positivas (valor '2'). A las reseñas escritas ausentes, se les asignó el valor de '1'. 

Ver notebook: [Proceso de Feature Engineering y Resultado](https://github.com/dosoriofc/PI_ML_OPS/blob/main/FuncionesAPI.ipynb)

### 4. Desarrollo de API

Se desarrollo una API con FastAPI y se deployó en Render, que permite realizar cinco (5) consultas sobre información relevante acerca de los videojuegos:

1. **PlayTimeGenre( genero : str ):** Devuelve el año con mas horas jugadas para el género dado.
2. **UserForGenre( genero : str ):** Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
3. **UsersRecommend( año : int ):** Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
4. **UsersNotRecommend( año : int ):** Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
5. **sentiment_analysis( año : int ):** Según el año de lanzamiento, devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

Ver notebook: [APIs y Resultado](https://github.com/dosoriofc/PI_ML_OPS/blob/main/FuncionesAPI.ipynb)

### 5. Modelo de aprendizaje automático

Se realizo un modelo de machine learning para armar un sistema de recomendación. En este caso el input es un usuario y el output es una lista de 5 juegos que se le recomienda a ese usuario, en general se explican como “A usuarios que son similares a tí también les gustó…”

- **recomendacion_juego( id de usuario ):** Ingresando el id de usuario, se genera una lista con 5 juegos recomendados.

Ver notebook: [ML y Resultado](https://github.com/dosoriofc/PI_ML_OPS/blob/main/FuncionesAPI.ipynb)

## Resultados

### 1. Deploy
Para el deploy de la API en FastAPI se seleccionó la plataforma Render la cual permite el deploy desde GitHub.

Link: [API y ML](https://pi-ml-ops-rfu3.onrender.com/docs)

### 2. Video
Se publico un video en youtube con un breve explicacion del proyecto, la metodologia empleada y los resultados obtenidos

Link: [Video en Youtube](https://pi-ml-ops-rfu3.onrender.com/docs)
