"""
Organizador de archivos CSV por año en tests/Presidenciales
Distribuye datos consolidados en subdirectorios organizados por año
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from pathlib import Path

def organize_years_from_raw_data():
    """
    Genera archivos por año directamente desde los datos crudos
    para años históricos (2002-2023)
    """
    
    YEARS_TO_PROCESS = [2002, 2006, 2007, 2009, 2013, 2017, 2021, 2023]
    BASE_DATA_PATH = "data/csv_files/generales"
    OUTPUT_BASE = "tests/Presidenciales"
    
    try:
        from elecu.elecu.restructure_results import Standarized_Results
        from elecu.elecu.extract_values import extract_eleccion, extract_votacion
    except ImportError as e:
        print(f"[ERROR] Could not import required modules: {e}")
        return 0
    
    processed_count = 0
    
    for year in YEARS_TO_PROCESS:
        year_dir = os.path.join(OUTPUT_BASE, str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        print(f"\n[{year}] Processing...")
        
        try:
            # Initialize standardization
            input_folder = os.path.join(BASE_DATA_PATH, str(year))
            standarized_folder = "elecu/elecu/data/Codigos_estandar/"
            
            if not os.path.exists(input_folder):
                print(f"  [SKIP] Data folder not found: {input_folder}")
                continue
            
            # Load and standardize data
            std_results = Standarized_Results(input_folder, standarized_folder)
            
            # Process results
            std_results.change_resultados()
            votacion, eleccion, _ = std_results.divide_resultados()
            
            # Process registry
            std_results.change_registro()
            
            # Extract election data at canton level
            if not eleccion.empty:
                # Format angosto (long)
                df_angosto = eleccion[['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE', 'VOTOS']].copy()
                df_angosto = df_angosto.groupby(['CANTON_CODIGO', 'VUELTA', 'CANDIDATO_NOMBRE'])['VOTOS'].sum().reset_index()
                df_angosto.to_csv(
                    os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_angosto_{year}.csv"),
                    index=False
                )
                
                # Format ancho (wide) - pivot by candidates
                try:
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
                except Exception as e:
                    print(f"  [WARN] Could not generate ancho format: {str(e)[:50]}")
                
                # Format corto (short) - blancos y nulos
                try:
                    df_blancos_nulos = df_angosto[
                        df_angosto['CANDIDATO_NOMBRE'].isin(['BLANCOS', 'NULOS'])
                    ].pivot_table(
                        index=['CANTON_CODIGO', 'VUELTA'],
                        columns='CANDIDATO_NOMBRE',
                        values='VOTOS',
                        aggfunc='first'
                    ).reset_index()
                    df_blancos_nulos.fillna(0, inplace=True)
                    df_blancos_nulos.to_csv(
                        os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_corto_{year}.csv"),
                        index=False
                    )
                except Exception as e:
                    print(f"  [WARN] Could not generate corto format: {str(e)[:50]}")
                
                print(f"  [OK] Votes saved ({df_angosto.shape[0]} records)")
            
            # Process elector data
            if not std_results.df_registro.empty:
                df_reg = std_results.df_registro.copy()
                
                # Format angosto (long)
                if 'CANTON_CODIGO' in df_reg.columns:
                    cols_angosto = [c for c in df_reg.columns if 'CANTON' in c or 'ELECTORES' in c]
                    if cols_angosto:
                        df_elec_angosto = df_reg[cols_angosto].drop_duplicates()
                        df_elec_angosto.to_csv(
                            os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv"),
                            index=False
                        )
                        
                        # Format corto (short) - with more details
                        cols_corto = [c for c in df_reg.columns if 'CANTON' in c or 'PROVINCIA' in c or 'ELECTORES' in c]
                        if cols_corto:
                            df_elec_corto = df_reg[cols_corto].drop_duplicates()
                            df_elec_corto.to_csv(
                                os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv"),
                                index=False
                            )
                        
                        print(f"  [OK] Electors saved ({df_elec_angosto.shape[0]} records)")
            
            processed_count += 1
            
        except Exception as e:
            print(f"  [ERROR] {str(e)[:100]}")
    
    return processed_count

def verify_year_directories():
    """Verifica que todos los directorios de años existan y contengan archivos"""
    
    OUTPUT_BASE = "tests/Presidenciales"
    ALL_YEARS = [2002, 2006, 2007, 2009, 2013, 2017, 2021, 2023, 2025]
    
    print("\n" + "="*70)
    print("DIRECTORY STRUCTURE")
    print("="*70)
    
    total_files = 0
    for year in ALL_YEARS:
        year_dir = os.path.join(OUTPUT_BASE, str(year))
        if os.path.exists(year_dir):
            files = [f for f in os.listdir(year_dir) if f.endswith('.csv')]
            if files:
                print(f"\n[{year}] {len(files)} files:")
                for f in sorted(files):
                    fpath = os.path.join(year_dir, f)
                    size = os.path.getsize(fpath) / 1024  # Size in KB
                    try:
                        df = pd.read_csv(fpath)
                        print(f"  • {f} ({df.shape[0]:,} rows × {df.shape[1]} cols, {size:.1f} KB)")
                        total_files += 1
                    except:
                        print(f"  • {f} (error reading)")
        else:
            print(f"\n[{year}] Directory does not exist")
    
    return total_files

def main():
    print("\n" + "="*70)
    print("PRESIDENTES ELECTION DATA ORGANIZER (2002-2025)")
    print("="*70)
    
    # Step 1: Try to organize years from raw data
    print("\n[Step 1] Processing years from raw data...")
    processed = organize_years_from_raw_data()
    print(f"\n[Summary] Successfully processed {processed} years")
    
    # Step 2: Verify structure
    total_files = verify_year_directories()
    
    print("\n" + "="*70)
    print(f"TOTAL: {total_files} CSV files organized across all years")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
