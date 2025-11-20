# Checklist de Implementación: Elecciones Seccionales (Prefectos) 2023

## Fase 1: Preparación ✓

### Verificaciones previas
- [x] Notebook `presindenciales.ipynb` está abierto
- [x] Módulos `elecu` están cargados en kernel
- [x] Datos seccionales 2023 existen en `../data/csv_files/seccionales/2023/`
- [x] Funciones base ya están definidas (`test_standarized_*`, `extract_eleccion`, etc.)
- [x] Diccionario de provincias está generado (`provincias_dict`)

### Verificar disponibilidad de datos seccionales
```python
# Ejecutar esta celda primero:
import os
seccionales_path = "../data/csv_files/seccionales/2023"
print("Contenido de seccionales/2023:")
for item in os.listdir(seccionales_path):
    print(f"  - {item}")
```

---

## Fase 2: Implementación de funciones ✓

### Código base ya agregado

Las siguientes funciones han sido añadidas al notebook:

1. **`extract_prefectos_names_and_votos()`**
   - [x] Definida (Nueva celda después de "Generación de Prefectos Seccionales 2023")
   - [x] Parámetro `dignidad_codigo="2"` 
   - [x] Rutas apuntan a datos seccionales
   - [ ] **VALIDAR**: Ejecutar celda 1 de esta sección

2. **`merge_prefectos_votes_by_sex()`**
   - [x] Definida (Nueva celda después de `extract_prefectos_names_and_votos`)
   - [x] Sin loop de vueltas (solo vuelta="1")
   - [x] Soporta agregación por sexo
   - [ ] **VALIDAR**: Ejecutar celda 2 de esta sección

### Verificación de sintaxis
```python
# Ejecutar después de definir las funciones:
import inspect

print("Función extract_prefectos_names_and_votos:")
print(f"  - Parámetros: {list(inspect.signature(extract_prefectos_names_and_votos).parameters.keys())}")

print("\nFunción merge_prefectos_votes_by_sex:")
print(f"  - Parámetros: {list(inspect.signature(merge_prefectos_votes_by_sex).parameters.keys())}")
```

---

## Fase 3: Pruebas básicas

### Test 1: Extracción simple
```python
# Ejecutar en celda de prueba:
df_test = extract_prefectos_names_and_votos(
    year=2023,
    dignidad_codigo="2",
    vuelta="1",
    agrupar_por_territorio="PROVINCIA",
    territorio_codigo=None,
    sexo="AGRUPAR"
)

# Verificaciones:
assert df_test is not None, "❌ DataFrame es None"
assert len(df_test) > 0, "❌ DataFrame está vacío"
assert 'PROVINCIA_CODIGO' in df_test.columns, "❌ Falta PROVINCIA_CODIGO"
assert 'PROVINCIA_NOMBRE' in df_test.columns, "❌ Falta PROVINCIA_NOMBRE"
assert 'VOTOS VALIDOS' in df_test.columns, "❌ Falta VOTOS VALIDOS"
assert 'ELECTORES' in df_test.columns, "❌ Falta ELECTORES"

print("✅ Test 1 PASSED")
print(f"  Filas: {len(df_test)}")
print(f"  Columnas: {len(df_test.columns)}")
print(f"  Primeras provincias: {df_test['PROVINCIA_NOMBRE'].unique()[:3].tolist()}")
```

### Test 2: Agregación por provincia
```python
# Ejecutar:
df_test_prov = extract_prefectos_names_and_votos(
    year=2023,
    dignidad_codigo="2",
    territorio_codigo="EC01",  # Solo Pichincha
    agrupar_por_territorio="PROVINCIA"
)

assert len(df_test_prov) == 1, f"❌ Esperaba 1 fila, obtuvo {len(df_test_prov)}"
assert df_test_prov['PROVINCIA_CODIGO'].iloc[0] == "EC01", "❌ PROVINCIA_CODIGO incorrecto"

print("✅ Test 2 PASSED")
print(f"  Provincia: {df_test_prov['PROVINCIA_NOMBRE'].iloc[0]}")
```

