from elecu.extract_values import extract_eleccion,  extract_votacion
from elecu.restructure_results import Standarized_Results

def test_standarized_resultados(year=2025,tipo="generales"):
    input_folder = f"data/csv_files/{tipo}/{year}"
    #standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder)#, standarized_folder)
    print(standarized_results.df_resultados)
    standarized_results.change_resultados()
    print(standarized_results.df_resultados)
    test = standarized_results.put_standar_geo_codes_results_cantones(drop_old=True,year=year)
    test_year_votacion, test_year_eleccion = standarized_results.divide_resultados()
    # test_2023_votacion.to_csv("../../tests/test_results/test_2023_votacion.csv", index=False)
    # test_2023_eleccion.to_csv("../../tests/test_results/test_2023_eleccion.csv", index=False)
    # return also the full standardized resultados dataframe (with geo codes) so callers can aggregate by territory
    return test_year_votacion, test_year_eleccion, standarized_results.df_resultados


def test_extract_eleccion(year=2025,tipo="generales"):
    # test with the 2023 results that are in the test folder
    df_votacion, df_resultados_pruned, df_resultados_full = test_standarized_resultados(year,tipo)
    # Mostrar columnas del DataFrame estandarizado (completo) antes de extraer
    print("Columnas del DataFrame resultados (completo):", df_resultados_full.columns.tolist())
    # Test 1: extract values for a specific dignidad using the full standardized resultados (contains geo codes)
    df_resultados_filtered = extract_eleccion(df_resultados_full, dignidad_codigo="1", territorio_codigo=None,agrupar_por_territorio="CANTON", sexo="AGRUPAR", vuelta="1")
    df_votacion_filtered = extract_votacion(df_votacion, dignidad_codigo="1", territorio_codigo=None,agrupar_por_territorio="CANTON", sexo="AGRUPAR", vuelta="1")
    print(df_resultados_filtered)
    print(df_resultados_filtered.columns)
    
