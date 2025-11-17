---
gaa_metadata:
  version: 1.0.0
  project_name: "GCP con Iterated Local Search"
  problem: "Graph Coloring Problem"
  metaheuristic: "Iterated Local Search"
  status: "active"
  created: "2025-11-17"
---

# Proyecto: Graph Coloring Problem con Iterated Local Search

## 🎯 Información del Proyecto

**Problema**: Graph Coloring Problem (GCP)  
**Metaheurística**: Iterated Local Search (ILS)  
**Objetivo**: Generar algoritmos automáticamente mediante GAA para resolver instancias de coloración de grafos

---

# PARTE 1: DEFINICIÓN DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Graph Coloring Problem (GCP)  
**Tipo**: Minimización  
**Categoría**: Combinatorial Optimization - NP-Complete

## Descripción Informal

El problema de coloración de grafos consiste en asignar colores a los vértices de un grafo de tal manera que ningún par de vértices adyacentes (conectados por una arista) tengan el mismo color, utilizando el mínimo número de colores posible.

**Aplicaciones**:
- Asignación de frecuencias en redes de comunicación
- Planificación de horarios (scheduling)
- Asignación de registros en compiladores
- Resolución de sudokus
- Diseño de circuitos VLSI

## Mathematical-Model

### Función Objetivo

```math
\text{Minimizar: } k = \text{número de colores utilizados}
```

### Restricciones

```math
c_i \neq c_j, \quad \forall (i,j) \in E
```

```math
c_i \in \{1, 2, \ldots, k\}, \quad \forall i \in V
```

### Variables de Decisión

- **c_i**: Color asignado al vértice i
- **V**: Conjunto de vértices del grafo
- **E**: Conjunto de aristas del grafo
- **k**: Número de colores utilizados (a minimizar)
- **n = |V|**: Número de vértices
- **m = |E|**: Número de aristas

## Domain-Operators

### Terminales Identificados

#### Constructivos
- **GreedyDSATUR**: Construcción voraz por grado de saturación (colores distintos en vecinos) [Brelaz1979]
- **GreedyLF**: Largest First - ordena por grado decreciente y asigna colores [Welsh1967]
- **GreedySL**: Smallest Last - ordena por grado creciente recursivamente [Matula1972]
- **RandomSequential**: Asignación secuencial aleatoria de colores [Johnson1974]
- **RLF**: Recursive Largest First - coloración recursiva por subconjuntos independientes [Leighton1979]

#### Mejora Local
- **KempeChain**: Intercambio de colores mediante cadenas de Kempe [Kempe1879]
- **TabuCol**: Búsqueda local con memoria tabú [Hertz1987]
- **OneVertexMove**: Cambia color de un vértice conflictivo al mejor color disponible [Galinier1999]
- **SwapColors**: Intercambia dos colores en toda la solución [Fleurent1996]

#### Perturbación
- **RandomRecolor**: Recolorea aleatoriamente k vértices [Chiarandini2005]
- **PartialDestroy**: Destruye coloración de subgrafo y reconstruye [Malaguti2008]
- **ColorClassMerge**: Fusiona dos clases de color y repara [Avanthay2003]

#### Intensificación
- **Intensify**: Reduce número de colores y repara violaciones [Galinier1999]
- **GreedyImprovement**: Mejora local exhaustiva cambiando colores [Hertz1987]

#### Reparación
- **RepairConflicts**: Elimina conflictos cambiando colores de vértices conflictivos [Johnson1991]
- **BacktrackRepair**: Reparación con backtracking limitado [Brelaz1979]

## Solution-Representation

**Estructura de datos**:
```python
# Vector de colores de longitud n (número de vértices)
c = [c_1, c_2, ..., c_n]
# donde c_i ∈ {1, 2, ..., k}
# c_i = color asignado al vértice i
```

**Ejemplo**:
```
Grafo: n=5 vértices, aristas={(0,1), (0,2), (1,2), (2,3), (3,4)}
Solución: c = [1, 2, 3, 1, 2]
Interpretación:
  - Vértice 0: color 1
  - Vértice 1: color 2
  - Vértice 2: color 3
  - Vértice 3: color 1
  - Vértice 4: color 2
Número de colores: k = 3
Conflictos: 0 (solución factible)
```

## Constraints

**Restricciones duras**:
1. **No adyacencia**: Vértices adyacentes deben tener colores diferentes
2. **Conectividad**: Todos los vértices deben estar coloreados

**Parámetros del problema**:
- **n**: Número de vértices
- **m**: Número de aristas
- **E**: Conjunto de aristas (pares de vértices)
- **Δ**: Grado máximo del grafo
- **χ**: Número cromático (mínimo teórico, usualmente desconocido)

## Evaluation-Criteria

**Métrica principal**: Número de colores utilizados (k)  
**Criterio de comparación**: Menor es mejor  
**Manejo de infactibilidad**: 
- **Penalización**: fitness = k + número_de_conflictos
- **Reparación**: Aplicar RepairConflicts antes de evaluar
- **Permitir infactibilidad temporal** durante búsqueda (enfoque TabuCol)

**Función objetivo con penalización**:
```python
def evaluate(coloring, graph):
    k = max(coloring)  # Número de colores
    conflicts = count_conflicts(coloring, graph.edges)
    return k + 100 * conflicts  # Penalización alta a conflictos
```

---

# PARTE 2: METAHEURÍSTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Iterated Local Search (ILS)  
**Tipo**: Metaheurística de trayectoria con perturbación e intensificación  
**Referencia**: [Lourenco2003, Stützle2006]

## Descripción del Método

Iterated Local Search (ILS) es una metaheurística que itera entre tres fases principales:
1. **Búsqueda local**: Intensificación hasta óptimo local
2. **Perturbación**: Escape del óptimo local mediante cambios significativos
3. **Criterio de aceptación**: Decide si acepta la nueva solución

**Ventajas para GAA en GCP**:
- Efectivo para problemas de coloración
- Balance entre intensificación (búsqueda local) y diversificación (perturbación)
- Estructura modular que se adapta bien a AST
- Resultados competitivos en benchmarks de GCP

## Configuration

**Parámetros principales**:

```yaml
max_iteraciones: 500
intensidad_perturbacion: 0.20  # Porcentaje de vértices a recolorear
tipo_busqueda_local: "best_improvement"  # First vs Best
criterio_aceptacion: "better_or_equal"  # Always, Better, Better-or-Equal
max_iteraciones_sin_mejora: 50
```

**Justificación**:
- 500 iteraciones: Balance entre calidad y tiempo
- 20% perturbación: Suficiente para escape, no tan drástico
- Best improvement: Mayor calidad de óptimos locales
- Better-or-equal: Permite diversificación moderada

## Search-Strategy

### Operadores de Búsqueda sobre AST

**Mutación de Nodo Función**:
- Reemplazar nodo de búsqueda local por otro tipo
- Ejemplo: `LocalSearch(KempeChain)` → `LocalSearch(OneVertexMove)`
- Probabilidad: 0.25

**Mutación de Terminal**:
- Cambiar operador de construcción o mejora
- Ejemplo: `GreedyDSATUR` → `GreedyLF`
- Probabilidad: 0.50

**Mutación de Parámetro**:
- Modificar intensidad de perturbación
- Ejemplo: perturb_ratio: 0.20 → 0.25
- Perturbación: ±15%
- Probabilidad: 0.25

### Estructura Típica de ILS

```python
def ILS():
    s = GenerarSolucionInicial()  # Construcción
    s = BusquedaLocal(s)           # Intensificación
    s_best = s
    
    for iter in range(max_iterations):
        s_pert = Perturbar(s)      # Escape
        s_new = BusquedaLocal(s_pert)  # Intensificación
        
        if Aceptar(s_new, s):
            s = s_new
        
        if f(s_new) < f(s_best):
            s_best = s_new
    
    return s_best
```

### Acceptance-Criteria

**Estrategias disponibles**:

1. **Always Accept** (Siempre acepta):
```python
def accept(s_new, s_current):
    return True
```

2. **Better Only** (Solo mejoras):
```python
def accept(s_new, s_current):
    return fitness(s_new) < fitness(s_current)
```

3. **Better-or-Equal** (Mejoras o iguales):
```python
def accept(s_new, s_current):
    return fitness(s_new) <= fitness(s_current)
```

**Seleccionado para GCP**: Better-or-Equal (permite moverse por plateaus)

## Presupuesto Computacional

**Criterio de parada**:
- [x] Número de iteraciones: 500
- [x] Iteraciones sin mejora: 50
- [ ] Tiempo límite: N/A
- [ ] Óptimo conocido alcanzado: Opcional

**Presupuesto por evaluación de AST**:
- Iteraciones ILS por instancia: 500
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~45 segundos

## AST-Specific Considerations

**Validación de AST**:
- Validar gramática después de mutación: Sí
- Reparación automática de AST inválidos: Sí
- Profundidad máxima del árbol: 10

**Inicialización**:
- Método: Grow (crecimiento aleatorio con profundidad variable)
- Profundidad inicial: 4-6
- Población inicial de AST: 1 (ILS es single-solution)

**Operadores obligatorios en AST**:
- Al menos un constructor (e.g., GreedyDSATUR)
- Al menos una búsqueda local
- Al menos una perturbación

---

# PARTE 3: DATASETS

## Ubicación de Datasets

