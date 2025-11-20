# Cambios para Procesar Elecciones Seccionales (Prefectos) 2023

## Resumen de cambios principales

El código para procesar **presidentes** ha sido adaptado para procesar **prefectos seccionales**. Los cambios son mínimos porque ambos usan la misma infraestructura de datos.

### Diferencias clave entre Presidentes y Prefectos:

| Aspecto | Presidentes | Prefectos |
|---------|------------|-----------|
| **Dignidad Código** | `"4"` | `"2"` |
| **Tipo de Elección** | Generales | Seccionales |
| **Ruta de Datos** | `data/csv_files/generales/{year}` | `data/csv_files/seccionales/{year}` ✅ |
| **Vueltas** | 2 vueltas (vuelta "4" y "2") | 1 vuelta (vuelta "1") |
| **Balotaje** | SÍ (si ninguno alcanza mayoría) | NO |
| **Nivel Geográfico Mínimo** | Provincia | Cantón (típicamente) |

## Cambios implementados en el notebook

### 1. Nueva función: `extract_prefectos_names_and_votos()`

**Parámetros:**
```python
extract_prefectos_names_and_votos(
    year=2023,                          # Año de elección
    dignidad_codigo="2",                # "2" = PREFECTO Y VICEPREFECTO
    vuelta="1",                         # Siempre "1" para prefectos
    agrupar_por_territorio="PROVINCIA", # "PROVINCIA" o "CANTON"
    territorio_codigo=None,             # Código específico (None = todos)
    sexo="AGRUPAR"                      # "S0", "S1", "AGRUPAR", o "AMBOS"
)
```

**Cambios respecto a presidentes:**
- El parámetro `dignidad_codigo` es `"2"` en lugar de `"4"`
- La ruta de datos ya apunta a `seccionales/{year}` (en el código base)
- La función es equivalente, solo cambia el filtro de dignidad

### 2. Nueva función: `merge_prefectos_votes_by_sex()`

**Diferencia principal:** 
- **Presidentes**: Procesa múltiples vueltas (vuelta "4" y "2") en un loop
- **Prefectos**: Procesa solo una vuelta (vuelta "1") - sin loop de vueltas

```python
merge_prefectos_votes_by_sex(
    year=2023,
    agrupar_por_territorio="CANTON",
    territorio_codigo="EC01",
    dignidad_codigo="2"
)
```

**Ventajas de esta estructura:**
- Código limpio y específico para prefectos
- No necesita lógica condicional compleja
- Claridad en la intención del código

### 3. Procesamiento de todas las provincias

```python
years = [2023]
df_prefectos_total = pd.DataFrame()

for year in years:
    for codigo, provincia in provincias_dict.items():
        df_provincia = merge_prefectos_votes_by_sex(
            year=year,
            agrupar_por_territorio="CANTON",
            territorio_codigo=codigo,
            dignidad_codigo="2"
        )
        df_prefectos_total = pd.concat([df_prefectos_total, df_provincia], ignore_index=True)
```

### 4. Guardado de resultados

```python
df_prefectos_total.to_csv("../tests/prefectos_votes_by_canton_2023.csv", index=False)
```

## Estructura del archivo de salida

El archivo CSV resultante tiene la siguiente estructura:

```
ANIO, DIGNIDAD_CODIGO, PROVINCIA_CODIGO, PROVINCIA_NOMBRE, CANTON_CODIGO, CANTON_NOMBRE,
[CANDIDATO_1_F], [CANDIDATO_1_M], [CANDIDATO_1_T],
[CANDIDATO_2_F], [CANDIDATO_2_M], [CANDIDATO_2_T],
...,
VOTOS VALIDOS_F, VOTOS VALIDOS_M, VOTOS VALIDOS_T,
BLANCOS_F, BLANCOS_M, BLANCOS_T,
NULOS_F, NULOS_M, NULOS_T,
ELECTORES_F, ELECTORES_M, ELECTORES_T,
SUFRAGANTES_F, SUFRAGANTES_M, SUFRAGANTES_T
```