### Test 3: Merge con estratificación por sexo
```python
# Ejecutar:
df_test_merge = merge_prefectos_votes_by_sex(
    year=2023,
    agrupar_por_territorio="CANTON",
    territorio_codigo="EC01",  # Pichincha
    dignidad_codigo="2"
)

assert df_test_merge is not None, "❌ DataFrame es None"
assert len(df_test_merge) > 0, "❌ DataFrame está vacío"
assert '_M' in str(df_test_merge.columns) or '_F' in str(df_test_merge.columns), \
    "❌ No hay sufijos de sexo en columnas"

print("✅ Test 3 PASSED")
print(f"  Filas: {len(df_test_merge)}")
print(f"  Columnas totales: {len(df_test_merge.columns)}")
# Mostrar columnas de candidatos (con sufijos)
cand_cols = [col for col in df_test_merge.columns if '_M' in col or '_F' in col or '_T' in col]
print(f"  Primeros candidatos: {cand_cols[:6]}")
```

---

## Fase 4: Procesamiento completo

### Test 4: Procesamiento de una sola provincia
```python
# Elegir una provincia para prueba
provincia_prueba = "EC01"  # Pichincha

df_provincia = merge_prefectos_votes_by_sex(
    year=2023,
    agrupar_por_territorio="CANTON",
    territorio_codigo=provincia_prueba,
    dignidad_codigo="2"
)

print(f"✅ Provincia procesada: {df_provincia['PROVINCIA_NOMBRE'].iloc[0]}")
print(f"  Cantones: {len(df_provincia)}")
print(f"  Candidatos: {sum(1 for col in df_provincia.columns if '_M' in col)}")
print("\nPrimeras 3 filas:")
print(df_provincia.iloc[:3, :6])  # Mostrar primeras 6 columnas
```

### Test 5: Procesamiento de todas las provincias
```python
# ⚠️ Esto toma tiempo. Ejecutar celda:
# "# Procesar prefectos para todas las provincias"

# Después de completar, ejecutar verificaciones:
assert len(df_prefectos_total) > 0, "❌ No hay datos"
assert 'PROVINCIA_NOMBRE' in df_prefectos_total.columns, "❌ Falta PROVINCIA_NOMBRE"

print("✅ Test 5 PASSED")
print(f"Total de registros: {len(df_prefectos_total)}")
print(f"Total de provincias: {df_prefectos_total['PROVINCIA_NOMBRE'].nunique()}")
print(f"Total de cantones: {df_prefectos_total['CANTON_NOMBRE'].nunique()}")
print(f"\nProvincias procesadas:")
print(df_prefectos_total['PROVINCIA_NOMBRE'].unique())
```

---

## Fase 5: Validación de datos

### Validación 1: Integridad de datos
```python
# Ejecutar después de procesar:
print("=== VALIDACIÓN DE INTEGRIDAD ===\n")

# 1. Verificar NaN
nulos = df_prefectos_total.isnull().sum()
if nulos.sum() > 0:
    print("⚠️ Columnas con valores NaN:")
    print(nulos[nulos > 0])
else:
    print("✅ No hay valores NaN")

# 2. Verificar duplicados
duplicados = df_prefectos_total.duplicated(subset=['ANIO', 'CANTON_CODIGO']).sum()
if duplicados > 0:
    print(f"⚠️ Hay {duplicados} registros duplicados")
else:
    print("✅ No hay duplicados en ANIO-CANTON_CODIGO")

# 3. Verificar consistencia de votos
print("\n=== VALIDACIÓN DE VOTOS ===")
df_prefectos_total['VOTOS_REALES'] = df_prefectos_total[[col for col in df_prefectos_total.columns 
                                                           if col not in ['ANIO', 'DIGNIDAD_CODIGO', 
                                                                        'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE',
                                                                        'CANTON_CODIGO', 'CANTON_NOMBRE',
                                                                        'VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 
                                                                        'VOTOS VALIDOS_T', 'BLANCOS_F', 
                                                                        'BLANCOS_M', 'BLANCOS_T', 'NULOS_F',
                                                                        'NULOS_M', 'NULOS_T', 'ELECTORES_F',
                                                                        'ELECTORES_M', 'ELECTORES_T',
                                                                        'SUFRAGANTES_F', 'SUFRAGANTES_M',
                                                                        'SUFRAGANTES_T']]].sum(axis=1)

diferencia = (df_prefectos_total['VOTOS VALIDOS_T'] - df_prefectos_total['VOTOS_REALES']).abs().sum()
if diferencia == 0:
    print("✅ VOTOS VALIDOS = suma de candidatos")
else:
    print(f"⚠️ Diferencia total: {diferencia}")
    print("  (Esto puede ser normal si hay candidatos con 0 votos)")
```

