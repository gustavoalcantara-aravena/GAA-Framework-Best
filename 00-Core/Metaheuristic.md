---
gaa_metadata:
  version: 1.0.0
  type: trigger
  last_modified: null
  triggers_update:
    - 02-Components/Search-Operators.md
    - 02-Components/Fitness-Function.md
    - 03-Experiments/Experimental-Design.md
    - 04-Generated/scripts/metaheuristic.py
  extraction_rules:
    algorithm_type: "section:Selected-Metaheuristic"
    parameters: "section:Configuration"
    operators: "section:Search-Strategy"
---

# Metaheurística Seleccionada

> **🎯 ARCHIVO EDITABLE**: Este archivo es un trigger principal. Al editarlo, se actualizarán automáticamente todos los archivos dependientes.

## Selected-Metaheuristic

**Algoritmo**: [Simulated Annealing | Genetic Algorithm | Tabu Search | GRASP | etc.]  
**Tipo**: [Local Search | Population-based | Hybrid]  
**Referencia**: [CitaAutorAño]

## Descripción del Método

[Breve descripción del funcionamiento de la metaheurística seleccionada]

Ejemplo:
```
Simulated Annealing (SA) es un método de búsqueda local que acepta 
soluciones de peor calidad con probabilidad decreciente, simulando 
el proceso de enfriamiento de un metal.
```

## Configuration

**Parámetros principales**:

Ejemplo para SA:
```markdown
- **Temperatura inicial**: T₀ = 100
- **Factor de enfriamiento**: α = 0.95
- **Iteraciones por temperatura**: L = 100
- **Temperatura final**: Tf = 0.01
```

Ejemplo para GA:
```markdown
- **Tamaño de población**: pop_size = 100
- **Tasa de mutación**: pm = 0.1
- **Tasa de crossover**: pc = 0.8
- **Estrategia de selección**: Tournament (k=3)
- **Criterio de parada**: 1000 generaciones
```

[Completa con tus parámetros]

## Search-Strategy

### Operadores de Búsqueda sobre AST

**Mutación**:
- **Mutación de nodo**: Reemplazar un nodo función por otro compatible
- **Mutación de terminal**: Cambiar un terminal por otro del dominio
- **Mutación de parámetro**: Modificar parámetros numéricos (±δ%)

**Crossover** (si aplica):
- **Subtree crossover**: Intercambiar subárboles entre dos AST
- **One-point crossover**: Punto de corte en representación lineal

**Perturbación**:
- [Describe estrategias de perturbación específicas]

### Acceptance-Criteria

Ejemplo para SA:
```
Criterio Metropolis: 
P(accept) = 1                    si ΔE < 0 (mejora)
P(accept) = exp(-ΔE/T)          si ΔE ≥ 0 (empeora)
```

Ejemplo para GA:
```
Elitismo: Mantener los mejores k individuos
Selección por torneo: k=3
```

[Completa con tu criterio]

## Presupuesto Computacional

**Criterio de parada**:
- [ ] Tiempo límite: [X segundos]
- [ ] Número de iteraciones: [X iteraciones]
- [ ] Número de evaluaciones: [X evaluaciones]
- [ ] Convergencia: Sin mejora en [X] iteraciones

## AST-Specific Considerations

**Validación de AST**:
- ¿Validar gramática después de mutación? [Sí/No]
- ¿Reparación automática de AST inválidos? [Sí/No]
- ¿Profundidad máxima del árbol? [número]

**Inicialización**:
- Método: [Random | Grow | Full | Ramped Half-and-Half]
- Profundidad inicial: [min-max]

---

## 📚 Referencias

[Papers sobre la metaheurística seleccionada]

---

## ✅ Estado de Sincronización

- [ ] Metaheurística seleccionada
- [ ] Parámetros configurados
- [ ] Operadores definidos
- [ ] Sincronizado con archivos dependientes
