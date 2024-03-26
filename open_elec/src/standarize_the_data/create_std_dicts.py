# Este script es para generar los diccionarios estandarizados de las dignidades, parroquias, cantones, provincias

# Path: source/standarize_the_data/create_std_dicts.py

import os
import pandas as pd
import numpy as np
import re
import sys
import unidecode
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
                path al directorio donde se guardaran los diccionarios estandarizados como csv
        '''
        if standarized_folder is None:
            self.standarized_folder = "data_csv/codigos_estandar"
        else:
            self.standarized_folder = standarized_folder
        
        self.input_folder = input_folder
        self.df_dignidades = self.recuperar_dignidades()
        # self.df_parroquias = self.recuperar_parroquias()
        # self.df_cantones = self.recuperar_cantones()
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
        
        #pd.DataFrame(dict_dignidades_std_post_2007).to_csv("data_csv/Codigos_estandar/dignidades/dignidades_std_post_2007.csv", index=False)
        #pd.DataFrame(dict_dignidades_std_pre_2007).to_csv("data_csv/Codigos_estandar/dignidades/dignidades_std_pre_2007.csv", index=False)
        
        # Hay un problema en ciertos años. Los códigos de las dignidades no son los mismos que los del diccionario o que los nombres de las dignidades no son los mismos que los del diccionario
        # Vamos a tener un diccionario de las equivalencias de los nombres de las dignidades
        # Por ejemplo si el nombre de la dignidad es PRESIDENTA/E Y VICEPRESIDENTA/E o PRESIDENTE Y VICEPRESIDENTE vamos a cambiarlo a PRESIDENCIA
        # Si el nombre de la dignidad es CONCEJALES RURALES vamos a cambiarlo a CONCEJO RURAL
        # Si el nombre de la dignidad es ALCALDES o ALCALDE MUNICIPAL o ALCALDES MUNICIPALES o ALCANCESA/ALCALDE vamos a cambiarlo a ALCALDIA
        # Si el nombre de la dignidad es CONCEJALES MUNICIPALES vamos a cambiarlo a CONCEJO MUNICIPAL
        
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
                    
        # # Find the maximum length among all lists
        # max_length = max(len(lst) for lst in dict_equivalencias.values())

        # # Fill shorter lists with NaN to make them equal length
        # for key, value in dict_equivalencias.items():
        #     dict_equivalencias[key] = value + [float('nan')] * (max_length - len(value))

        # # Create a DataFrame
        # df = pd.DataFrame.from_dict(dict_equivalencias, orient='index')
        # df.T.to_csv("data_csv/Codigos_estandar/dignidades/equivalencias_dignidades_T.csv", index=True)
        
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
        
        self.load_std_data
        
        dict_equivalencias_exterior = {
            "LATAM, CARIBE, AFRICA": ["AMERICA LATINA, EL CARIBE Y AFRICA", "AMERICA LATINA", "AMERICA LATINA EL CARIBE Y AFRICA","LATINOAMERICA, EL CARIBE Y AFRICA"],
            "NORTE-AMERICA": ["CANADA Y ESTADOS UNIDOS", "EE.UU CANADA", "EEUU Y CANADA", "EE.UU Y CANADA"],
            "EUROPA, ASIA, OCEANIA": ["EUROPA" , "ASIA, OCEANIA", "EUROPA ASIA OCEANIA", "EUROPA, ASIA Y OCEANIA","EUROPA ASIA Y OCEANIA","EUROPA, OCEANIA Y ASIA"],
            "VOTO EXTERIOR": ["VOTO EXTERIOR"],
            "ECUADOR": ["ECUADOR","NACION"]}
        #fill the dictionary with NaN to make them equal length
        # Find the maximum length among all lists
        # max_length = max(len(lst) for lst in dict_equivalencias_exterior.values())
        # # Fill shorter lists with NaN to make them equal length
        # for key, value in dict_equivalencias_exterior.items():
        #     dict_equivalencias_exterior[key] = value + [float('nan')] * (max_length - len(value))
        # # Create a DataFrame   
        #pd.DataFrame(dict_equivalencias_exterior).to_csv("data_csv/Codigos_estandar/provincias/equivalencias_exterior.csv", index=False)
        
        dict_provincias= { "PROVINCIA_CODIGO":["P00","P01","P02","P03","P04","P05","P06","P07","P08","P09","P10",
                                               "P11","P12","P13","P14","P15","P16","P17","P18","P19","P20","P21","P22","P23","P24","P25","P26","P27","P28"],
                           "PROVINCIA_NOMBRE":["ECUADOR","AZUAY", "BOLIVAR", "CANAR", "CARCHI", "COTOPAXI", "CHIMBORAZO", "EL ORO", "ESMERALDAS", "GUAYAS", "IMBABURA",
                                               "LOJA", "LOS RIOS", "MANABI", "MORONA SANTIAGO", "NAPO", "PASTAZA", "PICHINCHA", "TUNGURAHUA", "ZAMORA CHINCHIPE", "GALAPAGOS", "SUCUMBIOS", "ORELLANA", "STO DGO TSACHILAS", "SANTA ELENA", "VOTO EXTERIOR","EUROPA, ASIA, OCEANIA","NORTE-AMERICA","LATAM, CARIBE, AFRICA"],
                           "PROVINCIA_CODIGO_OLD":[0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                   11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]}      
        
        #pd.DataFrame(dict_provincias).to_csv("data_csv/Codigos_estandar/provincias/provincias_std.csv", index=False)
        
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
        #print(self.df_provincias)
        
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
        #Diccionario de nombres de cantones  esta en un csv
        
        #pd.DataFrame(dict_cantones).to_csv("data_csv/Codigos_estandar/cantones/cantones_std.csv", index=False)
        
          for key, value in dict_cantones.items():
            for v in value:
                self.df_provincias.loc[self.df_provincias["CANTON"]==v, "PROVINCIA_NOMBRE"] = key
                                         

    def test():
    
        

        #Test del metodo para el año 2013
        input_folder = "data_csv/seccionales/2023/diccionarios"
        std_dicts = Standard_Dictionaries(input_folder)
        #print(std_dicts.df_dignidades)
        #std_dicts.change_to_std_dignidades()
        #print(std_dicts.df_dignidades)
        print(std_dicts.df_provincias)
        std_dicts.change_to_std_provincias()