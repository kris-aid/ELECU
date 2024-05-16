import os
import pandas as pd
def convert_sav_to_csv(input_folder, output_folder):
    '''
    Convierte todos los archivos .sav en el directorio de entrada a archivos .csv en el directorio de salida.
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio de entrada que contiene los archivos .sav
        - output_folder: str
            path al directorio de salida donde se guardarán los archivos .csv
    
    Returns
    -------
        none
    
    Examples
    --------
    convert_sav_to_csv("data", "data_csv")
    '''

    # Crear el directorio de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        # Crear subdirectorios en el directorio de salida 
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        os.makedirs(output_subfolder, exist_ok=True)

        for file in files:
            if file.endswith(".sav"):
                # Construir los paths de entrada y salida
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_subfolder, os.path.splitext(file)[0] + ".csv")

                # Leer el archivo .sav en un DataFrame
                df = pd.read_spss(input_file_path)

                # Guardar el DataFrame como un archivo .csv
                df.to_csv(output_file_path, index=False)

                print(f"Converted {input_file_path} to {output_file_path}")
    return None

def get_data(link, download_folder):
    """
    Función que obtiene los datos de un archivo comprimido en la web y los guarda en un directorio local.
    (Trabajo en progreso)
    
    
    Parameters
    ----------
        - link: str
            URL del archivo comprimido
        - download_folder: str
            Directorio donde se guardarán los archivos descargados

    Returns
    -------
    None
    """
    #Trabajo en progreso