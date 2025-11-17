---
gaa_metadata:
  version: 1.0.0
  project_name: "VRPTW con GRASP"
  problem: "Vehicle Routing Problem with Time Windows"
  metaheuristic: "GRASP"
  status: "active"
  created: "2025-11-17"
---

# Proyecto: VRPTW con GRASP

## 🎯 Información del Proyecto

**Problema**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Metaheurística**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Objetivo**: Generar algoritmos automáticamente mediante GAA para resolver instancias de ruteo de vehículos con ventanas de tiempo

---

# PARTE 1: DEFINICIÓN DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Vehicle Routing Problem with Time Windows (VRPTW)  
**Tipo**: Minimización  
**Categoría**: Combinatorial Optimization - NP-Hard

## Descripción Informal

El problema de ruteo de vehículos con ventanas de tiempo (VRPTW) consiste en diseñar rutas óptimas para una flota de vehículos que deben atender un conjunto de clientes desde un depósito central. Cada cliente tiene:
- Una demanda de producto
- Una ventana de tiempo [a_i, b_i] durante la cual debe ser visitado
- Un tiempo de servicio s_i

Los vehículos tienen capacidad limitada y deben respetar las ventanas de tiempo de los clientes.

**Aplicaciones**:
- Logística de distribución urbana
- Ruteo de vehículos de transporte escolar
- Servicios de mensajería y paquetería
- Distribución de alimentos y bebidas
- Servicios de mantenimiento programado

## Mathematical-Model

### Función Objetivo

```math
\text{Minimizar: } Z = \sum_{k=1}^{K} \sum_{i=0}^{n} \sum_{j=0}^{n} c_{ij} x_{ijk}
```

Donde:
- c_{ij} = costo (distancia o tiempo) de viajar del nodo i al nodo j
- x_{ijk} = 1 si el vehículo k viaja directamente de i a j, 0 en otro caso

### Restricciones

**1. Asignación de clientes**:
```math
\sum_{k=1}^{K} \sum_{j=1}^{n} x_{ijk} = 1, \quad \forall i \in \{1, \ldots, n\}
```

**2. Conservación de flujo**:
```math
\sum_{i=0}^{n} x_{ijk} - \sum_{j=0}^{n} x_{jik} = 0, \quad \forall k, \forall i
```

**3. Capacidad del vehículo**:
```math
\sum_{i=1}^{n} q_i \sum_{j=0}^{n} x_{ijk} \leq Q, \quad \forall k
```

**4. Ventanas de tiempo**:
```math
a_i \leq w_{ik} \leq b_i, \quad \forall i, k
```

```math
w_{ik} + s_i + t_{ij} \leq w_{jk} + M(1 - x_{ijk}), \quad \forall i,j,k
```

### Variables de Decisión

- **x_{ijk}**: Variable binaria (ruta del vehículo k entre i y j)
- **w_{ik}**: Tiempo de inicio de servicio del vehículo k en el cliente i
- **n**: Número de clientes
- **K**: Número de vehículos disponibles
- **Q**: Capacidad de cada vehículo
- **q_i**: Demanda del cliente i
- **[a_i, b_i]**: Ventana de tiempo del cliente i
- **s_i**: Tiempo de servicio del cliente i
- **t_{ij}**: Tiempo de viaje entre i y j

## Domain-Operators

### Terminales Identificados

#### Constructivos
- **SavingsHeuristic**: Heurística de ahorros de Clarke-Wright [Clarke1964]
- **NearestNeighbor**: Vecino más cercano con consideración de tiempo [Solomon1987]
- **InsertionI1**: Inserción secuencial minimizando costo adicional [Solomon1987]
- **TimeOrientedNN**: Vecino más cercano priorizando urgencia temporal [Potvin1996]
- **RegretInsertion**: Inserción por arrepentimiento (diferencia entre mejor y segunda mejor posición) [Ropke2006]
- **RandomizedInsertion**: Inserción con componente aleatoria (GRASP-style) [Kontoravdis1995]

