---
gaa_metadata:
  version: 1.0.0
  type: trigger
  last_modified: null
  triggers_update:
    - 01-System/Grammar.md
    - 01-System/AST-Nodes.md
    - 02-Components/Fitness-Function.md
    - 02-Components/Evaluator.md
    - 03-Experiments/Instances.md
    - 03-Experiments/Metrics.md
    - 06-Datasets/Dataset-Specification.md
    - 04-Generated/scripts/problem.py
  extraction_rules:
    terminals: "section:Domain-Operators"
    objective: "section:Mathematical-Model"
    constraints: "section:Constraints"
    representation: "section:Solution-Representation"
---

# Definición del Problema

> **🎯 ARCHIVO EDITABLE**: Este archivo es un trigger principal. Al editarlo, se actualizarán automáticamente todos los archivos dependientes.

## Problema Seleccionado

**Nombre**: [A completar por el usuario]  
**Tipo**: [Minimización | Maximización]  
**Categoría**: [Combinatorial | Continuous | Mixed]

## Descripción Informal

[Describe brevemente el problema en lenguaje natural]

Ejemplo:
```
El problema de la mochila (Knapsack) consiste en seleccionar un subconjunto 
de ítems, cada uno con un valor y un peso, de manera que se maximice el 
valor total sin exceder la capacidad de la mochila.
```

## Mathematical-Model

**Función Objetivo**:
```math
[Escribe aquí la función objetivo en notación matemática]
```

**Restricciones**:
```math
[Escribe las restricciones del problema]
```

**Variables de Decisión**:
- [Variable 1]: descripción
- [Variable 2]: descripción

## Domain-Operators

### Terminales Identificados

> **Formato**: `- **NombreTerminal**: Descripción [CitaAutorAño]`

Ejemplo:
```markdown
- **GreedyValueDensity**: Construcción voraz por ratio valor/peso [Dantzig1957]
- **FlipWorstItem**: Mejora local removiendo ítem con peor contribución [Martello1990]
- **SwapItems**: Intercambio de ítems dentro/fuera de la mochila [Pisinger2005]
```

[Completa aquí tus terminales]

## Solution-Representation

**Estructura de datos**:
```
[Describe cómo se representa una solución]
```

Ejemplo:
```
Vector binario de longitud n: x = [x_1, x_2, ..., x_n]
donde x_i = 1 si el ítem i está en la mochila, 0 en caso contrario
```

## Constraints

**Restricciones duras**:
1. [Restricción 1]
2. [Restricción 2]

**Parámetros del problema**:
- [Parámetro 1]: descripción
- [Parámetro 2]: descripción

## Evaluation-Criteria

**Métrica principal**: [Nombre de la métrica]  
**Criterio de comparación**: [Mayor es mejor | Menor es mejor]  
**Manejo de infactibilidad**: [Penalización | Rechazo | Reparación]

---

## 📚 Referencias

[Lista de papers y artículos consultados]

---

## ✅ Estado de Sincronización

- [ ] Problema definido completamente
- [ ] Modelo matemático formalizado
- [ ] Operadores del dominio identificados
- [ ] Sincronizado con archivos dependientes
