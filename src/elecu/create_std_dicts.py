# Este script es para generar los diccionarios estandarizados de las dignidades, parroquias, cantones, provincias

# Path: create_std_dicts.py

import os
import pandas as pd
import numpy as np
import re
import sys
import unidecode

#get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
# establishes it as the current directory
os.chdir(current_directory)
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
            self.standarized_folder = "data/Codigos_estandar/"
        else:
            self.standarized_folder = standarized_folder
        
        self.input_folder = input_folder
        self.df_dignidades = self.recuperar_dignidades()
        self.df_parroquias = self.recuperar_parroquias()
        self.df_cantones = self.recuperar_cantones()
        self.df_provincias = self.recuperar_provincias()
    def load_std_data(self,file):
        '''
        Carga los diccionarios estandarizados de las elecciones
        
        Parameters
        ----------
            - file: str
                path al archivo csv que contiene el archivo que esta en la carpeta "data_csv/Codigos_estandar"
        Returns
        -------
            - DataFrame
                DataFrame con los códigos estandarizados para el procesamiento posterior
                
        Examples
        --------
        load_std_data("data_csv/Codigos_estandar/dignidades/dignidades_std_post_2007.csv")
        
        '''
        #Buscar en la carpeta "data_csv/Codigos_estandar" el archivo csv que contiene los códigos estandarizados
        # Construir el path del archivo
        file_path = os.path.join(self.standarized_folder, file)
        # Leer el archivo en un DataFrame
        df = pd.read_csv(file_path)
        return df
        
        
        
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
        return df_dignidades
    
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
        
        # Antes del 2007, el codigo 3 es para los concejos provinciales
        dict_std_dignidades_pre_2007 = { "DIGNIDAD_CODIGO":[1, 2, 3, 4, 5, 6, 7, 8],
                            "DIGNIDAD_NOMBRE":["PRESIDENCIA", "PREFECTURA", "CONCEJO PROVINCIAL", "ALCALDIA", "CONCEJO URBANO", "JUNTA PARROQUIAL", "ASAMBLEA PROVINCIAL", "PARLAMENTO ANDINO"],
                             "DIGNIDAD_AMBITO":["NACIONAL", "PROVINCIAL", "PROVINCIAL", "CANTONAL", "CANTONAL", "PARROQUIAL", "PROVINCIAL", "NACIONAL"]}
        
        
        #
        dict_std_dignidades_post_2007 = { "DIGNIDAD_CODIGO":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                           "DIGNIDAD_NOMBRE":["PRESIDENCIA", "PREFECTURA", "CONCEJO RURAL", "ALCALDIA", "CONCEJO URBANO", "JUNTA PARROQUIAL", "ASAMBLEA PROVINCIAL", "PARLAMENTO ANDINO", "ASAMBLEA NACIONAL", "ASAMBLEA CIRCUNSCRIPCION", "CPCCS M", "CPCCS H", "CPCCS NAC/EXT"],
                            "DIGNIDAD_AMBITO":["NACIONAL", "PROVINCIAL", "CANTONAL", "CANTONAL", "CANTONAL", "PARROQUIAL", "PROVINCIAL", "NACIONAL", "NACIONAL", "PROVINCIAL", "NACIONAL", "NACIONAL", "NACIONAL"]}
        
        
        dict_equivalencias= {
                    "PRESIDENCIA": ["PRESIDENTA/E Y VICEPRESIDENTA/E", "PRESIDENTE Y VICEPRESIDENTE"],
                    "PREFECTURA": ["PREFECTA / PREFECTO","PREFECTO PROVINCIAL", "PREFECTO Y VICEPREFECTO"],
                    "ALCALDIA": ["ALCALDES", "ALCALDE MUNICIPAL", "ALCALDES MUNICIPALES", "ALCALDESA / ALCALDE"],
                    "ASAMBLEA NACIONAL":["ASAMBLEISTAS NACIONALES"],
                    "ASAMBLEA PROVINCIAL": ["ASAMBLEISTAS PROVINCIALES", "ASAMBLEISTAS PROVINCIALES Y DEL EXTERIOR","DIPUTADOS PROVINCIALES"],
                    "ASAMBLEA CIRCUNSCRIPCION":["ASAMBLEISTAS POR CIRCUNSCRIPCION"],
                    "CONCEJO URBANO": ["CONCEJALES MUNICIPALES", "CONCEJALES URBANOS", "CONCEJAL MUNICIPAL"],
                    "CONCEJO RURAL": ["CONCEJALES RURALES"],
                    "CONCEJO PROVINCIAL": ["CONSEJEROS PROVINCIALES","CONSEJERO PROVINCIAL"],
                    "JUNTA PARROQUIAL": ["JUNTAS PARROQUIALES","MIEMBROS JUNTAS PARROQUIALES","VOCALES DE JUNTA PARROQUIAL",
                                        "VOCALES DE JUNTAS PARROQUIALES","VOCALES JUNTAS PARROQUIALES"],
                    "PARLAMENTO ANDINO": ["PARLAMENTARIOS ANDINOS"],
                    "CPCCS M": ["CPCCS (MUJERES)"],
                    "CPCCS H": ["CPCCS (HOMBRES)"],
                    "CPCCS NAC/EXT": ["CPCCS (NAC/EXT)"]}
                    
        #Vamos a cambiar los nombres de las dignidades
        #Primero vamos a cambiar los nombres de las dignidades que no son los mismos que los del diccionario
        for key, value in dict_equivalencias.items():
            for v in value:
                self.df_dignidades.loc[self.df_dignidades["DIGNIDAD_NOMBRE"]==v, "DIGNIDAD_NOMBRE"] = key
    
        
                
        #Si el año es antes del 2007, vamos a usar el diccionario de las dignidades antes del 2007
        if self.df_dignidades["ANIO"].astype(int).max() < 2007:
            codigos_std=pd.DataFrame(dict_std_dignidades_pre_2007)
        # Si el año es después del 2007, vamos a usar el diccionario de las dignidades después del 2007    
        else:
            codigos_std=pd.DataFrame(dict_std_dignidades_post_2007)
        
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
        #Diccionario de nombres de provincias del exterior y sus equivalentes
        
        #self.load_std_data
        
        dict_equivalencias_exterior = {
            "LATAM, CARIBE, AFRICA": ["AMERICA LATINA, EL CARIBE Y AFRICA", "AMERICA LATINA", "AMERICA LATINA EL CARIBE Y AFRICA","LATINOAMERICA, EL CARIBE Y AFRICA"],
            "NORTE-AMERICA": ["CANADA Y ESTADOS UNIDOS", "EE.UU CANADA", "EEUU Y CANADA", "EE.UU Y CANADA"],
            "EUROPA, ASIA, OCEANIA": ["EUROPA" , "ASIA, OCEANIA", "EUROPA ASIA OCEANIA", "EUROPA, ASIA Y OCEANIA","EUROPA ASIA Y OCEANIA","EUROPA, OCEANIA Y ASIA"],
            "VOTO EXTERIOR": ["VOTO EXTERIOR"],
            "ECUADOR": ["ECUADOR","NACION"]}
 
        
        dict_provincias= { "PROVINCIA_CODIGO":["P00","P01","P02","P03","P04","P05","P06","P07","P08","P09","P10",
                                               "P11","P12","P13","P14","P15","P16","P17","P18","P19","P20","P21","P22","P23","P24","P25","P26","P27","P28"],
                           "PROVINCIA_NOMBRE":["ECUADOR","AZUAY", "BOLIVAR", "CANAR", "CARCHI", "COTOPAXI", "CHIMBORAZO", "EL ORO", "ESMERALDAS", "GUAYAS", "IMBABURA",
                                               "LOJA", "LOS RIOS", "MANABI", "MORONA SANTIAGO", "NAPO", "PASTAZA", "PICHINCHA", "TUNGURAHUA", "ZAMORA CHINCHIPE", "GALAPAGOS", "SUCUMBIOS", "ORELLANA", "STO DGO TSACHILAS", "SANTA ELENA", "VOTO EXTERIOR","EUROPA, ASIA, OCEANIA","NORTE-AMERICA","LATAM, CARIBE, AFRICA"],
                           "PROVINCIA_CODIGO_OLD":[0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]}      
        
        
        #Vamos a cambiar los nombres de las dignidades
        #Primero vamos a cambiar los nombres de las dignidades que no son los mismos que los del diccionario
        for key, value in dict_equivalencias_exterior.items():
            for v in value:
                self.df_provincias.loc[self.df_provincias["PROVINCIA_NOMBRE"]==v, "PROVINCIA_NOMBRE"] = key
        
        # Vamos a hacer un left join con el DataFrame de las provincias estandarizadas
        self.df_provincias = self.df_provincias.merge(pd.DataFrame(dict_provincias), on="PROVINCIA_NOMBRE", how="left")
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
            df=self.load_std_data("cantones/std_cantones.csv")
        else:
            df=self.load_std_data("cantones/std_cantones_2009_2013.csv")
        # Vamos a hacer un left join con el DataFrame de los cantones estandarizados
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
        df=self.load_std_data("parroquias/std_parroquias.csv")
        
        if self.df_parroquias["ANIO"].astype(int).max() >= 2019:
           print("Está estandarizado")
        else:
            print("No está estandarizado, utilizar con cuidado")
        # Vamos a hacer un left join con el DataFrame de los cantones estandarizados
        
        self.df_parroquias = self.df_parroquias.merge(df, left_on="PARROQUIA_CODIGO",right_on="PARROQUIA_CODIGO_OLD", how="left")
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