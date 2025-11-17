# Proyecto: GCP-ILS

## Graph Coloring Problem con Iterated Local Search

**Estado**: ⏳ En configuración  
**Problema**: Graph Coloring Problem  
**Metaheurística**: Iterated Local Search

---

## 📁 Estructura del Proyecto

```
GCP-ILS/
├── problema_metaheuristica.md    # Especificación completa del proyecto
├── datasets/
│   ├── training/                 # Instancias para entrenamiento
│   ├── validation/               # Instancias para validación
│   └── test/                     # Instancias para test
└── generated/                    # Scripts Python generados (auto)
```

---

## 🚀 Inicio Rápido

### 1. Agregar Datasets

**Formato DIMACS** (`.col`):
```
p edge <n> <m>
e <v1> <v2>
e <v1> <v3>
...
```

**Formato Simplificado** (`.txt`):
```
n m
v1 v2
v1 v3
...
```

**Ejemplo** (`myciel3.col`):
```
p edge 11 20
e 1 2
e 1 4
e 1 7
e 1 9
e 2 3
e 2 6
...
```

### 2. Benchmarks Recomendados

**DIMACS Challenge**: https://mat.tepper.cmu.edu/COLOR/instances.html

**Series recomendadas**:
- **queen**: Grafos de reinas de ajedrez
- **myciel**: Grafos de Mycielski
- **anna, david, homer**: Grafos de registro
- **games120, miles**: Grafos de aplicaciones reales

**Sugerencias**:
- Training: myciel3, myciel4, queen5_5, anna, david (5 instancias)
- Validation: queen6_6, homer, huck (3 instancias)
- Test: jean, games120, miles250, fpsol2, zeroin (5-8 instancias)

### 3. Revisar Configuración

Ver archivo completo: `problema_metaheuristica.md`

**Terminales disponibles** (15 operadores):
- Constructivos: GreedyDSATUR, GreedyLF, GreedySL, RandomSequential, RLF
- Mejora: KempeChain, TabuCol, OneVertexMove, SwapColors
- Perturbación: RandomRecolor, PartialDestroy, ColorClassMerge
- Intensificación: Intensify, GreedyImprovement
- Reparación: RepairConflicts, BacktrackRepair

**Parámetros ILS**:
- Max iteraciones: 500
- Intensidad perturbación: 20%
- Criterio aceptación: Better-or-Equal

### 4. Generar Scripts

```bash
cd ../../
python 05-Automation/sync-engine.py --sync-project projects/GCP-ILS
python 05-Automation/sync-engine.py --generate-project projects/GCP-ILS
```

### 5. Ejecutar Experimentos

```bash
cd generated
python main.py --mode train --instances ../datasets/training/
python main.py --mode test --instances ../datasets/test/
```

---

## 📊 Métrica Principal

**Objetivo**: Minimizar número de colores (k)

**Evaluación**:
```python
fitness = k + 100 * num_conflicts
```

**Comparación**: 
- Best Known Solutions (BKS) de DIMACS
- Número cromático teórico (si se conoce)

---

## ✅ Checklist

- [ ] Datasets descargados de DIMACS
- [ ] Datasets organizados en `datasets/training/`, `validation/`, `test/`
- [ ] Especificación revisada en `problema_metaheuristica.md`
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Comparación con BKS
- [ ] Resultados analizados

---

## 📝 Notas Importantes

- **Formato DIMACS**: Los vértices se numeran desde 1 (no desde 0)
- **Infactibilidad**: ILS puede trabajar con soluciones infactibles temporalmente
- **Número cromático**: Para muchos grafos DIMACS, χ(G) es conocido o estimado
- **Tiempo de ejecución**: Grafos grandes (>500 vértices) pueden requerir más tiempo

---

## 📚 Referencias

- DIMACS Challenge: https://mat.tepper.cmu.edu/COLOR/
- Graph Coloring Page: https://web.stanford.edu/~mpw/gc/

---

Este proyecto forma parte del framework GAA (Generación Automática de Algoritmos).
Ver documentación principal en: `../../GAA-Agent-System-Prompt.md`
