---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
  auto_sync: true
---

# Evaluador de Soluciones

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md`.

## Contexto de Ejecución

```python
class ExecutionContext:
    """
    Contexto para la ejecución de un AST sobre una instancia.
    """
    
    def __init__(self, problem, instance, budget):
        self.problem = problem
        self.instance = instance
        self.budget = budget
        
        # Estado de ejecución
        self.current_solution = None
        self.best_solution = None
        self.best_fitness = float('-inf')
        
        # Métricas
        self.num_evaluations = 0
        self.elapsed_time = 0
        self.iteration = 0
        
        # Trazabilidad
        self.execution_trace = []
    
    def evaluate(self, solution):
        """Evalúa una solución y actualiza estadísticas"""
        fitness = self.problem.evaluate(solution)
        self.num_evaluations += 1
        
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = solution.copy()
        
        return fitness
    
    def is_budget_exhausted(self):
        """Verifica si se agotó el presupuesto"""
        if isinstance(self.budget, int):
            return self.num_evaluations >= self.budget
        elif isinstance(self.budget, float):
            return self.elapsed_time >= self.budget
        return False
```

## Evaluador de Problema

<!-- AUTO-GENERATED from 00-Core/Problem.md -->
```python
class ProblemEvaluator:
    """
    [Pendiente de generación desde Problem.md]
    """
    pass
```
<!-- END AUTO-GENERATED -->

---

## Estado de Sincronización

⏳ Pendiente de sincronización con `Problem.md`
