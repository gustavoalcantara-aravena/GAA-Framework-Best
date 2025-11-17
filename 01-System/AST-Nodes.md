---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 01-System/Grammar.md
    - 00-Core/Problem.md
  auto_sync: true
---

# Especificación de Nodos AST

> **⚠️ AUTO-GENERADO**: Clases Python para nodos del AST.

## Clase Base

```python
from abc import ABC, abstractmethod
from typing import Any, List, Dict

class ASTNode(ABC):
    """Clase base para todos los nodos del AST"""
    
    @abstractmethod
    def execute(self, context):
        """Ejecuta el nodo en el contexto dado"""
        pass
    
    @abstractmethod
    def to_json(self) -> Dict:
        """Serializa a JSON"""
        pass
    
    @abstractmethod
    def to_pseudocode(self, indent=0) -> str:
        """Genera pseudocódigo legible"""
        pass
```

## Nodos de Funciones

### Seq - Secuencia

```python
class Seq(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
    
    def execute(self, context):
        for stmt in self.statements:
            stmt.execute(context)
    
    def to_json(self):
        return {
            "type": "Seq",
            "body": [stmt.to_json() for stmt in self.statements]
        }
```

### If - Condicional

```python
class If(ASTNode):
    def __init__(self, condition: 'Condition', then_stmt: ASTNode, else_stmt: ASTNode):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    def execute(self, context):
        if self.condition.evaluate(context):
            self.then_stmt.execute(context)
        else:
            self.else_stmt.execute(context)
```

### While - Bucle con Presupuesto

```python
class While(ASTNode):
    def __init__(self, budget: 'Budget', body: ASTNode):
        self.budget = budget
        self.body = body
    
    def execute(self, context):
        while not self.budget.exhausted(context):
            self.body.execute(context)
            self.budget.consume(context)
```

## Nodos Terminales

<!-- AUTO-GENERATED from 00-Core/Problem.md::Domain-Operators -->

```python
# [Pendiente de sincronización]
# Se generarán clases para cada terminal identificado en Problem.md
```

<!-- END AUTO-GENERATED -->

## Nodos de Condiciones

```python
class IsFeasible(ASTNode):
    def evaluate(self, context):
        return context.problem.is_feasible(context.current_solution)

class Improves(ASTNode):
    def evaluate(self, context):
        return context.current_fitness > context.best_fitness
```

## Nodos de Presupuesto

```python
class IterBudget(ASTNode):
    def __init__(self, max_iters: int):
        self.max_iters = max_iters
        self.current_iter = 0
    
    def exhausted(self, context):
        return self.current_iter >= self.max_iters
    
    def consume(self, context):
        self.current_iter += 1
```

---

## Estado de Generación

⏳ Pendiente de sincronización
