# Proyectos GAA

Este directorio contiene proyectos específicos de Generación Automática de Algoritmos (GAA) para diferentes problemas de optimización combinatoria.

---

## 📂 Proyectos Disponibles

### 1. KBP-SA: Knapsack Problem con Simulated Annealing

**Problema**: Knapsack Problem (0/1)  
**Metaheurística**: Simulated Annealing  
**Estado**: ⏳ Pendiente de datasets

**Descripción**: Problema de la mochila clásico - seleccionar ítems maximizando valor sin exceder capacidad.

**Directorio**: `KBP-SA/`  
**Terminales**: 13 operadores (constructivos, mejora, perturbación, reparación)  
**Datasets requeridos**: Usuario debe proporcionar instancias en formato especificado

[Ver detalles →](KBP-SA/README.md)

---

### 2. GCP-ILS: Graph Coloring Problem con Iterated Local Search

**Problema**: Graph Coloring Problem  
**Metaheurística**: Iterated Local Search (ILS)  
**Estado**: ⏳ Pendiente de datasets

**Descripción**: Colorear vértices de un grafo minimizando número de colores, sin vértices adyacentes del mismo color.

**Directorio**: `GCP-ILS/`  
**Terminales**: 15 operadores (DSATUR, Kempe chains, TabuCol, etc.)  
**Datasets recomendados**: DIMACS Challenge benchmarks

[Ver detalles →](GCP-ILS/README.md)

---

### 3. VRPTW-GRASP: Vehicle Routing con GRASP

**Problema**: Vehicle Routing Problem with Time Windows  
**Metaheurística**: GRASP  
**Estado**: ⏳ Pendiente de datasets

**Descripción**: Diseñar rutas de vehículos respetando capacidad y ventanas de tiempo, minimizando distancia total.

**Directorio**: `VRPTW-GRASP/`  
**Terminales**: 22 operadores (Savings, Insertion, 2-opt, Or-opt, etc.)  
**Datasets recomendados**: Solomon Instances

[Ver detalles →](VRPTW-GRASP/README.md)

---

## 🔄 Estructura Común de Proyectos

Cada proyecto sigue la misma estructura:

```
ProjectName/
├── problema_metaheuristica.md    # Especificación completa
├── README.md                      # Guía rápida
├── datasets/
│   ├── training/                  # Instancias entrenamiento
│   ├── validation/                # Instancias validación
│   └── test/                      # Instancias test
└── generated/                     # Scripts generados (auto)
```

---

## 📋 Workflow General

### Para cada proyecto:

1. **Revisar especificación**
   ```bash
   cd <ProjectName>
   cat problema_metaheuristica.md
   ```

2. **Agregar datasets**
   - Colocar archivos en `datasets/training/`, `validation/`, `test/`
   - Seguir formato especificado en `problema_metaheuristica.md`

3. **Sincronizar con framework base**
   ```bash
   cd ../..
   python 05-Automation/sync-engine.py --sync-project projects/<ProjectName>
   ```

4. **Generar scripts Python**
   ```bash
   python 05-Automation/sync-engine.py --generate-project projects/<ProjectName>
   ```

5. **Ejecutar experimentos**
   ```bash
   cd projects/<ProjectName>/generated
   python main.py --mode train
   python main.py --mode test
   ```

---

## 🎯 Objetivos de GAA

Para cada proyecto, el sistema GAA:

1. **Genera automáticamente** algoritmos representados como AST
2. **Combina operadores** del dominio usando la gramática BNF
3. **Optimiza AST** usando la metaheurística seleccionada
4. **Evalúa** en instancias reales del problema
5. **Compara** con algoritmos de referencia y best known solutions

---

## 📊 Comparación de Proyectos

| Proyecto | Problema | Metaheurística | Complejidad | Terminales | Datasets |
|----------|----------|----------------|-------------|------------|----------|
| KBP-SA | Knapsack | SA | Media | 13 | Usuario |
| GCP-ILS | Graph Coloring | ILS | Alta | 15 | DIMACS |
| VRPTW-GRASP | VRP Time Windows | GRASP | Muy Alta | 22 | Solomon |

---

## 🔧 Personalización

### Agregar un Nuevo Proyecto

1. Crear directorio:
   ```bash
   mkdir projects/NewProblem-NewMeta
   mkdir -p projects/NewProblem-NewMeta/datasets/{training,validation,test}
   mkdir projects/NewProblem-NewMeta/generated
   ```

2. Crear `problema_metaheuristica.md` siguiendo la plantilla de proyectos existentes

3. Incluir:
   - Definición del problema (modelo matemático)
   - Domain-Operators (terminales identificados de la literatura)
   - Metaheurística seleccionada (parámetros)
   - Formato de datasets
   - Plan experimental

4. Crear `README.md` con instrucciones específicas

---

## 📚 Referencias del Framework

- **Prompt base**: `../GAA-Agent-System-Prompt.md`
- **Documentación**: `../README.md`
- **Guía rápida**: `../QUICKSTART.md`
- **Motor de sincronización**: `../05-Automation/sync-engine.py`

---

## ✅ Estado Global

| Proyecto | Especificación | Datasets | Scripts | Experimentos |
|----------|---------------|----------|---------|--------------|
| KBP-SA | ✅ | ⏳ | ❌ | ❌ |
| GCP-ILS | ✅ | ⏳ | ❌ | ❌ |
| VRPTW-GRASP | ✅ | ⏳ | ❌ | ❌ |

**Leyenda**: ✅ Completado | ⏳ En progreso | ❌ Pendiente

---

## 🤝 Contribución

Para agregar instancias a un proyecto:
1. Descarga datasets de fuentes recomendadas
2. Colócalos en las subcarpetas correspondientes
3. Verifica formato con script de validación (próximamente)
4. Actualiza checklist en README del proyecto

---

**Última actualización**: 2025-11-17
