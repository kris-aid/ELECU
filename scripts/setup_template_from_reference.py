#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

def setup_templates_from_reference():
    """Copiar datos del archivo de referencia del usuario a los templates"""
    
    # Leer archivo de referencia
    ref_file = Path('c:\\Users\\FELIPE\\Downloads\\ELECU\\presidentes_votacion_cantonal_formato_angosto.csv')
    ref_df = pd.read_csv(ref_file)
    
    print(f"Referencia: {len(ref_df)} filas")
    print(f"Años en referencia: {sorted(ref_df['ANIO'].unique())}")
    print(f"Columnas: {ref_df.columns.tolist()}\n")
    
    base_path = Path('c:\\Users\\FELIPE\\Downloads\\ELECU\\tests\\Presidenciales')
    
    # Copiar datos por año desde la referencia
    years_in_ref = [2002, 2006, 2009, 2013, 2017, 2021, 2023]
    
    for year in years_in_ref:
        year_data = ref_df[ref_df['ANIO'] == year].copy()
        
        if len(year_data) > 0:
            year_dir = base_path / str(year)
            year_dir.mkdir(exist_ok=True, parents=True)
            
            # Guardar en formato angosto
            angosto_file = year_dir / f'presidentes_votacion_cantonal_formato_angosto_{year}.csv'
            year_data.to_csv(angosto_file, index=False)
            print(f"[OK] {year}: {len(year_data)} registros guardados")
    
    # Para 2007 (no en referencia), crear template vacío
    year_dir = base_path / '2007'
    year_dir.mkdir(exist_ok=True, parents=True)
    empty_df = pd.DataFrame(columns=['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 
                                      'CANTON_CODIGO', 'CANTON_NOMBRE', 'CANDIDATO_NOMBRE', 
                                      'AGRUPACION', 'VOTOS'])
    empty_df.to_csv(year_dir / 'presidentes_votacion_cantonal_formato_angosto_2007.csv', index=False)
    print(f"[OK] 2007: template vacío creado")

if __name__ == '__main__':
    setup_templates_from_reference()
