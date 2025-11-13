"""
Simplified year-based organizer that creates clean CSV files for testing
Generates test data in a structure organized by year
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from pathlib import Path

def get_available_years():
    """Get list of available years in data folder"""
    base_path = "data/csv_files/generales"
    if not os.path.exists(base_path):
        return []
    
    years = []
    for item in os.listdir(base_path):
        if item.isdigit() and int(item) <= 2025:
            years.append(int(item))
    
    return sorted(years)

def create_minimal_test_structure():
    """Create minimal test CSV files for each available year"""
    
    OUTPUT_BASE = "tests/Presidenciales"
    available_years = get_available_years()
    
    print("\n" + "="*70)
    print("CREATING TEST STRUCTURE FOR ELECTORAL DATA (2002-2025)")
    print("="*70)
    
    # Ensure base directory exists
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    
    # Create year directories
    for year in available_years:
        year_dir = os.path.join(OUTPUT_BASE, str(year))
        os.makedirs(year_dir, exist_ok=True)
        print(f"\n[{year}] Directory created: {year_dir}")
    
    # Create placeholder CSV files  with minimal valid data structure
    candidate_dict = {
        2002: ["RODRIGO BORJA","JACINTO VELAZQUEZ","ALVARO NOBOA","LUCIO GUTIERREZ"],
        2006: ["RAFAEL CORREA","ALVARO NOBOA","LUIS VILLACIS","CYNTHIA VITERI"],
        2007: ["RAFAEL CORREA","ALVARO NOBOA"],
        2009: ["RAFAEL CORREA","LUCIO GUTIERREZ","ALVARO NOBOA"],
        2013: ["RAFAEL CORREA","GUILLERMO LASSO"],
        2017: ["LENIN MORENO","GUILLERMO LASSO"],
        2021: ["GUILLERMO LASSO","ANDRES ARAUZ","YAKU PEREZ"],
        2023: ["DANIEL NOBOA","LUISA GONZALEZ","YAKU PEREZ"],
        2025: ["DANIEL NOBOA AZIN","LUISA GONZALEZ","HENRY CUCALON"]
    }
    
    for year in available_years:
        year_dir = os.path.join(OUTPUT_BASE, str(year))
        candidates = candidate_dict.get(year, ["CANDIDATO_A", "CANDIDATO_B"])
        
        try:
            # Create sample vote data structure
            cantons_sample = ["EC0101", "EC0102", "EC0103"]  # Quito sample
            vuelta_values = [1, 2] if year not in [2007, 2009, 2013] else [1]
            
            # File 1: Formato angosto (long format)
            data_angosto = []
            for canton in cantons_sample:
                for vuelta in vuelta_values:
                    for candidate in candidates:
                        data_angosto.append({
                            'CANTON_CODIGO': canton,
                            'VUELTA': vuelta,
                            'CANDIDATO_NOMBRE': candidate,
                            'VOTOS': 100
                        })
            
            df_angosto = pd.DataFrame(data_angosto)
            df_angosto.to_csv(
                os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_angosto_{year}.csv"),
                index=False
            )
            print(f"  [OK] Created: presidentes_votacion_cantonal_formato_angosto_{year}.csv ({df_angosto.shape[0]} rows)")
            
            # File 2: Formato ancho (wide format)
            df_wide = df_angosto.pivot_table(
                index=['CANTON_CODIGO', 'VUELTA'],
                columns='CANDIDATO_NOMBRE',
                values='VOTOS',
                aggfunc='first'
            ).reset_index()
            df_wide.fillna(0, inplace=True)
            df_wide.to_csv(
                os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_ancho_{year}.csv"),
                index=False
            )
            print(f"  [OK] Created: presidentes_votacion_cantonal_formato_ancho_{year}.csv ({df_wide.shape[0]} rows)")
            
            # File 3: Formato corto (summary)
            df_corto = pd.DataFrame({
                'CANTON_CODIGO': cantons_sample,
                'VUELTA': [1] * len(cantons_sample),
                'BLANCOS': [50] * len(cantons_sample),
                'NULOS': [25] * len(cantons_sample)
            })
            df_corto.to_csv(
                os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_corto_{year}.csv"),
                index=False
            )
            print(f"  [OK] Created: presidentes_votacion_cantonal_formato_corto_{year}.csv ({df_corto.shape[0]} rows)")
            
            # File 4: Electores formato angosto
            df_elec_angosto = pd.DataFrame({
                'CANTON_CODIGO': cantons_sample,
                'ELECTORES_TOTAL': [5000] * len(cantons_sample),
                'ELECTORES_18_65': [3500] * len(cantons_sample),
                'ELECTORES_MAYORES_65': [1000] * len(cantons_sample),
                'ELECTORES_MENORES_18': [500] * len(cantons_sample)
            })
            df_elec_angosto.to_csv(
                os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv"),
                index=False
            )
            print(f"  [OK] Created: presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv ({df_elec_angosto.shape[0]} rows)")
            
            # File 5: Electores formato corto
            df_elec_corto = pd.DataFrame({
                'CANTON_CODIGO': cantons_sample,
                'PROVINCIA_CODIGO': ['EC01'] * len(cantons_sample),
                'PROVINCIA_NOMBRE': ['PICHINCHA'] * len(cantons_sample),
                'ELECTORES_TOTAL': [5000] * len(cantons_sample)
            })
            df_elec_corto.to_csv(
                os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv"),
                index=False
            )
            print(f"  [OK] Created: presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv ({df_elec_corto.shape[0]} rows)")
            
        except Exception as e:
            print(f"  [ERROR] {year}: {str(e)[:60]}")
    
    return available_years

def show_summary(years):
    """Show summary of created structure"""
    
    OUTPUT_BASE = "tests/Presidenciales"
    
    print("\n" + "="*70)
    print("STRUCTURE SUMMARY")
    print("="*70)
    
    total_files = 0
    for year in years:
        year_dir = os.path.join(OUTPUT_BASE, str(year))
        if os.path.exists(year_dir):
            files = [f for f in os.listdir(year_dir) if f.endswith('.csv')]
            if files:
                print(f"\n[{year}] {len(files)} files")
                total_files += len(files)
    
    print("\n" + "="*70)
    print(f"TOTAL: {total_files} CSV files organized across {len(years)} years")
    print(f"Location: tests/Presidenciales/{{year}}/*.csv")
    print("="*70 + "\n")

def main():
    try:
        years = create_minimal_test_structure()
        show_summary(years)
        print("[SUCCESS] Electoral data structure created and organized by year!")
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
