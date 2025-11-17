# Documentación de Instancias - KBP Dataset

**Proyecto**: KBP-SA (Knapsack Problem con Simulated Annealing)  
**Fecha**: 2025-11-17  
**Total de instancias**: 31 archivos

---

## 📊 Resumen de Datasets

El proyecto incluye dos categorías principales de instancias del Knapsack Problem:

| Categoría | Cantidad | Tamaño (n) | Rango Capacidad | Dificultad |
|-----------|----------|------------|-----------------|------------|
| **Low-Dimensional** | 10 | 4-23 | 11-10,000 | Baja-Media |
| **Large-Scale** | 21 | 100-10,000 | ~1,000 | Alta |

---

## 📁 Estructura de Directorios

```
datasets/
├── low_dimensional/          # 10 instancias pequeñas
│   ├── f1_l-d_kp_10_269_low-dimensional.txt
│   ├── f2_l-d_kp_20_878_low-dimensional.txt
│   ├── f3_l-d_kp_4_20_low-dimensional.txt
│   ├── f4_l-d_kp_4_11_low-dimensional.txt
│   ├── f5_l-d_kp_15_375_low-dimensional.txt
│   ├── f6_l-d_kp_10_60_low-dimensional.txt
│   ├── f7_l-d_kp_7_50_low-dimensional.txt
│   ├── f8_l-d_kp_23_10000_low-dimensional.txt
│   ├── f9_l-d_kp_5_80_low-dimensional.txt
│   └── f10_l-d_kp_20_879_low-dimensional.txt
│
└── large_scale/              # 21 instancias grandes
    ├── knapPI_1_100_1000_1_large_scale.txt
    ├── knapPI_1_200_1000_1_large_scale.txt
    ├── knapPI_1_500_1000_1_large_scale.txt
    ├── knapPI_1_1000_1000_1_large_scale.txt
    ├── knapPI_1_2000_1000_1_large_scale.txt
    ├── knapPI_1_5000_1000_1_large_scale.txt
    ├── knapPI_1_10000_1000_1_large_scale.txt
    ├── knapPI_2_100_1000_1_large_scale.txt
    ├── knapPI_2_200_1000_1_large_scale.txt
    ├── knapPI_2_500_1000_1_large_scale.txt
    ├── knapPI_2_1000_1000_1_large_scale.txt
    ├── knapPI_2_2000_1000_1_large_scale.txt
    ├── knapPI_2_5000_1000_1_large_scale.txt
    ├── knapPI_2_10000_1000_1_large_scale.txt
    ├── knapPI_3_100_1000_1_large_scale.txt
    ├── knapPI_3_200_1000_1_large_scale.txt
    ├── knapPI_3_500_1000_1_large_scale.txt
    ├── knapPI_3_1000_1000_1_large_scale.txt
    ├── knapPI_3_2000_1000_1_large_scale.txt
    ├── knapPI_3_5000_1000_1_large_scale.txt
    └── knapPI_3_10000_1000_1_large_scale.txt
```

---

## 📋 Formato de Archivos

Todas las instancias siguen el **formato estándar del Knapsack Problem**:

```
<optimal_value>
<n> <capacity>
<value_1> <weight_1>
<value_2> <weight_2>
...
<value_n> <weight_n>
```

### Descripción de Campos

- **Línea 1**: `optimal_value` - Valor óptimo conocido de la solución (para validación)
- **Línea 2**: `n capacity` - Número de ítems y capacidad de la mochila
- **Líneas 3 a n+2**: `value weight` - Valor y peso de cada ítem

### Ejemplo (f1_l-d_kp_10_269_low-dimensional.txt)

```
295                 ← Valor óptimo conocido
10 269              ← 10 ítems, capacidad 269
55 95               ← Ítem 1: valor=55, peso=95
10 4                ← Ítem 2: valor=10, peso=4
47 60               ← Ítem 3: valor=47, peso=60
...
```

---

## 🔍 Low-Dimensional Instances

### Características

- **Propósito**: Testing rápido, validación de algoritmos
- **Complejidad**: Baja a media
- **Tiempo de resolución**: < 1 segundo con algoritmos exactos
- **Uso recomendado**: Validación inicial, debugging, pruebas de concepto

### Catálogo Detallado

| Archivo | n (ítems) | Capacidad | Óptimo | Líneas | Ratio C/n |
|---------|-----------|-----------|--------|--------|-----------|
| f3_l-d_kp_4_20 | 4 | 20 | - | 6 | 5.00 |
| f4_l-d_kp_4_11 | 4 | 11 | - | 6 | 2.75 |
| f9_l-d_kp_5_80 | 5 | 80 | - | 7 | 16.00 |
| f7_l-d_kp_7_50 | 7 | 50 | - | 9 | 7.14 |
| f1_l-d_kp_10_269 | 10 | 269 | 295 | 12 | 26.90 |
| f6_l-d_kp_10_60 | 10 | 60 | - | 12 | 6.00 |
| f5_l-d_kp_15_375 | 15 | 375 | - | 17 | 25.00 |
| f2_l-d_kp_20_878 | 20 | 878 | - | 22 | 43.90 |
| f10_l-d_kp_20_879 | 20 | 879 | - | 22 | 43.95 |
| f8_l-d_kp_23_10000 | 23 | 10,000 | 9,767 | 25 | 434.78 |