```
projects/GCP-ILS/datasets/
├── training/          # Instancias para optimizar AST
│   └── [Archivos .col o .txt]
├── validation/        # Instancias para ajustar parámetros ILS
│   └── [Archivos .col o .txt]
└── test/              # Instancias para evaluación final
    └── [Archivos .col o .txt]
```

## Formato de Archivo de Instancia

**Formato DIMACS** (`.col`):
```
p edge <n> <m>
e <v1> <v2>
e <v1> <v3>
...
```

**Formato Simplificado** (`.txt`):
```
n m
v1 v2
v1 v3
...
```

**Ejemplo** (`myciel3.col`):
```
p edge 11 20
e 1 2
e 1 4
e 1 7
e 1 9
e 2 3
e 2 6
e 2 8
e 3 5
e 3 7
e 3 10
e 4 5
e 4 6
e 4 10
e 5 8
e 6 11
e 7 11
e 8 11
e 9 11
e 10 11
```

## Datasets Recomendados

**Benchmarks clásicos de GCP**:
- **DIMACS Challenge**: https://mat.tepper.cmu.edu/COLOR/instances.html
  - Series: queen, myciel, anna, david, homer, huck, jean, games120, miles, fpsol, inithx, zeroin, mulsol
- **COLOR02/03**: Instancias del Second/Third DIMACS Challenge
- **Grafos aleatorios**: G(n,p) con diferentes densidades

**Sugerencias**:
- Training: 5-10 instancias pequeñas-medianas (n < 100)
- Validation: 3-5 instancias medianas (50 < n < 200)
- Test: 5-10 instancias variadas incluyendo algunas grandes

---

# PARTE 4: GENERACIÓN Y EXPERIMENTACIÓN

## Algoritmo Generado

El sistema GAA generará algoritmos ILS representados como AST combinando:
- **Funciones**: `Seq`, `If`, `While`, `ApplyUntilNoImprove`, `LocalSearch`
- **Terminales**: Los 15 operadores identificados en Domain-Operators

**Ejemplo de AST para ILS**:
```json
{
  "type": "Seq",
  "body": [
    {"type": "Call", "name": "GreedyDSATUR"},
    {"type": "ApplyUntilNoImprove", 
     "stmt": {"type": "Call", "name": "KempeChain"},
     "stop": {"type": "Stagnation", "iters": 10}
    },
    {"type": "While", "budget": {"kind": "IterBudget", "value": 500},
     "body": {
       "type": "Seq",
       "body": [
         {"type": "Call", "name": "RandomRecolor", "args": {"ratio": 0.2}},
         {"type": "ApplyUntilNoImprove",
          "stmt": {"type": "Call", "name": "OneVertexMove"},
          "stop": {"type": "Stagnation", "iters": 5}
         },
         {"type": "If", "cond": {"type": "Improves"},
          "then": {"type": "Call", "name": "Intensify"},
          "else": {"type": "Call", "name": "PartialDestroy"}
         }
       ]
     }
    }
  ]
}
```

## Plan Experimental

**Variables independientes**:
- Algoritmos ILS generados por GAA (variaciones de AST)
- Configuraciones de perturbación (ratio)

**Variables dependientes**:
- Número de colores obtenido (k)
- Tiempo de ejecución
- Gap respecto a mejor conocido (best known)

**Instancias**:
- Diversas estructuras de grafos (aleatorios, bipartitos, planares, etc.)

**Réplicas**: 30 ejecuciones por configuración (ILS es estocástico)

**Análisis estadístico**:
- Test de Friedman para comparación múltiple
- Post-hoc: Nemenyi test
- Nivel de significancia: α = 0.05

---

## 📚 Referencias Bibliográficas

- [Brelaz1979] Brélaz, D. (1979). New methods to color the vertices of a graph. Communications of the ACM, 22(4), 251-256.
- [Welsh1967] Welsh, D. J., & Powell, M. B. (1967). An upper bound for the chromatic number of a graph. Computer Journal, 10(1), 85-86.
- [Hertz1987] Hertz, A., & de Werra, D. (1987). Using tabu search techniques for graph coloring. Computing, 39(4), 345-351.
- [Lourenco2003] Lourenço, H. R., Martin, O. C., & Stützle, T. (2003). Iterated local search. Handbook of metaheuristics, 320-353.
- [Galinier1999] Galinier, P., & Hao, J. K. (1999). Hybrid evolutionary algorithms for graph coloring. Journal of Combinatorial Optimization, 3(4), 379-397.

---

## ✅ Estado del Proyecto

- [x] Problema definido (GCP)
- [x] Modelo matemático formalizado
- [x] Operadores del dominio identificados (15 terminales)
- [x] Metaheurística seleccionada (ILS)
- [x] Parámetros configurados
- [ ] Datasets agregados (benchmarks DIMACS recomendados)
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados
