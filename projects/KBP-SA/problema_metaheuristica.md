---
gaa_metadata:
  version: 1.0.0
  project_name: "KBP con Simulated Annealing"
  problem: "Knapsack Problem"
  metaheuristic: "Simulated Annealing"
  status: "active"
  created: "2025-11-17"
---

# Proyecto: Knapsack Problem con Simulated Annealing

## 🎯 Información del Proyecto

**Problema**: Knapsack Problem (KBP)  
**Metaheurística**: Simulated Annealing (SA)  
**Objetivo**: Generar algoritmos automáticamente mediante GAA para resolver instancias del problema de la mochila

---

# PARTE 1: DEFINICIÓN DEL PROBLEMA

## Problema Seleccionado

**Nombre**: Knapsack Problem (KBP)  
**Tipo**: Maximización  
**Categoría**: Combinatorial Optimization - NP-Hard

## Descripción Informal

El problema de la mochila (Knapsack Problem) consiste en seleccionar un subconjunto de ítems, cada uno con un valor y un peso asociado, de manera que se maximice el valor total de los ítems seleccionados sin exceder la capacidad de peso de la mochila.

**Aplicaciones**:
- Asignación de recursos con restricción presupuestaria
- Selección de proyectos de inversión
- Carga de contenedores
- Planificación de producción

## Mathematical-Model

### Función Objetivo

```math
\text{Maximizar: } Z = \sum_{i=1}^{n} v_i x_i
```

### Restricciones

```math
\text{Sujeto a: } \sum_{i=1}^{n} w_i x_i \leq W
```

```math
x_i \in \{0,1\}, \quad \forall i = 1, \ldots, n
```

### Variables de Decisión

- **x_i**: Variable binaria que indica si el ítem i es seleccionado (1) o no (0)
- **n**: Número total de ítems disponibles
- **v_i**: Valor del ítem i
- **w_i**: Peso del ítem i
- **W**: Capacidad máxima de la mochila

## Domain-Operators

### Terminales Identificados

#### Constructivos
- **GreedyByValue**: Construcción voraz insertando ítems por valor decreciente [Dantzig1957]
- **GreedyByWeight**: Construcción voraz insertando ítems por peso creciente [Martello1990]
- **GreedyByRatio**: Construcción voraz por ratio valor/peso decreciente [Pisinger2005]
- **RandomConstruct**: Construcción aleatoria respetando capacidad [Khuri1994]

#### Mejora Local
- **FlipBestItem**: Mejora local cambiando estado del ítem que más mejore la solución [Martello1999]
- **FlipWorstItem**: Remueve el ítem con peor contribución (menor ratio v/w) [Pisinger2007]
- **OneExchange**: Intercambia un ítem dentro por uno fuera si mejora [Kellerer2004]
- **TwoExchange**: Intercambia dos ítems simultáneamente [Vazirani2001]

#### Perturbación
- **RandomFlip**: Cambia aleatoriamente el estado de k ítems [Glover1998]
- **ShakeByRemoval**: Remueve aleatoriamente k ítems de la mochila [Lourenco2003]
- **DestroyRepair**: Destruye porción de solución y reconstruye vorazmente [Shaw1998]

#### Reparación
- **RepairByRemoval**: Elimina ítems hasta que sea factible (comenzando por menor ratio) [Chu1998]
- **RepairByGreedy**: Reconstrucción voraz tras destrucción [Pisinger1999]

## Solution-Representation

**Estructura de datos**:
```python
# Vector binario de longitud n
x = [x_1, x_2, ..., x_n]
# donde x_i ∈ {0, 1}
# 1 = ítem i está en la mochila
# 0 = ítem i NO está en la mochila
```

**Ejemplo**:
```
Instancia: n=5, W=10
Items: [(v=10,w=5), (v=8,w=4), (v=6,w=3), (v=5,w=2), (v=4,w=1)]
Solución: x = [1, 0, 1, 1, 0]
Interpretación: Ítems 1, 3 y 4 seleccionados
Peso total: 5+3+2 = 10
Valor total: 10+6+5 = 21
```

## Constraints

**Restricciones duras**:
1. **Capacidad**: La suma de pesos de ítems seleccionados no debe exceder W
2. **Binariedad**: Cada ítem se selecciona exactamente 0 o 1 vez (no fraccionamiento)

**Parámetros del problema**:
- **n**: Número de ítems (tamaño de la instancia)
- **W**: Capacidad de la mochila
- **v**: Vector de valores [v_1, ..., v_n]
- **w**: Vector de pesos [w_1, ..., w_n]

## Evaluation-Criteria

**Métrica principal**: Valor total de los ítems seleccionados  
**Criterio de comparación**: Mayor es mejor  
**Manejo de infactibilidad**: 
- Penalización: fitness = -∞ para soluciones que excedan W
- Reparación: aplicar RepairByRemoval antes de evaluar

---

# PARTE 2: METAHEURÍSTICA SELECCIONADA

## Selected-Metaheuristic

**Algoritmo**: Simulated Annealing (SA)  
**Tipo**: Local Search con aceptación probabilística  
**Referencia**: [Kirkpatrick1983, Cerny1985]

## Descripción del Método

Simulated Annealing es una metaheurística inspirada en el proceso de enfriamiento de metales. Comienza con una temperatura alta que permite aceptar soluciones de peor calidad con alta probabilidad, y gradualmente disminuye la temperatura, haciendo la búsqueda más restrictiva. Esto permite escapar de óptimos locales en las etapas iniciales.

**Ventajas para GAA**:
- Simple de implementar sobre AST
- Pocos hiperparámetros
- Balance entre intensificación y diversificación
- Bien estudiado en literatura de KBP

## Configuration

**Parámetros principales**:

