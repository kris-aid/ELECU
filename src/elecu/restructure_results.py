
import os
import pandas as pd
import numpy as np
import re
import unidecode

#get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
# establishes it as the current directory
os.chdir(current_directory)
class Standarized_Results:
    '''
    Clase para reestructurar los resultados de las elecciones en Ecuador.
    
    
    '''
    def __init__(self, input_folder, standarized_folder=None):
        '''
        Inicializa la clase Standarized_Results.
        
        Parameters
        ----------
            - input_folder: str 
                path al directorio de entrada que contiene los archivos .csv
            - standarized_folder: str
                path al directorio donde se encuentran los diccionarios estandarizados como csv
        '''
        if standarized_folder is None:
            self.standarized_folder = "../data/Codigos_estandar/"
        else:
            self.standarized_folder = standarized_folder
        self.year = input_folder[-4:]
        self.input_folder = input_folder   
        self.df_registro = self.recuperar_registro()
        self.df_resultados = self.recuperar_resultados()   
          
        
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
    
    def create_dict_mapping(self,df):
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
    
    def recuperar_registro(self):
        '''
        Recupera el registro de los archivos de resultados.
        
        Returns
        -------
            - df_registro: pd.DataFrame
                DataFrame con el registro de los archivos de resultados.
        '''
        # Crear un DataFrame vacío
        df_registro = pd.DataFrame()
        #De la carpeta, buscar el archivo que empieza con registro_electoral
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith(".csv"):
                    if file.startswith("registro_electoral"):
                        # Construir el path del archivo
                        file_path = os.path.join(root, file)
                        # Leer el archivo en un DataFrame
                        df = pd.read_csv(file_path)
                        df.columns = [unidecode.unidecode(col) for col in df.columns]
                        año = re.findall(r'\d+', file)
                        df["ANIO"] = año[0]
                        df_registro = pd.concat([df_registro, df])
        return df_registro
    
    def change_registro(self):
        '''
        Cambia el registro de los archivos de resultados.
        
        Parameters
        ----------
            - df_registro: pd.DataFrame
                DataFrame con el registro de los archivos de resultados.
        Returns
        -------
            - df_registro: pd.DataFrame
                DataFrame con el registro de los archivos de resultados.
        '''
        
        # Cambiar el nombre de las columnas
        self.df_registro.columns = [unidecode.unidecode(col) for col in self.df_registro.columns]
        
        if 'GRANDES_GRUPOS_DE_EDAD' in self.df_registro.columns:
            self.df_registro.rename(columns={'GRANDES_GRUPOS_DE_EDAD': 'G_EDAD'}, inplace=True)
        elif 'GRANDES_GRUPOS_DE_EDAD_1V' in self.df_registro.columns:
            self.df_registro.rename(columns={'GRANDES_GRUPOS_DE_EDAD_1V': 'G_EDAD'}, inplace=True)
        elif 'G_EDAD' in self.df_registro.columns:
            pass
        
        #convert the column G_EDAD to string
        self.df_registro['G_EDAD'] = self.df_registro['G_EDAD'].astype(str)
    
        # Colocar el nombre correcto de la columna SEXO
        if 'SEXO' in self.df_registro.columns:
            pass
        elif 'JUNTA_SEXO' in self.df_registro.columns:
            self.df_registro.rename(columns={'JUNTA_SEXO': 'SEXO'}, inplace=True)
            
        #ahora se colocan los nombres correctos de las columnas de sexo
        df_sexo_names = self.load_std_data("registro_electoral/sexo_names_std.csv")
        sexo_mapping=self.create_dict_mapping(df_sexo_names)
        self.df_registro['SEXO'] = self.df_registro['SEXO'].map(sexo_mapping)
        
        # Colocar el nombre correcto de las columnas de electores
        df_electores_names = self.load_std_data("registro_electoral/electores_names_std.csv")
        electores_mapping=self.create_dict_mapping(df_electores_names)
        self.df_registro['G_EDAD'] = self.df_registro['G_EDAD'].map(electores_mapping)
        
        #drop la columna ANIO
        self.df_registro.drop("ANIO", axis=1, inplace=True)
       
        # Se va a pivotear el DataFrame para que las columnas sean los grupos de edad
        self.df_registro = self.df_registro.pivot_table(index=self.df_registro.columns.difference(['G_EDAD','ELECTORES']).tolist(), columns='G_EDAD', values='ELECTORES', aggfunc='first').reset_index()
        
        # Ahora se suma el valor de los electores por cada fila para obtener el total
        # se suman las columnas que empiezan con ELECTORES
        self.df_registro['TOTAL ELECTORES'] = self.df_registro[[col for col in self.df_registro.columns if 'ELECTORES' in col]].sum(axis=1)
        
        # si hay valores nulos, se reemplazan por 0
        self.df_registro.fillna(0, inplace=True)
        
        self.df_registro = self.df_registro[["PROVINCIA_CODIGO","CANTON_CODIGO","PARROQUIA_CODIGO","SEXO"]+[col for col in self.df_registro.columns if col.startswith("ELECTORES")]+["TOTAL ELECTORES"]]
        
        #ordenar by PROVINCIA_CODIGO, CANTON_CODIGO, PARROQUIA_CODIGO, SEXO
        self.df_registro.sort_values(by=["PROVINCIA_CODIGO","CANTON_CODIGO","PARROQUIA_CODIGO","SEXO"], inplace=True)
        
        return self.df_registro
    
    def put_standar_geo_codes_registro(self,drop_old=False):
        """ 
        Pone los códigos geográficos estandarizados en el DataFrame de registro
        Parameters
        ----------
        drop_old: bool
            Si es True, se eliminan las columnas que terminan con "_OLD"
        Returns
        -------
        - df_registro: pd.DataFrame
            DataFrame con los códigos geográficos estandarizados
            
        """
        
        # cargar a las parroquias estandarizadas
        std_parroquias = self.load_std_data("parroquias/std_parroquias.csv")
        
        # hacer un merge con el DataFrame de resultados, en std parroquias la columna es PARROQUIA_CODIGO_OLD, en resultados es PARROQUIA_CODIGO
        self.df_registro = pd.merge(self.df_registro, std_parroquias, left_on="PARROQUIA_CODIGO", right_on="PARROQUIA_CODIGO_OLD", how="left")
        
        # Renombrar las columnas que tienen "_x" al final con "_OLD" al final
        columns_to_rename_old={col:col[:-2]+"_OLD" for col in self.df_registro.columns if col.endswith("_x")}
        self.df_registro.rename(columns=columns_to_rename_old, inplace=True)
        
        old_columns = [col for col in self.df_registro.columns if col.endswith("_OLD")]
        
        #Si drop_old es True, se eliminan las columnas que terminan con "_OLD"
        if drop_old==True:
            self.df_registro.drop(columns=old_columns, axis=1, inplace=True)
            
            
        # Renombrar las columnas que tienen "_y" al final con "" al final
        columns_to_rename={col:col[:-2] for col in self.df_registro.columns if col.endswith("_y")}
        self.df_registro.rename(columns=columns_to_rename, inplace=True)
        
        # Ordenar las columnas
        columnas_ordenadas = ["PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO"]+[col for col in self.df_registro.columns if col.startswith("ELECTORES")]+["TOTAL ELECTORES"]
        self.df_registro = self.df_registro[columnas_ordenadas]
        self.df_registro.sort_values(by=["PROVINCIA_CODIGO","CANTON_CODIGO","PARROQUIA_CODIGO","SEXO"], inplace=True)
        
        return self.df_registro

    def put_standar_geo_codes_registro_canton(self, year,drop_old=False):
        """
        Pone los códigos geográficos estandarizados en el DataFrame de registro para cantones
        Parameters
        ----------
        year: int
            Año de la elección

        drop_old: bool
            Si es True, se eliminan las columnas que terminan con "_OLD"
        Returns
        -------
        - df_registro: pd.DataFrame
            DataFrame con los códigos geográficos estandarizados

        """

        # cargar a los cantones estandarizados
        if year == 2009 or year == 2013:
            std_cantones = self.load_std_data("cantones/std_cantones_2009_2013.csv")
        else:
            std_cantones = self.load_std_data("cantones/std_cantones.csv")

        # hacer un merge con el DataFrame de resultados, en std cantones la columna es CANTON_CODIGO_OLD, en resultados es CANTON_CODIGO
        self.df_registro = pd.merge(self.df_registro, std_cantones, left_on="CANTON_CODIGO",
                                    right_on="CANTON_CODIGO_OLD", how="left")

        # Renombrar las columnas que tienen "_x" al final con "_OLD" al final
        columns_to_rename_old = {col: col[:-2] + "_OLD" for col in self.df_registro.columns if col.endswith("_x")}
        self.df_registro.rename(columns=columns_to_rename_old, inplace=True)

        old_columns = [col for col in self.df_registro.columns if col.endswith("_OLD")]

        # Si drop_old es True, se eliminan las columnas que terminan con "_OLD"
        if drop_old == True:
            self.df_registro.drop(columns=old_columns, axis=1, inplace=True)

        # Renombrar las columnas que tienen "_y" al final con "" al final
        columns_to_rename = {col: col[:-2] for col in self.df_registro.columns if col.endswith("_y")}
        self.df_registro.rename(columns=columns_to_rename, inplace=True)

        # Ordenar las columnas
        columnas_ordenadas = ["PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO"] + [col for col in
                                                                                                  self.df_registro.columns
                                                                                                  if col.startswith(
                "ELECTORES")] + ["TOTAL ELECTORES"]
        self.df_registro = self.df_registro[columnas_ordenadas]
        self.df_registro.sort_values(by=["PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO"], inplace=True)

        return self.df_registro

    def recuperar_resultados(self):
        '''
        Recupera los resultados de los archivos de resultados.
        
        Returns
        -------
            - df_resultados: pd.DataFrame
                DataFrame con los resultados de los archivos de resultados raw
        '''
        df_resultados = pd.DataFrame()
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                if file.endswith(".csv"):
                    if file.startswith("resultados"):
                        # Construir el path del archivo
                        file_path = os.path.join(root, file)
                        # Leer el archivo en un DataFrame
                        df = pd.read_csv(file_path)
                        df.columns = [unidecode.unidecode(col) for col in df.columns]
                        anio = file.split("resultados")[1].split(".")[0][1:]
                        vuelta = anio.split("_")[2]
                        df["VUELTA"] = vuelta
                        df_resultados = pd.concat([df_resultados, df])
        return df_resultados
    
    def change_resultados(self):
        '''
        Cambia los resultados de los archivos de resultados.
        
        Returns
        -------
            - df_resultados: pd.DataFrame
                DataFrame con los resultados de los archivos de resultados estandarizados
                
        '''
        anio=self.input_folder[-4:]
        # Cambiar el nombre de las columnas
        self.df_resultados.columns = [unidecode.unidecode(col) for col in self.df_resultados.columns]

        #Colocar el nombre correcto de las columna SEXO
        if 'SEX_JUNTA'  in self.df_resultados.columns:
            self.df_resultados.rename(columns={'SEX_JUNTA': 'SEXO'}, inplace=True)
        elif 'JUNTA_SEXO' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'JUNTA_SEXO': 'SEXO'}, inplace=True)  
        elif 'SEXO' in self.df_resultados.columns:
            pass    
        self.df_resultados['SEXO'] = self.df_resultados['SEXO'].astype(str)
        
        
        # Colocar el nombre correcto de las columnas de blancos y nulos
        if "VOTOS_EN_BLANCO" in self.df_resultados.columns:
            self.df_resultados.rename(columns={'VOTOS_EN_BLANCO': 'BLANCOS'}, inplace=True)
        else:
            pass
        
        if "VOTOS_NULOS" in self.df_resultados.columns:
            self.df_resultados.rename(columns={'VOTOS_NULOS': 'NULOS'}, inplace=True)
        else:
            pass
        
        # colocar el nombre del codigo de candidato
        if 'CANDIDATO_CODIGO_RESULTADOS' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'CANDIDATO_CODIGO_RESULTADOS': 'CANDIDATO_CODIGO'}, inplace=True)
        else:
            pass
        # Colocar el nombre de la columna de votos
        if 'VOTOS' in self.df_resultados.columns:
            pass
        elif 'CANDIDATO_VOTOS' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'CANDIDATO_VOTOS': 'VOTOS'}, inplace=True)
        
        
        
        #drop columns if they are present
        if 'NUMERO_DE_ACTAS' in self.df_resultados.columns:
            self.df_resultados.drop("NUMERO_DE_ACTAS", axis=1, inplace=True)
        if 'NUMERO_DE_JUNTAS' in self.df_resultados.columns:
            self.df_resultados.drop("NUMERO_DE_JUNTAS", axis=1, inplace=True)
        if 'CANDIDATO_ESTADO' in self.df_resultados.columns:
            self.df_resultados.drop("CANDIDATO_ESTADO", axis=1, inplace=True)
            
            
        #Colocar los nombres correctos de la columna sexo
        df_sexo_names = self.load_std_data("resultados/sexo_names_std.csv")
        sex_mapping = self.create_dict_mapping(df_sexo_names)
        self.df_resultados['SEXO'] = self.df_resultados['SEXO'].map(sex_mapping) 

        
        # Si el anio es menor a 2007, se carga el diccionario de dignidades pre 2007
        if int(anio) < 2007:
            df_dignidades_codes = self.load_std_data("dignidades/std_dignidades_pre_2007.csv")
            
        # Si el anio es mayor o igual a 2007, se carga el diccionario de dignidades post 2007
        else:
            df_dignidades_codes = self.load_std_data("dignidades/std_dignidades_post_2007.csv")
        
        if "DIGNIDAD_NOMBRE" not in self.df_resultados.columns:
            #El anio son los ultimos 4 caracteres de la carpeta de entrada
            anio = self.input_folder[-4:]
            path_diccionario_dignidades = self.input_folder + "/diccionarios/dignidades_"+anio+".csv"
            df_diccionario_dignidades = pd.read_csv(path_diccionario_dignidades)
            
            #Colocar el nombre de la dignidad
            self.df_resultados = pd.merge(self.df_resultados, df_diccionario_dignidades, on="DIGNIDAD_CODIGO", how="left")
            self.df_resultados.drop("DIGNIDAD_AMBITO", axis=1, inplace=True)
            
        #Unidecode la columna DIGNIDAD_NOMBRE
        self.df_resultados['DIGNIDAD_NOMBRE'] = self.df_resultados['DIGNIDAD_NOMBRE'].apply(unidecode.unidecode)  
        df_dignidades_names = self.load_std_data("dignidades/equivalencias_dignidades.csv")
        map_dignidades =self.create_dict_mapping(df_dignidades_names)
        self.df_resultados['DIGNIDAD_NOMBRE'] = self.df_resultados['DIGNIDAD_NOMBRE'].map(map_dignidades)
       
        # Si no existe la columna DIGNIDAD_CODIGO, se crea una columna DIGNIDAD_CODIGO con valores NaN
        if "DIGNIDAD_CODIGO" not in self.df_resultados.columns:
            #crear una columna DIGNIDAD_CODIGO con valores NaN
            self.df_resultados["DIGNIDAD_CODIGO"] = np.nan
            # poner la columna DIGNIDAD_CODIGO al principio
            self.df_resultados = self.df_resultados[["DIGNIDAD_CODIGO"]+[col for col in self.df_resultados.columns if col != "DIGNIDAD_CODIGO"]]
            
        # en df_dignidades_codes se encuentran los códigos de las dignidades, hacer un merge con el DataFrame de resultados
        self.df_resultados = pd.merge(self.df_resultados, df_dignidades_codes, on="DIGNIDAD_NOMBRE", how="left")
        self.df_resultados.drop("DIGNIDAD_AMBITO", axis=1, inplace=True)
        self.df_resultados.drop("DIGNIDAD_CODIGO_x", axis=1, inplace=True)
        self.df_resultados.rename(columns={'DIGNIDAD_CODIGO_y': 'DIGNIDAD_CODIGO'}, inplace=True)       
            
        return self.df_resultados
    
    def put_standar_geo_codes_results(self,drop_old=False):
        """ 
        Pone los códigos geográficos estandarizados en el DataFrame de resultados
        
        Parameters
        ----------
        drop_old: bool
            Si es True, se eliminan las columnas que terminan con "_OLD"
        Returns
        -------
        - df_resultados: pd.DataFrame
            DataFrame con los códigos geográficos estandarizados
            
        """
    
        # cargar a las parroquias estandarizadas
        std_parroquias = self.load_std_data("parroquias/std_parroquias.csv")
        # hacer un merge con el DataFrame de resultados, en std parroquias la columna es PARROQUIA_CODIGO_OLD, en resultados es PARROQUIA_CODIGO
        self.df_resultados = pd.merge(self.df_resultados, std_parroquias, left_on="PARROQUIA_CODIGO", right_on="PARROQUIA_CODIGO_OLD", how="left")
        # rename the columns that have "_x" at the end with "_OLD" at the end
        
        columns_to_rename_old={col:col[:-2]+"_OLD" for col in self.df_resultados.columns if col.endswith("_x")}
        self.df_resultados.rename(columns=columns_to_rename_old, inplace=True)
        
        old_columns = [col for col in self.df_resultados.columns if col.endswith("_OLD")]
        if drop_old==True:
           self.df_resultados.drop(columns=old_columns, axis=1, inplace=True)
        #rename columns with "_y" at the end
        columns_to_rename={col:col[:-2] for col in self.df_resultados.columns if col.endswith("_y")}
        self.df_resultados.rename(columns=columns_to_rename, inplace=True)
        
        columnas_ordenadas = ["DIGNIDAD_CODIGO","PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO"]+[col for col in self.df_resultados if col.startswith("CIRCUNSCRIPCION")]+[col for col in self.df_resultados.columns if col.startswith("CANDIDATO_")]+[col for col in self.df_resultados.columns if col.startswith("OP_")]+["SEXO", 'BLANCOS', 'NULOS',"VOTOS",'VUELTA']
        if drop_old==False:
            columnas_ordenadas = columnas_ordenadas + old_columns
        # ordenar las columnas
        self.df_resultados = self.df_resultados[columnas_ordenadas]
        #encode the columns to int
        #si hay valores nulos, se reemplazan por 0
        self.df_resultados["DIGNIDAD_CODIGO"] = self.df_resultados["DIGNIDAD_CODIGO"].fillna(0)
        
        self.df_resultados["DIGNIDAD_CODIGO"] = self.df_resultados["DIGNIDAD_CODIGO"].astype(int)
        self.df_resultados["VOTOS"].fillna(0, inplace=True)
        self.df_resultados["VOTOS"] = self.df_resultados["VOTOS"].astype(int)
        self.df_resultados["BLANCOS"] = self.df_resultados["BLANCOS"].astype(int)
        self.df_resultados["NULOS"] = self.df_resultados["NULOS"].astype(int)
        return self.df_resultados

    def put_standar_geo_codes_results_cantones(self,year, drop_old=False):
        """
        Pone los códigos geográficos estandarizados en el DataFrame de resultados

        Parameters
        ----------
        year : int
            Año de la elección
        drop_old: bool
            Si es True, se eliminan las columnas que terminan con "_OLD"
        Returns
        -------
        - df_resultados: pd.DataFrame
            DataFrame con los códigos geográficos estandarizados

        """

        # cargar a las cantonces estandarizadas
        if year ==2009 or year == 2013:
            std_cantones = self.load_std_data("cantones/std_cantones_2009_2013.csv")
        else:
            std_cantones = self.load_std_data("cantones/std_cantones.csv")

        # hacer un merge con el DataFrame de resultados, en std cantonces la columna es CANTON_CODIGO_OLD, en resultados es CANTON_CODIGO
        self.df_resultados = pd.merge(self.df_resultados, std_cantones, left_on="CANTON_CODIGO",
                                      right_on="CANTON_CODIGO_OLD", how="left")
        # rename the columns that have "_x" at the end with "_OLD" at the end

        columns_to_rename_old = {col: col[:-2] + "_OLD" for col in self.df_resultados.columns if col.endswith("_x")}
        self.df_resultados.rename(columns=columns_to_rename_old, inplace=True)

        old_columns = [col for col in self.df_resultados.columns if col.endswith("_OLD")]
        if drop_old == True:
            self.df_resultados.drop(columns=old_columns, axis=1, inplace=True)
        # rename columns with "_y" at the end
        columns_to_rename = {col: col[:-2] for col in self.df_resultados.columns if col.endswith("_y")}
        self.df_resultados.rename(columns=columns_to_rename, inplace=True)

        columnas_ordenadas = ["DIGNIDAD_CODIGO", "PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO"] + [col for col
                                                                                                             in
                                                                                                             self.df_resultados
                                                                                                             if
                                                                                                             col.startswith(
                                                                                                                 "CIRCUNSCRIPCION")] + [
                                 col for col in self.df_resultados.columns if col.startswith("CANDIDATO_")] + [col for
                                                                                                               col in
                                                                                                               self.df_resultados.columns
                                                                                                               if
                                                                                                               col.startswith(
                                                                                                                   "OP_")] + [
                                 "SEXO", 'BLANCOS', 'NULOS', "VOTOS", 'VUELTA']
        if drop_old == False:
            columnas_ordenadas = columnas_ordenadas + old_columns
        # ordenar las columnas
        self.df_resultados = self.df_resultados[columnas_ordenadas]
        # encode the columns to int
        # si hay valores nulos, se reemplazan por 0
        #print the row with null values in DIGNIDAD_CODIGO
        #print(self.df_resultados[self.df_resultados["DIGNIDAD_CODIGO"].isnull()])

        self.df_resultados["DIGNIDAD_CODIGO"] = self.df_resultados["DIGNIDAD_CODIGO"].fillna(0)

        self.df_resultados["DIGNIDAD_CODIGO"] = self.df_resultados["DIGNIDAD_CODIGO"].astype(int)
        self.df_resultados["VOTOS"].fillna(0, inplace=True)
        self.df_resultados["VOTOS"] = self.df_resultados["VOTOS"].astype(int)
        self.df_resultados["BLANCOS"] = self.df_resultados["BLANCOS"].astype(int)
        self.df_resultados["NULOS"] = self.df_resultados["NULOS"].astype(int)
        return self.df_resultados

    def divide_resultados(self):
        '''
        Divide los resultados en dos DataFrames: uno con los resultados de la votación y otro con la elección de candidatos.
        
        Returns
        -------
            - df_votacion: pd.DataFrame
                DataFrame con los resultados de la votación.
            - df_eleccion: pd.DataFrame
                DataFrame con la elección de candidatos.
        
        '''
        # se va a utilizar las columnas de la tabla de resultados para dividir en dos DataFrames 
        columnas_de_votacion = ["DIGNIDAD_CODIGO","PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO", 'BLANCOS', 'NULOS','VUELTA']
        columnas_de_eleccion = ["DIGNIDAD_CODIGO","PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO", "VOTOS", 'VUELTA']
        # preserve the columns if they are present
        if 'SUFRAGANTES' in self.df_resultados.columns:
            columnas_de_votacion.append('SUFRAGANTES')
            
        if 'OP_VOTOS_EN_PLANCHA' in self.df_resultados.columns:
            columnas_de_eleccion.append('OP_VOTOS_EN_PLANCHA')
            
        if 'CIRCUNSCRIPCION_CODIGO' in self.df_resultados.columns:
            columnas_de_votacion.append('CIRCUNSCRIPCION_CODIGO')
            columnas_de_eleccion.append('CIRCUNSCRIPCION_CODIGO')
            
        if 'CIRCUNSCRIPCION_NOMBRE' in self.df_resultados.columns:
            columnas_de_votacion.append('CIRCUNSCRIPCION_NOMBRE')
            columnas_de_eleccion.append('CIRCUNSCRIPCION_NOMBRE')
            
        if 'CANDIDATO_CODIGO' in self.df_resultados.columns:
            columnas_de_eleccion.append('CANDIDATO_CODIGO')
        if 'CANDIDATO_NOMBRE' in self.df_resultados.columns:
            columnas_de_eleccion.append('CANDIDATO_NOMBRE')
        if 'OP_CODIGO' in self.df_resultados.columns:
            columnas_de_eleccion.append('OP_CODIGO')
        if 'OP_NOMBRE' in self.df_resultados.columns:
            columnas_de_eleccion.append('OP_NOMBRE')
        if 'OP_LISTA' in self.df_resultados.columns:
            columnas_de_eleccion.append('OP_LISTA')
        if 'OP_SIGLAS' in self.df_resultados.columns:
            columnas_de_eleccion.append('OP_SIGLAS')
            
        
        df_votacion= self.df_resultados[columnas_de_votacion].copy()
        df_votacion.sort_values(["BLANCOS","NULOS"], ascending=False, inplace=True)
        #if year is 2017 or later
        df_votacion["PARROQUIA_CODIGO"] = df_votacion["PARROQUIA_CODIGO"].astype(int)
        if int(self.year) >= 2017:
            problematic_parroquia = 6150 # Replace with actual parroquia_codigo
            df_problematic = df_votacion[df_votacion["PARROQUIA_CODIGO"] == problematic_parroquia]

            df_problematic = df_votacion[
                (df_votacion["PARROQUIA_CODIGO"] == problematic_parroquia) & (df_votacion["DIGNIDAD_CODIGO"] == 1)]
            df_others = df_votacion[
                ~((df_votacion["PARROQUIA_CODIGO"] == problematic_parroquia) & (df_votacion["DIGNIDAD_CODIGO"] == 1))]


            df_problematic= df_problematic.drop_duplicates(subset=["DIGNIDAD_CODIGO","PARROQUIA_CODIGO","SEXO","VUELTA","CIRCUNSCRIPCION_CODIGO"], keep='first')
            # If DIGNIDAD_CODIGO is 1 for the problematic parroquia, group by SEXO and VUELTA, summing BLANCOS and NULOS
            if not df_problematic.empty:
                df_problematic_grouped = (
                    df_problematic
                    .groupby(["DIGNIDAD_CODIGO", "PARROQUIA_CODIGO", "SEXO", "VUELTA"], as_index=False)
                    .agg({"BLANCOS": "sum", "NULOS": "sum", "CIRCUNSCRIPCION_CODIGO": "first"})
                )

                df_problematic_grouped["PROVINCIA_CODIGO"] = df_problematic["PROVINCIA_CODIGO"].iloc[0]
                df_problematic_grouped["CANTON_CODIGO"] = df_problematic["CANTON_CODIGO"].iloc[0]
                df_problematic_grouped["CIRCUNSCRIPCION_NOMBRE"] = df_problematic["CIRCUNSCRIPCION_NOMBRE"].iloc[0]

                # Drop duplicates in the non-problematic data
                df_others = df_others.drop_duplicates(subset=["DIGNIDAD_CODIGO", "PARROQUIA_CODIGO", "SEXO", "VUELTA"],
                                                      keep="first")

                # Combine the grouped problematic data back with the rest
                df_votacion = pd.concat([df_others, df_problematic_grouped], ignore_index=True)
            else:
                # If no special case, just use the original data
                df_votacion = pd.concat([df_others, df_problematic], ignore_index=True)





            # Combine the grouped problematic data back with the rest
            df_votacion = pd.concat([df_others, df_problematic_grouped], ignore_index=True)
        else:
            df_votacion = df_votacion.drop_duplicates(subset=["DIGNIDAD_CODIGO","PARROQUIA_CODIGO","SEXO","VUELTA"], keep='first')
        #df_votacion= df_votacion.drop_duplicates(subset=columnas_de_votacion, keep='first')
        df_eleccion = self.df_resultados.copy()
        # in df_eleccion we want to drop the columns that are in columnas_de_votacion and are not in columnas_de_eleccion
        columnas_no_ele = [col for col in df_eleccion.columns if col not in columnas_de_eleccion]
        df_eleccion = df_eleccion.drop(columns=columnas_no_ele)
        return df_votacion, df_eleccion
        
        