#### Mejora Local - Intra-ruta
- **TwoOpt**: Mejora 2-opt dentro de una ruta [Lin1965]
- **OrOpt**: Reubicación de secuencias de 1, 2 o 3 clientes [Or1976]
- **ThreeOpt**: Mejora 3-opt (más intensiva) [Lin1965]
- **Relocate**: Mover un cliente a otra posición en la misma ruta [Savelsbergh1992]

#### Mejora Local - Inter-ruta
- **CrossExchange**: Intercambio de segmentos entre rutas [Taillard1997]
- **TwoOptStar**: 2-opt* entre dos rutas diferentes [Potvin1996]
- **SwapCustomers**: Intercambio de clientes entre rutas [Bräysy2005]
- **Relocate Inter**: Mover cliente de una ruta a otra [Pisinger2007]

#### Perturbación
- **EjectionChain**: Cadenas de eyección de clientes [Glover1996]
- **RuinRecreate**: Destruye parcialmente rutas y reconstruye [Schrimpf2000]
- **RandomRemoval**: Remoción aleatoria de k clientes y reinserción [Shaw1998]
- **RouteElimination**: Elimina una ruta completa y redistribuye clientes [Nagata2010]

#### Reparación
- **RepairCapacity**: Repara violaciones de capacidad removiendo clientes [Bräysy2005]
- **RepairTimeWindows**: Ajusta rutas para cumplir ventanas de tiempo [Potvin1996]
- **GreedyRepair**: Reconstrucción voraz tras destrucción [Pisinger2007]

## Solution-Representation

**Estructura de datos**:
```python
# Lista de rutas, cada ruta es una secuencia de clientes
routes = [
    [0, c1, c3, c5, 0],  # Ruta 1: depósito → c1 → c3 → c5 → depósito
    [0, c2, c4, 0],       # Ruta 2: depósito → c2 → c4 → depósito
    [0, c6, c7, c8, 0]    # Ruta 3: depósito → c6 → c7 → c8 → depósito
]
```

**Ejemplo**:
```
Instancia: 8 clientes, 3 vehículos, Q=100

Solución:
Route 1: 0 → 1(q=30) → 3(q=25) → 5(q=20) → 0  [Carga total: 75]
Route 2: 0 → 2(q=40) → 4(q=35) → 0             [Carga total: 75]
Route 3: 0 → 6(q=15) → 7(q=20) → 8(q=10) → 0  [Carga total: 45]

Costo total: 245.6 unidades
Violaciones: 0 (factible)
```

## Constraints

**Restricciones duras**:
1. **Capacidad**: La demanda acumulada en cada ruta no debe exceder Q
2. **Ventanas de tiempo**: Cada cliente debe ser visitado dentro de su ventana [a_i, b_i]
3. **Cobertura**: Todos los clientes deben ser visitados exactamente una vez
4. **Depósito**: Todas las rutas inician y terminan en el depósito (nodo 0)

**Restricciones blandas** (pueden penalizarse):
- Minimizar número de vehículos utilizados
- Balancear carga entre vehículos

**Parámetros del problema**:
- **n**: Número de clientes
- **K**: Número de vehículos disponibles
- **Q**: Capacidad de vehículos
- **q_i**: Demanda del cliente i
- **[a_i, b_i]**: Ventana de tiempo del cliente i
- **s_i**: Tiempo de servicio del cliente i
- **c_{ij}**: Matriz de distancias/tiempos
- **(x_i, y_i)**: Coordenadas geográficas del cliente i

## Evaluation-Criteria

**Métrica principal**: Distancia total recorrida (o costo total)  
**Métricas secundarias**:
- Número de vehículos utilizados
- Violaciones de ventanas de tiempo
- Violaciones de capacidad

**Criterio de comparación**: Menor es mejor  

