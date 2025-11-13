#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

base = Path('c:\\Users\\FELIPE\\Downloads\\ELECU\\tests\\Presidenciales')

files = {
    'ANGOSTO': base / 'presidentes_votacion_consolidado_2002_2025.csv',
    'ANCHO': base / 'presidentes_votacion_consolidado_2002_2025_ancho.csv',
    'RESUMEN': base / 'presidentes_resumen_nacional_2002_2025.csv'
}

for tipo, filepath in files.items():
    if filepath.exists():
        df = pd.read_csv(filepath)
        size_mb = filepath.stat().st_size / (1024*1024)
        print(f"\n{tipo}: {len(df)} filas x {len(df.columns)} columnas ({size_mb:.1f} MB)")
        
        if tipo == 'ANGOSTO':
            print(f"  Años: {sorted(df['ANIO'].unique())}")
            print(f"  Candidatos: {df['CANDIDATO_NOMBRE'].nunique()} unicos")
            print(f"  Cantons: {df['CANTON_CODIGO'].nunique()}")
        elif tipo == 'ANCHO':
            print(f"  Columnas: {df.columns[:5].tolist()}... (total {len(df.columns)})")
        elif tipo == 'RESUMEN':
            top_3 = df.nlargest(3, 'TOTAL_VOTOS')[['CANDIDATO_NOMBRE', 'ANIO', 'TOTAL_VOTOS']]
            print(f"  Top 3 candidatos: {top_3['CANDIDATO_NOMBRE'].tolist()}")