```yaml
temperatura_inicial: 100.0
temperatura_final: 0.01
factor_enfriamiento: 0.95
iteraciones_por_temperatura: 100
criterio_parada: temperatura < temperatura_final
```

**Justificación**:
- T₀=100: Permite exploración inicial amplia
- α=0.95: Enfriamiento geométrico estándar
- L=100: Balance entre calidad y tiempo
- Tf=0.01: Convergencia suficiente

## Search-Strategy

### Operadores de Búsqueda sobre AST

**Mutación de Nodo Función**:
- Reemplazar un nodo función (e.g., `If`) por otro compatible (e.g., `While`)
- Probabilidad: 0.3

**Mutación de Terminal**:
- Cambiar un terminal por otro del dominio KBP
- Ejemplo: `GreedyByValue` → `GreedyByRatio`
- Probabilidad: 0.5

**Mutación de Parámetro**:
- Modificar parámetros numéricos (e.g., k en RandomFlip)
- Perturbación: ±20%
- Probabilidad: 0.2

### Acceptance-Criteria

**Criterio Metropolis**:

```python
def accept(current_fitness, new_fitness, temperature):
    if new_fitness > current_fitness:
        return True  # Siempre acepta mejora
    else:
        delta_E = new_fitness - current_fitness
        probability = exp(delta_E / temperature)
        return random() < probability
```

**Esquema de Enfriamiento**:
```python
T_{k+1} = α * T_k
```

## Presupuesto Computacional

**Criterio de parada**:
- [x] Temperatura límite: T < 0.01
- [x] Número máximo de temperaturas: 200
- [ ] Tiempo límite: N/A
- [ ] Convergencia: N/A

**Presupuesto por evaluación de AST**:
- Evaluaciones por instancia: 1000
- Instancias de entrenamiento: 5-10
- Tiempo estimado por AST: ~30 segundos

## AST-Specific Considerations

**Validación de AST**:
- Validar gramática después de mutación: Sí
- Reparación automática de AST inválidos: Sí
- Profundidad máxima del árbol: 8

**Inicialización**:
- Método: Random (generación aleatoria válida)
- Profundidad inicial: 3-5
- Población inicial de AST: 1 (SA es single-solution)

---

# PARTE 3: DATASETS

## Ubicación de Datasets

```
projects/KBP-SA/datasets/
├── training/          # Instancias para optimizar AST
│   └── [Usuario debe proporcionar archivos .txt]
├── validation/        # Instancias para ajustar parámetros SA
│   └── [Usuario debe proporcionar archivos .txt]
└── test/              # Instancias para evaluación final
    └── [Usuario debe proporcionar archivos .txt]
```

## Formato de Archivo de Instancia

```
n W
v_1 w_1
v_2 w_2
...
v_n w_n
```

**Ejemplo** (`knapsack_10_269.txt`):
```
10 269
55 95
10 4
47 60
5 32
4 23
50 72
8 80
61 62
85 65
87 46
```

## Instrucciones para el Usuario

**Por favor, proporciona tus instancias en el formato indicado arriba**:

1. Coloca archivos `.txt` en `datasets/training/` (5-10 instancias)
2. Coloca archivos `.txt` en `datasets/validation/` (3-5 instancias)
3. Coloca archivos `.txt` en `datasets/test/` (5-10 instancias)

**Fuentes recomendadas**:
- Pisinger's benchmark: http://hjemmesider.diku.dk/~pisinger/
- OR-Library: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/
- Instancias propias

---

# PARTE 4: GENERACIÓN Y EXPERIMENTACIÓN

## Algoritmo Generado

El sistema GAA generará algoritmos representados como AST combinando:
- **Funciones**: `Seq`, `If`, `While`, `For`, `LocalSearch`, `GreedyConstruct`
- **Terminales**: Los 13 operadores identificados en Domain-Operators

**Ejemplo de AST**:
```json
{
  "type": "Seq",
  "body": [
    {"type": "GreedyConstruct", "heuristic": "GreedyByRatio"},
    {"type": "While", "budget": {"kind": "IterBudget", "value": 100},
     "body": {
       "type": "If",
       "cond": {"type": "Improves"},
       "then": {"type": "Call", "name": "OneExchange"},
       "else": {"type": "Call", "name": "RandomFlip", "args": {"k": 2}}
     }
    }
  ]
}
```

## Plan Experimental

**Variables independientes**:
- Algoritmos generados por GAA (población de AST)

**Variables dependientes**:
- Calidad de solución (valor total)
- Tiempo de ejecución
- Gap respecto a óptimo conocido (si disponible)

**Réplicas**: 30 ejecuciones por configuración

**Análisis estadístico**:
- Prueba de Wilcoxon para comparación pareada
- Nivel de significancia: α = 0.05

---

## 📚 Referencias Bibliográficas

- [Dantzig1957] Dantzig, G. B. (1957). Discrete-variable extremum problems. Operations Research, 5(2), 266-277.
- [Martello1990] Martello, S., & Toth, P. (1990). Knapsack problems: algorithms and computer implementations. John Wiley & Sons.
- [Pisinger2005] Pisinger, D. (2005). Where are the hard knapsack problems?. Computers & Operations Research, 32(9), 2271-2284.
- [Kirkpatrick1983] Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by simulated annealing. Science, 220(4598), 671-680.
- [Kellerer2004] Kellerer, H., Pferschy, U., & Pisinger, D. (2004). Knapsack problems. Springer.

---

## ✅ Estado del Proyecto

- [x] Problema definido (KBP)
- [x] Modelo matemático formalizado
- [x] Operadores del dominio identificados (13 terminales)
- [x] Metaheurística seleccionada (SA)
- [x] Parámetros configurados
- [ ] Datasets proporcionados por usuario
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados
