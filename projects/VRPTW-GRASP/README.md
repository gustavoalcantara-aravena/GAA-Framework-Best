# Proyecto: VRPTW-GRASP

## Vehicle Routing Problem with Time Windows con GRASP

**Estado**: ⏳ En configuración  
**Problema**: VRPTW (Vehicle Routing Problem with Time Windows)  
**Metaheurística**: GRASP (Greedy Randomized Adaptive Search Procedure)

---

## 📁 Estructura del Proyecto

```
VRPTW-GRASP/
├── problema_metaheuristica.md    # Especificación completa del proyecto
├── datasets/
│   ├── training/                 # Instancias Solomon para entrenamiento
│   ├── validation/               # Instancias para validación
│   └── test/                     # Instancias para evaluación final
└── generated/                    # Scripts Python generados (auto)
```

---

## 🚀 Inicio Rápido

### 1. Agregar Datasets

**Formato Solomon**:
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

### 2. Benchmarks Recomendados

**Solomon Instances** (1987):
- **Tipo R**: Clientes distribuidos aleatoriamente (R101, R102, ..., R112)
- **Tipo C**: Clientes agrupados en clusters (C101, C102, ..., C109)
- **Tipo RC**: Mezcla (RC101, RC102, ..., RC108)

**Series**:
- **100-series**: Horizontes de tiempo cortos (más difícil)
- **200-series**: Horizontes de tiempo largos (más fácil)

**Descarga**: http://web.cba.neu.edu/~msolomon/problems.htm

**Sugerencias para el proyecto**:
- **Training**: R101, C101, RC101, R201, C201 (5 instancias)
- **Validation**: R102, C102, RC102 (3 instancias)
- **Test**: R103, R104, C103, C104, RC103, RC104, R202, C202 (8 instancias)

### 3. Revisar Configuración

Ver archivo completo: `problema_metaheuristica.md`

**Terminales disponibles** (22 operadores):

**Constructivos**:
- SavingsHeuristic, NearestNeighbor, InsertionI1, TimeOrientedNN, RegretInsertion, RandomizedInsertion

**Mejora Intra-ruta**:
- TwoOpt, OrOpt, ThreeOpt, Relocate

**Mejora Inter-ruta**:
- CrossExchange, TwoOptStar, SwapCustomers, RelocateInter

**Perturbación**:
- EjectionChain, RuinRecreate, RandomRemoval, RouteElimination

**Reparación**:
- RepairCapacity, RepairTimeWindows, GreedyRepair

**Parámetros GRASP**:
- Max iteraciones: 100
- Alpha (RCL): 0.15
- Búsqueda local: VND (Variable Neighborhood Descent)

### 4. Generar Scripts

```bash
cd ../../
python 05-Automation/sync-engine.py --sync-project projects/VRPTW-GRASP
python 05-Automation/sync-engine.py --generate-project projects/VRPTW-GRASP
```

### 5. Ejecutar Experimentos

```bash
cd generated
python main.py --mode train --instances ../datasets/training/
python main.py --mode test --instances ../datasets/test/ --replicas 30
```

---

## 📊 Métricas de Evaluación

### Primaria
**Distancia total recorrida**: Σ(distancias de todas las rutas)

### Secundarias
- Número de vehículos utilizados
- Violaciones de ventanas de tiempo
- Violaciones de capacidad
- Tiempo de ejecución

### Función de Fitness
```python
fitness = distancia_total + 1000 * (violaciones_capacidad + violaciones_tiempo)
```

### Comparación
- **Best Known Solutions (BKS)** de Solomon
- **Gap = (solución - BKS) / BKS * 100**

---

## 📈 Resultados Esperados

**Solomon Instances - Best Known Solutions**:

| Instancia | BKS Vehículos | BKS Distancia |
|-----------|---------------|---------------|
| R101      | 19            | 1650.80       |
| C101      | 10            | 828.94        |
| RC101     | 14            | 1696.95       |
| R201      | 4             | 1252.37       |
| C201      | 3             | 591.56        |

**Objetivo**: Generar algoritmos que se acerquen a estos valores

---

## ✅ Checklist

- [ ] Datasets Solomon descargados
- [ ] Datasets organizados en `datasets/training/`, `validation/`, `test/`
- [ ] Especificación revisada en `problema_metaheuristica.md`
- [ ] Scripts generados
- [ ] Experimentos ejecutados (30 réplicas por instancia)
- [ ] Gap vs BKS calculado
- [ ] Análisis estadístico completado
- [ ] Resultados documentados

---

## 📝 Notas Importantes

**Consideraciones de implementación**:
- Las distancias pueden calcularse como euclidianas o según matriz
- Ventanas de tiempo: Permitir espera si se llega antes de `a_i`
- Capacidad: Acumular demandas y verificar contra `Q`
- Depósito: Siempre es el nodo 0

**Validación de soluciones**:
```python
def validate_solution(routes, instance):
    # 1. Todos los clientes visitados exactamente una vez
    # 2. Capacidad respetada en cada ruta
    # 3. Ventanas de tiempo respetadas
    # 4. Todas las rutas inician y terminan en depósito (0)
```

**Complejidad**:
- VRPTW es más complejo que KBP y GCP
- Evaluación de soluciones es más costosa (verificar restricciones múltiples)
- Búsqueda local requiere más tiempo (operadores inter-ruta)

---

## 🔗 Referencias Útiles

- **Solomon Benchmark**: http://web.cba.neu.edu/~msolomon/problems.htm
- **Gehring & Homberger** (instancias grandes): http://www.sintef.no/projectweb/top/vrptw/
- **VRP Web**: http://www.bernabe.dorronsoro.es/vrp/

---

Este proyecto forma parte del framework GAA (Generación Automática de Algoritmos).
Ver documentación principal en: `../../GAA-Agent-System-Prompt.md`
