---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
    - 00-Core/Metaheuristic.md
  sync_rules:
    - source: "00-Core/Problem.md::Mathematical-Model"
      action: "extract_objective"
      target: "section:Objective-Function"
    - source: "00-Core/Metaheuristic.md::Search-Strategy"
      action: "extract_acceptance"
      target: "section:Acceptance-Criteria"
  auto_sync: true
---

# Función de Fitness para AST

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md` y `Metaheuristic.md`.

## Objetivo

Evaluar la calidad de un algoritmo (representado como AST) ejecutándolo sobre un conjunto de instancias del problema.

## Objective-Function

<!-- AUTO-GENERATED from 00-Core/Problem.md::Mathematical-Model -->
```python
def evaluate_solution(solution, problem_instance):
    """
    [Pendiente de extracción desde Problem.md]
    """
    pass
```
<!-- END AUTO-GENERATED -->

## AST-Fitness

```python
def evaluate_ast(ast, problem, instances, budget):
    """
    Evalúa un AST ejecutándolo sobre múltiples instancias.
    
    Args:
        ast: Árbol sintáctico del algoritmo
        problem: Instancia del problema
        instances: Lista de instancias de prueba
        budget: Presupuesto computacional por instancia
    
    Returns:
        fitness: Tupla (calidad_promedio, tiempo_promedio, tasa_factibilidad)
    """
    results = []
    
    for instance in instances:
        context = ExecutionContext(
            problem=problem,
            instance=instance,
            budget=budget
        )
        
        try:
            ast.execute(context)
            quality = problem.evaluate(context.best_solution)
            time = context.elapsed_time
            feasible = problem.is_feasible(context.best_solution)
            
            results.append({
                'quality': quality,
                'time': time,
                'feasible': feasible
            })
        except Exception as e:
            # Penalizar AST que causan errores
            results.append({
                'quality': float('-inf'),
                'time': budget,
                'feasible': False
            })
    
    # Agregar resultados
    avg_quality = sum(r['quality'] for r in results) / len(results)
    avg_time = sum(r['time'] for r in results) / len(results)
    feasibility_rate = sum(r['feasible'] for r in results) / len(results)
    
    # Fitness multi-objetivo
    fitness = (avg_quality, -avg_time, feasibility_rate)
    
    return fitness
```

## Acceptance-Criteria

<!-- AUTO-GENERATED from 00-Core/Metaheuristic.md::Search-Strategy -->
```python
# [Pendiente de extracción desde Metaheuristic.md]
```
<!-- END AUTO-GENERATED -->

## Aggregation Strategies

### Promedio Simple
```python
fitness = mean(qualities)
```

### Promedio Ponderado por Tiempo
```python
fitness = sum(q / t for q, t in zip(qualities, times)) / len(qualities)
```

### Pareto Multi-objetivo
```python
fitness = (quality, -time, feasibility_rate)
```

---

## Estado de Sincronización

⏳ Pendiente de sincronización con `Problem.md` y `Metaheuristic.md`