**Manejo de infactibilidad**:
```python
def evaluate(solution):
    total_distance = sum_route_distances(solution)
    capacity_violations = sum_capacity_excess(solution)
    time_violations = sum_time_window_violations(solution)
    
    # Penalizaciones
    penalty = 1000 * capacity_violations + 1000 * time_violations
    
    return total_distance + penalty
```

**Métrica jerárquica** (lexicográfica):
1. Minimizar violaciones (factibilidad)
2. Minimizar número de vehículos
3. Minimizar distancia total

---

# PARTE 2: METAHEURÍSTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Greedy Randomized Adaptive Search Procedure (GRASP)  
**Tipo**: Metaheurística constructiva con búsqueda local  
**Referencia**: [Feo1995, Resende2009]

## Descripción del Método

GRASP es una metaheurística iterativa de dos fases:
1. **Fase Constructiva**: Construcción voraz aleatoria (greedy randomized)
   - En cada paso, selecciona aleatoriamente de entre las mejores opciones (RCL - Restricted Candidate List)
   - Balancea voracidad y aleatoriedad

2. **Fase de Búsqueda Local**: Mejora la solución construida
   - Aplica operadores de mejora hasta alcanzar óptimo local

**Ventajas para GAA en VRPTW**:
- Combina construcción y mejora (dos pilares del diseño de heurísticas)
- Parámetro α controla balance entre voracidad y aleatoriedad
- Efectivo para problemas de ruteo
- Genera soluciones diversas en cada iteración

## Configuration

**Parámetros principales**:

```yaml
max_iteraciones: 100
alpha: 0.15                    # Parámetro RCL: 0=voraz, 1=aleatorio
tamaño_rcl: null               # Alternativa: usar tamaño fijo de RCL
tipo_mejora: "VND"             # Variable Neighborhood Descent
max_sin_mejora: 20             # Criterio de parada adicional
```

**Parámetros del RCL (Restricted Candidate List)**:
```python
# Opción 1: Por valor (alpha-based)
threshold = c_min + alpha * (c_max - c_min)
RCL = {i : c_i <= threshold}

# Opción 2: Por tamaño (size-based)
RCL = {top k candidatos según costo}
```

**Justificación**:
- 100 iteraciones: Diversidad suficiente
- α=0.15: Balance entre voracidad (0) y aleatoriedad (1)
- VND: Variable Neighborhood Descent para búsqueda local exhaustiva

## Search-Strategy

### Operadores de Búsqueda sobre AST

**Mutación de Nodo Función**:
- Cambiar tipo de bucle o estructura de control
- Ejemplo: `ChooseBestOf(5, Construct)` → `For(10, Construct)`
- Probabilidad: 0.20

**Mutación de Terminal**:
- Cambiar heurística constructiva
- Ejemplo: `SavingsHeuristic` → `RegretInsertion`
- Cambiar operador de mejora local
- Ejemplo: `TwoOpt` → `OrOpt`
- Probabilidad: 0.60

**Mutación de Parámetro**:
- Modificar α (parámetro RCL)
- Modificar k en operadores paramétricos
- Perturbación: ±10%
- Probabilidad: 0.20

### Estructura Típica de GRASP

```python
def GRASP():
    s_best = None
    f_best = infinity
    
    for iter in range(max_iterations):
        # Fase Constructiva (Greedy Randomized)
        s = GreedyRandomizedConstruction(alpha)
        
        # Fase de Búsqueda Local
        s = LocalSearch(s)
        
        # Actualizar mejor solución
        if f(s) < f_best:
            s_best = s
            f_best = f(s)
    
    return s_best
```

### Construcción Voraz Aleatoria