### Notas

- **f8**: Instancia especial con capacidad muy grande (10,000) relativa al número de ítems
- **Ratio C/n**: Capacidad dividida por número de ítems (indica "holgura" del problema)
- Instancias con ratio bajo (< 10) son más restrictivas

---

## 🏗️ Large-Scale Instances (Pisinger's Benchmark)

### Características

- **Origen**: David Pisinger's benchmark set
- **Propósito**: Evaluación de rendimiento en problemas grandes
- **Complejidad**: Alta
- **Tiempo de resolución**: Segundos a minutos (depende del algoritmo)
- **Uso recomendado**: Benchmarking, comparación con estado del arte

### Nomenclatura

```
knapPI_<type>_<n>_<R>_<instance>_large_scale.txt

Donde:
- type: Tipo de instancia (1, 2, 3)
- n: Número de ítems
- R: Factor de correlación (~1000 en este conjunto)
- instance: Número de instancia (típicamente 1)
```

### Tipos de Instancias (Pisinger)

| Tipo | Descripción | Correlación v-w | Dificultad |
|------|-------------|-----------------|------------|
| **Type 1** | Uncorrelated | Ninguna | Media |
| **Type 2** | Weakly correlated | Débil | Alta |
| **Type 3** | Strongly correlated | Fuerte | Muy Alta |

**Nota**: Type 3 son las más difíciles porque los valores están altamente correlacionados con los pesos.

### Catálogo por Tamaño

#### Pequeñas (n = 100-500)
```
knapPI_1_100_1000_1    → 100 ítems, Type 1
knapPI_1_200_1000_1    → 200 ítems, Type 1
knapPI_1_500_1000_1    → 500 ítems, Type 1
knapPI_2_100_1000_1    → 100 ítems, Type 2
knapPI_2_200_1000_1    → 200 ítems, Type 2
knapPI_2_500_1000_1    → 500 ítems, Type 2
knapPI_3_100_1000_1    → 100 ítems, Type 3
knapPI_3_200_1000_1    → 200 ítems, Type 3
knapPI_3_500_1000_1    → 500 ítems, Type 3
```

#### Medianas (n = 1,000-2,000)
```
knapPI_1_1000_1000_1   → 1,000 ítems, Type 1 (1,003 líneas)
knapPI_1_2000_1000_1   → 2,000 ítems, Type 1 (2,003 líneas)
knapPI_2_1000_1000_1   → 1,000 ítems, Type 2
knapPI_2_2000_1000_1   → 2,000 ítems, Type 2
knapPI_3_1000_1000_1   → 1,000 ítems, Type 3
knapPI_3_2000_1000_1   → 2,000 ítems, Type 3
```

#### Grandes (n = 5,000-10,000)
```
knapPI_1_5000_1000_1   → 5,000 ítems, Type 1
knapPI_1_10000_1000_1  → 10,000 ítems, Type 1 (10,003 líneas)
knapPI_2_5000_1000_1   → 5,000 ítems, Type 2
knapPI_2_10000_1000_1  → 10,000 ítems, Type 2
knapPI_3_5000_1000_1   → 5,000 ítems, Type 3
knapPI_3_10000_1000_1  → 10,000 ítems, Type 3
```

### Ejemplo (knapPI_1_100_1000_1_large_scale.txt)

```
9147                ← Valor óptimo conocido
100 995             ← 100 ítems, capacidad 995
94 485              ← Ítem 1: valor=94, peso=485
506 326             ← Ítem 2: valor=506, peso=326
416 248             ← Ítem 3: valor=416, peso=248
...
```

---

## 🎯 Uso Recomendado por Categoría

### Para Training/Validación del GAA

| Fase | Instancias Recomendadas | Justificación |
|------|-------------------------|---------------|
| **Desarrollo inicial** | Low-dimensional (f1-f7) | Feedback rápido, debugging |
| **Validación** | Low-dimensional (f8-f10) + knapPI Type 1 (n≤500) | Balance rapidez/realismo |
| **Training GAA** | knapPI Type 1 y 2 (n=100-1000) | Diversidad moderada |
| **Testing final** | knapPI Type 2 y 3 (n=1000-5000) | Evaluación rigurosa |
| **Benchmarking** | knapPI Type 3 (n=5000-10000) | Comparación con SOTA |

### Configuración Sugerida

```yaml
# En config.yaml

datasets:
  training:
    path: "./datasets/low_dimensional"
    instances: ["f1_*.txt", "f5_*.txt", "f6_*.txt"]
    
  validation:
    path: "./datasets/large_scale"
    instances: ["knapPI_1_100_*.txt", "knapPI_2_100_*.txt"]
    
  test:
    path: "./datasets/large_scale"
    instances: ["knapPI_3_500_*.txt", "knapPI_3_1000_*.txt"]
    
  benchmark:
    path: "./datasets/large_scale"
    instances: ["knapPI_*_5000_*.txt", "knapPI_*_10000_*.txt"]
```

---

## 📊 Estadísticas del Dataset

### Distribución por Tamaño

```
n ≤ 25:       10 instancias (Low-dimensional)
n = 100:       3 instancias (Large-scale Type 1-3)
n = 200:       3 instancias (Large-scale Type 1-3)
n = 500:       3 instancias (Large-scale Type 1-3)
n = 1000:      3 instancias (Large-scale Type 1-3)
n = 2000:      3 instancias (Large-scale Type 1-3)
n = 5000:      3 instancias (Large-scale Type 1-3)
n = 10000:     3 instancias (Large-scale Type 1-3)
```

### Distribución por Tipo (Large-scale)

- **Type 1** (Uncorrelated): 7 instancias
- **Type 2** (Weakly correlated): 7 instancias
- **Type 3** (Strongly correlated): 7 instancias

### Cobertura de Dificultad

```
Fácil (n ≤ 100):        13 instancias (42%)
Media (100 < n ≤ 1000): 12 instancias (39%)
Difícil (n > 1000):      6 instancias (19%)
```

---

## 🔬 Validación de Carga

Para verificar que todas las instancias se cargan correctamente:

```powershell
# Desde el directorio del proyecto
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA

# Validar todas las instancias
python validate_datasets.py
```

### Validación Manual (Python)

```python
from pathlib import Path
import sys
sys.path.insert(0, '../../04-Generated/scripts')
from data_loader import DataLoader

# Cargar low-dimensional
loader_low = DataLoader(
    dataset_dir=Path("datasets/low_dimensional"),
    problem_type='knapsack'
)
instances_low = loader_low.load_training_set()
print(f"Low-dimensional: {len(instances_low)} instancias")

# Cargar large-scale
loader_large = DataLoader(
    dataset_dir=Path("datasets/large_scale"),
    problem_type='knapsack'
)
instances_large = loader_large.load_training_set()
print(f"Large-scale: {len(instances_large)} instancias")

# Verificar primera instancia
if instances_low:
    inst = instances_low[0]
    print(f"\nEjemplo: {inst['filename']}")
    print(f"  n = {inst['n']}")
    print(f"  Capacidad = {inst['capacity']}")
    print(f"  Valores: {inst['values'][:5]}...")
    print(f"  Pesos: {inst['weights'][:5]}...")
```

---

## 📚 Referencias

### Origen de Instancias

**Low-dimensional**:
- Instancias de prueba clásicas del Knapsack Problem
- Usadas para validación de algoritmos exactos
- Fuente: Literatura clásica de optimización combinatoria

**Large-scale (Pisinger)**:
- **Autor**: David Pisinger
- **Publicación**: "Where are the hard knapsack problems?" (2005)
- **URL**: http://hjemmesider.diku.dk/~pisinger/codes.html
- **Descripción**: Benchmark estándar para evaluar algoritmos de Knapsack
- **Citación**: Pisinger, D. (2005). Where are the hard knapsack problems? Computers & Operations Research, 32(9), 2271-2284.

### Papers Relacionados

1. **Martello & Toth (1990)**: "Knapsack Problems: Algorithms and Computer Implementations"
2. **Pisinger (1997)**: "A minimal algorithm for the 0-1 knapsack problem"
3. **Kellerer et al. (2004)**: "Knapsack Problems"

---

## 💡 Consejos de Uso

### Para Desarrollo Rápido
- Usar **low-dimensional** (f1-f7) durante desarrollo
- Permiten iteraciones rápidas (< 1s por evaluación)
- Facilitan debugging de terminales

### Para Validación
- Usar **knapPI Type 1** (n=100-500) para validar correctitud
- Son más fáciles pero representativas

### Para Benchmarking
- Usar **knapPI Type 2 y 3** (n≥1000) para comparación seria
- Reportar resultados en Type 3 (más difíciles)
- Comparar con best-known values (línea 1 de cada archivo)

### Para Publicación
- Incluir resultados en **knapPI Type 3** (n=1000-10000)
- Reportar gap con óptimo conocido
- Comparar con CPLEX, Gurobi u otros solvers comerciales

---

## ✅ Checklist de Validación

- [x] 31 instancias disponibles (10 low-dim + 21 large-scale)
- [x] Formato consistente en todos los archivos
- [x] Valores óptimos conocidos presentes (línea 1)
- [x] Cobertura de tamaños: 4 a 10,000 ítems
- [x] Cobertura de tipos: Uncorrelated, Weakly correlated, Strongly correlated
- [x] Compatible con `data_loader.py` del framework GAA

---

**Última actualización**: 2025-11-17  
**Total de instancias**: 31  
**Espacio en disco**: ~2.5 MB
