"""
Generate presidential election CSV files for all years (2002-2025)
organized by year in tests/Presidenciales/{year}/ directories
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from pathlib import Path

# Configuration
AVAILABLE_YEARS = [2002, 2006, 2007, 2009, 2013, 2017, 2021, 2023, 2025]
CANDIDATOS = {
    2002: ["RODRIGO BORJA","JACINTO VELAZQUEZ","ANTONIO VARGAS","OSVALDO HURTADO",
           "ALVARO NOBOA","XAVIER NEIRA","CESAR ALARCON","IVONNE BAKI","JACOBO BUCARAM","LUCIO GUTIERREZ"],
    2006: ["JAIME DEMERVAL","RAFAEL CORREA","ALVARO NOBOA","GILMAR GUTIERREZ","LEON ROLDOS","LUIS VILLACIS",
           "LUIS MACAS","LENIN TORRES","MARCO PROANO","MARCELO LARREA","CYNTHIA VITERI","CARLOS SAGNAY","FERNANDO ROSERO"],
    2009: ["RAFAEL CORREA","LUCIO GUTIERREZ","ALVARO NOBOA","MARTHA ROLDOS","MELBA JACOME",
    "CARLOS GONZALEZ","DIEGO DELGADO JARA","CARLOS SAGNAY"],
    2013: ["RAFAEL CORREA","GUILLERMO LASSO","ALBERTO ACOSTA","MAURICIO RODAS","LUCIO GUTIERREZ",
    "ALVARO NOBOA","NORMAN WRAY","NELSON ZAVALA"],
    2017: ["PATRICIO ZUQUILANDA","IVAN ESPINEL","CYNTHIA VITERI","JAIME BUCARAM",
           "PACO MONCAYO","WASHINGTON PESANTEZ","GUILLERMO LASSO","LENIN MORENO"],
    2021: ["ANDRES ARAUZ","LUCIO GUTIERREZ","GERSON ALMEIDA","ISIDRO ROMERO","CARLOS SAGNAY",
            "XAVIER HERVAS","PEDRO FREILE","CESAR MONTUFAR","YAKU PEREZ","GIOVANNY ANDRADE","GUSTAVO LARREA",
            "GUILLERMO LASSO","GUILLERMO CELI","JUAN FERNANDO VELASCO","PAUL CARRASCO","XIMENA PENA"],
    2023: ["YAKU PEREZ","DANIEL NOBOA","LUISA GONZALEZ","JAN TOPIC","OTTO SONNENHOLZNER","BOLIVAR ARMIJOS","FERNANDO VILLAVICENCIO",
            "XAVIER HERVAS"],
    2025: ["ANDREA GONZALEZ","CARLOS RABASCALL","DANIEL NOBOA AZIN","ENRIQUE GOMEZ","FRANCESCO TABACCHI",
            "HENRY CUCALON","HENRY KRONFLE KOZHAYA","IVAN SAQUICELA","JIMMY JAIRALA VALLAZZA","JORGE ESCALA",
            "JUAN IVAN CUEVA","LEONIDAS IZA","LUIS FELIPE TILLERIA","LUISA GONZALEZ","PEDRO GRANJA","VICTOR ARAUS"]
}

def load_consolidated_data(data_path="tests/Presidenciales/presidentes_votacion_cantonal_formato_corto.csv"):
    """Load pre-consolidated data (assumed to exist from presindenciales.py)"""
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Loaded consolidated data: {data_path}")
        return df
    except FileNotFoundError:
        print(f"⚠️  File not found: {data_path}")
        print("   Make sure presindenciales.py has been run first.")
        return None

def create_year_directories(base_dir="tests/Presidenciales"):
    """Create year-specific subdirectories"""
    for year in AVAILABLE_YEARS:
        year_dir = os.path.join(base_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)
    print(f"✅ Created directories for all years in {base_dir}")

def generate_year_specific_files(df_votes, df_electors, base_dir="tests/Presidenciales"):
    """
    Generate year-specific CSV files from consolidated dataframes
    """
    success_count = 0
    
    for year in AVAILABLE_YEARS:
        year_dir = os.path.join(base_dir, str(year))
        
        # Filter data for this year
        df_votes_year = df_votes[df_votes['ANIO'] == year] if df_votes is not None else pd.DataFrame()
        df_electors_year = df_electors[df_electors['ANIO'] == year] if df_electors is not None else pd.DataFrame()
        
        if df_votes_year.empty and df_electors_year.empty:
            print(f"⚠️  No data for year {year}")
            continue
        
        try:
            # Process votes if available
            if not df_votes_year.empty:
                # Angosto format (long)
                df_votes_year_clean = df_votes_year[df_votes_year['CANDIDATO_NOMBRE'].notna()].copy()
                df_votes_year_clean.to_csv(
                    os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_angosto_{year}.csv"),
                    index=False
                )
                
                # Ancho format (wide) - pivot by candidate
                df_votes_pivot = df_votes_year_clean[
                    ~df_votes_year_clean['CANDIDATO_NOMBRE'].isin(['BLANCOS', 'NULOS'])
                ].copy()
                
                if not df_votes_pivot.empty:
                    try:
                        # Create wide pivot
                        df_wide = df_votes_pivot.pivot_table(
                            index=['VUELTA', 'CANTON_CODIGO'],
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
                        print(f"  ⚠️  Could not create ancho format for {year}: {str(e)[:60]}")
                
                # Corto format (summary)
                df_votes_corto = df_votes_year_clean[
                    df_votes_year_clean['CANDIDATO_NOMBRE'].isin(['BLANCOS', 'NULOS'])
                ][['ANIO', 'VUELTA', 'CANTON_CODIGO', 'CANDIDATO_NOMBRE', 'VOTOS']].copy()
                
                if not df_votes_corto.empty:
                    df_votes_corto_pivot = df_votes_corto.pivot_table(
                        index=['ANIO', 'VUELTA', 'CANTON_CODIGO'],
                        columns='CANDIDATO_NOMBRE',
                        values='VOTOS',
                        aggfunc='first'
                    ).reset_index()
                    df_votes_corto_pivot.fillna(0, inplace=True)
                    df_votes_corto_pivot.to_csv(
                        os.path.join(year_dir, f"presidentes_votacion_cantonal_formato_corto_{year}.csv"),
                        index=False
                    )
                
                print(f"✅ Year {year}: Votes saved (angosto, ancho, corto formats)")
            
            # Process electors if available
            if not df_electors_year.empty:
                # Angosto format
                df_electors_angosto = df_electors_year[
                    ['ANIO', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE', 'AGRUPACION', 'CANTIDAD']
                ].drop_duplicates()
                df_electors_angosto.to_csv(
                    os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_angosto_{year}.csv"),
                    index=False
                )
                
                # Corto format
                df_electors_corto = df_electors_year[
                    ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE', 'AGRUPACION', 'CATEGORIA', 'CANTIDAD']
                ].drop_duplicates()
                df_electors_corto.to_csv(
                    os.path.join(year_dir, f"presidentes_electores_sufragantes_cantonal_formato_corto_{year}.csv"),
                    index=False
                )
                
                print(f"✅ Year {year}: Electors saved (angosto, corto formats)")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Year {year}: Error - {str(e)[:100]}")
    
    return success_count

def generate_summary_report(base_dir="tests/Presidenciales"):
    """Generate a summary of all generated files"""
    print("\n" + "="*70)
    print("📊 SUMMARY OF GENERATED FILES")
    print("="*70)
    
    for year in AVAILABLE_YEARS:
        year_dir = os.path.join(base_dir, str(year))
        if os.path.exists(year_dir):
            files = [f for f in os.listdir(year_dir) if f.endswith('.csv')]
            if files:
                print(f"\n📁 {year}/ ({len(files)} files)")
                for f in sorted(files):
                    file_path = os.path.join(year_dir, f)
                    try:
                        df = pd.read_csv(file_path)
                        print(f"   • {f}")
                        print(f"     └─ {df.shape[0]:>6} rows × {df.shape[1]:>2} columns")
                    except Exception as e:
                        print(f"   • {f} (⚠️  error reading: {str(e)[:30]})")

def main():
    print("\n" + "="*70)
    print("🚀 GENERATING PRESIDENTIAL ELECTION DATA (2002-2025)")
    print("="*70 + "\n")
    
    # Step 1: Create year directories
    create_year_directories()
    
    # Step 2: Load consolidated data
    print("\n📂 Loading consolidated data...")
    try:
        # Try to load from consolidated files generated by presindenciales.py
        df_votes = pd.read_csv("tests/Presidenciales/presidentes_votacion_cantonal_formato_corto.csv")
        df_electors = pd.read_csv("tests/Presidenciales/presidentes_electores_sufragantes_cantonal_formato_corto.csv")
        print(f"✅ Loaded votes: {df_votes.shape[0]} records")
        print(f"✅ Loaded electors: {df_electors.shape[0]} records")
    except FileNotFoundError as e:
        print(f"⚠️  Could not load consolidated files: {e}")
        df_votes = None
        df_electors = None
    
    # Step 3: Generate year-specific files
    if df_votes is not None or df_electors is not None:
        print("\n📝 Generating year-specific files...")
        success = generate_year_specific_files(df_votes, df_electors)
        print(f"\n✅ Successfully processed {success}/{len(AVAILABLE_YEARS)} years")
    
    # Step 4: Generate summary
    generate_summary_report()
    
    print("\n" + "="*70)
    print("✨ DONE! All files organized by year in tests/Presidenciales/")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
