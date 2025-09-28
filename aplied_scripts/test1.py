#%%
import pandas as pd
from elecu.elecu.extract_values import extract_eleccion
#%%
#
#%%
def test_create_std_dicts():
    input_folder = "data_csv/seccionales/2009"
    std_dicts = Standard_Dictionaries(input_folder)
    print(std_dicts.df_provincias)
    std_dicts.change_to_std_provincias()
    print(std_dicts.df_provincias)
    print(std_dicts.df_cantones)
    std_dicts.change_to_std_cantones()
    print(std_dicts.df_cantones)
    print(std_dicts.df_parroquias)
    std_dicts.change_to_std_parroquias()
    print(std_dicts.df_parroquias)
#%%
from elecu.elecu.restructure_results import Standarized_Results
def test_standarized_registro(year=2023):
    input_folder = f"../../data_csv/generales/{year}"
    standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    #print(standarized_results.df_resultados)
    print(standarized_results.df_registro)
    #standarized_results.change_resultados()
    standarized_results.change_registro()
    print(standarized_results.df_registro)
    test_registro = standarized_results.put_standar_geo_codes_registro(drop_old=True)
    columnas_agrupar = ['PROVINCIA_CODIGO', 'CANTON_CODIGO', 'PARROQUIA_CODIGO']
    df_resultados = df_resultados.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()
    return test_registro


def test_standarized_resultados(year=2023):
    input_folder = f"../../data_csv/generales/{year}"
    standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    print(standarized_results.df_resultados)
    standarized_results.change_resultados()
    print(standarized_results.df_resultados)
    test = standarized_results.put_standar_geo_codes_results(drop_old=True)
    test_year_votacion, test_year_eleccion = standarized_results.divide_resultados()
    # test_2023_votacion.to_csv("../../tests/test_results/test_2023_votacion.csv", index=False)
    # test_2023_eleccion.to_csv("../../tests/test_results/test_2023_eleccion.csv", index=False)


from elecu.elecu.extract_values import extract_eleccion

def test_extract_eleccion(year=2023):

    # test with the 2023 results that are in the test folder
    df_resultados = pd.read_csv(f"../../tests/test_results/test_{year}_eleccion.csv")
    # Test 1: extract values for a specific dignidad
    df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo=None,agrupar_por_territorio="PROVINCIA", sexo="AGRUPAR", vuelta=1)
    print(df_resultados_filtered)
    print(df_resultados_filtered.columns)
#%%

from elecu.elecu.visualize_results import visualize_results_presidentes
def test_visualize_results():
    df_resultados = pd.read_csv("../../tests/test_results/test_2023_eleccion.csv")
    df_resultados = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS", vuelta=1)
    #df_resultados.to_csv("../../../tests/test_results/test_2023_eleccion_filtered.csv", index=False)
    visualize_results_presidentes(df_resultados, bar_plot=True, pie_plot=True)
    print("Visualización completada")
#%%
if __name__ == "__main__":

   test_visualize_results()