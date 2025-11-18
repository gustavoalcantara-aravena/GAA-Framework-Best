# KBP-SA: Knapsack Problem con Simulated Annealing

Framework completo de optimización para el problema de la mochila (0/1 Knapsack) usando Simulated Annealing y generación automática de algoritmos.

[![Tests](https://img.shields.io/badge/tests-18%20passing-success)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Datasets](https://img.shields.io/badge/datasets-31%20validated-green)]()

---

## 📂 Estructura del Proyecto

```
KBP-SA/
├── 📁 core/                    # Componentes base del problema
│   ├── problem.py             # KnapsackProblem (definición)
│   ├── solution.py            # KnapsackSolution (representación)
│   └── evaluation.py          # KnapsackEvaluator (métricas)
│
├── 📁 operators/               # Operadores de búsqueda
│   ├── constructive.py        # Construcción de soluciones
│   ├── improvement.py         # Búsqueda local
│   ├── perturbation.py        # Perturbaciones
│   └── repair.py              # Reparación de factibilidad
│
├── 📁 metaheuristic/          # Simulated Annealing
│   ├── sa_core.py             # Motor principal del SA
│   ├── cooling_schedules.py  # Esquemas de enfriamiento
│   └── acceptance.py          # Criterios de aceptación
│
├── 📁 gaa/                     # Sistema GAA (Generación Automática)
│   ├── grammar.py             # Gramática BNF
│   ├── ast_nodes.py           # Nodos del AST
│   ├── generator.py           # Generador de algoritmos
│   └── interpreter.py         # Intérprete de AST
│
├── 📁 experimentation/        # Framework experimental
│   ├── runner.py              # Ejecución en batch
│   ├── metrics.py             # Métricas de calidad
│   ├── statistics.py          # Análisis estadístico
│   ├── visualization.py       # Generación de gráficas (SA avanzadas)
│   ├── ast_visualization.py   # Visualización de árboles sintácticos
│   └── tracking.py            # Sistema de tracking de variables
│
├── 📁 data/                    # Gestión de datos
│   ├── loader.py              # Carga de instancias
│   └── validator.py           # Validación de formato
│
├── 📁 utils/                   # Utilidades
│   ├── config.py              # Gestión de configuración
│   ├── logging.py             # Sistema de logs
│   └── random.py              # Generadores aleatorios
│
├── 📁 datasets/               # 31 instancias benchmark
│   ├── low_dimensional/       # 10 instancias (n=4-23)
│   └── large_scale/           # 21 instancias (n=100-10,000)
│
├── 📁 tests/                   # Tests unitarios
│   └── test_core.py           # 18 tests (100% passing)
│
├── 📁 scripts/                 # Scripts ejecutables
│   ├── demo_complete.py       # Demo completo del sistema
│   ├── demo_experimentation.py # Experimentos con gráficas (TODAS las instancias)
│   ├── demo_acceptance_rate.py # Visualización SA
│   ├── test_single_instance.py # Test con una instancia (f1)
│   ├── test_all_low_dimensional.py # Test de TODAS las instancias + reporte
│   ├── test_gap_visualization.py # Test de gap evolution
│   ├── test_acceptance_visualization.py # Suite completa SA (6 gráficas)
│   ├── test_ast_visualization.py # Test renderizado AST
│   ├── quick_ast_test.py      # Validación rápida Graphviz
│   ├── experiment_large_scale.py # Experimentos large-scale
│   ├── test_quick.py          # Validación rápida
│   ├── validate_datasets.py   # Validación de datasets
│   ├── generate_example_datasets.py # Generación de ejemplos
│   └── run.py                 # Ejecución principal
│
├── 📁 docs/                    # Documentación
│   ├── QUICKSTART_EJECUTABLE.md # Inicio rápido
│   ├── COMO_EJECUTAR_EXPERIMENTOS.md # Guía de experimentos
│   ├── TRACKING_LOGS.md       # Sistema de tracking
│   ├── SA_VISUALIZER_IMPLEMENTATION_PLAN.md # Plan de visualizaciones SA
│   ├── README_SISTEMA.md      # Documentación completa
│   ├── DATASET_STATUS.md      # Estado de datasets
│   ├── INSTRUCTIONS.md        # Instrucciones generales
│   ├── QUICKSTART.md          # Quick start general
│   └── ploteos.md             # Especificaciones de gráficas
│
├── 📁 config/                  # Configuración
│   ├── config.yaml            # Configuración del proyecto
│   └── problema_metaheuristica.md # Especificación del problema
│
├── 📁 output/                  # Resultados (no versionado)
│   ├── low_dimensional/       # Salidas instancias pequeñas
│   └── large_scale/           # Salidas instancias grandes
│
├── .gitignore                 # Archivos ignorados por Git
├── requirements.txt           # Dependencias Python
└── README.md                  # Este archivo
```

---

## 🚀 Quick Start

### 1. Instalación

```bash
# Navegar al proyecto
cd projects/KBP-SA

# Instalar dependencias
pip install -r requirements.txt

# Instalar Graphviz (para visualización AST)
pip install graphviz

# Instalar ejecutable Graphviz (Windows)
winget install graphviz
# O descargar desde: https://graphviz.org/download/
```

### 2. Validación Rápida (10 segundos)

```bash
python scripts/test_quick.py
```

**Salida esperada:**
```
✅ Todos los datasets válidos
✅ Sistema operativo correctamente
```

### 3. Demo Completo (30 segundos)

```bash
python scripts/demo_complete.py
```

Ejecuta el sistema completo en una instancia pequeña.

### 4. Experimentos con Gráficas (2-5 minutos)

```bash
python scripts/demo_experimentation.py
```

**Ejecuta experimentos con TODAS las instancias low-dimensional (10 instancias)**:
- 3 algoritmos GAA generados
- 3 repeticiones por instancia
- Total: 90 ejecuciones (10 × 3 × 3)

**Todas las visualizaciones en UNA sola carpeta:**
- `output/low_dimensional_YYYYMMDD_HHMMSS/`
  - Gráficas estadísticas (boxplot, bars, scatter)
  - Gráficas SA (gap_evolution, acceptance_rate, delta_e_distribution)
  - **AST del mejor algoritmo (best_algorithm_ast.png)**

### 5. Visualización Simulated Annealing

```bash
python scripts/demo_acceptance_rate.py
```

Muestra evolución de temperatura y tasa de aceptación.

### 6. Test Completo de Visualizaciones SA (Nuevo)

```bash
python scripts/test_acceptance_visualization.py
```

**Ejecuta SA con TODAS las instancias low-dimensional**:
- Visualizaciones detalladas de la primera instancia (más pequeña)
- Tracking completo de variables SA

**Genera 6 gráficas avanzadas:**
- Gap evolution con temperatura dual-axis
- Acceptance rate (3 ventanas: 50/100/200)
- Distribución de ΔE (dual subplot)
- Balance exploración-explotación (stacked area)

**Salida en:** `output/test_acceptance/`

### 7. Visualización de AST (Nuevo)

```bash
python scripts/test_ast_visualization.py
```

**Genera 3 gráficas de árboles sintácticos:**
- algorithm_1_ast.png
- algorithm_2_ast.png
- ast_comparison.png (comparación lado a lado)

**Salida en:** `output/ast_visualizations/`

**Requisitos:** Graphviz instalado (ejecutable + Python library)

### 8. Test Completo de Todas las Instancias (Nuevo)

```bash
python scripts/test_all_low_dimensional.py
```

**Ejecuta SA en las 10 instancias low-dimensional**:
- Una ejecución por instancia
- Reporte comparativo completo
- Estadísticas agregadas (gaps, tiempos, tasa de éxito)
- Guardado en JSON con timestamp

**Salida en:** `output/test_all_low_dimensional/results_TIMESTAMP.json`

**Tiempo estimado:** 30-60 segundos

---

## 📊 Datasets

### Low-Dimensional (10 instancias)
- **Tamaño**: n=4 a n=23 ítems
- **Fuente**: Pisinger (2005)
- **Uso**: Validación y pruebas rápidas

### Large-Scale (21 instancias)
- **Tamaño**: n=100 a n=10,000 ítems
- **Series**: knapPI_1, knapPI_2, knapPI_3
- **Uso**: Evaluación de escalabilidad

**Total**: ✅ 31 instancias validadas

Ver detalles en: [`docs/DATASET_STATUS.md`](docs/DATASET_STATUS.md)

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest tests/test_core.py -v

# Resultado esperado
# =================== 18 passed in 0.16s ===================
```

**Cobertura:**
- ✅ KnapsackProblem (validación, creación)
- ✅ KnapsackSolution (operaciones, factibilidad)
- ✅ KnapsackEvaluator (gap, métricas)
- ✅ DatasetLoader (carga, validación)

---

## 📈 Sistema de Tracking

El sistema incluye tracking automático de variables durante la optimización:

**Variables trackeadas:**
- Iteración, temperatura, valores (actual, mejor)
- Diferencia de energía, probabilidad de aceptación
- Gap al óptimo, tasa de aceptación
- Tiempo transcurrido, mejoras acumuladas

**Archivos generados:**
```
output/{dataset}/{instance}/
├── summary.json               # Resumen ejecutivo
├── tracking_full.csv          # Log por iteración
├── tracking_temperature.csv   # Log por temperatura
├── tracking_acceptance.csv    # Decisiones de aceptación
├── convergence.json           # Datos de convergencia
└── metadata.json              # Información del experimento
```

Ver documentación: [`docs/TRACKING_LOGS.md`](docs/TRACKING_LOGS.md)

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [`docs/QUICKSTART_EJECUTABLE.md`](docs/QUICKSTART_EJECUTABLE.md) | Guía de inicio rápido ejecutable |
| [`docs/COMO_EJECUTAR_EXPERIMENTOS.md`](docs/COMO_EJECUTAR_EXPERIMENTOS.md) | Cómo ejecutar experimentos completos |
| [`docs/TRACKING_LOGS.md`](docs/TRACKING_LOGS.md) | Sistema de logging y tracking |
| [`docs/SA_VISUALIZER_IMPLEMENTATION_PLAN.md`](docs/SA_VISUALIZER_IMPLEMENTATION_PLAN.md) | Plan completo de visualizaciones SA (8 categorías, 23 tipos) |
| [`docs/README_SISTEMA.md`](docs/README_SISTEMA.md) | Documentación técnica completa |
| [`docs/DATASET_STATUS.md`](docs/DATASET_STATUS.md) | Estado y validación de datasets |

---

## 🔧 Configuración

### Parámetros del SA

Editar en `config/config.yaml`:

```yaml
simulated_annealing:
  T0: 100.0                    # Temperatura inicial
  alpha: 0.95                  # Factor de enfriamiento
  iterations_per_temp: 100     # Iteraciones por temperatura
  T_min: 0.01                  # Temperatura mínima
  max_evaluations: 10000       # Presupuesto máximo
```

### Operadores Disponibles

```python
from operators.improvement import (
    OneExchange,        # Intercambio 1-1
    TwoExchange,        # Intercambio 2-2
    BitFlip,            # Flip de bit
    SwapItems           # Swap de ítems
)
```

---

## 📊 Resultados

### Métricas Calculadas

- **Gap to Optimal**: `((optimal - best) / optimal) * 100`
- **Success Rate**: Porcentaje de ejecuciones que alcanzan el óptimo
- **Average Gap**: Gap promedio sobre repeticiones
- **Convergence Speed**: Iteraciones hasta convergencia

### Visualizaciones

El sistema genera automáticamente:

**Visualizaciones Generales:**
1. **Boxplots**: Comparación de calidad por algoritmo
2. **Barras con error**: Gaps promedio con intervalos de confianza
3. **Scatter plots**: Tiempo vs calidad

**Visualizaciones SA Avanzadas (Nuevo):**
4. **Gap Evolution**: Evolución del gap con temperatura dual-axis
5. **Acceptance Rate**: Tasa de aceptación con temperatura dual-axis
6. **ΔE Distribution**: Histograma dual (aceptados/rechazados + mejoras/empeoramientos)
7. **Exploration-Exploitation Balance**: Área apilada (exploración vs explotación)

**Visualizaciones AST (Nuevo):**
8. **AST Graphviz**: Renderizado profesional de árboles sintácticos (PNG/PDF/SVG)
9. **AST ASCII**: Visualización en terminal
10. **AST Comparison**: Comparación lado a lado de múltiples algoritmos

Ver plan completo: [`docs/SA_VISUALIZER_IMPLEMENTATION_PLAN.md`](docs/SA_VISUALIZER_IMPLEMENTATION_PLAN.md)

---

## 📄 Licencia

Ver [LICENSE](../../LICENSE) en el repositorio raíz.

---

## 👤 Autor

**Gustavo Alcántara-Aravena**
- GitHub: [@gustavoalcantara-aravena](https://github.com/gustavoalcantara-aravena)
- Repositorio Principal: [GAA-Framework](https://github.com/gustavoalcantara-aravena/GAA-Framework)

---

**⭐ Estado del Proyecto**

| Componente | Estado |
|------------|--------|
| Core (Problem, Solution, Evaluation) | ✅ Producción |
| Operadores (14 operadores) | ✅ Completo |
| Simulated Annealing | ✅ Funcional |
| Sistema GAA | ✅ Implementado |
| Experimentación | ✅ Completo |
| Tracking | ✅ Implementado |
| **Visualización SA Avanzada** | ✅ **Nuevo: 4 gráficas** |
| **Visualización AST** | ✅ **Nuevo: Graphviz + ASCII** |
| Tests (18 tests) | ✅ 100% passing |
| Datasets (31 instancias) | ✅ Validados |
| Documentación | ✅ Completa |

---

**Última actualización**: 17 de noviembre de 2025

---

## 🎨 Nuevas Funcionalidades (v2.0)

### Sistema de Visualización SA Avanzado

**Módulo:** `experimentation/visualization.py`

**4 nuevos métodos:**

1. **`plot_gap_evolution()`**
   - Gráfica de gap (%) con temperatura dual-axis
   - Marca mejoras automáticamente
   - Panel estadístico con gap inicial/final/mínimo/promedio
   - Línea de tendencia polinómica

2. **`plot_acceptance_rate()`**
   - Tasa de aceptación con temperatura dual-axis
   - Ventana móvil configurable (50/100/200 iteraciones)
   - Media y líneas de referencia
   - Panel estadístico completo

3. **`plot_delta_e_distribution()`**
   - Dual subplot: Aceptados/Rechazados + Mejoras/Empeoramientos
   - Histogramas superpuestos
   - Estadísticas de ΔE (promedio, mediana)
   - Clasificación automática de movimientos

4. **`plot_exploration_exploitation_balance()`**
   - Área apilada: Explotación (verde) / Exploración (naranja) / Rechazados (rojo)
   - Temperatura dual-axis logarítmica
   - Detección de punto de transición (exploración < 10%)
   - Proporciones móviles con ventana configurable

### Sistema de Visualización AST

**Módulo:** `experimentation/ast_visualization.py`

**Clase:** `ASTVisualizer`

**Funcionalidades:**

- **`plot_ast_graphviz()`**: Renderizado profesional (PNG/PDF/SVG, 300 DPI)
- **`print_ast_ascii()`**: Visualización en terminal con box-drawing chars
- **`plot_ast_comparison()`**: Comparación lado a lado de múltiples algoritmos
- **`get_ast_statistics()`**: Análisis de estructura (nodos, profundidad, operadores)

**Características:**
- 10 tipos de nodos con colores específicos
- Etiquetas con parámetros (iteraciones, estrategias, operadores)
- Construcción recursiva del árbol
- Compatible con Graphviz v14.0.4

### Scripts de Test

**5 nuevos scripts de validación:**

1. **`test_single_instance.py`**: Test con f1 (óptimo: 295/295 ✅)
2. **`test_gap_visualization.py`**: Validación gap evolution
3. **`test_acceptance_visualization.py`**: Suite completa (6 gráficas)
4. **`test_ast_visualization.py`**: Renderizado AST (3 gráficas)
5. **`quick_ast_test.py`**: Validación rápida Graphviz

### Integración en Demo

**`scripts/demo_experimentation.py`** actualizado:

- **Paso 6.5 (nuevo)**: Visualización automática del mejor algoritmo
  - ASCII tree en terminal
  - PNG profesional con Graphviz
  - Estadísticas de AST (nodos, profundidad, operadores)

### Dependencias Nuevas

```bash
pip install graphviz  # Python library v0.21
winget install graphviz  # Ejecutable v14.0.4 (Windows)
```

**PATH requerido:** `C:\Program Files\Graphviz\bin`

---

## 📊 Ejemplos de Output

### Gap Evolution
![Gap Evolution](docs/images/gap_evolution_example.png)
- Eje Y izquierdo: Gap (%)
- Eje Y derecho: Temperatura (logarítmica)
- Marcadores de mejoras
- Panel estadístico

### AST Visualization
![AST Example](docs/images/ast_example.png)
- Nodos coloreados por tipo
- Parámetros visibles
- Estructura clara y profesional

---

**Última actualización**: 17 de noviembre de 2025
