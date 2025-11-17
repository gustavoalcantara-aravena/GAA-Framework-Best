# KBP-SA: Sistema GAA Modular

**Sistema de Generación Automática de Algoritmos (GAA) para el Problema de la Mochila (Knapsack Problem) usando Simulated Annealing**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Este proyecto implementa un framework completo de **Generación Automática de Algoritmos (GAA)** para resolver el problema de la mochila 0/1 (Knapsack Problem) utilizando Simulated Annealing como metaheurística maestra.

El sistema sigue la metodología GAA de 7 fases:

1. **Definición del Problema** - Modelo matemático del KBP
2. **Extracción de Terminales** - 14 operadores de literatura
3. **Generación de Algoritmos** - AST, gramática BNF, intérprete
4. **Problema Maestro** - Simulated Annealing completo
5. **Experimentación** - Análisis estadístico robusto
6. **Algoritmos Finales** - Selección de top-3
7. **Documentación** - Reporte científico

## 🏗️ Arquitectura Modular

```
KBP-SA/
├── core/                    # Definición del problema
│   ├── problem.py          # KnapsackProblem
│   ├── solution.py         # KnapsackSolution
│   └── evaluation.py       # KnapsackEvaluator
│
├── operators/               # 14 Terminales GAA
│   ├── constructive.py     # 4 constructivos (Greedy, Random)
│   ├── improvement.py      # 4 de mejora (Flip, Exchange)
│   ├── perturbation.py     # 3 de perturbación (Shake, Destroy)
│   └── repair.py           # 2 de reparación
│
├── gaa/                     # Sistema GAA
│   ├── ast_nodes.py        # 10 tipos de nodos AST
│   ├── grammar.py          # Gramática BNF
│   ├── generator.py        # Generador de algoritmos
│   └── interpreter.py      # Intérprete AST
│
├── metaheuristic/           # Simulated Annealing
│   ├── sa_core.py          # Motor principal SA
│   ├── cooling_schedules.py # 5 esquemas de enfriamiento
│   └── acceptance.py       # 6 criterios de aceptación
│
├── data/                    # Gestión de datasets
│   ├── loader.py           # Carga de instancias
│   └── validator.py        # Validación
│
├── utils/                   # Utilidades
│   ├── config.py           # Gestión de configuración
│   ├── logging.py          # Sistema de logging
│   └── random.py           # Gestión de semillas
│
├── experimentation/         # Fase 5 GAA
│   ├── runner.py           # Ejecución de experimentos
│   ├── metrics.py          # Métricas de calidad/rendimiento
│   ├── statistics.py       # Análisis estadístico
│   └── visualization.py    # Gráficas y reportes
│
├── datasets/                # Instancias de benchmarking
│   ├── low_dimensional/    # 10 instancias pequeñas
│   └── large_scale/        # 21 instancias grandes
│
└── output/                  # Resultados
    ├── experiments/        # Datos experimentales
    └── plots/              # Visualizaciones
```

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip

### Instalación básica

```bash
# Clonar repositorio
git clone <repo-url>
cd KBP-SA

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias principales

- `numpy` - Operaciones numéricas
- `scipy` - Tests estadísticos
- `matplotlib` (opcional) - Visualizaciones
- `pandas` (opcional) - Análisis de datos

## 📖 Uso

### Demo Completo End-to-End

```bash
python demo_complete.py
```

Este script ejecuta 5 demostraciones:
1. Carga de instancias
2. Generación automática de 3 algoritmos
3. Ejecución con intérprete AST
4. Simulated Annealing tradicional
5. Comparación de métodos constructivos

### Demo de Experimentación

```bash
python demo_experimentation.py
```

Ejecuta experimentos completos con:
- Múltiples algoritmos generados automáticamente
- Repeticiones estadísticas (configurable)
- Análisis estadístico (tests, intervalos de confianza)
- Visualizaciones (boxplots, barras, scatter)
- Reportes en JSON y HTML

### Uso Programático

#### Cargar una instancia

```python
from data.loader import DatasetLoader

loader = DatasetLoader()
instances = loader.load_folder("low_dimensional")
problem = instances[0]  # Primera instancia

print(f"Instancia: {problem.name}")
print(f"Items: {problem.n}, Capacidad: {problem.capacity}")
```

#### Generar un algoritmo

```python
from gaa.grammar import Grammar
from gaa.generator import AlgorithmGenerator

grammar = Grammar(min_depth=2, max_depth=4)
generator = AlgorithmGenerator(grammar=grammar, seed=42)

algorithm = generator.generate_with_validation()
print(algorithm.to_pseudocode())
```

#### Ejecutar un algoritmo

```python
from gaa.interpreter import ASTInterpreter

interpreter = ASTInterpreter(problem, seed=42)
solution = interpreter.execute(algorithm)

print(f"Valor: {solution.value}")
print(f"Factible: {solution.is_feasible}")
```

#### Ejecutar Simulated Annealing

```python
from metaheuristic.sa_core import SimulatedAnnealing
from operators.constructive import GreedyByRatio

# Configurar SA
sa = SimulatedAnnealing(
    problem=problem,
    T0=100.0,
    alpha=0.95,
    iterations_per_temp=50,
    seed=42
)

