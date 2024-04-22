import pandas as pd
import numpy as np
import os

def extract_eleccion(df_resultados,dignidad_codigo=None,territorio_codigo=None,agrupar_por_territorio=None,sexo=None,vuelta=None):
    """
    Extrae los valores de la elección de acuerdo a los parámetros de entrada
    
    Parameters
    ----------
    df_resultados : DataFrame
        DataFrame con los resultados de la elección
    dignidad_codigo : int
        Código de la dignidad a filtrar
    territorio_codigo : str
        Código del territorio a filtrar (provincia, cantón, parroquia)
    agrupar_por_territorio : str
        Agrupar los resultados por territorio (PAIS, PROVINCIA, CANTON, CIRCUNSCRIPCION, PARROQUIA)
    sexo : str
        Sexo a filtrar (S0, S1, AMBOS, AGRUPAR)
    vuelta : int
        Vuelta a filtrar(1, 2,None)

    Returns
    -------
    DataFrame
        DataFrame con los resultados de la elección filtrados
        
    Examples
    --------
    >>> df_resultados = pd.read_csv("test_2023_eleccion.csv")
    >>> df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS", vuelta=None)
    >>> print(df_resultados_filtered)
    >>>  PROVINCIA_CODIGO  OP_CODIGO        CANDIDATO_NOMBRE SEXO  VUELTA   VOTOS
    >>>               P01       18.0  FERNANDO VILLAVICENCIO   S0       1   36890
    >>>               P01       18.0  FERNANDO VILLAVICENCIO   S1       1   44222
    >>>               ...       ...                      ...  ...     ...     ...
    """
    columnas_agrupar= ['SEXO', 'VUELTA']
    
    if "CANDIDATO_NOMBRE" in df_resultados.columns:
        columnas_agrupar.insert(0, "CANDIDATO_NOMBRE")
    if "CANDIDATO_CODIGO" in df_resultados.columns:
        columnas_agrupar.insert(0, "CANDIDATO_CODIGO")
    if "OP_CODIGO" in df_resultados.columns:
        columnas_agrupar.insert(0, "OP_CODIGO")
    
    # Filter by dignidad
    if dignidad_codigo is not None:
        df_resultados = df_resultados[df_resultados['DIGNIDAD_CODIGO'] == dignidad_codigo]
    # Filter by territory
    if territorio_codigo is not None:
        if territorio_codigo.startswith('P'):
            df_resultados = df_resultados[df_resultados['PROVINCIA_CODIGO'] == territorio_codigo]
        if territorio_codigo.startswith('C'):
            df_resultados = df_resultados[df_resultados['CANTON_CODIGO'] == territorio_codigo]
        if territorio_codigo.startswith('Q'):
            df_resultados = df_resultados[df_resultados['PARROQUIA_CODIGO'] == territorio_codigo]

    if agrupar_por_territorio is not None:
        if agrupar_por_territorio == 'PAIS':
            pass
        if agrupar_por_territorio == 'PROVINCIA':
            columnas_agrupar.insert(0, 'PROVINCIA_CODIGO')
        if agrupar_por_territorio == 'CANTON':
            columnas_agrupar.insert(0, 'CANTON_CODIGO')
        if agrupar_por_territorio == 'CIRCUNSCRIPCION':
            columnas_agrupar.insert(0, 'CIRCUNSCRIPCION_CODIGO')
        if agrupar_por_territorio == 'PARROQUIA':
            columnas_agrupar.insert(0, 'PARROQUIA_CODIGO')
        df_resultados= df_resultados.groupby(columnas_agrupar)['VOTOS'].sum().reset_index()
      
          
    if sexo is not None:
        if sexo == 'S0' or sexo=="S1":
            df_resultados = df_resultados[df_resultados['SEXO'] == sexo]
        if sexo== "AMBOS":
            pass
        if sexo== "AGRUPAR":
            #delete the "SEXO" column in columnas_agrupar
            columnas_agrupar.remove('SEXO')
            df_resultados = df_resultados.groupby(columnas_agrupar)['VOTOS'].sum().reset_index()
    if vuelta is not None:
        df_resultados = df_resultados[df_resultados['VUELTA'] == vuelta]
    else:
        pass
    return df_resultados
if __name__ == "__main__":
     #get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # establishes it as the current directory
    os.chdir(current_directory)
    # test with the 2023 results that are in the test folder
    df_resultados = pd.read_csv("../../tests/test_results/test_2023_eleccion.csv")

    # Test 1: extract values for a specific dignidad
    df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS", vuelta=None)
    print(df_resultados_filtered)
    print(df_resultados_filtered.columns)