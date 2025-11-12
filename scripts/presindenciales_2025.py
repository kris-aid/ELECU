#%%
import elecu.restructure_results
import elecu.extract_values
import elecu.visualize_results
from elecu.extract_values import extract_eleccion, extract_votacion
import pandas as pd
from elecu.restructure_results import Standarized_Results


#%%
def test_standarized_registro(year=2023):
    input_folder = f"../data/csv_files/generales/{year}"
    standarized_folder = "elecu/elecu/data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)

    #print(standarized_results.df_registro)
    standarized_results.change_registro()
    #print(standarized_results.df_registro)
    test_registro = standarized_results.put_standar_geo_codes_registro_canton(drop_old=True,year=year)
    if "ELECTORES MENORES A 18" not in test_registro.columns:
        test_registro["ELECTORES MENORES A 18"]=0
    return test_registro


def test_standarized_resultados(year=2023):
    input_folder = f"../data/csv_files/generales/{year}"
    standarized_folder = "elecu/elecu/data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    #print(standarized_results.df_resultados)
    standarized_results.change_resultados()
    #print(standarized_results.df_resultados)
    test = standarized_results.put_standar_geo_codes_results_cantones(drop_old=True,year=year)
    test_year_votacion, test_year_eleccion = standarized_results.divide_resultados()
    return test_year_votacion, test_year_eleccion,test

#%%
# Procesar 2025
print("Procesando año 2025...")
year = 2025
test_year_votacion, test_year_eleccion, test = test_standarized_resultados(year)
print(f"✓ Datos de {year} cargados correctamente")
print(f"  - Votación shape: {test_year_votacion.shape}")
print(f"  - Elección shape: {test_year_eleccion.shape}")

# Generar archivos de salida para 2025
print("\nGenerando archivos de salida para 2025...")

# Archivo 1: presidentes_votacion_cantonal_formato_angosto_2025.csv (Formato angosto/largo)
# Formato: CANTON_CODIGO, VUELTA, CANDIDATO_NOMBRE, VOTOS
presidentes_votacion_corto = test_year_eleccion[['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE', 'VOTOS']].copy()
# Agrupar por CANTON_CODIGO, VUELTA y CANDIDATO_NOMBRE sumando los votos (por si hay duplicados)
presidentes_votacion_corto = presidentes_votacion_corto.groupby(['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE']).agg({
    'VOTOS': 'sum'
}).reset_index()
presidentes_votacion_corto = presidentes_votacion_corto.drop_duplicates()
presidentes_votacion_corto.to_csv("../tests/Presidenciales/2025/presidentes_votacion_cantonal_formato_angosto_2025.csv", index=False)
print(f"✓ Guardado: presidentes_votacion_cantonal_formato_angosto_2025.csv ({presidentes_votacion_corto.shape[0]} filas)")

# Archivo 2: presidentes_electores_sufragantes_cantonal_formato_angosto_2025.csv
test_registro_2025 = test_standarized_registro(year)
# Mantener solo columnas de canton, electores, etc (sin SEXO para formato angosto)
columnas_registro = [col for col in test_registro_2025.columns if 'CANTON' in col or 'ELECTORES' in col or 'SUFRAGANTES' in col]
test_registro_2025_filtered = test_registro_2025[columnas_registro].copy()
test_registro_2025_filtered = test_registro_2025_filtered.drop_duplicates()
test_registro_2025_filtered.to_csv("../tests/Presidenciales/2025/presidentes_electores_sufragantes_cantonal_formato_angosto_2025.csv", index=False)
print(f"✓ Guardado: presidentes_electores_sufragantes_cantonal_formato_angosto_2025.csv ({test_registro_2025_filtered.shape[0]} filas)")

# Archivo 3: presidentes_votacion_cantonal_formato_ancho_2025.csv (Formato ancho con candidatos como columnas)
presidentes_votacion_ancho = test_year_eleccion[['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE', 'VOTOS']].copy()
# Pivot table para formato ancho: candidatos como columnas
presidentes_votacion_ancho = presidentes_votacion_ancho.pivot_table(
    index=['CANTON_CODIGO', 'VUELTA'],
    columns='CANDIDATO_NOMBRE',
    values='VOTOS',
    aggfunc='sum'
).reset_index()
presidentes_votacion_ancho.to_csv("../tests/Presidenciales/2025/presidentes_votacion_cantonal_formato_ancho_2025.csv", index=False)
print(f"✓ Guardado: presidentes_votacion_cantonal_formato_ancho_2025.csv ({presidentes_votacion_ancho.shape[0]} filas)")

print("\n✓ Generación completada. Los archivos están en: ../tests/Presidenciales/2025/")
