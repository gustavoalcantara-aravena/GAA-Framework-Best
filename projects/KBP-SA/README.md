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
│   ├── visualization.py       # Generación de gráficas
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
│   ├── demo_experimentation.py # Experimentos con gráficas
│   ├── demo_acceptance_rate.py # Visualización SA
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

### 4. Experimentos con Gráficas (1-2 minutos)

```bash
python scripts/demo_experimentation.py
```

**Gráficas generadas en:**
- `output/low_dimensional/plots_{instance}_TIMESTAMP/`

### 5. Visualización Simulated Annealing

```bash
python scripts/demo_acceptance_rate.py
```

Muestra evolución de temperatura y tasa de aceptación.

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

1. **Boxplots**: Comparación de calidad por algoritmo
2. **Barras con error**: Gaps promedio con intervalos de confianza
3. **Scatter plots**: Tiempo vs calidad
4. **Convergencia**: Evolución del mejor valor
5. **Temperatura**: Temperatura vs tasa de aceptación

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
| Tests (18 tests) | ✅ 100% passing |
| Datasets (31 instancias) | ✅ Validados |
| Documentación | ✅ Completa |

---

**Última actualización**: Diciembre 2024
