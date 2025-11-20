# Comparación: Presidentes vs Prefectos

## Cambios mínimos requeridos

### Cambio 1: Código de Dignidad
```python
# PRESIDENTES
dignidad_codigo="4"

# PREFECTOS
dignidad_codigo="2"
```

### Cambio 2: Manejo de Vueltas
```python
# PRESIDENTES - Múltiples vueltas
election_rounds = ["4", "2"]  # Puede haber runoff
for vuelta in election_rounds:
    # Procesar vuelta 4
    # Procesar vuelta 2

# PREFECTOS - Solo una vuelta
vuelta = "1"  # No hay runoff
# Procesar vuelta 1
```

### Cambio 3: Nivel Geográfico típico
```python
# PRESIDENTES - Pueden ser provincia o cantón
agrupar_por_territorio="PROVINCIA"  # O "CANTON"

# PREFECTOS - Típicamente cantón
agrupar_por_territorio="CANTON"  # Menor nivel geográfico
```

---

## Matriz de similitudes y diferencias

### Similitudes (Código reutilizable)
✅ Ambos usan `extract_eleccion()` de `elecu.extract_values`
✅ Ambos usan `test_standarized_registro()` y `test_standarized_resultados()`
✅ Ambos tienen estratificación por sexo (S0, S1, AGRUPAR)
✅ Ambos calculan VOTOS VALIDOS, BLANCOS, NULOS, SUFRAGANTES
✅ Ambos fusionan datos de candidatos y organizaciones políticas
✅ Ambos usan pivot_table para convertir de formato largo a ancho

### Diferencias (Ajustes necesarios)

| Aspecto | Presidentes | Prefectos |
|---------|-------------|-----------|
| Dignidad | "4" | "2" |
| Elección | Generales | Seccionales |
| Vueltas | 2 (runoff) | 1 |
| Ruta | generales/{year} | seccionales/{year} |
| Loop vueltas | SÍ | NO |
| Nivel común | Provincia | Cantón |

---

## Estructura de las funciones

### Presidentes (Original)
```
extract_presidentes_names_and_votos()
    ↓
merge_presidentes_votes_by_rounds()  ← Itera sobre vueltas
    ├─ Vuelta 4
    ├─ Vuelta 2
    └─ Fusiona ambas
        ↓
    df_votaciones_total
        ↓
    add_electores_column_with_suffixes_not_agregated()
        ↓
    df_votaciones_final → CSV
```

### Prefectos (Nueva implementación)
```
extract_prefectos_names_and_votos()
    ↓
merge_prefectos_votes_by_sex()  ← Solo vuelta 1
    ├─ Sexo S0 (Masc)
    ├─ Sexo S1 (Fem)
    └─ Sexo AGRUPAR (Total)
        ↓
    df_prefectos_total
        ↓
    (Mismo flujo que presidentes para electores y formato final)
```

---

## Lineas de código que cambian

### En `extract_prefectos_names_and_votos()`:
```python
# Línea 6: Cambiar parámetro default
- dignidad_codigo="4"
+ dignidad_codigo="2"

# Línea 14: Path de datos
- f"../data/csv_files/generales/{year}"
+ f"../data/csv_files/seccionales/{year}"  # Pero esto ya se usa en test_standarized_*

# Línea 18: Filtrar por dignidad correcta
- dignidad_codigo="4"
+ dignidad_codigo="2"
```

### En `merge_prefectos_votes_by_sex()`:
```python
# Simplificar: NO iterar sobre vueltas
- for vuelta in election_rounds:  # ["4", "2"]
+ vuelta = "1"  # Solo una vuelta

# NO concatenar múltiples vueltas
- final_df = pd.concat(combined_dfs, ignore_index=True)
+ final_df = df_merged  # Solo un dataframe
```

---

## Diagrama de flujo de datos

```
CSV Seccionales 2023 (generales + seccionales)
        ↓
test_standarized_resultados(2023)
    ├─ test_year_votacion (blancos, nulos)
    ├─ test_year_eleccion (candidatos, votos)
    └─ test (raw data)
        ↓
extract_prefectos_names_and_votos(dignidad_codigo="2")
    ├─ Merge candidatos names
    ├─ Merge organizaciones names
    ├─ Merge territorios (provincia/cantón)
    ├─ PIVOT TABLE (long → wide)
    └─ Añadir blancos, nulos, electores
        ↓
merge_prefectos_votes_by_sex()
    ├─ Extract S0, S1, AGRUPAR
    ├─ Apply suffixes (_M, _F, _T)
    └─ Merge horizontally
        ↓
df_prefectos_total
        ↓
[Guardar CSV]
        ↓
[Opción: Agregar electores por edad/sexo]
        ↓
[Archivo final: prefectos_votacion_cantonal_complete_2023.csv]
```

---

## Verificación de cambios

Después de implementar, verifica con:

```python
# 1. Que la función extrae datos correctamente
df_test = extract_prefectos_names_and_votos(year=2023, dignidad_codigo="2")
assert df_test is not None
assert len(df_test) > 0
print("✓ Extracción OK")

# 2. Que los nombres de candidatos se cargan
candidato_cols = [col for col in df_test.columns if col not in [
    'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE',
    'VOTOS VALIDOS', 'BLANCOS', 'NULOS', 'ELECTORES', 'SUFRAGANTES'
]]
assert len(candidato_cols) > 0
print(f"✓ Candidatos encontrados: {candidato_cols}")

# 3. Que merge funciona
df_merged = merge_prefectos_votes_by_sex(2023, "CANTON", "EC01", "2")
assert df_merged is not None
assert '_M' in df_merged.columns[0] or '_F' in str(df_merged.columns)
print("✓ Merge OK")

# 4. Que procesa todas las provincias
df_all = pd.DataFrame()
for codigo in list(provincias_dict.keys())[:3]:  # Prueba 3 provincias
    df = merge_prefectos_votes_by_sex(2023, "CANTON", codigo, "2")
    df_all = pd.concat([df_all, df], ignore_index=True)
print(f"✓ Procesadas {df_all['PROVINCIA_NOMBRE'].nunique()} provincias")
```

---

## Próxima extensión: Otros años

Para procesar otras elecciones seccionales:

```python
# Años disponibles para seccionales:
seccionales_years = [2004, 2009, 2014, 2019, 2023]

# Procesarlas todas
for year in seccionales_years:
    df_prefectos = pd.DataFrame()
    for codigo in provincias_dict.keys():
        df = merge_prefectos_votes_by_sex(year, "CANTON", codigo, "2")
        df_prefectos = pd.concat([df_prefectos, df], ignore_index=True)
    df_prefectos.to_csv(f"../tests/prefectos_{year}.csv", index=False)
    print(f"✓ Guardado: prefectos_{year}.csv")
```
