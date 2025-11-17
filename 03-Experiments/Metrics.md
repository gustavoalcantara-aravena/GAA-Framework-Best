---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
  auto_sync: true
---

# Definición de Métricas

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md`.

## Métricas de Calidad

### Métrica Principal

<!-- AUTO-GENERATED from 00-Core/Problem.md::Evaluation-Criteria -->
**Métrica**: [Pendiente de extracción]  
**Objetivo**: [Maximizar | Minimizar]  
**Rango**: [min, max]
<!-- END AUTO-GENERATED -->

### Métricas Secundarias

- **Tasa de factibilidad**: Porcentaje de soluciones factibles generadas
- **Diversidad**: Medida de variabilidad en el conjunto de soluciones

## Métricas de Eficiencia

### Tiempo Computacional

```python
def measure_time(algorithm, instance):
    import time
    start = time.time()
    solution = algorithm.run(instance)
    elapsed = time.time() - start
    return elapsed
```

### Número de Evaluaciones

```python
def count_evaluations(context):
    return context.num_evaluations
```

## Métricas de Convergencia

### Progreso

```python
def convergence_rate(fitness_history):
    """Tasa de mejora por iteración"""
    improvements = [fitness_history[i+1] - fitness_history[i] 
                   for i in range(len(fitness_history)-1)]
    return sum(improvements) / len(improvements)
```

### Estancamiento

```python
def stagnation_count(fitness_history, tolerance=1e-6):
    """Número de iteraciones sin mejora significativa"""
    count = 0
    for i in range(1, len(fitness_history)):
        if abs(fitness_history[i] - fitness_history[i-1]) < tolerance:
            count += 1
    return count
```

## Métricas Comparativas

### Gap con Óptimo

```python
def compute_gap(obtained, optimal):
    """Gap porcentual respecto al óptimo conocido"""
    return abs(optimal - obtained) / abs(optimal) * 100
```

### Ranking

```python
def compute_ranking(results):
    """Asigna ranking a cada algoritmo por instancia"""
    rankings = []
    for instance_results in results:
        sorted_algs = sorted(instance_results.items(), 
                           key=lambda x: x[1], 
                           reverse=True)
        ranking = {alg: i+1 for i, (alg, _) in enumerate(sorted_algs)}
        rankings.append(ranking)
    return rankings
```

---

## Estado

⏳ Pendiente de sincronización con `Problem.md`