```python
def GreedyRandomizedConstruction(alpha):
    solution = initialize_empty_routes()
    unrouted = all_customers.copy()
    
    while unrouted:
        # Evaluar costos de inserción
        costs = evaluate_insertion_costs(unrouted, solution)
        c_min, c_max = min(costs), max(costs)
        
        # Construir RCL
        threshold = c_min + alpha * (c_max - c_min)
        RCL = [i for i in unrouted if costs[i] <= threshold]
        
        # Seleccionar aleatoriamente de RCL
        selected = random.choice(RCL)
        
        # Insertar en mejor posición
        insert_customer(selected, solution)
        unrouted.remove(selected)
    
    return solution
```

### Búsqueda Local (VND)

```python
def VariableNeighborhoodDescent(solution):
    neighborhoods = [TwoOpt, OrOpt, Relocate, SwapCustomers]
    k = 0
    
    while k < len(neighborhoods):
        s_new = neighborhoods[k](solution)
        
        if f(s_new) < f(solution):
            solution = s_new
            k = 0  # Reiniciar desde primer vecindario
        else:
            k += 1  # Pasar al siguiente vecindario
    
    return solution
```

## Presupuesto Computacional

**Criterio de parada**:
- [x] Número de iteraciones GRASP: 100
- [x] Iteraciones sin mejora: 20
- [ ] Tiempo límite: N/A
- [ ] Óptimo conocido alcanzado: Opcional

**Presupuesto por evaluación de AST**:
- Iteraciones GRASP por instancia: 100
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~60 segundos (VRPTW es más costoso)

## AST-Specific Considerations

**Validación de AST**:
- Validar gramática después de mutación: Sí
- Reparación automática de AST inválidos: Sí
- Profundidad máxima del árbol: 10

**Inicialización**:
- Método: Ramped Half-and-Half (combinación de Full y Grow)
- Profundidad inicial: 4-7
- Población inicial de AST: 1 (GRASP es single-solution por iteración)

**Operadores obligatorios en AST para GRASP**:
- Al menos un constructor randomizado
- Al menos dos operadores de mejora local (para VND)
- Reparación de restricciones

---

# PARTE 3: DATASETS

## Ubicación de Datasets

```
projects/VRPTW-GRASP/datasets/
├── training/          # Instancias para optimizar AST
│   └── [Archivos .txt]
├── validation/        # Instancias para ajustar parámetros
│   └── [Archivos .txt]
└── test/              # Instancias para evaluación final
    └── [Archivos .txt]
```

## Formato de Archivo de Instancia

**Formato Solomon** (estándar VRPTW):
```
VEHICLE
NUMBER     CAPACITY
  K          Q

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
    0       x0        y0          0         0          T            0
    1       x1        y1         q1        a1         b1           s1
    2       x2        y2         q2        a2         b2           s2
    ...
```

**Ejemplo** (Solomon R101 - extracto):
```
VEHICLE
NUMBER     CAPACITY
  25         200

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME

    0      35       35          0          0       230           0   
    1      41       49         10        161       171          10   
    2      35       17          7         50        60          10   
    3      55       45         13        116       126          10   
```

## Datasets Recomendados

**Benchmarks clásicos de VRPTW**:

1. **Solomon Instances** (1987):
   - Tipo R: Clientes distribuidos aleatoriamente
   - Tipo C: Clientes en clusters
   - Tipo RC: Mezcla de aleatorio y clusters
   - Tamaños: R101, R102, ..., RC108 (25-100 clientes)

2. **Gehring & Homberger** (1999):
   - Extensión de Solomon para instancias grandes
   - Tamaños: 200, 400, 600, 800, 1000 clientes

3. **Homberger & Gehring** (2005):
   - Instancias con diferentes horizontes temporales

**Fuentes**:
- Solomon: http://web.cba.neu.edu/~msolomon/problems.htm
- Gehring & Homberger: http://www.sintef.no/projectweb/top/vrptw/

**Sugerencias para el proyecto**:
- **Training**: 5 instancias Solomon pequeñas (R101, C101, RC101, R201, C201)
- **Validation**: 3 instancias medianas
- **Test**: 5-8 instancias variadas