# Solución inicial
constructor = GreedyByRatio(problem)
initial = constructor.construct()

# Optimizar
best = sa.optimize(initial)
print(f"Mejor valor: {best.value}")
```

#### Ejecutar experimentos

```python
from experimentation.runner import ExperimentRunner, ExperimentConfig

config = ExperimentConfig(
    name="my_experiment",
    instances=["f1_l-d_kp_10_269_low-dimensional"],
    algorithms=[
        {'name': 'Algorithm1', 'ast': algorithm1},
        {'name': 'Algorithm2', 'ast': algorithm2}
    ],
    repetitions=30
)

runner = ExperimentRunner(config)
runner.load_instances("low_dimensional")
results = runner.run_all()
runner.save_results()
```

## 📊 Datasets

El sistema incluye 31 instancias de benchmarking:

### Low-Dimensional (10 instancias)
- Rango: 4-23 ítems
- Valores óptimos conocidos
- Fuente: Pisinger format

### Large-Scale (21 instancias)
- Rango: 100-10,000 ítems
- 1,000 variables por instancia
- Tipos: knapPI_1, knapPI_2, knapPI_3

## 🔬 Operadores Implementados

### Constructivos (4)
- **GreedyByValue** [Dantzig1957]: Ordena por valor descendente
- **GreedyByWeight** [Martello1990]: Ordena por peso ascendente
- **GreedyByRatio** [Pisinger2005]: Ordena por ratio valor/peso
- **RandomConstruct** [Khuri1994]: Construcción aleatoria

### Mejora (4)
- **FlipBestItem** [Martello1999]: Flip del mejor ítem
- **FlipWorstItem** [Pisinger2007]: Flip del peor ítem
- **OneExchange** [Kellerer2004]: Intercambio 1-1
- **TwoExchange** [Vazirani2001]: Intercambio 2-2

### Perturbación (3)
- **RandomFlip** [Glover1998]: k flips aleatorios
- **ShakeByRemoval** [Lourenco2003]: Elimina k ítems
- **DestroyRepair** [Shaw1998]: Destruye y reconstruye

### Reparación (2)
- **RepairByRemoval** [Chu1998]: Elimina hasta factibilidad
- **RepairByGreedy** [Pisinger1999]: Repara y completa vorazmente

Todos los operadores incluyen referencias bibliográficas completas.

## 📈 Experimentación

El módulo `experimentation/` proporciona:

### Métricas de Calidad
- Gap al óptimo (%)
- Estadísticas (media, desviación, mediana, rango)
- Coeficiente de variación
- Tasa de éxito

### Métricas de Rendimiento
- Tiempo de ejecución
- Iteraciones/evaluaciones
- Eficiencia (valor/segundo)
- Convergencia

### Análisis Estadístico
- Estadísticas descriptivas
- Intervalos de confianza (95%)
- Test de normalidad (Shapiro-Wilk)
- Tests paramétricos: t-test pareado
- Tests no paramétricos: Wilcoxon, Mann-Whitney, Friedman
- Tamaño del efecto (Cohen's d)
- Rankings promedio

### Visualizaciones
- Curvas de convergencia
- Boxplots comparativos
- Gráficas de barras con IC
- Scatter tiempo vs calidad
- Performance profiles
- Reportes HTML

## 🧪 Testing

```bash
# Ejecutar tests unitarios (cuando estén implementados)
python -m pytest tests/

# Validar datasets
python validate_datasets.py
```

## 📚 Referencias Bibliográficas

El sistema está basado en más de 20 referencias científicas, incluyendo:

- Kirkpatrick et al. (1983): Optimization by Simulated Annealing
- Pisinger (2005): Where are the hard knapsack problems?
- Dolan & Moré (2002): Benchmarking optimization software
- Barr et al. (1995): Designing computational experiments
- Derrac et al. (2011): Statistical tests tutorial

Ver archivos individuales para referencias completas.

## 🔧 Configuración

El archivo `config.yaml` permite configurar:

```yaml
metaheuristic:
  parameters:
    T0: 100.0
    alpha: 0.95
    iterations_per_temp: 100
    T_min: 0.01

experimentation:
  repetitions: 30
  alpha: 0.05
  output_dir: "output/experiments"

logging:
  level: "INFO"
  file: "logs/kbp_sa.log"
```

## 📝 Resultados

Los resultados se guardan en:

- **JSON**: Datos completos de experimentos (`output/experiments/`)
- **Gráficas**: PNG de alta resolución (`output/plots/`)
- **HTML**: Reportes interactivos
- **Logs**: Ejecución detallada (`logs/`)

## 🤝 Contribuciones

Este es un proyecto de investigación académica. Para contribuciones:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para detalles

## 👥 Autores

- Proyecto de Tesis Doctoral
- Sistema GAA para KBP-SA

## 🙏 Agradecimientos

- Comunidad científica de metaheurísticas
- Autores de papers citados
- Benchmarks de Pisinger

---

**Documentación completa**: Ver archivos individuales en cada módulo para documentación técnica detallada.

**Estado del Proyecto**: ✅ Implementación completa de Fases 1-5 GAA
