

import os
import pandas as pd
import numpy as np
import re
import sys
import shutil
import unidecode

# Recuperar todas los diccionarios de dignidades de las elecciones y colocarlos en un dataframe

input_folder = "data_csv"

def recuperar_dignidades(input_folder):
    '''
    Recupera todas los diccionarios de dignidades de las elecciones y coloca los en un dataframe
    Se cambian los nombres de las columnas para que no tengan caracteres especiales
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_dignidades: DataFrame
            DataFrame con los códigos de dignidades de las elecciones
    
    Examples
    --------
    recuperar_dignidades("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_dignidades = pd.DataFrame()
    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("dignidades"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres y ambitos de las dignidades están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"] else x)
                    
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_dignidades = pd.concat([df_dignidades, df])
    return df_dignidades

df_dignidades = recuperar_dignidades(input_folder)
print(df_dignidades)

# Ahora vamos a crear un data frame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico.
# Y se van a crear columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año.
# Si no hay código para esa DIGNIDAD_NOMBRE en ese año, se va a colocar un NaN
#comprobar si la DIGNIDAD_NOMBRE ya está en el dataframe y si no está, agregarla.
# Si la DIGNIDAD_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
# Si la DIGNIDAD_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección

def crear_df_dignidades(df_dignidades):
    '''
    Crea un data frame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico.
    Y se van a crear columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año.
    Si no hay código para esa DIGNIDAD_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_dignidades: DataFrame
            DataFrame con los códigos de dignidades de las elecciones
    
    Returns
    -------
        - df_dignidades_std: DataFrame
            DataFrame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico y columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año
    
    Examples
    --------
    crear_df_dignidades(df_dignidades)
         
    '''
    # Crear un DataFrame vacío
    df_dignidades_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_dignidades.iterrows():
        # Revisar si la DIGNIDAD_NOMBRE ya está en el dataframe
        if row["DIGNIDAD_NOMBRE"] not in df_dignidades_std.index:
            # Si la DIGNIDAD_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], "DIGNIDAD_AMBITO"] = row["DIGNIDAD_AMBITO"]
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], row["ANIO"]] = row["DIGNIDAD_CODIGO"]
        else:
            # Si la DIGNIDAD_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], row["ANIO"]] = row["DIGNIDAD_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_dignidades_std = df_dignidades_std.reindex(sorted(df_dignidades_std.columns), axis=1)
    # Colocar las filas en orden
    df_dignidades_std = df_dignidades_std.sort_index()
    return df_dignidades_std

df_dignidades_std = crear_df_dignidades(df_dignidades)
print(df_dignidades_std)

