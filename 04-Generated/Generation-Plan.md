---
gaa_metadata:
  version: 1.0.0
  type: orchestrator
  depends_on:
    - 00-Core/Problem.md
    - 00-Core/Metaheuristic.md
    - 01-System/Grammar.md
    - 02-Components/Fitness-Function.md
    - 02-Components/Search-Operators.md
  generation_plan:
    enabled: true
    auto_generate: true
  validation:
    pre_generate: true
    post_generate: true
---

# Plan de Generación de Scripts

> **⚠️ AUTO-GENERADO**: Plan orquestador de generación de código.

## Dependency Check

| Archivo | Estado | Última Modificación |
|---------|--------|---------------------|
| `00-Core/Problem.md` | ⏳ Sin completar | - |
| `00-Core/Metaheuristic.md` | ⏳ Sin completar | - |
| `01-System/Grammar.md` | ⏳ Sin sincronizar | - |
| `02-Components/Fitness-Function.md` | ⏳ Sin sincronizar | - |
| `06-Datasets/Dataset-Specification.md` | ⏳ Sin sincronizar | - |

## Scripts a Generar

### 1. problem.py

**Fuente**: `00-Core/Problem.md`  
**Estado**: ❌ No generado  
**Prioridad**: Alta  

**Incluye**:
- Clase `Problem`
- Método `evaluate(solution)`
- Método `is_feasible(solution)`
- Método `load_instance(path)`

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target problem.py
```

---

### 2. ast_nodes.py

**Fuente**: `01-System/Grammar.md` + `01-System/AST-Nodes.md`  
**Estado**: ❌ No generado  
**Prioridad**: Alta  

**Incluye**:
- Clase base `ASTNode`
- Clases de funciones: `Seq`, `If`, `While`, `For`, etc.
- Clases de terminales: [Desde Grammar.md]
- Métodos: `execute()`, `to_json()`, `to_pseudocode()`

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target ast_nodes.py
```

---

### 3. metaheuristic.py

**Fuente**: `00-Core/Metaheuristic.md` + `02-Components/Search-Operators.md`  
**Estado**: ❌ No generado  
**Prioridad**: Alta  

**Incluye**:
- Clase principal de metaheurística
- Operadores de mutación/crossover
- Criterio de aceptación
- Loop principal de optimización

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target metaheuristic.py
```

---

### 4. fitness.py

**Fuente**: `02-Components/Fitness-Function.md`  
**Estado**: ❌ No generado  
**Prioridad**: Media  

**Incluye**:
- `evaluate_ast(ast, instances)`
- `evaluate_solution(solution, problem)`
- Agregación de resultados

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target fitness.py
```

---

### 5. data_loader.py

**Fuente**: `06-Datasets/Dataset-Specification.md`  
**Estado**: ❌ No generado  
**Prioridad**: Media  

**Incluye**:
- Carga de instancias
- Validación de formato
- Generación de estadísticas

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target data_loader.py
```

---

### 6. main.py

**Fuente**: Orquestación de todos los módulos  
**Estado**: ❌ No generado  
**Prioridad**: Baja  

**Incluye**:
- Pipeline completo
- Configuración de experimentos
- Ejecución y reporte

**Comando de generación**:
```bash
python 05-Automation/code-generator.py --target main.py
```

---

## Orden de Generación Recomendado

1. ✅ `problem.py` (independiente)
2. ✅ `ast_nodes.py` (independiente)
3. ✅ `data_loader.py` (independiente)
4. ⏳ `fitness.py` (requiere problem.py)
5. ⏳ `metaheuristic.py` (requiere ast_nodes.py, fitness.py)
6. ⏳ `main.py` (requiere todos los anteriores)

## Comandos Rápidos

### Generar todos los scripts
```bash
python 05-Automation/code-generator.py --generate-all
```

### Validar antes de generar
```bash
python 05-Automation/code-generator.py --validate
```

### Generar y ejecutar tests
```bash
python 05-Automation/code-generator.py --generate-all --test
```

---

## Estado General

🔴 **No listo para generación**  
Razón: Archivos fuente no completados

### Pasos Siguientes

1. Completar `00-Core/Problem.md`
2. Ejecutar sincronización: `python 05-Automation/sync-engine.py --sync`
3. Completar `00-Core/Metaheuristic.md`
4. Validar sincronización
5. Generar scripts
