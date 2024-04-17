
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
        # Crear una columna con el año
        for col in self.df_registro.columns:
            if 'G_EDAD' in col:
                self.df_registro[col] = self.df_registro[col].astype(str)
        
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
        Recupera los resultados de los archivos de resultados.'''
        for 
        
if __name__ == "__main__":
    #get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # establishes it as the current directory
    os.chdir(current_directory)
    print(current_directory)
    #D:\Open-ELEC\data_csv\seccionales\2014\diccionarios
    input_folder = "../../../data_csv/seccionales/2004"
    standarized_folder = "../data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    print(standarized_results.df_registro)
    print(standarized_results.change_registro())