from elecu.restructure_results import Standarized_Results
import os
def test_standarized_registro(year=2023):
    input_folder = f"data/csv_files/generales/{year}"
    #standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder)#, standarized_folder)
    #print(standarized_results.df_resultados)
    print(standarized_results.df_registro)
    #standarized_results.change_resultados()
    standarized_results.change_registro()
    print(standarized_results.df_registro)
    test_registro = standarized_results.put_standar_geo_codes_registro_canton(drop_old=True,year=year)
    columnas_agrupar = ['PROVINCIA_CODIGO', 'CANTON_CODIGO', 'PARROQUIA_CODIGO']
    test_registro = test_registro.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()
    return test_registro


def test_standarized_resultados(year=2023):
    input_folder = f"data/csv_files/generales/{year}"
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

if __name__ == "__main__":
    print(os.getcwd())
    registro=test_standarized_registro(2023)
    votacion,eleccion=test_standarized_resultados(2023)
    
    