**Nota:** 
- `_F` = Votos femeninos
- `_M` = Votos masculinos  
- `_T` = Total (ambos géneros)

## Extendiendo a otras dignidades seccionales

Para procesar **alcaldes** o **concejales**, solo necesitas cambiar el código de dignidad:

### Códigos de Dignidad para Elecciones Seccionales 2023:

```python
"2" = PREFECTO Y VICEPREFECTO
"3" = ALCALDE Y VICEALCALDE
"5" = CONCEJALES
"6" = VOCALES DE JUNTAS PARROQUIALES
```

**Ejemplo para alcaldes:**

```python
# Para alcaldes
df_alcaldes_total = pd.DataFrame()

for codigo, provincia in provincias_dict.items():
    df_provincia = merge_prefectos_votes_by_sex(
        year=2023,
        agrupar_por_territorio="CANTON",
        territorio_codigo=codigo,
        dignidad_codigo="3"  # Alcaldes
    )
    df_alcaldes_total = pd.concat([df_alcaldes_total, df_provincia], ignore_index=True)

df_alcaldes_total.to_csv("../tests/alcaldes_votes_by_canton_2023.csv", index=False)
```

## Flujo completo de ejecución

1. **Celda 1-2**: Cargar módulos (ya existe)
2. **Celda 3-4**: Definir funciones de estandarización (ya existe)
3. **Celdas nuevas**: Funciones específicas para prefectos
   - `extract_prefectos_names_and_votos()` 
   - `merge_prefectos_votes_by_sex()`
4. **Celda nueva**: Ejecutar prueba en una provincia
5. **Celda nueva**: Procesar todas las provincias
6. **Celda nueva**: Guardar CSV

## Consideraciones importantes

### Validación de datos

Después de ejecutar el procesamiento, verifica:

```python
# Ver primeros registros
print(df_prefectos_total.head())

# Ver resumen estadístico
print(df_prefectos_total.info())
print(df_prefectos_total.describe())

# Verificar que no hay NaN en candidatos
print(df_prefectos_total.isnull().sum())

# Verificar cantidad de cantones
print(f"Total de registros: {len(df_prefectos_total)}")
print(f"Provincias únicas: {df_prefectos_total['PROVINCIA_NOMBRE'].nunique()}")
```

### Posibles errores y soluciones

**Error**: `DIGNIDAD_CODIGO == "2" returns empty DataFrame`
- **Causa**: El archivo de datos seccionales 2023 podría no contener datos de prefectos
- **Solución**: Verificar disponibilidad de datos en `../data/csv_files/seccionales/2023/`

**Error**: `candidatos_{year}.csv` no encontrado
- **Causa**: El archivo de candidatos para el año específico no existe
- **Solución**: Asegurar que el archivo existe en la ruta correcta

**Columnas faltantes**:
- Verificar que el archivo de datos tiene las columnas esperadas
- Usar `test_standarized_resultados(2023)` para inspeccionar la estructura

## Próximos pasos

1. Ejecutar las celdas nuevas en orden
2. Validar que `df_prefectos_total` se genera correctamente
3. Completar el procesamiento similar al de presidentes (agregar electores, ordenar columnas, etc.)
4. Repetir para otras dignidades (alcaldes, concejales, vocales)
5. Crear un script consolidado que procese todas las dignidades

## Referencias

- **Dignidades disponibles**: Ver `../data/csv_files/seccionales/2023/diccionarios/dignidades_*.csv`
- **Estructura de datos**: Ver `../../aplied_scripts/study_resultados.ipynb`
- **Estándar de provincias**: `../data/csv_files/Codigos_estandar/provincias/std_provincias.csv`
- **Estándar de cantones**: `../data/csv_files/Codigos_estandar/cantones/std_cantones.csv`
