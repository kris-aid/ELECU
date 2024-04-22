import pandas as pd
from open_elec.transform_to_csv import convert_sav_to_csv

def test_convert_sav_to_csv():
    input_folder = "data"
    output_folder = "data_csv"
    convert_sav_to_csv(input_folder, output_folder)
    
from open_elec.create_std_dicts import Standard_Dictionaries

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
    
from open_elec.restructure_results import Standarized_Results    
def test_standarized_results():
    input_folder = "data_csv/generales/2023"
    standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    print(standarized_results.df_resultados)
    standarized_results.change_resultados()
    test = standarized_results.put_standar_geo_codes_results(drop_old=True)
    test.to_csv("tests/test_results/test_2023.csv", index=False)
    test_2023_votacion, test_2023_eleccion = standarized_results.divide_resultados()
    test_2023_votacion.to_csv("tests/test_results/test_2023_votacion.csv", index=False)
    test_2023_eleccion.to_csv("tests/test_results/test_2023_eleccion.csv", index=False)
    
from open_elec.extract_values import extract_eleccion

def test_extract_eleccion():

    # test with the 2023 results that are in the test folder
    df_resultados = pd.read_csv("../../tests/test_results/test_2023_eleccion.csv")
    # Test 1: extract values for a specific dignidad
    df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS", vuelta=None)
    print(df_resultados_filtered)
    print(df_resultados_filtered.columns)

from open_elec.visualize_results import visualize_results
def test_visualize_results():
    df_resultados = pd.read_csv("../../tests/test_results/test_2023_eleccion.csv")
    df_resultados = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo="P01",agrupar_por_territorio="PROVINCIA", sexo="AMBOS", vuelta=1)
    #df_resultados.to_csv("../../../tests/test_results/test_2023_eleccion_filtered.csv", index=False)
    visualize_results(df_resultados, bar_plot=True, pie_plot=True)
    print("Visualización completada")

if __name__ == "__main__":

    test_standarized_results()