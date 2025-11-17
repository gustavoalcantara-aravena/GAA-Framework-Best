---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  last_synced: null
  depends_on:
    - 00-Core/Problem.md
  sync_rules:
    - source: "00-Core/Problem.md::Domain-Operators"
      action: "extract_terminals"
      target: "section:Terminals"
  readonly: true
  auto_sync: true
---

# Gramática GAA

> **⚠️ AUTO-GENERADO**: Este archivo se sincroniza automáticamente desde `00-Core/Problem.md`.

## BNF Base

```bnf
<Prog> ::= Seq(<Stmt>*)

<Stmt> ::= If(<Cond>, <Stmt>, <Stmt>)
         | While(<Bud>, <Stmt>)
         | For(<Int>, <Stmt>)
         | Seq(<Stmt>*)
         | ChooseBestOf(<Int>, <Stmt>)
         | ApplyUntilNoImprove(<Stmt>, <Stop>)
         | LocalSearch(<Neighborhood>, <Acceptance>)
         | GreedyConstruct(<Heuristic>)
         | DestroyRepair(<Destroy>, <Repair>)
         | RuinRecreate(<Destroy>, <Recreate>)
         | Call(<Terminal>)

<Cond> ::= IsFeasible() 
         | Improves() 
         | Prob(<Float>) 
         | Stagnation()

<Bud>  ::= IterBudget(<Int>) 
         | TimeBudget(<Float_s>)

<Terminal> ::= [Se extraerá de Problem.md::Domain-Operators]
```

## Terminals

<!-- AUTO-GENERATED from 00-Core/Problem.md::Domain-Operators -->
```bnf
<Terminal> ::= [Pendiente de sincronización]
```
<!-- END AUTO-GENERATED -->

## Functions (Nodos Internos)

| Función | Aridad | Parámetros | Descripción |
|---------|--------|------------|-------------|
| `Seq` | n | List[Stmt] | Secuencia de instrucciones |
| `If` | 3 | Cond, Stmt, Stmt | Condicional |
| `While` | 2 | Budget, Stmt | Bucle con presupuesto |
| `For` | 2 | Int, Stmt | Bucle con iteraciones fijas |
| `ChooseBestOf` | 2 | Int, Stmt | Ejecuta n veces y elige mejor |
| `ApplyUntilNoImprove` | 2 | Stmt, Stop | Aplica hasta no mejorar |
| `LocalSearch` | 2 | Neighborhood, Acceptance | Búsqueda local |
| `GreedyConstruct` | 1 | Heuristic | Construcción voraz |
| `DestroyRepair` | 2 | Destroy, Repair | ALNS-style |
| `RuinRecreate` | 2 | Destroy, Recreate | LNS-style |
| `Call` | 1 | Terminal | Invoca un terminal |

## Validation Rules

- Profundidad máxima del árbol: [Por definir en Metaheuristic.md]
- Todos los nodos hoja deben ser terminales
- Los condicionales requieren condiciones válidas
- Los bucles requieren presupuestos válidos

---

## Validation Status

⏳ Pendiente de sincronización con `00-Core/Problem.md`
