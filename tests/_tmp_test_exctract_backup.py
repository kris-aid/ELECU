# backup of original test_exctract.py
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
    # Mostrar columnas del DataFrame estandarizado (completo) antes de agrupar por cantones
    print("Columnas del DataFrame resultados (completo):", df_resultados_full.columns.tolist())
    resultados = {}
    
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
        
        # Verificar columnas antes de guardar
        print(f"\nColumnas en elección vuelta {vuelta}:")
        print(df_eleccion.columns.tolist())
        
        resultados[f"vuelta_{vuelta}"] = {
            "eleccion": df_eleccion,
            "votacion": df_votacion_filtered
        }
        
        if save_csv:
            import os
            os.makedirs("test_results", exist_ok=True)
            df_eleccion.to_csv(f"test_results/eleccion_cantonal_v{vuelta}_{year}.csv", index=False)
            df_votacion_filtered.to_csv(f"test_results/votacion_cantonal_v{vuelta}_{year}.csv", index=False)
            
        print(f"\nResultados vuelta {vuelta}:")
        print(f"Registros elección: {len(df_eleccion)}")
        print(f"Registros votación: {len(df_votacion_filtered)}")
    
    return resultados

if __name__ == "__main__":
    # Ejecutar extracción de resultados
    resultados = extract_resultados_cantonal(2025, "generales", save_csv=True)
    
    # Mostrar estructura de los datos
    for vuelta in ['1', '2']:
        print(f"\nColumnas disponibles en vuelta {vuelta}:")
        print("Elección:", resultados[f"vuelta_{vuelta}"]['eleccion'].columns.tolist())
        print("Votación:", resultados[f"vuelta_{vuelta}"]['votacion'].columns.tolist())
