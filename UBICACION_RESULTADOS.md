# 📁 Ubicación de Resultados: Presidenciales vs Seccionales 2023

## Estructura de carpetas

```
c:\Users\FELIPE\Downloads\ELECU\
├── tests/
│   ├── test_results/
│   │   ├── presidentes_votes_by_canton_2025.csv          ← Intermediario
│   │   ├── presidentes_votacion_cantonal_complete_with_electores_F_M_2025.csv  ← Final presidentes
│   │   ├── test_registro_2023.csv
│   │   └── test_registro_2023.xlsx
│   ├── presidentes_votes_by_canton_2025.csv              ← Intermediario
│   └── test_convert_sav_to_csv.py (y otros tests)
└── scripts/
    └── presindenciales.ipynb  ← Código que genera los resultados
```

---

## Resultados de PRESIDENCIALES 2023

### 📍 Ubicación actual (Guardado)

**NO HAY RESULTADOS DE 2023 guardados aún**

Los archivos que existen son de **2025**:
- `c:\Users\FELIPE\Downloads\ELECU\tests\presidentes_votes_by_canton_2025.csv`
- `c:\Users\FELIPE\Downloads\ELECU\tests\test_results\presidentes_votes_by_canton_2025.csv`

### 📝 Donde se guardarán (después de ejecutar)

El código en el notebook guardará:

1. **Archivo intermediario** (votos sin electores):
   ```
   ../tests/presidentes_votes_by_canton_2023.csv
   ```
   **Ruta completa:**
   ```
   c:\Users\FELIPE\Downloads\ELECU\tests\presidentes_votes_by_canton_2023.csv
   ```

2. **Archivo final** (votos + electores completo):
   ```
   ../tests/test_results/presidentes_votacion_cantonal_complete_with_electores_F_M_2023.csv
   ```
   **Ruta completa:**
   ```
   c:\Users\FELIPE\Downloads\ELECU\tests\test_results\presidentes_votacion_cantonal_complete_with_electores_F_M_2023.csv
   ```

### 📊 Contenido del archivo final de presidentes:

```
Columnas:
├── Metadata
│   ├── ANIO (2023)
│   ├── VUELTA (4 o 2)
│   ├── PROVINCIA_CODIGO (EC01, EC02, etc.)
│   └── PROVINCIA_NOMBRE
├── Geografía
│   ├── CANTON_CODIGO
│   └── CANTON_NOMBRE
├── Votos por candidato (con sufijos _M, _F, _T)
│   ├── YAKU_PEREZ_M, YAKU_PEREZ_F, YAKU_PEREZ_T
│   ├── DANIEL_NOBOA_M, DANIEL_NOBOA_F, DANIEL_NOBOA_T
│   └── ... (8 candidatos total)
├── Sumarios de votos
│   ├── VOTOS VALIDOS_F, VOTOS VALIDOS_M, VOTOS VALIDOS_T
│   ├── BLANCOS_F, BLANCOS_M, BLANCOS_T
│   ├── NULOS_F, NULOS_M, NULOS_T
├── Electores por edad y sexo
│   ├── ELECTORES MENORES A 18_F, ELECTORES MENORES A 18_M
│   ├── ELECTORES DE 18 A 65_F, ELECTORES DE 18 A 65_M
│   ├── ELECTORES MAYORES A 65_F, ELECTORES MAYORES A 65_M
│   ├── ELECTORES_F_T, ELECTORES_M_T, ELECTORES_T
└── Sufragantes
    ├── SUFRAGANTES_F, SUFRAGANTES_M, SUFRAGANTES_T
```

---

## Resultados de SECCIONALES 2023 (Prefectos)

### 📍 Ubicación (después de ejecutar)

El nuevo código que agregué guardará:

1. **Archivo de prefectos** (votos por candidato):
   ```
   ../tests/prefectos_votes_by_canton_2023.csv
   ```
   **Ruta completa:**
   ```
   c:\Users\FELIPE\Downloads\ELECU\tests\prefectos_votes_by_canton_2023.csv
   ```

2. **Archivo final de prefectos** (opcional, si completas el flujo):
   ```
   ../tests/test_results/prefectos_votacion_cantonal_complete_2023.csv
   ```
   **Ruta completa:**
   ```
   c:\Users\FELIPE\Downloads\ELECU\tests\test_results\prefectos_votacion_cantonal_complete_2023.csv
   ```

### 📊 Contenido del archivo de prefectos:

