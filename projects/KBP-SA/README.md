# Proyecto: KBP-SA

## Knapsack Problem con Simulated Annealing

**Estado**: ⏳ En configuración  
**Problema**: Knapsack Problem (0/1)  
**Metaheurística**: Simulated Annealing

---

## 📁 Estructura del Proyecto

```
KBP-SA/
├── problema_metaheuristica.md    # Especificación completa del proyecto
├── config.yaml                   # Configuración de experimentos
├── run.py                        # Script principal de ejecución
├── validate_datasets.py          # Validador de instancias
├── generate_example_datasets.py  # Generador de ejemplos
├── INSTRUCTIONS.md               # Guía de ejecución
├── datasets/
│   ├── low_dimensional/          # ✅ 10 instancias (n=4-23)
│   ├── large_scale/              # ✅ 21 instancias (n=100-10000)
│   ├── INSTANCES_DOCUMENTATION.md # 📖 Documentación completa
│   ├── training/                 # Para datasets custom
│   ├── validation/               # Para datasets custom
│   └── test/                     # Para datasets custom
└── generated/                    # Resultados y logs
```

**📖 Ver documentación completa de instancias**: [datasets/INSTANCES_DOCUMENTATION.md](datasets/INSTANCES_DOCUMENTATION.md)

---

## 🚀 Inicio Rápido

### Opción A: Usar Instancias Incluidas (Recomendado)

**El proyecto ya incluye 31 instancias listas para usar**:
- ✅ **10 instancias low-dimensional** (n=4-23) - Para testing rápido
- ✅ **21 instancias large-scale** (n=100-10,000) - Pisinger's benchmark

Ver detalles completos en: [datasets/INSTANCES_DOCUMENTATION.md](datasets/INSTANCES_DOCUMENTATION.md)

```powershell
# 1. Validar que las instancias se cargan correctamente
python validate_datasets.py

# 2. Ejecutar optimización
python run.py
```

### Opción B: Generar Instancias de Ejemplo

```powershell
python generate_example_datasets.py
```

### Opción C: Agregar tus Propios Datasets

**Formato requerido**:

```
n W
v_1 w_1
v_2 w_2
...
v_n w_n
```

**Ejemplo** (`knapsack_10.txt`):
```
10 269
55 95
10 4
47 60
5 32
4 23
50 72
8 80
61 62
85 65
87 46
```

**Coloca tus archivos en**:
- `datasets/training/*.txt` (para optimizar el AST)
- `datasets/validation/*.txt` (para validar)
- `datasets/test/*.txt` (para evaluación final)

---

## 📊 Datasets Incluidos

### Low-Dimensional (10 instancias)
Instancias pequeñas ideales para desarrollo y debugging:
- **f1 - f10**: Tamaños de 4 a 23 ítems
- **Uso**: Validación rápida, testing inicial
- **Tiempo de resolución**: < 1 segundo

### Large-Scale (21 instancias - Pisinger's Benchmark)
Instancias estándar para benchmarking serio:
- **knapPI Type 1**: 7 instancias (uncorrelated)
- **knapPI Type 2**: 7 instancias (weakly correlated)
- **knapPI Type 3**: 7 instancias (strongly correlated)
- **Tamaños**: 100, 200, 500, 1000, 2000, 5000, 10000 ítems
- **Uso**: Evaluación rigurosa, comparación con estado del arte

**📖 Documentación completa**: [datasets/INSTANCES_DOCUMENTATION.md](datasets/INSTANCES_DOCUMENTATION.md)

---

## 🎯 Uso Recomendado de Instancias

```yaml
# Training GAA (desarrollo rápido)
low_dimensional/f1_*.txt
low_dimensional/f5_*.txt
large_scale/knapPI_1_100_*.txt

# Validation (ajuste de parámetros)
low_dimensional/f8_*.txt
large_scale/knapPI_2_500_*.txt

# Testing (evaluación final)
large_scale/knapPI_3_1000_*.txt
large_scale/knapPI_3_2000_*.txt

# Benchmarking (comparación SOTA)
large_scale/knapPI_*_5000_*.txt
large_scale/knapPI_*_10000_*.txt
```

---

## 🔬 Validación de Datasets

```powershell
python validate_datasets.py
```

**Salida esperada**:
```
✅ Low-dimensional: 10 instancias válidas
✅ Large-scale: 21 instancias válidas
✅ Total: 31 instancias listas para usar
```

### 2. Ejecutar Optimización

```powershell
python run.py
```

El script automáticamente:
1. Carga instancias desde `datasets/low_dimensional/` y `datasets/large_scale/`
2. Configura Simulated Annealing con los parámetros de `config.yaml`
3. Ejecuta la optimización del GAA
4. Guarda el mejor algoritmo en `generated/results/`

---

## ⚙️ Configuración

Ver archivos completos:
- **problema_metaheuristica.md** - Especificación del problema y terminales
- **config.yaml** - Parámetros de experimentos
- **INSTRUCTIONS.md** - Guía paso a paso
### Terminales Disponibles (13 operadores)
- **Constructivos**: GreedyByValue, GreedyByWeight, GreedyByRatio, RandomConstruct
- **Mejora**: FlipBestItem, FlipWorstItem, OneExchange, TwoExchange
- **Perturbación**: RandomFlip, ShakeByRemoval, DestroyRepair
- **Reparación**: RepairByRemoval, RepairByGreedy

### Parámetros Simulated Annealing
- **Temperatura inicial**: 100.0
- **Factor enfriamiento**: 0.95 (geométrico)
- **Iteraciones por temperatura**: 100
- **Max evaluaciones**: 10,000

---

## 📚 Referencias y Benchmarks

### Origen de Instancias

**Low-dimensional**: Instancias clásicas de la literatura  
**Large-scale**: Pisinger's benchmark (2005)
- **Paper**: "Where are the hard knapsack problems?"
- **URL**: http://hjemmesider.diku.dk/~pisinger/codes.html
- **Citación**: Pisinger, D. (2005). Computers & Operations Research, 32(9), 2271-2284

### Otras Fuentes (opcionales)
- **OR-Library**: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/knapsack.html
- **MIPLIB**: https://miplib.zib.de/

---

## 📖 Documentación

- **Especificación del problema**: [problema_metaheuristica.md](problema_metaheuristica.md)
- **Instancias disponibles**: [datasets/INSTANCES_DOCUMENTATION.md](datasets/INSTANCES_DOCUMENTATION.md)
- **Guía de ejecución**: [INSTRUCTIONS.md](INSTRUCTIONS.md)
- **Configuración**: [config.yaml](config.yaml)

---

**Estado**: ✅ Listo para ejecutar  
**Instancias**: 31 disponibles (10 low-dim + 21 large-scale)  
**Última actualización**: 2025-11-17

---

## ✅ Checklist

- [ ] Datasets agregados en `datasets/training/`
- [ ] Datasets agregados en `datasets/validation/`
- [ ] Datasets agregados en `datasets/test/`
- [ ] Especificación revisada en `problema_metaheuristica.md`
- [ ] Scripts generados
- [ ] Experimentos ejecutados
- [ ] Resultados analizados

---

## 📝 Notas

Este proyecto forma parte del framework GAA (Generación Automática de Algoritmos).
Ver documentación principal en: `../../GAA-Agent-System-Prompt.md`
