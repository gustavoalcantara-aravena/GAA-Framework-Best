# Guía de Ejecución del Sistema de Experimentación KBP-SA

## Descripción General

Este documento describe el proceso completo para ejecutar el sistema de experimentación que genera visualizaciones estadísticas y de Simulated Annealing (SA) para instancias del Problema de la Mochila (Knapsack Problem).

**Última actualización**: 19 de noviembre de 2025

---

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Ejecución para Low-Dimensional](#ejecución-para-low-dimensional)
5. [Ejecución para Large-Scale](#ejecución-para-large-scale)
6. [Salidas Generadas](#salidas-generadas)
7. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

### Software Requerido

1. **Python 3.12+**
   - Anaconda recomendado (incluye la mayoría de dependencias)

2. **Graphviz** (para visualización de AST)
   - Instalación en Windows: `winget install --id Graphviz.Graphviz -e`
   - Verificación: `dot -V`

3. **Dependencias Python**
   ```bash
   pip install numpy matplotlib scipy
   pip install graphviz
   ```

### Configuración de PATH (Windows)

Si Graphviz no está en el PATH del sistema:

```powershell
$env:Path += ";C:\Program Files\Graphviz\bin"
```

Para hacerlo permanente, agregar en las variables de entorno del sistema:
- Variable: `Path`
- Valor: `C:\Program Files\Graphviz\bin`

---

## Configuración del Entorno

### 1. Ubicación del Proyecto

```bash
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
```

### 2. Verificar Estructura de Datasets

Asegurarse de que existan las siguientes carpetas:

```
datasets/
├── low_dimensional/       # 10 instancias (f1-f10)
│   ├── f1_l-d_kp_10_269_low-dimensional.txt
│   ├── f2_l-d_kp_20_878_low-dimensional.txt
│   ├── ...
│   └── f10_l-d_kp_20_879_low-dimensional.txt
│
└── large_scale/          # 21 instancias (knapPI_*)
    ├── knapPI_1_100_1000_1_large_scale.txt
    ├── knapPI_1_200_1000_1_large_scale.txt
    ├── ...
    └── knapPI_3_10000_1000_1_large_scale.txt
```

### 3. Verificar Carga de Instancias

**Low-dimensional:**
```powershell
python -c "from data.loader import DatasetLoader; from pathlib import Path; loader = DatasetLoader(Path('datasets')); instances = loader.load_folder('low_dimensional'); print(f'Instancias low: {len(instances)}')"
```
**Esperado**: `Instancias low: 10`

**Large-scale:**
```powershell
python -c "from data.loader import DatasetLoader; from pathlib import Path; loader = DatasetLoader(Path('datasets')); instances = loader.load_folder('large_scale'); print(f'Instancias large: {len(instances)}')"
```
**Esperado**: `Instancias large: 21`

---

## Estructura del Proyecto

### Archivos Principales

```
KBP-SA/
├── scripts/
│   └── demo_experimentation.py    # Script principal de experimentación
├── datasets/                      # Instancias del problema
├── output/                        # Resultados generados
├── experimentation/               # Módulo de análisis
│   ├── runner.py                 # Ejecutor de experimentos
│   ├── visualization.py          # Generador de gráficas
│   └── statistics.py             # Análisis estadístico
└── gaa/                          # Grammar-based Algorithm Generator
```

### Configuración en demo_experimentation.py

Parámetros clave (líneas 324-334):

```python
config = ExperimentConfig(
    name="all_instances_experiment",       # Nombre del experimento
    instances=instance_names,              # Lista de instancias a procesar
    algorithms=algorithms,                 # Algoritmos GAA generados (3 por defecto)
    repetitions=1,                        # Repeticiones por experimento
    max_time_seconds=60.0,                # Timeout por ejecución
    output_dir="output/all_instances_experiments"
)
```

---

## Ejecución para Low-Dimensional

### Paso 1: Ejecutar el Script

```powershell
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
$env:Path += ";C:\Program Files\Graphviz\bin"
python scripts/demo_experimentation.py
```

### Paso 2: Proceso de Ejecución

El script ejecuta automáticamente los siguientes pasos:

1. **🧬 Paso 1**: Generación de algoritmos GAA
   - Genera 3 algoritmos usando la gramática
   - Muestra pseudocódigo de cada uno

2. **⚙️ Paso 2**: Configuración del experimento
   - Carga 10 instancias low-dimensional
   - Configura 30 experimentos totales (10 instancias × 3 algoritmos × 1 rep)

3. **🚀 Paso 3**: Ejecución de experimentos
   - Ejecuta cada algoritmo en cada instancia
   - Muestra progreso: `[X/30] instancia × algoritmo ... ✅`

4. **💾 Paso 4**: Guardado de resultados
   - JSON: `output/all_instances_experiments/experiment_*.json`

5. **📊 Paso 5**: Análisis estadístico
   - Estadísticas descriptivas por algoritmo
   - Intervalos de confianza (95%)

6. **🔬 Paso 6**: Comparación estadística
   - Test de Friedman (comparación múltiple)
   - Test de Wilcoxon (comparación pareada)
   - Tamaño del efecto (Cohen's d)

7. **📈 Paso 7**: Generación de visualizaciones
   - **7.1**: AST del mejor algoritmo
   - **7.2**: Gráficas de comparación estadística (3)
   - **7.3**: Gráficas SA del grupo (3 agregadas + 10 por instancia)

### Paso 3: Verificar Resultados

**Carpeta de salida:**
```
output/plots_low_dimensional_YYYYMMDD_HHMMSS/
```

**Conteo de archivos:**
```powershell
$latest = Get-ChildItem "output\plots_low_dimensional_*" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-ChildItem $latest.FullName -Filter *.png | Measure-Object | Select-Object Count
```
**Esperado**: 17 archivos PNG

---

## Ejecución para Large-Scale

### Modificaciones Necesarias

Editar `scripts/demo_experimentation.py`:

#### Cambio 1: Cargar instancias large-scale (líneas 314-315)

**Antes:**
```python
datasets_dir = Path(__file__).parent.parent / "datasets"
loader = DatasetLoader(datasets_dir)
all_instances = loader.load_folder("low_dimensional")
```

**Después:**
```python
datasets_dir = Path(__file__).parent.parent / "datasets"
loader = DatasetLoader(datasets_dir)
all_instances = loader.load_folder("large_scale")
```

#### Cambio 2: Ajustar configuración (líneas 324-334)

```python
config = ExperimentConfig(
    name="large_scale_experiment",         # Nombre descriptivo
    instances=instance_names,
    algorithms=algorithms,
    repetitions=1,                        # Aumentar a 3-5 para análisis robusto
    max_time_seconds=300.0,              # Aumentar timeout (5 min)
    output_dir="output/large_scale_experiments"
)
```

#### Cambio 3: Actualizar carga de instancias en runner (línea 349)

**Antes:**
```python
runner.load_instances("low_dimensional")
```

**Después:**
```python
runner.load_instances("large_scale")
```

#### Cambio 4: Actualizar carpeta de visualizaciones (líneas 525, 546)

**Antes:**
```python
plots_dir = f"output/plots_low_dimensional_{timestamp}"
# ...
group_instances = loader.load_folder("low_dimensional")
```

**Después:**
```python
plots_dir = f"output/plots_large_scale_{timestamp}"
# ...
group_instances = loader.load_folder("large_scale")
```

### Ejecución

```powershell
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
$env:Path += ";C:\Program Files\Graphviz\bin"
python scripts/demo_experimentation.py
```

### Salida Esperada

**Carpeta:**
```
output/plots_large_scale_YYYYMMDD_HHMMSS/
```

**Archivos esperados**: 28 PNG
- 3 gráficas estadísticas
- 1 AST
- 3 gráficas SA agregadas
- 21 gráficas exploration-exploitation (una por instancia)

---

## Salidas Generadas

### Estructura de Archivos de Salida

```
output/
├── all_instances_experiments/
│   └── experiment_all_instances_experiment_YYYYMMDD_HHMMSS.json
│
└── plots_low_dimensional_YYYYMMDD_HHMMSS/
    ├── demo_boxplot.png                              # Comparación boxplot
    ├── demo_bars.png                                 # Gap promedio por algoritmo
    ├── demo_scatter.png                              # Tiempo vs calidad
    ├── best_algorithm_ast.png                        # Estructura del mejor algoritmo
    ├── gap_evolution.png                             # Media ± std de gaps
    ├── acceptance_rate.png                           # Tasa promedio de aceptación
    ├── delta_e_distribution.png                      # Distribución combinada de ΔE
    ├── exploration_exploitation_f1_l-d_kp_10_269.png
    ├── exploration_exploitation_f2_l-d_kp_20_878.png
    ├── ...                                           # Una por cada instancia
    └── exploration_exploitation_f10_l-d_kp_20_879.png
```

### Descripción de Gráficas

#### Gráficas Estadísticas (Grupo)

1. **demo_boxplot.png**
   - Comparación de gap al óptimo entre algoritmos
   - Muestra mediana, cuartiles y outliers

2. **demo_bars.png**
   - Gap promedio por algoritmo con barras de error (std)

3. **demo_scatter.png**
   - Trade-off entre tiempo de ejecución y calidad de solución

4. **best_algorithm_ast.png**
   - Visualización gráfica de la estructura del mejor algoritmo
   - Muestra operadores y flujo de control

#### Gráficas SA Agregadas (Grupo)

5. **gap_evolution.png**
   - Evolución del gap durante la búsqueda
   - Banda sombreada: desviación estándar entre instancias
   - Línea: media del gap
   - Eje derecho: temperatura (escala log)

6. **acceptance_rate.png**
   - Tasa de aceptación de movimientos
   - Calculada con ventana móvil (100 iteraciones)
   - Muestra transición de exploración a explotación

7. **delta_e_distribution.png**
   - Distribución de cambios de energía (ΔE)
   - Separado por movimientos aceptados/rechazados
   - Datos combinados de todas las instancias

#### Gráficas SA Individuales (Por Instancia)

8-17. **exploration_exploitation_<instancia>.png**
   - Balance entre exploración y explotación por instancia
   - Área apilada mostrando proporciones:
     * Verde: Explotación (mejoras)
     * Naranja: Exploración (empeoramientos aceptados)
     * Rojo: Rechazados
   - Panel estadístico con métricas clave
   - Línea de temperatura superpuesta

---

## Solución de Problemas

### Error: "Graphviz no encontrado"

**Síntoma:**
```
❌ Error generando gráfico AST: failed to execute WindowsPath('dot')
```

**Solución:**
```powershell
# Verificar instalación
dot -V

# Si no está en PATH, agregar temporalmente
$env:Path += ";C:\Program Files\Graphviz\bin"

# O instalar
winget install --id Graphviz.Graphviz -e
```

### Error: "Encoding UTF-8"

**Síntoma:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solución:**
El script ya incluye configuración UTF-8 para Windows (líneas 18-21):
```python
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### Falta de Instancias

**Síntoma:**
```
❌ No se pudieron cargar instancias. Abortando.
```

**Solución:**
```powershell
# Verificar que existen las carpetas
Test-Path "datasets\low_dimensional"
Test-Path "datasets\large_scale"

# Listar archivos
Get-ChildItem "datasets\low_dimensional"
```

### Memoria Insuficiente (Large-Scale)

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Solución:**
- Reducir `repetitions` a 1
- Procesar instancias en lotes
- Aumentar memoria virtual del sistema

### Script Demasiado Lento

**Optimizaciones:**

1. Reducir evaluaciones SA:
   ```python
   sa = SimulatedAnnealing(
       problem=instance,
       T0=100.0,
       alpha=0.95,
       max_evaluations=2000,  # Reducir de 5000
       ...
   )
   ```

2. Reducir repeticiones:
   ```python
   repetitions=1  # En lugar de 3 o más
   ```

3. Procesar subset de instancias:
   ```python
   instance_names = instance_names[:5]  # Solo primeras 5
   ```

---

## Tiempos de Ejecución Estimados

### Low-Dimensional (10 instancias)

| Componente | Tiempo |
|------------|--------|
| Experimentos (30 ejecuciones) | ~8-10 seg |
| Análisis estadístico | ~1 seg |
| Gráficas estadísticas | ~2 seg |
| SA tracking (10 instancias) | ~30-40 seg |
| Gráficas SA | ~10-15 seg |
| **TOTAL** | **~1.5 minutos** |

### Large-Scale (21 instancias)

| Componente | Tiempo |
|------------|--------|
| Experimentos (63 ejecuciones) | ~5-10 min |
| Análisis estadístico | ~2 seg |
| Gráficas estadísticas | ~3 seg |
| SA tracking (21 instancias) | ~5-10 min |
| Gráficas SA | ~30-60 seg |
| **TOTAL** | **~15-20 minutos** |

*Nota: Los tiempos varían según hardware y complejidad de algoritmos generados.*

---

## Verificación de Resultados

### Checklist Post-Ejecución

**Low-Dimensional:**
- [ ] JSON de resultados generado en `output/all_instances_experiments/`
- [ ] Carpeta `plots_low_dimensional_*` creada
- [ ] 17 archivos PNG generados (3 + 1 + 3 + 10)
- [ ] Todos los archivos > 10 KB (gráficas válidas)
- [ ] Consola muestra: "✅ Experimentos completados: 30/30"

**Large-Scale:**
- [ ] JSON de resultados generado en `output/large_scale_experiments/`
- [ ] Carpeta `plots_large_scale_*` creada
- [ ] 28 archivos PNG generados (3 + 1 + 3 + 21)
- [ ] Todos los archivos > 10 KB
- [ ] Consola muestra: "✅ Experimentos completados: 63/63"

### Comando de Verificación

```powershell
# Contar archivos PNG generados
$latest = Get-ChildItem "output\plots_*" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Write-Host "Carpeta: $($latest.Name)"
$pngs = Get-ChildItem $latest.FullName -Filter *.png
Write-Host "Archivos PNG: $($pngs.Count)"
$pngs | Select-Object Name, @{N="KB";E={[math]::Round($_.Length/1KB,1)}} | Format-Table
```

---

## Contacto y Soporte

Para problemas o dudas sobre el sistema de experimentación:
- Revisar logs en la consola
- Verificar archivos de configuración
- Consultar documentación de módulos individuales en `experimentation/`

**Última revisión**: 19 de noviembre de 2025
