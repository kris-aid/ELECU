#%%
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from elecu.elecu import restructure_results, extract_values, visualize_results
from elecu.elecu.extract_values import extract_eleccion, extract_votacion
import pandas as pd
from elecu.elecu.restructure_results import Standarized_Results


#%%
def test_standarized_registro(year=2023):
    input_folder = f"data/csv_files/generales/{year}"
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
    input_folder = f"data/csv_files/generales/{year}"
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

# Create output directory
output_dir = f"tests/Presidenciales/{year}"
os.makedirs(output_dir, exist_ok=True)

test_year_votacion, test_year_eleccion, test = test_standarized_resultados(year)
print(f"[OK] Datos de {year} cargados correctamente")
print(f"  - Votacion shape: {test_year_votacion.shape}")
print(f"  - Eleccion shape: {test_year_eleccion.shape}")

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
presidentes_votacion_corto.to_csv(f"{output_dir}/presidentes_votacion_cantonal_formato_angosto_{year}.csv", index=False)
print(f"[OK] Guardado: presidentes_votacion_cantonal_formato_angosto_{year}.csv ({presidentes_votacion_corto.shape[0]} filas)")

# Archivo 2: presidentes_electores_sufragantes_cantonal_formato_angosto_2025.csv
test_registro_2025 = test_standarized_registro(year)
# Mantener solo columnas de canton, electores, etc (sin SEXO para formato angosto)
columnas_registro = [col for col in test_registro_2025.columns if 'CANTON' in col or 'ELECTORES' in col or 'SUFRAGANTES' in col]
test_registro_2025_filtered = test_registro_2025[columnas_registro].copy()
test_registro_2025_filtered = test_registro_2025_filtered.drop_duplicates()
test_registro_2025_filtered.to_csv(f"{output_dir}/presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv", index=False)
print(f"[OK] Guardado: presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv ({test_registro_2025_filtered.shape[0]} filas)")

# Archivo 3: presidentes_votacion_cantonal_formato_ancho_2025.csv (Formato ancho con candidatos como columnas)
presidentes_votacion_ancho = test_year_eleccion[['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE', 'VOTOS']].copy()
# Pivot table para formato ancho: candidatos como columnas
presidentes_votacion_ancho = presidentes_votacion_ancho.pivot_table(
    index=['CANTON_CODIGO', 'VUELTA'],
    columns='CANDIDATO_NOMBRE',
    values='VOTOS',
    aggfunc='sum'
).reset_index()
presidentes_votacion_ancho.to_csv(f"{output_dir}/presidentes_votacion_cantonal_formato_ancho_{year}.csv", index=False)
print(f"[OK] Guardado: presidentes_votacion_cantonal_formato_ancho_{year}.csv ({presidentes_votacion_ancho.shape[0]} filas)")

print(f"\n[SUCCESS] Generacion completada. Los archivos estan en: {output_dir}/")
