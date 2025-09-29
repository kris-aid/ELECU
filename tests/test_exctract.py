
from elecu.extract_values import extract_eleccion,  extract_votacion
from elecu.restructure_results import Standarized_Results

def test_standarized_resultados(year=2023,tipo="generales"):
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
    return test_year_votacion, test_year_eleccion


def test_extract_eleccion(year=2023,tipo="generales"):
    # test with the 2023 results that are in the test folder
    df_votacion,df_resultados = test_standarized_resultados(year,tipo)
    # Test 1: extract values for a specific dignidad
    df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo="4", territorio_codigo="EC0901",agrupar_por_territorio="CANTON", sexo="AGRUPAR", vuelta="1")
    df_votacion_filtered = extract_votacion(df_votacion, dignidad_codigo="4", territorio_codigo="EC0901",agrupar_por_territorio="CANTON", sexo="AGRUPAR", vuelta="1")
    print(df_resultados_filtered)
    print(df_resultados_filtered.columns)
    
if __name__ == "__main__":
    test_extract_eleccion(2023,"seccionales")