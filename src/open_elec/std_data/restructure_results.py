
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
    def __init__(self, input_folder, output_folder):
        '''
        Inicializa la clase Standarized_Results.
        
        Parameters
        ----------
            - input_folder: str 
                path al directorio de entrada que contiene los archivos .csv
            - output_folder: str
                path al directorio de salida donde se guardarán los archivos .csv
        
        Returns
        -------
            none
        
        Examples
        --------
        Standarized_Results("data_csv", "data_csv_restructured")
        '''
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.df = pd.DataFrame()
        self.df_restructured = pd.DataFrame()
        
    def restructure_results(self):
        '''
        Reestructura los resultados de las elecciones en Ecuador.
        
        Parameters
        ----------
            none
        
        Returns
        -------
            none
        
        Examples
        --------
        Standarized_Results("data_csv", "data_csv_restructured")
        '''
        # Crear el directorio de salida si no existe
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Listar todos los archivos en el directorio de entrada y sus subdirectorios
        for root, dirs, files in os.walk(self.input_folder):
            # Crear subdirectorios en el directorio de salida 
            relative_path = os.path.relpath(root, self.input_folder)
            output_subfolder = os.path.join(self.output_folder, relative_path)
            os.makedirs(output_subfolder, exist_ok=True)

            for file in files:
                if file.endswith(".csv"):
                    # Construir los paths de entrada y salida
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(output_subfolder, file)

                    # Leer el archivo .csv en un DataFrame
                    self.df = pd.read_csv(input_file_path)
                    
                    # Reestructurar los resultados
                    self.df_restructured = self.restructure_dataframe(self.df)
                    
                    # Guardar el DataFrame reestructurado como un archivo .csv
                    self.df_restructured.to_csv(output_file_path, index=False)

                    print(f"Restructured {input_file_path} to {output_file_path}")
        return None