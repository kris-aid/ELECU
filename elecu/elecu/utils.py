import pandas as pd
import importlib.resources
def create_dict_mapping(df):
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

def load_std_data(resource_path):
    '''
    Carga los diccionarios estandarizados de las elecciones desde el paquete.

    Parameters
    ----------
        - resource_path: str
            Ruta del archivo csv RELATIVA al paquete 'elecu',
            usando barras normales y SIN la carpeta 'data/Codigos_estandar'.
            Ej: "dignidades/dignidades_std_post_2007.csv"

    Returns
    -------
        - DataFrame
            DataFrame con los códigos estandarizados para el procesamiento posterior
    '''
    # 1. Define the module where the resource is located
    package_name = 'elecu.data.Codigos_estandar'

    # 2. Get the actual file name from the path
    #    (e.g., "dignidades/dignidades_std_post_2007.csv" -> "dignidades_std_post_2007.csv")
    #    This assumes the structure is flattened or you only pass the filename.
    #    A safer method is to use files() and join them.

    # 3. Use files() for a modern, path-like object approach (Python 3.9+)
    #    This handles subdirectories better than open_text()
    resource = importlib.resources.files(package_name) / resource_path
    if resource_path=="provincias/equivalencias_exterior.csv":
        septator=";"
    else:
        septator=","
    # The 'resource' variable is now a pathlib.Path object pointing to the file.
    with resource.open('r') as archivo:
        df = pd.read_csv(archivo, sep=septator,encoding='latin-1')

    return df