---

# PARTE 4: GENERACIÓN Y EXPERIMENTACIÓN

## Algoritmo Generado

El sistema GAA generará algoritmos GRASP representados como AST combinando:
- **Funciones**: `Seq`, `For`, `ChooseBestOf`, `ApplyUntilNoImprove`, `LocalSearch`
- **Terminales**: Los 22 operadores identificados en Domain-Operators

**Ejemplo de AST para GRASP**:
```json
{
  "type": "ChooseBestOf",
  "n": 100,
  "stmt": {
    "type": "Seq",
    "body": [
      {
        "type": "Call",
        "name": "RandomizedInsertion",
        "args": {"alpha": 0.15}
      },
      {
        "type": "Seq",
        "body": [
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "TwoOpt"},
            "stop": {"type": "Stagnation", "iters": 5}
          },
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "OrOpt"},
            "stop": {"type": "Stagnation", "iters": 5}
          },
          {
            "type": "ApplyUntilNoImprove",
            "stmt": {"type": "Call", "name": "SwapCustomers"},
            "stop": {"type": "Stagnation", "iters": 3}
          }
        ]
      }
    ]
  }
}
```

## Plan Experimental

**Variables independientes**:
- Algoritmos GRASP generados por GAA
- Parámetro α (puede ser ajustado por el AST)
- Conjunto de operadores de mejora local

**Variables dependientes**:
- Distancia total
- Número de vehículos utilizados
- Tiempo de ejecución
- Gap respecto a best known solutions

**Comparación**:
- Contra best known solutions (BKS) de Solomon
- Contra algoritmos GRASP de referencia
- Entre algoritmos generados por GAA

**Réplicas**: 30 ejecuciones por configuración (GRASP es estocástico)

**Análisis estadístico**:
- Test de Kruskal-Wallis para comparación múltiple
- Análisis de convergencia
- Trade-off calidad vs tiempo
- Nivel de significancia: α = 0.05

---

## 📚 Referencias Bibliográficas

- [Solomon1987] Solomon, M. M. (1987). Algorithms for the vehicle routing and scheduling problems with time window constraints. Operations Research, 35(2), 254-265.
- [Clarke1964] Clarke, G., & Wright, J. W. (1964). Scheduling of vehicles from a central depot to a number of delivery points. Operations Research, 12(4), 568-581.
- [Feo1995] Feo, T. A., & Resende, M. G. (1995). Greedy randomized adaptive search procedures. Journal of Global Optimization, 6(2), 109-133.
- [Resende2009] Resende, M. G., & Ribeiro, C. C. (2009). Greedy randomized adaptive search procedures. Handbook of Metaheuristics, 219-249.
- [Ropke2006] Ropke, S., & Pisinger, D. (2006). An adaptive large neighborhood search heuristic for the pickup and delivery problem with time windows. Transportation Science, 40(4), 455-472.
- [Bräysy2005] Bräysy, O., & Gendreau, M. (2005). Vehicle routing problem with time windows, Part I & II. Transportation Science, 39(1-2).

---

## ✅ Estado del Proyecto

- [x] Problema definido (VRPTW)
- [x] Modelo matemático formalizado
- [x] Operadores del dominio identificados (22 terminales)
- [x] Metaheurística seleccionada (GRASP)
- [x] Parámetros configurados
- [ ] Datasets agregados (Solomon instances recomendados)
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados

---

## 💡 Notas Adicionales

**Consideraciones de implementación**:
- El cálculo de distancias puede ser Euclidiano o basado en matriz
- Las ventanas de tiempo pueden requerir espera (arrival antes de a_i)
- La evaluación de inserción debe considerar impacto en tiempo de rutas completas
- Reparación de restricciones es crítica para mantener factibilidad

**Extensiones posibles**:
- VRPTW con flota heterogénea
- Múltiples depósitos
- Backhauls (recogidas y entregas)
- Demandas estocásticas