def extract_resultados_cantonal(year=2025, tipo="generales", save_csv=True):
    """
    Extrae resultados de primera y segunda vuelta a nivel cantonal.
    Args:
        year: int - año de la elección
        tipo: str - tipo de elección ('generales')
        save_csv: bool - si guardar archivos CSV
    Returns:
        dict con resultados por vuelta
    """
    df_votacion, df_resultados_pruned, df_resultados_full = test_standarized_resultados(year, tipo)
    print("Columnas del DataFrame resultados (completo):", df_resultados_full.columns.tolist())
    resultados = {}
    
    # Cargar diccionario de cantones
    import os
    import pandas as pd
    candidates = [
        os.path.join("data", "Codigos_estandar", "cantones", "std_cantones.csv"),
        os.path.join("elecu", "elecu", "data", "Codigos_estandar", "cantones", "std_cantones.csv"),
        os.path.join("elecu", "data", "Codigos_estandar", "cantones", "std_cantones.csv"),
    ]
    std_path = None
    for c in candidates:
        if os.path.exists(c):
            std_path = c
            break

    std_cant = None
    if std_path is not None:
        std_cant = pd.read_csv(std_path)
        for col in std_cant.columns:
            if "CODIGO" in col:
                std_cant[col] = std_cant[col].astype(str)
    
    # Lista para almacenar DataFrames de cada vuelta
    dfs_eleccion = []
    dfs_votacion = []
    
    for vuelta in ['1', '2']:
        # Extraer resultados elección
        df_eleccion = extract_eleccion(
            df_resultados_full, 
            dignidad_codigo="1",
            territorio_codigo=None,
            agrupar_por_territorio="CANTON",
            sexo="AGRUPAR",
            vuelta=vuelta
        )
        
        # Extraer resultados votación
        df_votacion_filtered = extract_votacion(
            df_votacion,
            dignidad_codigo="1",
            territorio_codigo=None,
            agrupar_por_territorio="CANTON",
            sexo="AGRUPAR",
            vuelta=vuelta
        )
        
        # Agregar nombres de cantones si está disponible
        if std_cant is not None:
            if 'CANTON_CODIGO' in df_eleccion.columns:
                df_eleccion = df_eleccion.merge(std_cant[['CANTON_CODIGO', 'CANTON_NOMBRE']], on='CANTON_CODIGO', how='left')
            if 'CANTON_CODIGO' in df_votacion_filtered.columns:
                df_votacion_filtered = df_votacion_filtered.merge(std_cant[['CANTON_CODIGO', 'CANTON_NOMBRE']], on='CANTON_CODIGO', how='left')

        # Reordenar columnas para poner CANTON_NOMBRE después de CANTON_CODIGO
        def _move_name_after_code(df):
            if 'CANTON_CODIGO' in df.columns and 'CANTON_NOMBRE' in df.columns:
                cols = list(df.columns)
                cols = [c for c in cols if c != 'CANTON_NOMBRE']
                try:
                    idx = cols.index('CANTON_CODIGO')
                except ValueError:
                    return df
                cols.insert(idx+1, 'CANTON_NOMBRE')
                return df[cols]
            return df

        df_eleccion = _move_name_after_code(df_eleccion)
        df_votacion_filtered = _move_name_after_code(df_votacion_filtered)
        
        dfs_eleccion.append(df_eleccion)
        dfs_votacion.append(df_votacion_filtered)
        
        resultados[f"vuelta_{vuelta}"] = {
            "eleccion": df_eleccion,
            "votacion": df_votacion_filtered
        }
    
    if save_csv:
        os.makedirs("test_results", exist_ok=True)
        
        # Formato angosto (todas las vueltas juntas)
        df_eleccion_completo = pd.concat(dfs_eleccion)
        df_votacion_completo = pd.concat(dfs_votacion)
        
        # Añadir columna AÑO
        df_eleccion_completo['AÑO'] = year
        df_votacion_completo['AÑO'] = year
        
        df_eleccion_completo.to_csv(f"test_results/eleccion_cantonal_todas_vueltas_{year}.csv", index=False)
        df_votacion_completo.to_csv(f"test_results/votacion_cantonal_todas_vueltas_{year}.csv", index=False)
        
        # Formato ancho (una fila por cantón)
        df_eleccion_ancho = df_eleccion_completo.pivot_table(
            index=['CANTON_CODIGO', 'CANTON_NOMBRE'],
            columns=['VUELTA', 'CANDIDATO_NOMBRE'],
            values='VOTOS',
            aggfunc='first'
        ).reset_index()
        
        # Aplanar nombres de columnas multinivel
        df_eleccion_ancho.columns = [
            f"{col[1]}_{col[0]}" if col[1] and col[0] else col[0] 
            for col in df_eleccion_ancho.columns
        ]
        
        # Añadir columna AÑO
        df_eleccion_ancho['AÑO'] = year
        
        df_eleccion_ancho.to_csv(f"test_results/eleccion_cantonal_formato_ancho_{year}.csv", index=False)
        
        print("\nArchivos guardados:")
        print(f"- Formato angosto (todas las vueltas): eleccion_cantonal_todas_vueltas_{year}.csv")
        print(f"- Formato ancho: eleccion_cantonal_formato_ancho_{year}.csv")
        
    return resultados

if __name__ == "__main__":
    # Ejecutar extracción de resultados
    resultados = extract_resultados_cantonal(2025, "generales", save_csv=True)
    
    # Mostrar estructura de los datos
    for vuelta in ['1', '2']:
        print(f"\nColumnas disponibles en vuelta {vuelta}:")
        print("Elección:", resultados[f"vuelta_{vuelta}"]['eleccion'].columns.tolist())
        print("Votación:", resultados[f"vuelta_{vuelta}"]['votacion'].columns.tolist())