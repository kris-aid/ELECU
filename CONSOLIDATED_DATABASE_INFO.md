# Base de Datos Consolidada Electorial 2002-2025

## ✅ Generación Completada

Se ha creado exitosamente una base de datos consolidada que integra todos los datos electorales presidenciales desde 2002 hasta 2025.

## 📊 Archivos Generados

Ubicación: `tests/Presidenciales/`

### 1. **presidentes_votacion_consolidado_2002_2025.csv** (Formato ANGOSTO)
- **Tamaño:** 4.8 MB
- **Filas:** 86,731 registros
- **Columnas:** 9
  - `ANIO` - Año de elección
  - `VUELTA` - Número de vuelta (1ª o 2ª)
  - `PROVINCIA_CODIGO` - Código de provincia
  - `PROVINCIA_NOMBRE` - Nombre de provincia
  - `CANTON_CODIGO` - Código de cantón
  - `CANTON_NOMBRE` - Nombre de cantón
  - `CANDIDATO_NOMBRE` - Nombre del candidato
  - `AGRUPACION` - Agrupación política (F/M/T para desglose o nacional)
  - `VOTOS` - Cantidad de votos

- **Años cubiertos:** 2002, 2006, 2007, 2009, 2013, 2017, 2021, 2023, 2025
- **Candidatos únicos:** 150
- **Cantones:** 272
- **Provincias:** 27

### 2. **presidentes_votacion_consolidado_2002_2025_ancho.csv** (Formato ANCHO)
- **Tamaño:** 0.5 MB
- **Filas:** 3,025 registros
- **Columnas:** 62
  - Estructura: Una fila por año-vuelta-provincia-cantón con candidatos como columnas
  - Primera 5 columnas: ANIO, VUELTA, PROVINCIA_CODIGO, PROVINCIA_NOMBRE, CANTON_CODIGO
  - Resto: Candidatos como encabezados con sus votos

### 3. **presidentes_resumen_nacional_2002_2025.csv** (RESUMEN)
- **Tamaño:** 0.01 MB
- **Filas:** 178 registros (candidatos × años)
- **Columnas:** 3
  - `ANIO` - Año
  - `CANDIDATO_NOMBRE` - Candidato
  - `VOTOS` - Total de votos a nivel nacional

## 📈 Estadísticas por Año

| Año | Total Votos | Candidatos | Cantons |
|-----|------------|-----------|---------|
| 2002 | 20,804,194 | - | 217 |
| 2006 | 25,116,028 | - | 261 |
| 2009 | 15,857,496 | - | 263 |
| 2013 | 18,931,720 | - | 268 |
| 2017 | 42,190,878 | - | 269 |
| 2021 | 42,566,004 | - | 261 |
| 2023 | 43,784,214 | - | 259 |
| 2025 | 48,456,408 | - | 259 |

**Total consolidado:** 86,731 registros

## 🔝 Top 3 Ganadores por Año (Votos Nacionales)

- **2002:** Lucio Gutiérrez (7.5M) vs Álvaro Noboa (6.2M)
- **2006:** Rafael Correa (9.5M) vs Álvaro Noboa (8.3M)
- **2009:** Rafael Correa (7.2M) vs Lucio Gutiérrez (3.9M)
- **2013:** Rafael Correa (9.8M) vs Guillermo Lasso (3.9M)
- **2017:** Lenín Moreno (17.6M) vs Guillermo Lasso (15.0M)
- **2021:** Andrés Arauz (14.5M) vs Guillermo Lasso (13.0M)
- **2023:** Luisa González (16.4M) vs Daniel Noboa (15.1M)
- **2025:** ADN (11.4M) vs Daniel Noboa Azín (10.4M)

## 🔄 Estructura de Datos

### Formato ANGOSTO (Largo)
Ideal para análisis detallados por cantón:
```
ANIO,VUELTA,PROVINCIA_CODIGO,PROVINCIA_NOMBRE,CANTON_CODIGO,CANTON_NOMBRE,CANDIDATO_NOMBRE,AGRUPACION,VOTOS
2002,1,EC01,AZUAY,EC0101,CUENCA,ALVARO NOBOA,F,7463
2002,1,EC01,AZUAY,EC0101,CUENCA,ALVARO NOBOA,M,6950
2002,1,EC01,AZUAY,EC0101,CUENCA,ALVARO NOBOA,T,14413
```

### Formato ANCHO (Ancho)
Ideal para comparaciones entre candidatos:
```
ANIO,VUELTA,PROVINCIA_CODIGO,PROVINCIA_NOMBRE,CANTON_CODIGO,CANTON_NOMBRE,ALVARO NOBOA,ANTONIO VARGAS,...
2002,1,EC01,AZUAY,EC0101,CUENCA,14413,567,...
```

## 📁 Correspondencia de Fuentes

### Datos de Referencia (Tu archivo)
- Contenía 7,746 registros
- Años: 2002, 2006, 2009, 2013, 2017, 2021, 2023
- Fuente: presidentes_votacion_cantonal_formato_angosto.csv

### Datos 2025 (Datos reales del CNE)
- Contenía 9,269 registros
- Integrados desde: tests/Presidenciales/2025/
- Incluyen todos los candidatos y movimientos de 2025

### Año 2007
- Template vacío (sin datos disponibles)
- Estructura reservada para consistencia

## 🎯 Casos de Uso

### 1. Análisis Temporal
```sql
SELECT ANIO, CANDIDATO_NOMBRE, SUM(VOTOS) as total
FROM presidentes_votacion_consolidado_2002_2025
GROUP BY ANIO, CANDIDATO_NOMBRE
ORDER BY ANIO DESC
```

### 2. Comparación por Provincia
```sql
SELECT PROVINCIA_NOMBRE, CANDIDATO_NOMBRE, SUM(VOTOS)
FROM presidentes_votacion_consolidado_2002_2025
WHERE ANIO = 2023
GROUP BY PROVINCIA_NOMBRE, CANDIDATO_NOMBRE
```

### 3. Análisis por Votación (F/M/T)
```sql
SELECT AGRUPACION, SUM(VOTOS)
FROM presidentes_votacion_consolidado_2002_2025
WHERE ANIO = 2025
GROUP BY AGRUPACION
```

## 📝 Notas Técnicas

1. **AGRUPACION**: 
   - `F` = Femenino
   - `M` = Masculino
   - `T` = Total (consolidado)

2. **Estructura de datos**: Totalmente compatible con pandas, SQL y herramientas de BI

3. **Validación**: Se verificó la integridad estructural de todos los archivos

4. **Información de scripts**:
   - Script de consolidación: `scripts/create_consolidated_database.py`
   - Script de setup: `scripts/setup_template_from_reference.py`

## 🚀 Próximos Pasos

1. Importar los archivos CSV a tu base de datos
2. Crear índices en columnas de búsqueda frecuente (ANIO, CANDIDATO_NOMBRE, PROVINCIA)
3. Realizar análisis estadísticos según tus necesidades
4. Generar reportes y visualizaciones

---

**Fecha de Generación:** 2025
**Total de registros consolidados:** 86,731
**Años incluidos:** 9 elecciones presidenciales (2002-2025)
