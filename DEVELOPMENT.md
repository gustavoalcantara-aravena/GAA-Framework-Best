# Guía de Desarrollo - GAA Framework

## 🎯 Para Desarrolladores

Esta guía te ayudará a extender y personalizar el framework GAA para tus propios problemas de optimización.

---

## 📋 Tabla de Contenidos

1. [Configuración Inicial](#configuración-inicial)
2. [Crear un Nuevo Proyecto](#crear-un-nuevo-proyecto)
3. [Definir Tu Problema](#definir-tu-problema)
4. [Añadir Terminales](#añadir-terminales)
5. [Configurar Metaheurística](#configurar-metaheurística)
6. [Preparar Datasets](#preparar-datasets)
7. [Ejecutar Experimentos](#ejecutar-experimentos)
8. [Debugging](#debugging)

---

## ⚙️ Configuración Inicial

### 1. Instalar Dependencias

```powershell
# Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar requirements
pip install -r requirements.txt
```

### 2. Verificar Instalación

```powershell
python 05-Automation/sync-engine.py --validate
```

---

## 🆕 Crear un Nuevo Proyecto

### Estructura Básica

```powershell
# Crear directorios
mkdir projects/MiProblema-SA
mkdir projects/MiProblema-SA/datasets/training
mkdir projects/MiProblema-SA/datasets/validation
mkdir projects/MiProblema-SA/datasets/test
mkdir projects/MiProblema-SA/generated
```

### Archivos Necesarios

1. **problema_metaheuristica.md** - Especificación completa
2. **config.yaml** - Configuración de experimentos
3. **run.py** - Script de ejecución
4. **validate_datasets.py** - Validación de datos

---

## 📝 Definir Tu Problema

### 1. Crear `problema_metaheuristica.md`

```markdown
---
gaa_metadata:
  version: 1.0.0
  project_name: "Mi Problema con SA"
  problem: "Nombre del Problema"
  metaheuristic: "Simulated Annealing"
  status: "active"
---

# Proyecto: Mi Problema con SA

## Mathematical-Model

### Función Objetivo
```math
\text{Minimizar: } f(x) = ...
```

### Restricciones
```math
g_i(x) \leq 0, \quad i = 1, \ldots, m
h_j(x) = 0, \quad j = 1, \ldots, p
```

## Domain-Operators

### Constructivos
- **MiConstructor1**: Descripción [Autor2024]
- **MiConstructor2**: Descripción [Autor2023]

### Mejora Local
- **MiBusquedaLocal**: Descripción [Autor2022]

### Perturbación
- **MiPerturbacion**: Descripción [Autor2021]
```

### 2. Definir Representación de Soluciones

```python
## Solution-Representation

**Estructura de datos**:
```python
# Ejemplo: Vector de enteros
x = [x_1, x_2, ..., x_n]
# donde x_i representa...
```

**Restricciones**:
- Restricción 1: descripción
- Restricción 2: descripción
```

---

## 🔧 Añadir Terminales

### Paso 1: Identificar Operadores de la Literatura

```markdown
## Domain-Operators

### Terminal1
- **NombreTerminal**: Descripción detallada del operador
- **Referencia**: [Autor2024] - "Título del paper"
- **Complejidad**: O(n log n)
- **Parámetros**: p1, p2
```

### Paso 2: Implementar en Python

Edita `04-Generated/scripts/fitness.py`:

```python
def _get_terminals(self, problem: Problem) -> Dict[str, callable]:
    
    def mi_terminal(context: dict) -> None:
        """Descripción del terminal"""
        current = context['current_solution']
        
        # Implementar lógica del operador
        # ...
        
        context['current_solution'] = nueva_solucion
        self._update_best(context)
    
    return {
        'MiTerminal': mi_terminal,
        # ... otros terminales
    }
```

### Paso 3: Sincronizar

```powershell
python 05-Automation/sync-engine.py --sync
```

Los terminales se añadirán automáticamente a `Grammar.md`.

---

## 🎛️ Configurar Metaheurística

### config.yaml

```yaml
metaheuristic:
  name: "Simulated Annealing"
  type: "SA"
  
  parameters:
    T0: 100.0                    # Temperatura inicial
    alpha: 0.95                  # Factor de enfriamiento
    iterations_per_temp: 100     # Iteraciones por temperatura
    T_min: 0.01                  # Temperatura mínima
    max_evaluations: 10000       # Máximo de evaluaciones
```

### Parámetros Recomendados

| Metaheurística | Parámetro | Rango Típico | Recomendación |
|----------------|-----------|--------------|---------------|
| **SA** | T0 | 10-1000 | Depende del rango de Δf |
| **SA** | α | 0.8-0.99 | 0.95 para enfriamiento lento |
| **GP** | pop_size | 50-500 | 100 para problemas medianos |
| **GP** | crossover_rate | 0.6-0.9 | 0.8 estándar |

---

## 📊 Preparar Datasets

### Formato del Archivo

Cada problema tiene su formato específico. Ejemplo para TSP:

```
# tsp_n20.txt
20
0 10 15 20 25
10 0 35 30 12
15 35 0 18 22
...
```

### Validar Formato

```python
# validate_datasets.py

def _parse_mi_problema(self, file_path: Path) -> Dict[str, Any]:
    """Parser personalizado"""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Parsear según tu formato
    n = int(lines[0])
    data = ...
    
    return {
        'n': n,
        'data': data,
        'problem_type': 'mi_problema'
    }
```

### Ejecutar Validación

```powershell
cd projects/MiProblema-SA
python validate_datasets.py
```

---

## 🚀 Ejecutar Experimentos

### Ejecución Básica

```powershell
cd projects/KBP-SA
python run.py
```

### Ejecución con Configuración Custom

```python
# run_custom.py
import yaml

# Modificar config dinámicamente
config = load_config()
config['metaheuristic']['parameters']['T0'] = 200.0

# Ejecutar con nuevo config
...
```

### Ejecución Múltiple (Batch)

```powershell
# Ejecutar 30 runs con diferentes seeds
for ($i=1; $i -le 30; $i++) {
    python run.py --seed $i
}
```

---

## 🐛 Debugging

### 1. Verificar Sincronización

```powershell
python 05-Automation/sync-engine.py --validate
```

**Problemas comunes**:
- ❌ YAML frontmatter mal formateado
- ❌ Secciones faltantes en `.md`
- ❌ Nombres de terminales con espacios

### 2. Inspeccionar AST Generado

```python
# En run.py, después de optimize()

print("AST completo:")
print(best_algorithm.to_string())

# Ver todos los nodos
all_nodes = best_algorithm.get_all_nodes()
for i, node in enumerate(all_nodes):
    print(f"Nodo {i}: {type(node).__name__}")
```

### 3. Debugging de Fitness

```python
# En fitness.py

def evaluate(self, algorithm_ast: ASTNode, max_evaluations: int = 1000) -> float:
    print(f"[DEBUG] Evaluando AST tamaño {algorithm_ast.size()}")
    
    results = []
    for instance_data in self.training_instances:
        result = self._run_algorithm(algorithm_ast, problem_instance, max_evaluations)
        print(f"[DEBUG] Instancia: fitness={result}")
        results.append(result)
    
    return np.mean(results)
```

### 4. Verificar Datasets

```python
from data_loader import DataLoader

loader = DataLoader(dataset_dir="./datasets", problem_type="knapsack")
instances = loader.load_training_set()

# Inspeccionar primera instancia
print(instances[0])
print(loader.validate_instance(instances[0]))
```

### 5. Logs Detallados

```yaml
# En config.yaml
logging:
  level: "DEBUG"  # Cambiar de INFO a DEBUG
  console: true
```

---

## 🧪 Testing

### Crear Tests Unitarios

```python
# tests/test_mi_problema.py

import pytest
from problem import MiProblema

def test_evaluate():
    instance = {...}
    problem = MiProblema(instance)
    solution = problem.random_solution()
    
    fitness = problem.evaluate(solution)
    assert fitness >= 0

def test_feasibility():
    problem = MiProblema(instance)
    solution = problem.random_solution()
    
    assert problem.is_feasible(solution)
```

### Ejecutar Tests

```powershell
pytest tests/ -v
```

---

## 📈 Optimización de Performance

### 1. Usar NumPy para Operaciones Numéricas

```python
# ❌ Lento
total = sum([x * y for x, y in zip(values, weights)])

# ✅ Rápido
import numpy as np
total = np.sum(values * weights)
```

### 2. Cachear Evaluaciones

```python
class Problem:
    def __init__(self):
        self._cache = {}
    
    def evaluate(self, solution):
        key = tuple(solution.representation)
        if key not in self._cache:
            self._cache[key] = self._compute_fitness(solution)
        return self._cache[key]
```

### 3. Limitar Tamaño de AST

```yaml
# En config.yaml
gaa:
  max_depth: 5  # Limitar profundidad
  max_size: 100  # Limitar número total de nodos
```

---

## 📚 Recursos Adicionales

### Papers Recomendados

- **Genetic Programming**: Koza (1992)
- **Simulated Annealing**: Kirkpatrick et al. (1983)
- **Hyper-heuristics**: Burke et al. (2013)
- **AutoML**: Hutter et al. (2019)

### Benchmarks Estándar

- **Knapsack**: Pisinger, OR-Library
- **TSP**: TSPLIB
- **Graph Coloring**: DIMACS Challenge
- **VRP**: Solomon Instances

---

## 🤝 Contribuir

### Proceso

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/mi-feature`
3. Commit cambios: `git commit -m "Añadir mi-feature"`
4. Push: `git push origin feature/mi-feature`
5. Crear Pull Request

### Estándares de Código

- **Black** para formateo: `black .`
- **Flake8** para linting: `flake8 .`
- **Mypy** para type hints: `mypy .`

---

## ❓ FAQ

**P: ¿Cómo añado un nuevo tipo de nodo al AST?**

R: Edita `04-Generated/scripts/ast_nodes.py` y añade una nueva clase heredando de `ASTNode`. Luego actualiza `01-System/AST-Nodes.md`.

**P: ¿Puedo usar múltiples metaheurísticas en un proyecto?**

R: Sí, modifica `run.py` para ejecutar varias metaheurísticas y compara resultados.

**P: ¿Cómo acelero la evaluación?**

R: Usa menos instancias de entrenamiento, reduce `max_evaluations`, o paraleliza con `multiprocessing`.

---

**Última actualización**: 2025-11-17  
**Versión**: 1.0.0
