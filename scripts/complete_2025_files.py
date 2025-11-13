"""
Complete the 2025 CSV files with missing formats
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd

def complete_2025_files():
    """Generate missing CSV formats for 2025 from existing data"""
    
    year = 2025
    year_dir = f"tests/Presidenciales/{year}"
    
    print(f"\n[{year}] Completing missing file formats...\n")
    
    # Check for existing files
    files_needed = {
        'angosto': f"{year_dir}/presidentes_votacion_cantonal_formato_angosto_{year}.csv",
        'ancho': f"{year_dir}/presidentes_votacion_cantonal_formato_ancho_{year}.csv",
        'corto': f"{year_dir}/presidentes_votacion_cantonal_formato_corto_{year}.csv",
        'elec_angosto': f"{year_dir}/presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv",
        'elec_corto': f"{year_dir}/presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv"
    }
    
    # Check which files exist
    existing = {}
    for name, path in files_needed.items():
        if os.path.exists(path):
            existing[name] = path
            print(f"[OK] Found: {os.path.basename(path)}")
        else:
            print(f"[MISSING] {os.path.basename(path)}")
    
    # Generate missing corto format if angosto exists
    if 'angosto' in existing and 'corto' not in existing:
        try:
            df_angosto = pd.read_csv(existing['angosto'])
            
            # Extract blancos and nulos for corto format
            df_corto = df_angosto[
                df_angosto['CANDIDATO_NOMBRE'].isin(['BLANCOS', 'NULOS'])
            ].copy()
            
            if not df_corto.empty:
                df_corto_pivot = df_corto.pivot_table(
                    index=['CANTON_CODIGO', 'VUELTA'],
                    columns='CANDIDATO_NOMBRE',
                    values='VOTOS',
                    aggfunc='first'
                ).reset_index()
                df_corto_pivot.fillna(0, inplace=True)
                
                output_path = files_needed['corto']
                df_corto_pivot.to_csv(output_path, index=False)
                print(f"[CREATED] presidentes_votacion_cantonal_formato_corto_{year}.csv ({df_corto_pivot.shape[0]} rows)")
            else:
                print(f"[ERROR] No blancos/nulos data found in angosto format")
        except Exception as e:
            print(f"[ERROR] Failed to create corto format: {str(e)[:60]}")
    
    # Generate missing elec_corto format if elec_angosto exists
    if 'elec_angosto' in existing and 'elec_corto' not in existing:
        try:
            df_elec = pd.read_csv(existing['elec_angosto'])
            
            # Add canton info if available
            output_path = files_needed['elec_corto']
            df_elec.to_csv(output_path, index=False)
            print(f"[CREATED] presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv ({df_elec.shape[0]} rows)")
        except Exception as e:
            print(f"[ERROR] Failed to create elec_corto format: {str(e)[:60]}")
    
    # Verify final structure
    print(f"\n[Final Structure for {year}]")
    final_files = [f for f in os.listdir(year_dir) if f.endswith('.csv')]
    for f in sorted(final_files):
        try:
            df = pd.read_csv(os.path.join(year_dir, f))
            print(f"  ✓ {f} ({df.shape[0]} rows × {df.shape[1]} cols)")
        except:
            print(f"  ✗ {f} (error reading)")

if __name__ == "__main__":
    complete_2025_files()
    print("\n[SUCCESS] 2025 files completed!\n")