### Validación 2: Cobertura geográfica
```python
print("\n=== VALIDACIÓN GEOGRÁFICA ===\n")

# 1. Provincias
provincias_esperadas = set(provincias_dict.values())
provincias_obtenidas = set(df_prefectos_total['PROVINCIA_NOMBRE'].unique())
faltantes = provincias_esperadas - provincias_obtenidas
extras = provincias_obtenidas - provincias_esperadas

if len(faltantes) == 0 and len(extras) == 0:
    print(f"✅ Todas las {len(provincias_obtenidas)} provincias cubiertas")
else:
    if faltantes:
        print(f"⚠️ Provincias faltantes: {faltantes}")
    if extras:
        print(f"⚠️ Provincias extras: {extras}")

# 2. Cantones por provincia
print(f"\n✅ Cantones procesados por provincia:")
cantones_por_prov = df_prefectos_total.groupby('PROVINCIA_NOMBRE')['CANTON_NOMBRE'].nunique().sort_values(ascending=False)
for prov, cant in cantones_por_prov.head(5).items():
    print(f"  - {prov}: {cant} cantones")
print(f"  ...")
```

### Validación 3: Sensatez de números
```python
print("\n=== VALIDACIÓN DE SENSATEZ ===\n")

# 1. Electores razonables
print("Electores por canton:")
print(f"  Min: {df_prefectos_total['ELECTORES_T'].min():,}")
print(f"  Max: {df_prefectos_total['ELECTORES_T'].max():,}")
print(f"  Promedio: {df_prefectos_total['ELECTORES_T'].mean():,.0f}")

# 2. Participación razonable
df_prefectos_total['PARTICIPACION'] = (
    df_prefectos_total['SUFRAGANTES_T'] / df_prefectos_total['ELECTORES_T'] * 100
)
participacion_baja = df_prefectos_total[df_prefectos_total['PARTICIPACION'] < 20]
participacion_alta = df_prefectos_total[df_prefectos_total['PARTICIPACION'] > 100]

if len(participacion_baja) > 0:
    print(f"\n⚠️ {len(participacion_baja)} cantones con participación < 20%")
if len(participacion_alta) > 0:
    print(f"⚠️ {len(participacion_alta)} cantones con participación > 100%")
if len(participacion_baja) == 0 and len(participacion_alta) == 0:
    print(f"\n✅ Participación en rango razonable (20-100%)")
    print(f"  Promedio: {df_prefectos_total['PARTICIPACION'].mean():.1f}%")

# Limpiar columna temporal
df_prefectos_total.drop('PARTICIPACION', axis=1, inplace=True)
```

---

## Fase 6: Guardado de resultados

### Guardar CSV base
```python
# Ejecutar celda: "# Guardar resultados de prefectos"

# Verificar que se guardó
import os
archivo_salida = "../tests/prefectos_votes_by_canton_2023.csv"
if os.path.exists(archivo_salida):
    print(f"✅ Archivo guardado: {archivo_salida}")
    tamaño_mb = os.path.getsize(archivo_salida) / (1024 * 1024)
    print(f"  Tamaño: {tamaño_mb:.2f} MB")
    
    # Verificar leyendo de vuelta
    df_verify = pd.read_csv(archivo_salida)
    print(f"  Filas: {len(df_verify)}")
    print(f"  Columnas: {len(df_verify.columns)}")
else:
    print(f"❌ Archivo no encontrado: {archivo_salida}")
```

