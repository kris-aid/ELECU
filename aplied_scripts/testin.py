

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



def recuperar_provincias(input_folder):

    '''
        Recupera todas los diccionarios de provincias de las elecciones y coloca los en un dataframe
        Se cambian las columnas para que no tengan caracteres especiales
        
        Paramaters
        ----------
            - input_folder: str 
                path al directorio que contiene los archivos .csv
        
        Returns
        -------
            - df_provincias: DataFrame
                DataFrame con los códigos de provincias de las elecciones
        
        Examples
        --------
        recuperar_provincias("data_csv")
             
        '''
    # Crear un DataFrame vacío
    df_provincias = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "provincias"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("provincias"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Provincias están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["PROVINCIA_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["PROVINCIA_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_provincias = pd.concat([df_provincias, df])
    return df_provincias

def crear_df_provincias(df_provincias):
    '''
    Crea un data frame con el nombre de la PROVINCIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PROVINCIA_NOMBRE en ese año.
    Si no hay código para esa PROVINCIA_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_provincias: DataFrame
            DataFrame con los códigos de provincias de las elecciones
    
    Returns
    -------
        - df_provincias_std: DataFrame
            DataFrame con el nombre de la PROVINCIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PROVINCIA_NOMBRE en ese año
    
    Examples
    --------
    crear_df_provincias(df_provincias)
         
    '''
    # Crear un DataFrame vacío
    df_provincias_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_provincias.iterrows():
        # Revisar si la PROVINCIA_NOMBRE ya está en el dataframe
        if row["PROVINCIA_NOMBRE"] not in df_provincias_std.index:
            # Si la PROVINCIA_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_provincias_std.loc[row["PROVINCIA_NOMBRE"], row["ANIO"]] = row["PROVINCIA_CODIGO"]
        else:
            # Si la PROVINCIA_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_provincias_std.loc[row["PROVINCIA_NOMBRE"], row["ANIO"]] = row["PROVINCIA_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_provincias_std = df_provincias_std.reindex(sorted(df_provincias_std.columns), axis=1)
    # Colocar las filas en orden
    df_provincias_std = df_provincias_std.sort_index()
    return df_provincias_std



def recuperar_cantones(input_folder):
    '''
    Recupera todas los diccionarios de cantones de las elecciones y coloca los en un dataframe
    Se cambian las columnas para que no tengan caracteres especiales
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_cantones: DataFrame
            DataFrame con los códigos de cantones de las elecciones
    
    Examples
    --------
    recuperar_cantones("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_cantones = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "cantones"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("cantones"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Cantones están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["CANTON_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["CANTON_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_cantones = pd.concat([df_cantones, df])
    return df_cantones

def crear_df_cantones(df_cantones):
    '''
    Crea un data frame con el nombre de la CANTON_NOMBRE y columnas para cada año con el código que le corresponde a esa CANTON_NOMBRE en ese año.
    Si no hay código para esa CANTON_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_cantones: DataFrame
            DataFrame con los códigos de cantones de las elecciones
    
    Returns
    -------
        - df_cantones_std: DataFrame
            DataFrame con el nombre de la CANTON_NOMBRE y columnas para cada año con el código que le corresponde a esa CANTON_NOMBRE en ese año
    
    Examples
    --------
    crear_df_cantones(df_cantones)
         
    '''
    # Crear un DataFrame vacío
    df_cantones_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_cantones.iterrows():
        # Revisar si la CANTON_NOMBRE ya está en el dataframe
        if row["CANTON_NOMBRE"] not in df_cantones_std.index:
            # Si la CANTON_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_cantones_std.loc[row["CANTON_NOMBRE"], row["ANIO"]] = row["CANTON_CODIGO"]
        else:
            # Si la CANTON_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_cantones_std.loc[row["CANTON_NOMBRE"], row["ANIO"]] = row["CANTON_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_cantones_std = df_cantones_std.reindex(sorted(df_cantones_std.columns), axis=1)
    # Colocar las filas en orden
    df_cantones_std = df_cantones_std.sort_index()
    return df_cantones_std

# Por lo pronto solo se estudia el codigo de la parroquia, no el canton ni la provincia
def recuperar_parroquias(input_folder):
    '''
    Recupera todas los diccionarios de parroquias de las elecciones y coloca los en un dataframe
    Se cambian las columnas para que no tengan caracteres especiales
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_parroquias: DataFrame
            DataFrame con los códigos de parroquias de las elecciones
    
    Examples
    --------
    recuperar_parroquias("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_parroquias = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "parroquias"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("parroquias"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Parroquias están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["PARROQUIA_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["PARROQUIA_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_parroquias = pd.concat([df_parroquias, df])
    return df_parroquias

def crear_df_parroquias(df_parroquias):
    '''
    Crea un data frame con el nombre de la PARROQUIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PARROQUIA_NOMBRE en ese año.
    Si no hay código para esa PARROQUIA_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_parroquias: DataFrame
            DataFrame con los códigos de parroquias de las elecciones
    
    Returns
    -------
        - df_parroquias_std: DataFrame
            DataFrame con el nombre de la PARROQUIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PARROQUIA_NOMBRE en ese año
    
    Examples
    --------
    crear_df_parroquias(df_parroquias)
         
    '''
    # Crear un DataFrame vacío
    df_parroquias_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_parroquias.iterrows():
        # Revisar si la PARROQUIA_NOMBRE ya está en el dataframe
        if row["PARROQUIA_NOMBRE"] not in df_parroquias_std.index:
            # Si la PARROQUIA_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_parroquias_std.loc[row["PARROQUIA_NOMBRE"], row["ANIO"]] = row["PARROQUIA_CODIGO"]
        else:
            # Si la PARROQUIA_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_parroquias_std.loc[row["PARROQUIA_NOMBRE"], row["ANIO"]] = row["PARROQUIA_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_parroquias_std = df_parroquias_std.reindex(sorted(df_parroquias_std.columns), axis=1)
    # Colocar las filas en orden
    df_parroquias_std = df_parroquias_std.sort_index()
    return df_parroquias_std




# df_dignidades = recuperar_dignidades(input_folder)
# print(df_dignidades)
# df_dignidades_std = crear_df_dignidades(df_dignidades)
# print(df_dignidades_std)


# df_provincias = recuperar_provincias(input_folder)
# print(df_provincias)
# df_provincias_total=crear_df_provincias(df_provincias)
# print(df_provincias_total)
# df_provincias_total.to_csv("data_csv/Codigos_estandar/provincias_total.csv", index=True, header=True)


# df_cantones = recuperar_cantones(input_folder)
# #print(df_cantones)
# df_cantones_total=crear_df_cantones(df_cantones)
# print(df_cantones_total)
# df_cantones_total.to_csv("data_csv/Codigos_estandar/cantones_total.csv", index=True, header=True)

# df_parroquias=recuperar_parroquias(input_folder)
# #print(df_parroquias)
# df_parroquias_total=crear_df_parroquias(df_parroquias)
# print(df_parroquias_total)
# df_parroquias_total.to_csv("data_csv/Codigos_estandar/parroquias_total.csv", index=True, header=True)


#TODO: revisar las provincias a las que pertenecen los cantones por año
#TODO: revisar si hay parroquias que no pertenecen a un cantón
#TODO: revisar si hay parroquias que no pertenecen a una provincia

def recuperar_info(input_folder,dictionary_to_use, columns_to_preserve, column_to_study):
    '''
    Recupera todas los diccionarios de códigos de las elecciones y coloca los en un dataframe
    Se cambian los nombres de las columnas para que no tengan caracteres especiales
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
        - dictionary_to_use: str
            nombre del archivo que se quiere recuperar
        - columns_to_preserve: list
            lista con los nombres de las columnas que se quieren mantener
       
            
    
    Returns
    -------
        - df_info: DataFrame
            DataFrame con los códigos de la columna que se quiere recuperar el código
    
    Examples
    --------
    recuperar_info("data_csv", "dignidades", ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"], "DIGNIDAD_CODIGO")
         
    '''
    # Crear un DataFrame vacío
    df_info = pd.DataFrame()
    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith(dictionary_to_use):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    print(file_path)
                    df = pd.read_csv(file_path,low_memory=False)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #el valor de las columnas deben ser strings
                    df = df.map(str)
                    
                    #if the df has NaN values, replace them with a string "SIN INFORMACION"
                    df.fillna("SIN INFORMACION", inplace=True)
                    
                    #Los nombres y ambitos de las dignidades están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in columns_to_preserve else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in columns_to_preserve else x)
                    
                    
                    #drop columns that are not in columns_to_preserve and are not the column to study
                    columns_to_drop = [col for col in df.columns if col not in columns_to_preserve and col != column_to_study]
                    df = df.drop(columns_to_drop, axis=1)
                    #añadir el año de la elección al DataFrame
                    print(file)
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_info = pd.concat([df_info, df])
    df_info.fillna("SIN INFORMACION", inplace=True)                
    return df_info

def crear_df_info(df_info, column_to_study, column_to_use):
    '''
    Crea un data frame con el nombre de la columna que se quiere recuperar el código y ámbito geográfico.
    Y se van a crear columnas para cada año con el código que le corresponde a esa columna en ese año.
    Si no hay código para esa columna en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_info: DataFrame
            DataFrame con los códigos de la columna que se quiere recuperar el código
        - column_to_study: str
            nombre de la columna que se está estudiando
        - column_to_use: str
            nombre de la columna que se quiere recuperar el código
    
    Returns
    -------
        - df_info_std: DataFrame
            DataFrame con el nombre de la columna que se quiere recuperar el código y ámbito geográfico y columnas para cada año con el código que le corresponde a esa columna en ese año
    
    Examples
    --------
    crear_df_info(df_info, ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"], "DIGNIDAD_CODIGO")
         
    '''
    # Crear un DataFrame vacío
    df_info_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_info.iterrows():
        #Print something to check that it is running
        print(row["ANIO"])
        # Revisar si la columna que se quiere recuperar el código ya está en el dataframe
        if row[column_to_study] not in df_info_std.index:
            # Si la columna que se quiere recuperar el código no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_info_std.loc[row[column_to_study], row["ANIO"]] = row[column_to_use]
        else:
            # Si la columna que se quiere recuperar el código ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_info_std.loc[row[column_to_study], row["ANIO"]] = row[column_to_use]
    
    # Colocar las columnas de los años en orden
    df_info_std = df_info_std.reindex(sorted(df_info_std.columns), axis=1)
    # Colocar las filas en orden
    df_info_std = df_info_std.sort_index()
    return df_info_std

# df_cantones_provincia_codigo=recuperar_info(input_folder, "cantones", ["CANTON_NOMBRE"],"CANTON_CODIGO")
# print(df_cantones_provincia_codigo)
# df_cantones_provincia_codigo_std=crear_df_info(df_cantones_provincia_codigo, "CANTON_CODIGO", "CANTON_NOMBRE")
# print(df_cantones_provincia_codigo_std)
# df_cantones_provincia_codigo_std.to_csv("data_csv/Codigos_estandar/codigo_vs_canton.csv", index=True, header=True)

# df_candidatos_nombre_anio=recuperar_info(input_folder, "candidatos", ["CANDIDATO_NOMBRE","CANDIDATO_EDAD","DIGNIDAD_CODIGO","DIGNIDAD_NOMBRE"],"CANDIDATO_CODIGO")
# print(df_candidatos_nombre_anio)
# df_candidatos_nombre_anio.to_csv("data_csv/Codigos_estandar/candidatos/1_candidatos_nombre_anio.csv", index=False, header=True)
# df_parroquias_codigo=recuperar_info(input_folder, "parroquias", ["PARROQUIA_NOMBRE"],"CANTON_NOMBRE")
# print(df_parroquias_codigo)
# df_parroquias_codigo_std=crear_df_info(df_parroquias_codigo, "PARROQUIA_NOMBRE", "CANON_NOMBRE")
# print(df_parroquias_codigo_std)
# df_parroquias_codigo_std.to_csv("data_csv/Codigos_estandar/all_parroquias_vs_estado.csv", index=True, header=True)

# df_candidatos=recuperar_info(input_folder,"candidatos", ["CANDIDATO_NOMBRE"],"CANDIDATO_CODIGO")
# print(df_candidatos)
# df_candidatos.to_csv("data_csv/Codigos_estandar/candidatos/1_candidatos.csv", index=True, header=True)
# df_candidatos_std=crear_df_info(df_candidatos, "CANDIDATO_NOMBRE", "CANDIDATO_CODIGO")
# df_candidatos_std.to_csv("data_csv/Codigos_estandar/candidatos/candidatos_matrix.csv")

# df_organizaciones=recuperar_info(input_folder,"organizaciones_politicas", ["OP_NOMBRE","OP_AMBITO","OP_SIGLAS","OP_CODIGO"],"OP_SIGLA")
# print(df_organizaciones)
# df_organizaciones.to_csv("data_csv/Codigos_estandar/organizaciones/2_organizaciones.csv", index=True, header=True)
#df_organizaciones_std=crear_df_info(df_organizaciones, "OP_SIGLAS", "OP_NOMBRE")
#df_organizaciones_std.to_csv("data_csv/Codigos_estandar/organizaciones/2_organizaciones_matrix.csv")


def extract_unique_values_results(input_file,columnas_a_considerar):
    extracted_values = []
    df = pd.read_csv(input_file)
    # Using nunique() method
    num_unique_values = df['PARROQUIA_CODIGO'].nunique()
    #extraer dataframe con DIGNIDAD_CODIGO=6.0
    df_vocales = df[df['DIGNIDAD_CODIGO'] == 6.0]
    num_unique_values_6 = df_vocales['PARROQUIA_CODIGO'].nunique()
    print("Number of unique values in the column:", num_unique_values_6)
    # Columnas a considerar para identificar filas duplicadas
    print(df)
   # df.sort_values(by=columnas_a_considerar)
    #df.to_csv("data_csv/seccionales/2023/resultados/resultados_2023_v_1.csv")
    # Filtrar filas duplicadas basadas en las columnas especificadas
    df_filtrado= df.drop_duplicates(subset=columnas_a_considerar, keep='first')
    #ordenar
    #df_filtrado.sort_values(by=columnas_a_considerar, inplace=True)
    #print(df_filtrado)
    #df_filtrado.to_csv("data_csv/Codigos_estandar/resultados/resultados_duplicados_sec_2019.csv", index=False)
    # Mostrar el resultado
    return df_filtrado
columnas_a_considerar = ['DIGNIDAD_CODIGO', 'PROVINCIA_CODIGO', 'CANTON_CODIGO', 'CIRCUNSCRIPCION_CODIGO', 'PARROQUIA_CODIGO', 'BLANCOS', 'NULOS', 'JUNTA_SEXO']
#columnas_duplicated=['PARROQUIA_CODIGO', 'BLANCOS', 'NULOS', 'JUNTA_SEXO',]
#df_filtrado_1=extract_unique_values_results("data_csv/seccionales/2019/resultados/resultados_2019_v_1.csv",columnas_duplicated)
df_filtrado=extract_unique_values_results("data_csv/seccionales/2019/resultados/resultados_2019_v_1.csv",columnas_a_considerar)
#print(df_filtrado_1)
#print(df_filtrado)

#print(df_filtrado.columns)
def assign_unique_identifier(columnas_a_considerar, df):
    '''
    Asigna un identificador único a cada fila del DataFrame basado en las columnas especificadas.
    
    Parameters
    ----------
        - columnas_a_considerar: list
            Lista de nombres de columnas a considerar para identificar filas duplicadas.
        - df: DataFrame
            DataFrame con los datos a procesar.
    
    Returns
    -------
        - df_con_id: DataFrame
            DataFrame con un identificador único asignado a cada fila.
    
    Examples
    --------
    assign_unique_identifier(['DIGNIDAD_CODIGO', 'PROVINCIA_CODIGO', 'CANTON_CODIGO', 'CIRCUNSCRIPCION_CODIGO', 'PARROQUIA_CODIGO', 'BLANCOS', 'NULOS', 'JUNTA_SEXO'], df)
    '''
    # Crear un identificador único basado en la columna de Parroquia
    df['ID'] = df["PARROQUIA_CODIGO"].astype(str) + "_"+ df["JUNTA_SEXO"].astype(str)
    # drop the columns that are not the considered columns
    
    columns_to_drop = [col for col in df.columns if col not in columnas_a_considerar and col != "ID" and col != "SUFRAGANTES" and col != "CICUNSCRIPCION_NOMBRE"]
    df_con_id = df.drop(columns_to_drop, axis=1)
    #colocar la columna ID al principio
    df_con_id = df_con_id[['ID'] + [col for col in df_con_id.columns if (col != 'ID')]]
    return df_con_id

df_con_id = assign_unique_identifier(columnas_a_considerar, df_filtrado)
#df_con_id.to_csv("data_csv/Codigos_estandar/resultados/resultados_2019_sec_v_1_con_id.csv", index=False)
#find the row that match the PARROQUIA_NOMBRE

#conservar:
#DIGNIDAD_CODIGO,PARROQUIA_CODIGO,CIRUSCRIPCION_CODIGO,JUNTA_SEXO,BLANCOS,NULOS,SUFRAGANTES

#conservar=['DIGNIDAD_CODIGO', 'CIRCUNSCRIPCION_CODIGO','CIRCUNSCRIPCION_NOMBRE', 'PARROQUIA_CODIGO','JUNTA_SEXO', 'BLANCOS', 'NULOS', 'SUFRAGANTES', 'ID']

#drop other columns
#df_con_id = df_con_id[conservar]
#df_con_id.sort_values(by=["ID",'DIGNIDAD_CODIGO'], inplace=True)

#print(df_con_id)


def find_row(df, column, value):
    '''
    Encuentra la fila en un DataFrame que coincide con un valor específico en una columna.
    
    Parameters
    ----------
        - df: DataFrame
            DataFrame con los datos a procesar.
        - column: str
            Nombre de la columna en la que buscar el valor.
        - value: str
            Valor a buscar en la columna.
    
    Returns
    -------
        - row: Series
            Fila que coincide con el valor especificado.
    
    Examples
    --------
    find_row(df, 'PARROQUIA_NOMBRE', 'SAN ANTONIO')
    '''
    rows = df[df[column] == value]
    return rows

#Extract the the rows of the same DIGNIDAD_CODIGO
df_1=find_row(df_filtrado, 'JUNTA_SEXO', 'F')

print(df_1)
df2=find_row(df_1,'DIGNIDAD_CODIGO', 6.0 )
print(df2)


#df_1=find_row(df_filtrado, 'PARROQUIA_NOMBRE', 'COMITE DEL PUEBLO')

#df_2=find_row(df_filtrado, 'ID', '7150.0_F')
#print(df_2)