# Primero vamos a estandarizar los códigos  de dignidades de todas las bases.
# Vamos a crear un diccionario con los códigos de las dignidades, su ambito georáfico y su nombre

dict_dignidades = {1: ["PRESIDENCIA", "NACIONAL"],
                   2: ["PREFECTURA", "PROVINCIAL"],
                   3: ["CONSEJO PROVINCIAL", "PROVINCIAL"],
                   4: ["ALCALDÍA", "CANTONAL"],
                   5: ["CONCEJO MUNICIPAL", "CANTONAL"],
                   6: ["JUNTA PARROQUIAL", "PARROQUIAL"],
                   7: ["ASAMBLEA PROVINCIAL", "PROVINCIAL"],
                   8: ["PARLAMENTO ANDINO", "NACIONAL"],
                   9: ["ASAMBLEA NACIONAL", "NACIONAL"],
                   10:["ASAMBLEA CIRCUNSCRIPCION","PROVINCIAL"],
                   11:["CPCCS MUJERES","NACIONAL"],
                   12:["CPCCS HOMBRES","NACIONAL"],
                   13:["CPCCS NACIONAL/EXTRANJERO","NACIONAL"]}

#Vamos a revisar si los códigos de dignidades de las bases de datos son los mismos que los del diccionario
# Cada eleccion tiene un directorio llamado diccionarios que contiene un archivo llamado "dignidades_@año.csv" que contiene
# los códigos de dignidades de esa elección. Vamos a tomar todos los archivos de ese directorio y vamos a revisar si los
# códigos de dignidades son los mismos que los del diccionario. Si no son los mismos, vamos a cambiar los códigos de las


import os
import pandas as pd
import numpy as np
import re
import sys
import shutil

def check_dignidades(input_folder, dict_dignidades):
    '''
    Revisa si los códigos de dignidades de las bases de datos son los mismos que los del diccionario.
    Si no son los mismos, cambia los códigos de las bases de datos para que sean los mismos que los del diccionario.
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
        - dict_dignidades: dict
            diccionario con los códigos de las dignidades, su ambito georáfico y su nombre
    
    Returns
    -------
        none
    
    Examples
    --------
    check_dignidades("data_csv", dict_dignidades)
         
    '''
    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("dignidades"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    # Revisar si el DataFrame tiene la columna "dignidad"
                    if "dignidad" in df.columns:
                        # Revisar si los códigos de dignidades de la base de datos son los mismos que los del diccionario
                        if not df["dignidad"].isin(dict_dignidades.keys()).all():
                            # Si no son los mismos, cambiar los códigos de las bases de datos para que sean los mismos que los del diccionario
                            df["dignidad"] = df["dignidad"].map(dict_dignidades)
                            # Guardar el DataFrame con los códigos de dignidades cambiados
                            df.to_csv(file_path, index=False)
                            print(f"Changed the dignity codes of {file_path}")
                
    return None
