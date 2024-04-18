
import os
import pandas as pd
import numpy as np
import re
import sys
import unidecode

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
        print(file_path)
        df = pd.read_csv(file_path)
        return df
        
    
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
       
        self.df_registro['G_EDAD'] = self.df_registro['G_EDAD'].astype(str)
        
        if 'SEXO' in self.df_registro.columns:
            pass
        elif 'JUNTA_SEXO' in self.df_registro.columns:
            self.df_registro.rename(columns={'JUNTA_SEXO': 'SEXO'}, inplace=True)
        
        # Now for the SEXO column we want to change the values based on the sexo_names_std in the standarized folder
        df_sexo_names = self.load_std_data("registro_electoral/sexo_names_std.csv")
    
        # retrieve the values of each row in the df_sexo_names as a list
        for _, row_eq in df_sexo_names.iterrows():
            row_eq=row_eq.values.tolist()
            
            for index, row in self.df_registro.iterrows():
                sexo=row['SEXO']
                if sexo in row_eq:
                    #print(sexo)
                    self.df_registro.at[index,'SEXO']=row_eq[0]
        df_electores_names = self.load_std_data("registro_electoral/electores_names_std.csv")
        
        for _, row_eq in df_electores_names.iterrows():
            row_eq=row_eq.values.tolist()
            
            for index, row in self.df_registro.iterrows():
                elector=row['G_EDAD']
                if elector in row_eq:
                    #print(elector)
                    self.df_registro.at[index,'G_EDAD']=row_eq[0]
        
        self.df_registro.drop("ANIO", axis=1, inplace=True)
        
        #Now we want to pivot the table. All the columns will be the same except G_EDAD y ELECTORES
        #We will have new columns for each value of G_EDAD and ELECTORES
        self.df_registro = self.df_registro.pivot_table(index=self.df_registro.columns.difference(['G_EDAD','ELECTORES']).tolist(), columns='G_EDAD', values='ELECTORES', aggfunc='first').reset_index()
        
        # Ahora se suma el valor de los electores por cada fila para obtener el total
        # se suman las columnas que empiezan con ELECTORES
        self.df_registro['TOTAL ELECTORES'] = self.df_registro[[col for col in self.df_registro.columns if 'ELECTORES' in col]].sum(axis=1)
        # the NaN values are replaced by 0
        self.df_registro.fillna(0, inplace=True)
        
        self.df_registro = self.df_registro[["PROVINCIA_CODIGO","CANTON_CODIGO","PARROQUIA_CODIGO","SEXO"]+[col for col in self.df_registro.columns if col.startswith("ELECTORES")]+["TOTAL ELECTORES"]]
        #sort by PROVINCIA_CODIGO, CANTON_CODIGO, PARROQUIA_CODIGO, SEXO
        self.df_registro.sort_values(by=["PROVINCIA_CODIGO","CANTON_CODIGO","PARROQUIA_CODIGO","SEXO"], inplace=True)
        
        return self.df_registro
    
    def recuperar_resultados(self):
        '''
        Recupera los resultados de los archivos de resultados.
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
                        df["ANIO"] = anio
                        df_resultados = pd.concat([df_resultados, df])
        return df_resultados
    
    def change_resultados(self):
        '''
        Cambia los resultados de los archivos de resultados.
        '''
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
        
        
        # Colocar el nombre correcto de las columnas de la circunscripcion
        if 'CIRCUSCRIPCION_CODIGO_ORIGINAL' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'CIRCUSCRIPCION_CODIGO_ORIGINAL': 'CIRCUNSCRIPCION_CODIGO'}, inplace=True)
        else:
            pass
        
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
        if 'CODIGO_CANDIDATO_RESULTADO' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'CODIGO_CANDIDATO_RESULTADO': 'CODIGO_CANDIDATO'}, inplace=True)
        else:
            pass
        # Colocar el nombre de la columna de votos
        if 'VOTOS' in self.df_resultados.columns:
            pass
        elif 'CANDIDATO_VOTOS' in self.df_resultados.columns:
            self.df_resultados.rename(columns={'CANDIDATO_VOTOS': 'VOTOS'}, inplace=True)
        
        rows_to_preserve = ["PROVINCIA_CODIGO", "CANTON_CODIGO", "PARROQUIA_CODIGO", "SEXO"]
        
        #drop columns if they are present
        if 'NUMERO_DE_ACTAS' in self.df_resultados.columns:
            self.df_resultados.drop("NUMERO_DE_ACTAS", axis=1, inplace=True)
        if 'NUMERO_DE_JUNTAS' in self.df_resultados.columns:
            self.df_resultados.drop("NUMERO_DE_JUNTAS", axis=1, inplace=True)
        if 'CANDIDATO_ESTADO' in self.df_resultados.columns:
            self.df_resultados.drop("CANDIDATO_ESTADO", axis=1, inplace=True)
        
        # preserve the columns if they are present
        if 'OP_VOTO_EN_PLANCHA' in self.df_resultados.columns:
            rows_to_preserve.append('OP_VOTO_EN_PLANCHA')
        
        if 'CIRCUNSCRIPCION_CODIGO' in self.df_resultados.columns:
            rows_to_preserve.append('CIRCUNSCRIPCION_CODIGO')
        if 'CIRCUNSCRIPCION_NOMBRE' in self.df_resultados.columns:
            rows_to_preserve.append('CIRCUNSCRIPCION_NOMBRE')
        if 'SUFRAGANTES' in self.df_resultados.columns:
            rows_to_preserve.append('SUFRAGANTES')
            
        # Now for the SEXO column we want to change the values based on the sexo_names_std in the standarized folder
        df_sexo_names = self.load_std_data("resultados/sexo_names_std.csv")
        # retrieve the values of each row in the df_sexo_names as a list
        for _, row_eq in df_sexo_names.iterrows():
            row_eq=row_eq.values.tolist()
            
            for index, row in self.df_resultados.iterrows():
                sexo=row['SEXO']
                if sexo in row_eq:
                    #print(sexo)
                    self.df_resultados.at[index,'SEXO']=row_eq[0]
        
        
        
if __name__ == "__main__":
    #get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # establishes it as the current directory
    os.chdir(current_directory)
    print(current_directory)
    #D:\Open-ELEC\data_csv\seccionales\2014\diccionarios
    input_folder = "../../../data_csv/generales/2021"
    standarized_folder = "../data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    print(standarized_results.df_resultados)