---

## Fase 7: Completación (Opcional)

Si deseas seguir el mismo flujo que presidentes:

### Agregar electores por grupo de edad
```python
# Crear función análoga a:
# add_electores_column_with_suffixes_not_agregated()

df_prefectos_electores = add_electores_column_with_suffixes_not_agregated(2023, "CANTON_CODIGO")

# Hacer merge con prefectos_total
df_prefectos_complete = pd.merge(
    df_prefectos_total,
    df_prefectos_electores,
    on=["ANIO", "CANTON_CODIGO"],
    how="inner"
)

# Guardar versión completa
df_prefectos_complete.to_csv(
    "../tests/prefectos_votacion_cantonal_complete_2023.csv",
    index=False
)
print("✅ Guardado: prefectos_votacion_cantonal_complete_2023.csv")
```

---

## Matriz de estado

| Paso | Descripción | Estado | Fecha | Notas |
|------|-------------|--------|-------|-------|
| 1.1 | Verificar datos seccionales | ⏳ Pendiente | - | Ejecutar verificación |
| 2.1 | Definir `extract_prefectos_names_and_votos()` | ✅ Hecho | - | Agregada al notebook |
| 2.2 | Definir `merge_prefectos_votes_by_sex()` | ✅ Hecho | - | Agregada al notebook |
| 3.1 | Test 1: Extracción simple | ⏳ Pendiente | - | Ejecutar script |
| 3.2 | Test 2: Agregación por provincia | ⏳ Pendiente | - | Ejecutar script |
| 3.3 | Test 3: Merge con sexo | ⏳ Pendiente | - | Ejecutar script |
| 4.1 | Test 4: Una provincia | ⏳ Pendiente | - | Ejecutar script |
| 4.2 | Test 5: Todas las provincias | ⏳ Pendiente | - | Toma 5-10 min |
| 5.1 | Validación integridad | ⏳ Pendiente | - | Ejecutar script |
| 5.2 | Validación geográfica | ⏳ Pendiente | - | Ejecutar script |
| 5.3 | Validación sensatez | ⏳ Pendiente | - | Ejecutar script |
| 6.1 | Guardar CSV base | ⏳ Pendiente | - | Ejecutar celda |
| 7.1 | Agregar electores (opcional) | ⏳ Pendiente | - | Flujo completo |

---

## Resolución de problemas comunes

### Problema 1: "DIGNIDAD_CODIGO == '2' returns empty DataFrame"
```python
# Verificar qué dignidades están disponibles
test_year_votacion, _, _ = test_standarized_resultados(2023)
print("Dignidades disponibles:")
print(test_year_votacion['DIGNIDAD_CODIGO'].unique())
```

### Problema 2: "candidatos_{year}.csv not found"
```python
# Verificar ruta correcta
import os
ruta = f"../data/csv_files/seccionales/2023/organizaciones_politicas/"
if os.path.exists(ruta):
    print("Archivos disponibles:")
    print(os.listdir(ruta))
else:
    print(f"Ruta no existe: {ruta}")
```

### Problema 3: "Columna esperada no existe"
```python
# Inspeccionar estructura de datos
test_year_eleccion_test = test_standarized_resultados(2023)[1]
print("Columnas disponibles:")
print(test_year_eleccion_test.columns.tolist())
```

---

## Próximos pasos después de completar

1. ✅ Procesar **alcaldes** (`dignidad_codigo="3"`)
2. ✅ Procesar **concejales** (`dignidad_codigo="5"`)
3. ✅ Procesar **vocales de juntas** (`dignidad_codigo="6"`)
4. ✅ Consolidar en un único script
5. ✅ Extender a otros años (2019, 2014, 2009, 2004)
6. ✅ Crear comparativas históricas
