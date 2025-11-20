# Este script es para generar los diccionarios estandarizados de las dignidades, parroquias, cantones, provincias

# Path: create_std_dicts.py
from .constants import *
from .utils import *
import pandas as pd
import numpy as np
import re
import os
import unidecode
import importlib.resources
# #get the current directory
# current_directory = os.path.dirname(os.path.abspath(__file__))
# # establishes it as the current directory
# os.chdir(current_directory)
class Standard_Dictionaries:
    '''
    Clase para estandarizar los diccionarios de las elecciones
    
    Examples
    --------
    
    input_folder = "data_csv/seccionales/2023/diccionarios"
    std_dicts = Standard_Dictionaries(input_folder)
    std_dicts.change_to_std_dignidades()
    
    '''
    def __init__(self, input_folder,standarized_folder=None):
        '''
        Inicializa la clase
        Parameters
        ----------
            - input_folder: str 
                path al directorio que contiene los archivos .csv
            - standarized_folder: str
                path al directorio donde se encuentran los diccionarios estandarizados como csv
        '''
        if standarized_folder is None:
            self.standarized_folder = CODIGOS_ESTANDAR_PATH
        else:
            self.standarized_folder = standarized_folder
        
        self.input_folder = input_folder + "/diccionarios"
        self.df_dignidades = self.recuperar_dignidades()
        self.df_parroquias = self.recuperar_parroquias()
        self.df_cantones = self.recuperar_cantones()
        self.df_provincias = self.recuperar_provincias()

        
    def recuperar_dignidades(self):
        '''
        Recupera todas los diccionarios de dignidades de las elecciones y coloca los en un dataframe
        Se cambian las columnas para que no tengan caracteres especiales
        
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
        #De la carpeta, buscar el archivo que empieza con "dignidades"
        for root, dirs, files in os.walk(self.input_folder):
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
                        # if there is "DIGNIDADA_CODIGO_RESULTADOS" column, rename it to "DIGNIDAD_CODIGO"
                        if "DIGNIDADA_CODIGO_RESULTADOS" in df_dignidades.columns:
                            df_dignidades = df_dignidades.rename(columns={"DIGNIDADA_CODIGO_RESULTADOS": "DIGNIDAD_CODIGO"})
                        # stop the loop
                        return df_dignidades

        return df_dignidades

    def create_dict_mapping(self, df):
        '''
        Crea un diccionario de mapeo a partir de un DataFrame.

        Parameters
        ----------
            - df: pd.DataFrame
                DataFrame con varias columnas. La primera columna es el estandar y las demás columnas son equivalentes.

        Returns
        -------
            - mapping_dict: dict
                Diccionario con el mapeo de las columnas del DataFrame.
            '''
        # Initialize an empty dictionary to store the mapping
        mapping_dict = {}

        # Iterate over the columns of the DataFrame excluding the first one
        for column in df.columns[1:]:
            # Iterate over the rows of the DataFrame
            for index, row in df.iterrows():
                # If the value in the current cell is not "No especificado"
                if row[column] != "No especificado" or row[column] != None:
                    # Use the value in the first column as the key and the value in the current column as the value in the dictionary
                    mapping_dict[row[column]] = row[0]

        return mapping_dict
    def change_to_std_dignidades(self):
        '''
        Cambia los nombres y códigos de las dignidades a los nombres y códigos estandarizados
        
        Paramaters
        ----------
            - df_dignidades: DataFrame
                DataFrame con los códigos de dignidades de las elecciones
                
        
        Returns
        -------
            - df_dignidades: DataFrame
                DataFrame con los códigos de dignidades de las elecciones estandarizados    
    
        '''

        #Si el año es antes del 2007, vamos a usar el diccionario de las dignidades antes del 2007
        if self.df_dignidades["ANIO"].astype(int).max() < 2007:
            codigos_std=load_std_data("dignidades/std_dignidades_pre_2007.csv")
        # Si el año es después del 2007, vamos a usar el diccionario de las dignidades después del 2007    
        else:
            codigos_std=load_std_data("dignidades/std_dignidades_post_2007.csv")

        df_dignidades_names = load_std_data("dignidades/equivalencias_dignidades.csv")
        map_dignidades = self.create_dict_mapping(df_dignidades_names)
        self.df_dignidades['DIGNIDAD_NOMBRE'] = self.df_dignidades['DIGNIDAD_NOMBRE'].map(map_dignidades)

        # Vamos a hacer un left join con el DataFrame de las dignidades estandarizadas
        self.df_dignidades = self.df_dignidades.merge(codigos_std, on="DIGNIDAD_NOMBRE", how="left")
        # Y nos quedamos con los códigos estandarizados
        self.df_dignidades["DIGNIDAD_CODIGO"] = self.df_dignidades["DIGNIDAD_CODIGO_y"]
        self.df_dignidades["DIGNIDAD_AMBITO"] = self.df_dignidades["DIGNIDAD_AMBITO_x"]
        self.df_dignidades["DIGNIDAD_CODIGO_OLD"] = self.df_dignidades["DIGNIDAD_CODIGO_x"]
        #self.df_dignidades["DIGNIDAD_NOMBREs_OLD"] = self.df_dignidades["DIGNIDAD_NOMBRE"]
        # Eliminamos las columnas que no necesitamos
        self.df_dignidades = self.df_dignidades.drop(columns=["DIGNIDAD_CODIGO_x", "DIGNIDAD_CODIGO_y","DIGNIDAD_AMBITO_x","DIGNIDAD_AMBITO_y", "ANIO"])

    def recuperar_provincias(self):
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
        for root, dirs, files in os.walk(self.input_folder):
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
        return df_provincias
        
    def change_to_std_provincias(self):
        '''
        Cambia los nombres y códigos de las provincias a los nombres y códigos estandarizados
        
        Paramaters
        ----------
            - df_provincias: DataFrame
                DataFrame con los códigos de provincias de las elecciones
                
        
        Returns
        -------
            - df_provincias: DataFrame
                DataFrame con los códigos de provincias de las elecciones estandarizados    
    
        '''

        equivalencias_df=load_std_data("provincias/equivalencias_exterior.csv")
        dict_provincias = self.create_dict_mapping(equivalencias_df)
        # only map the provincias that are in the dictionary

        self.df_provincias["PROVINCIA_NOMBRE"] = self.df_provincias["PROVINCIA_NOMBRE"].map(lambda x: dict_provincias.get(x, x))
        provincias_std_df=load_std_data("provincias/std_provincias.csv")
        # Vamos a hacer un left join con el DataFrame de las provincias estandarizadas
        self.df_provincias = self.df_provincias.merge(provincias_std_df, on="PROVINCIA_NOMBRE", how="left")
        # Y nos quedamos con los códigos estandarizados
        self.df_provincias["PROVINCIA_CODIGO"] = self.df_provincias["PROVINCIA_CODIGO_y"]
        self.df_provincias["PROVINCIA_CODIGO_OLD"] = self.df_provincias["PROVINCIA_CODIGO_x"]
        # Eliminamos las columnas que no necesitamos
        self.df_provincias = self.df_provincias.drop(columns=["PROVINCIA_CODIGO_x", "PROVINCIA_CODIGO_y", "ANIO"])
        
    def recuperar_cantones(self):
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
        for root, dirs, files in os.walk(self.input_folder):
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
        return df_cantones    
    
    def change_to_std_cantones(self):
        '''
        Cambia los nombres y códigos de los cantones a los nombres y códigos estandarizados
        
        Paramaters
        ----------
            - df_cantones: DataFrame
                DataFrame con los códigos de cantones de las elecciones
                
        
        Returns
        -------
            - df_cantones: DataFrame
                DataFrame con los códigos de cantones de las elecciones estandarizados    
    
        '''
        # Si el año es antes del 2009 y después del 2023, vamos a usar el diccionario de los cantones antes del 2009
        if self.df_cantones["ANIO"].astype(int).max() < 2009 or self.df_cantones["ANIO"].astype(int).max() > 2013:
            df=load_std_data("cantones/std_cantones.csv")
        else:
            df=load_std_data("cantones/std_cantones_2009_2013.csv")
        # Vamos a hacer un left join con el DataFrame de los cantones estandarizados
        self.df_cantones["CANTON_CODIGO"] = self.df_cantones["CANTON_CODIGO"].astype(str)
        self.df_cantones = self.df_cantones.merge(df, left_on="CANTON_CODIGO",right_on="CANTON_CODIGO_OLD", how="left")
        #quitar las columnas que no necesitamos
        for col in self.df_cantones.columns:
            if col.endswith("_x"):
                self.df_cantones = self.df_cantones.drop(columns=[col])
        #drop Anio, caambiar y renombrar las columnas
        self.df_cantones = self.df_cantones.drop(columns=["ANIO"])
        for col in self.df_cantones.columns:
            if col.endswith("_y"):
                self.df_cantones = self.df_cantones.rename(columns={col:col[:-2]})
                
        return self.df_cantones
        
    def recuperar_parroquias(self):
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
        for root, dirs, files in os.walk(self.input_folder):
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
        return df_parroquias
    
    def change_to_std_parroquias(self):
        '''
        Cambia los nombres y códigos de las parroquias a los nombres y códigos estandarizados
        
        Paramaters
        ----------
            - df_parroquias: DataFrame
                DataFrame con los códigos de parroquias de las elecciones
                
        
        Returns
        -------
            - df_parroquias: DataFrame
                DataFrame con los códigos de parroquias de las elecciones estandarizados    
    
        '''
        # Si el año es antes del 2019 se avisa que no está estandarizado

        
        if self.df_parroquias["ANIO"].astype(int).max() >= 2019:
            df = load_std_data("parroquias/std_parroquias.csv")
            print("Está estandarizado")
        elif self.df_parroquias["ANIO"].astype(int).max() == 2025:
            df = load_std_data("parroquias/std_parroquias_2025.csv")
            print("Está estandarizado")
        else:
            print("No está estandarizado, utilizar con cuidado")
        # Vamos a hacer un left join con el DataFrame de los cantones estandarizados
        self.df_parroquias["PARROQUIA_CODIGO"] = self.df_parroquias["PARROQUIA_CODIGO"].astype(str)
        self.df_parroquias = self.df_parroquias.merge(df, left_on="PARROQUIA_CODIGO",right_on="PARROQUIA_CODIGO_OLD", how="left")
        # si parroquia codigo _y es nulo, print that row
        missing_parroquias = self.df_parroquias[self.df_parroquias["PARROQUIA_CODIGO_y"].isnull()]
        if not missing_parroquias.empty:
            print("Las siguientes parroquias no tienen código estandarizado:")
            print(missing_parroquias[["PROVINCIA_CODIGO_x","CANTON_CODIGO_x","PARROQUIA_CODIGO_x","PARROQUIA_NOMBRE_x"]])
        #quitar las columnas que no necesitamos
        for col in self.df_parroquias.columns:
            if col.endswith("_x"):
                self.df_parroquias = self.df_parroquias.drop(columns=[col])
        #drop Anio, caambiar y renombrar las columnas
        self.df_parroquias = self.df_parroquias.drop(columns=["ANIO"])

        for col in self.df_parroquias.columns:
            if col.endswith("_y"):
                self.df_parroquias = self.df_parroquias.rename(columns={col:col[:-2]})
        # ordenar las columnas
        self.df_parroquias = self.df_parroquias[["PROVINCIA_CODIGO","PROVINCIA_NOMBRE","CANTON_CODIGO","CANTON_NOMBRE","PARROQUIA_CODIGO","PARROQUIA_CODIGO_OLD","PARROQUIA_NOMBRE","PARROQUIA_ESTADO"]]
        return self.df_parroquias
    