```
Columnas:
├── Metadata
│   ├── ANIO (2023)
│   ├── DIGNIDAD_CODIGO ("2" = PREFECTO Y VICEPREFECTO)
│   ├── PROVINCIA_CODIGO
│   └── PROVINCIA_NOMBRE
├── Geografía
│   ├── CANTON_CODIGO
│   └── CANTON_NOMBRE
├── Votos por candidato (con sufijos _M, _F, _T)
│   ├── [CANDIDATO_1_M], [CANDIDATO_1_F], [CANDIDATO_1_T]
│   ├── [CANDIDATO_2_M], [CANDIDATO_2_F], [CANDIDATO_2_T]
│   └── ...
├── Sumarios
│   ├── VOTOS VALIDOS_F, VOTOS VALIDOS_M, VOTOS VALIDOS_T
│   ├── BLANCOS_F, BLANCOS_M, BLANCOS_T
│   ├── NULOS_F, NULOS_M, NULOS_T
├── Electores
│   ├── ELECTORES_F, ELECTORES_M, ELECTORES_T
└── Sufragantes
    ├── SUFRAGANTES_F, SUFRAGANTES_M, SUFRAGANTES_T
```

---

## Comparación: Dónde se guardan

| Elección | Tipo | Archivo Intermediario | Archivo Final |
|----------|------|----------------------|---------------|
| **Presidenciales 2023** | Generales | `tests/presidentes_votes_by_canton_2023.csv` | `tests/test_results/presidentes_votacion_cantonal_complete_with_electores_F_M_2023.csv` |
| **Prefectos 2023** | Seccionales | `tests/prefectos_votes_by_canton_2023.csv` | `tests/test_results/prefectos_votacion_cantonal_complete_2023.csv` |
| **Alcaldes 2023** | Seccionales | `tests/alcaldes_votes_by_canton_2023.csv` | `tests/test_results/alcaldes_votacion_cantonal_complete_2023.csv` |
| **Concejales 2023** | Seccionales | `tests/concejales_votes_by_canton_2023.csv` | `tests/test_results/concejales_votacion_cantonal_complete_2023.csv` |

---

## Pasos para ver los resultados

### Después de ejecutar el código de presidenciales:

1. **Ir a la carpeta de tests:**
   ```powershell
   cd c:\Users\FELIPE\Downloads\ELECU\tests
   ```

2. **Ver archivos generados:**
   ```powershell
   ls -Name *.csv
   ```

3. **Abrir en Excel o Python:**
   ```python
   import pandas as pd
   
   # Ver presidentes
   df_pres = pd.read_csv("test_results/presidentes_votacion_cantonal_complete_with_electores_F_M_2023.csv")
   print(df_pres.head())
   print(f"Filas: {len(df_pres)}, Columnas: {len(df_pres.columns)}")
   
   # Ver prefectos (después de generarlos)
   df_pref = pd.read_csv("prefectos_votes_by_canton_2023.csv")
   print(df_pref.head())
   ```

---

## Verificación rápida en Terminal

```powershell
# Ver tamaño y fecha de los archivos
Get-ChildItem c:\Users\FELIPE\Downloads\ELECU\tests\*.csv | Select-Object Name, Length, LastWriteTime

# Ver tamaño en carpeta test_results
Get-ChildItem c:\Users\FELIPE\Downloads\ELECU\tests\test_results\*.csv | Select-Object Name, Length, LastWriteTime
```

---

## ⚠️ Importante

**Nota sobre las rutas relativas en el código:**

El código usa rutas relativas como `../tests/`:
- Esto depende de dónde se ejecute el notebook
- Si estás en `scripts/presindenciales.ipynb`
- `../tests/` apunta a `c:\Users\FELIPE\Downloads\ELECU\tests\`

Si ejecutas desde otro lugar, asegúrate de que el working directory sea correcto:

```python
import os
print(f"Working directory: {os.getcwd()}")

# Debería ser: c:\Users\FELIPE\Downloads\ELECU\scripts
```

---

## Resumen rápido 🎯

```
📊 PRESIDENCIALES 2023:
   └─ tests/test_results/presidentes_votacion_cantonal_complete_with_electores_F_M_2023.csv

📊 SECCIONALES 2023 (Prefectos):
   └─ tests/prefectos_votes_by_canton_2023.csv
      (o tests/test_results/prefectos_votacion_cantonal_complete_2023.csv si completas el flujo)
```

**Ambos en:** `c:\Users\FELIPE\Downloads\ELECU\tests\`
