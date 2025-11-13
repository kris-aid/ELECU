"""
Crear base de datos consolidada con todos los años (2002-2025)
Unifica todos los archivos CSV en un solo archivo
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from pathlib import Path

def consolidate_all_years():
    """
    Consolida todos los archivos de votación de todos los años
    en un único archivo CSV unificado
    """
    
    base_path = "tests/Presidenciales"
    output_file = "tests/Presidenciales/presidentes_votacion_consolidado_2002_2025.csv"
    
    all_years = [2002, 2006, 2007, 2009, 2013, 2017, 2021, 2023, 2025]
    dataframes = []
    
    print("\n" + "="*70)
    print("CONSOLIDANDO DATOS ELECTORALES 2002-2025")
    print("="*70 + "\n")
    
    for year in all_years:
        year_path = os.path.join(base_path, str(year))
        angosto_file = os.path.join(year_path, f"presidentes_votacion_cantonal_formato_angosto_{year}.csv")
        
        if os.path.exists(angosto_file):
            try:
                df = pd.read_csv(angosto_file)
                
                # Asegurar que tenga las columnas requeridas
                if 'ANIO' not in df.columns:
                    df['ANIO'] = year
                if 'VUELTA' not in df.columns:
                    df['VUELTA'] = 1
                
                dataframes.append(df)
                print(f"[OK] {year}: {df.shape[0]:,} registros cargados")
                
            except Exception as e:
                print(f"[ERROR] {year}: {str(e)[:60]}")
        else:
            print(f"[SKIP] {year}: Archivo no encontrado")
    
    if dataframes:
        # Consolidar todos los dataframes
        consolidated = pd.concat(dataframes, ignore_index=True)
        
        # Reordenar columnas para consistencia
        cols_order = ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 
                      'CANTON_CODIGO', 'CANTON_NOMBRE', 'CANDIDATO_NOMBRE', 'AGRUPACION', 'VOTOS']
        
        available_cols = [c for c in cols_order if c in consolidated.columns]
        consolidated = consolidated[available_cols]
        
        # Llenar NaN en columnas de texto
        if 'AGRUPACION' in consolidated.columns:
            consolidated['AGRUPACION'] = consolidated['AGRUPACION'].fillna('T')
        consolidated['VOTOS'] = consolidated['VOTOS'].fillna(0).astype(int)
        
        # Ordenar por año, vuelta, provincia, canton
        consolidated = consolidated.sort_values(by=['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'CANTON_CODIGO'])
        
        # Guardar
        consolidated.to_csv(output_file, index=False)
        
        print("\n" + "="*70)
        print("RESULTADOS")
        print("="*70)
        print(f"\nTotal de filas consolidadas: {len(consolidated):,}")
        print(f"Años cubiertos: {sorted(consolidated['ANIO'].unique())}")
        print(f"Candidatos únicos: {consolidated['CANDIDATO_NOMBRE'].nunique()}")
        print(f"Cantons: {consolidated['CANTON_CODIGO'].nunique()}")
        print(f"Provincias: {consolidated['PROVINCIA_CODIGO'].nunique()}")
        
        print(f"\nArchivo guardado: {output_file}")
        print(f"Tamaño: {os.path.getsize(output_file) / 1024:.1f} KB")
        
        # Mostrar resumen por año
        print("\nResumen por año:")
        summary = consolidated.groupby('ANIO').agg({
            'VOTOS': 'sum',
            'CANDIDATO_NOMBRE': 'nunique',
            'CANTON_CODIGO': 'nunique'
        }).rename(columns={'VOTOS': 'Total_Votos', 'CANDIDATO_NOMBRE': 'Candidatos', 'CANTON_CODIGO': 'Cantons'})
        print(summary)
        
        return consolidated
    else:
        print("[ERROR] No se pudieron cargar datos de ningún año")
        return None

def create_wide_format_consolidated():
    """
    Crea una versión en formato ancho (wide) consolidado
    """
    
    consolidated_file = "tests/Presidenciales/presidentes_votacion_consolidado_2002_2025.csv"
    
    if not os.path.exists(consolidated_file):
        print("[ERROR] Archivo consolidado no existe. Ejecute consolidate_all_years() primero.")
        return
    
    df = pd.read_csv(consolidated_file)
    
    print("\nCreando formato ANCHO consolidado...")
    
    # Agrupar por año, vuelta, canton y pivotar por candidato
    df_wide = df.pivot_table(
        index=['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'],
        columns='CANDIDATO_NOMBRE',
        values='VOTOS',
        aggfunc='sum'
    ).reset_index()
    
    df_wide = df_wide.fillna(0).astype({col: int for col in df_wide.columns[6:]})
    
    output_file = "tests/Presidenciales/presidentes_votacion_consolidado_2002_2025_ancho.csv"
    df_wide.to_csv(output_file, index=False)
    
    print(f"[OK] Archivo ancho guardado: {output_file}")
    print(f"     {df_wide.shape[0]:,} filas × {df_wide.shape[1]} columnas")
    
    return df_wide

def create_summary_by_year():
    """
    Crea un resumen de votación total por año y candidato
    """
    
    consolidated_file = "tests/Presidenciales/presidentes_votacion_consolidado_2002_2025.csv"
    
    if not os.path.exists(consolidated_file):
        print("[ERROR] Archivo consolidado no existe.")
        return
    
    df = pd.read_csv(consolidated_file)
    
    print("\nCreando resumen por año y candidato...")
    
    # Resumen: total votos por año, candidato
    summary = df.groupby(['ANIO', 'CANDIDATO_NOMBRE'])['VOTOS'].sum().reset_index()
    summary = summary.sort_values(['ANIO', 'VOTOS'], ascending=[True, False])
    
    output_file = "tests/Presidenciales/presidentes_resumen_nacional_2002_2025.csv"
    summary.to_csv(output_file, index=False)
    
    print(f"[OK] Resumen guardado: {output_file}")
    print(f"     {summary.shape[0]:,} registros (candidato-año)")
    
    # Mostrar top 5 por año
    print("\nTop 5 candidatos por año:")
    for year in sorted(df['ANIO'].unique()):
        print(f"\n  {year}:")
        top = summary[summary['ANIO'] == year].head(5)
        for _, row in top.iterrows():
            print(f"    {row['CANDIDATO_NOMBRE']}: {int(row['VOTOS']):,} votos")
    
    return summary

def main():
    print("\n" + "="*70)
    print("CONSOLIDADOR DE DATOS ELECTORALES (2002-2025)")
    print("="*70)
    
    # Paso 1: Consolidar formato angosto
    consolidated = consolidate_all_years()
    
    if consolidated is not None:
        # Paso 2: Crear formato ancho
        create_wide_format_consolidated()
        
        # Paso 3: Crear resumen nacional
        create_summary_by_year()
        
        print("\n" + "="*70)
        print("CONSOLIDACION COMPLETADA")
        print("="*70)
        print("\nArchivos generados:")
        print("  1. presidentes_votacion_consolidado_2002_2025.csv (ANGOSTO)")
        print("  2. presidentes_votacion_consolidado_2002_2025_ancho.csv (ANCHO)")
        print("  3. presidentes_resumen_nacional_2002_2025.csv (RESUMEN)")
        print("\nTodos en: tests/Presidenciales/")
        print("\n")

if __name__ == "__main__":
    main()
