import pandas as pd
import numpy as np
import os
#     #get the current directory
# current_directory = os.path.dirname(os.path.abspath(__file__))
# # establishes it as the current directory
# os.chdir(current_directory)
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
        if len(territorio_codigo) == 4:  # EC + 2 digits (Provincias)
            df_resultados = df_resultados[df_resultados['PROVINCIA_CODIGO'] == territorio_codigo]
        elif len(territorio_codigo) == 6:  # EC + 4 digits (Cantones)
            df_resultados = df_resultados[df_resultados['CANTON_CODIGO'] == territorio_codigo]
        elif len(territorio_codigo) == 8:  # EC + 6 digits (Parroquias)
            df_resultados = df_resultados[df_resultados['PARROQUIA_CODIGO'] == territorio_codigo]
    else:
        pass

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

def extract_votacion(df_votacion,dignidad_codigo=None,territorio_codigo=None,agrupar_por_territorio=None,sexo=None,vuelta=None):
    """
    Extrae los valores de la votación de acuerdo a los parámetros de entrada

    Parameters
    ----------
    df_votacion : DataFrame
        DataFrame con los resultados de la votación
    territorio_codigo : str
        Código del territorio a filtrar (provincia, cantón, parroquia)
    agrupar_por_territorio : str
        Agrupar los resultados por territorio (PAIS, PROVINCIA, CANTON, CIRCUNSCRIPCION, PARROQUIA)
    sexo : str
        Sexo a filtrar (S0, S1, AMBOS, AGRUPAR)

    Returns
    -------
    DataFrame
        DataFrame con los resultados de la votación filtrados

    Examples
    --------
    >>> df_votacion = pd.read_csv("test_2023_votacion.csv")
    >>> df_votacion_filtered = extract_votacion(df_votacion, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS")
    >>> print(df_votacion_filtered)
    >>>  PROVINCIA
    >>>  P01    100000
    """
    columnas_agrupar = ['SEXO', 'VUELTA']
    if dignidad_codigo is not None:
        df_votacion = df_votacion[df_votacion['DIGNIDAD_CODIGO'] == dignidad_codigo]
    # Filter by territory
    if territorio_codigo is not None:
        if len(territorio_codigo) == 4:  # EC + 2 digits (Provincias)
            df_votacion = df_votacion[df_votacion['PROVINCIA_CODIGO'] == territorio_codigo]
        elif len(territorio_codigo) == 6:  # EC + 4 digits (Cantones)
            df_votacion = df_votacion[df_votacion['CANTON_CODIGO'] == territorio_codigo]
        elif len(territorio_codigo) == 8:  # EC + 6 digits (Parroquias)
            df_votacion = df_votacion[df_votacion['PARROQUIA_CODIGO'] == territorio_codigo]

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

        # df_votacion_blancos = df_votacion.groupby(columnas_agrupar)['BLANCOS'].sum().reset_index()
        # df_votacion_nulos = df_votacion.groupby(columnas_agrupar)['NULOS'].sum().reset_index()
        # df_votacion = pd.merge(df_votacion_blancos, df_votacion_nulos, on=columnas_agrupar)

    if sexo is not None:
        if sexo == 'S0' or sexo == "S1":
            df_votacion = df_votacion[df_votacion['SEXO'] == sexo]
        if sexo == "AMBOS":
            pass
        if sexo == "AGRUPAR":
            # delete the "SEXO" column in columnas_agrupar
            columnas_agrupar.remove('SEXO')
        df_votacion_blancos = df_votacion.groupby(columnas_agrupar)['BLANCOS'].sum().reset_index()
        df_votacion_nulos = df_votacion.groupby(columnas_agrupar)['NULOS'].sum().reset_index()
        df_votacion = pd.merge(df_votacion_blancos, df_votacion_nulos, on=columnas_agrupar)

    if vuelta is not None:
        df_votacion = df_votacion[df_votacion['VUELTA'] == vuelta]
    else:
        pass
    return df_votacion


