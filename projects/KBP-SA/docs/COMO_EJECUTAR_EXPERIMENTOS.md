# 🧪 Guía de Ejecución de Experimentos - KBP-SA

## 📍 Ubicación
Estás en: `c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA`

---

## 🚀 Opción 1: Demo Rápida (5 minutos)

### Ejecutar demo completo del sistema
```powershell
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
C:/Users/alfab/Documents/Projects/.venv/Scripts/python.exe demo_complete.py
```

**Qué hace:**
- ✅ Carga 1 instancia de prueba
- ✅ Genera 3 algoritmos automáticamente
- ✅ Ejecuta con intérprete AST
- ✅ Ejecuta Simulated Annealing
- ✅ Compara 4 métodos constructivos

**Tiempo:** ~30 segundos

---

## 🔬 Opción 2: Experimentos Completos (Demo)

### Ejecutar demo de experimentación con análisis estadístico
```powershell
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
C:/Users/alfab/Documents/Projects/.venv/Scripts/python.exe demo_experimentation.py
```

**Qué hace:**
- 🧬 Genera 3 algoritmos GAA automáticamente
- 📊 Ejecuta en 3 instancias × 3 algoritmos × 5 repeticiones = 45 experimentos
- 📈 Análisis estadístico completo:
  - Estadísticas descriptivas
  - Intervalos de confianza (95%)
  - Test de Friedman
  - Test de Wilcoxon pareado
  - Tamaño del efecto (Cohen's d)
- 📊 Genera visualizaciones (si matplotlib disponible):
  - Boxplots comparativos
  - Gráficas de barras con errores
  - Scatter tiempo vs calidad
- 💾 Guarda resultados en:
  - `output/demo_experiments/` (JSON)
  - `output/demo_plots/` (PNG)

**Tiempo:** ~2-5 minutos

**Instancias usadas:**
- f1_l-d_kp_10_269_low-dimensional (10 ítems)
- f3_l-d_kp_4_20_low-dimensional (4 ítems)
- f4_l-d_kp_4_11_low-dimensional (4 ítems)

---

## 🎯 Opción 3: Experimentos Personalizados

### Crear tu propio experimento

```python
# experimento_custom.py
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from experimentation.runner import ExperimentRunner, ExperimentConfig
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar

# 1. Generar algoritmos
grammar = Grammar(min_depth=2, max_depth=4)
generator = AlgorithmGenerator(grammar=grammar, seed=42)

algorithms = []
for i in range(5):  # 5 algoritmos
    ast = generator.generate_with_validation()  # Genera con estructura aleatoria
    if ast:
        algorithms.append({
            'name': f'Algorithm_{i+1}',
            'ast': ast
        })

# 2. Configurar experimento
config = ExperimentConfig(
    name="mi_experimento",
    instances=[
        "f1_l-d_kp_10_269_low-dimensional",
        "f2_l-d_kp_20_878_low-dimensional",
        "f3_l-d_kp_4_20_low-dimensional",
        "f6_l-d_kp_10_60_low-dimensional",
        "f7_l-d_kp_7_50_low-dimensional"
    ],
    algorithms=algorithms,
    repetitions=30,  # 30 repeticiones para validez estadística
    max_time_seconds=60.0,
    output_dir="output/mi_experimento"
)

# 3. Ejecutar
runner = ExperimentRunner(config)
runner.load_instances("low_dimensional")
results = runner.run_all(verbose=True)

# 4. Guardar
runner.save_results()

print(f"\n✅ Completado! Total ejecuciones: {len(results)}")
```

**Ejecutar:**
```powershell
C:/Users/alfab/Documents/Projects/.venv/Scripts/python.exe experimento_custom.py
```

---

## 📊 Opción 4: Experimentos en Large Scale

### Para instancias grandes (100-10,000 ítems)

```python
# experimento_large.py
config = ExperimentConfig(
    name="large_scale_experiment",
    instances=[
        "knapPI_1_100_1000_1_large_scale",
        "knapPI_1_200_1000_1_large_scale",
        "knapPI_1_500_1000_1_large_scale"
    ],
    algorithms=algorithms[:3],  # Solo top-3 algoritmos
    repetitions=10,  # Menos repeticiones (son más lentas)
    max_time_seconds=300.0,  # 5 minutos por ejecución
    output_dir="output/large_scale"
)

runner = ExperimentRunner(config)
runner.load_instances("large_scale")
results = runner.run_all(verbose=True)
runner.save_results()
```

---

## 📈 Ver Resultados

### Resultados en JSON
```powershell
# Ver resultados de demo
cat output/demo_experiments/experiment_demo_experiment_*.json

# O abrirlos con Python
```

```python
import json
from pathlib import Path

# Cargar último experimento
results_dir = Path("output/demo_experiments")
json_files = list(results_dir.glob("*.json"))
latest = max(json_files, key=lambda p: p.stat().st_mtime)

with open(latest) as f:
    data = json.load(f)

# Ver resumen
print(f"Experimentos totales: {data['summary']['total_experiments']}")
print(f"Exitosos: {data['summary']['successful']}")

# Ver por algoritmo
for alg, stats in data['summary']['by_algorithm'].items():
    print(f"\n{alg}:")
    print(f"  Gap promedio: {stats['avg_gap']:.2f}%")
    print(f"  Tiempo promedio: {stats['avg_time']:.3f}s")
```

### Visualizaciones
```powershell
# Ver gráficas generadas
explorer output/demo_plots
```

---

## 🔧 Configuración Avanzada

### Instancias Disponibles

**Low-dimensional (10 instancias):**
```
f1_l-d_kp_10_269_low-dimensional      (10 ítems, óptimo: 295)
f2_l-d_kp_20_878_low-dimensional      (20 ítems, óptimo: 1024)
f3_l-d_kp_4_20_low-dimensional        (4 ítems, óptimo: 35)
f4_l-d_kp_4_11_low-dimensional        (4 ítems, óptimo: 23)
f5_l-d_kp_15_375_low-dimensional      (15 ítems, óptimo: N/A - tiene error)
f6_l-d_kp_10_60_low-dimensional       (10 ítems, óptimo: 52)
f7_l-d_kp_7_50_low-dimensional        (7 ítems, óptimo: 107)
f8_l-d_kp_23_10000_low-dimensional    (23 ítems, óptimo: 9767)
f9_l-d_kp_5_80_low-dimensional        (5 ítems, óptimo: 130)
f10_l-d_kp_20_879_low-dimensional     (20 ítems, óptimo: 1025)
```

**Large-scale (21 instancias):**
```
knapPI_1_100_1000_1_large_scale       (100 ítems)
knapPI_1_200_1000_1_large_scale       (200 ítems)
knapPI_1_500_1000_1_large_scale       (500 ítems)
knapPI_1_1000_1000_1_large_scale      (1000 ítems)
knapPI_1_2000_1000_1_large_scale      (2000 ítems)
knapPI_1_5000_1000_1_large_scale      (5000 ítems)
knapPI_1_10000_1000_1_large_scale     (10000 ítems)
... (similar para knapPI_2 y knapPI_3)
```

### Estrategias de Generación de Algoritmos

```python
# El generador elige automáticamente entre 4 estrategias:
# - simple: Construcción + mejora básica
# - iterative: Con bucles y búsqueda local
# - multistart: Múltiples construcciones
# - complex: Estructura más profunda

# Generar con estrategia aleatoria
ast = generator.generate_with_validation()

# Para controlar profundidad
ast = generator.generate_with_validation(max_depth=3)

# Generar población de algoritmos diversos
population = generator.generate_population(size=50)
```

---

## 🎯 Workflow Completo Recomendado

### Para tu Tesis

1. **Validación rápida (10 min)**
   ```powershell
   python demo_experimentation.py
   ```

2. **Generar población de algoritmos (5 min)**
   ```python
   # Generar 50 algoritmos
   population = generator.generate_population(size=50)
   # Guardados en output/generated/
   ```

3. **Experimentos de validación (30 min)**
   ```python
   # Top 10 algoritmos en 5 instancias pequeñas
   config = ExperimentConfig(
       name="validation",
       instances=["f1...", "f2...", "f3...", "f6...", "f7..."],
       algorithms=population[:10],
       repetitions=30
   )
   ```

4. **Seleccionar Top-3 (análisis manual)**
   ```python
   # Basado en rankings estadísticos
   analyzer = StatisticalAnalyzer()
   comparison = analyzer.compare_multiple_algorithms(results)
   top3 = sorted(comparison['average_rankings'].items(), 
                 key=lambda x: x[1])[:3]
   ```

5. **Experimentos finales (2-3 horas)**
   ```python
   # Top-3 en todas las instancias large_scale
   config = ExperimentConfig(
       name="final_test",
       instances=all_large_scale_instances,
       algorithms=top3_algorithms,
       repetitions=30
   )
   ```

6. **Análisis final y visualizaciones**
   ```python
   visualizer = ResultsVisualizer()
   visualizer.plot_boxplot_comparison(...)
   visualizer.plot_convergence(...)
   visualizer.generate_html_report(...)
   ```

---

## ⚡ Tips de Rendimiento

### Acelerar experimentos
- Reducir `repetitions` a 5-10 para pruebas rápidas
- Usar solo instancias pequeñas inicialmente
- Ajustar `max_time_seconds` apropiadamente
- Ejecutar en paralelo (manual, múltiples terminales)

### Para debugging
```python
# Ejecutar solo 1 combinación
results = runner.run_single(problem, algorithm, seed=42, repetition=0)
print(results)
```

---

## 📞 Ayuda Rápida

**¿No encuentra instancias?**
```python
from data.loader import DatasetLoader
loader = DatasetLoader()
print(loader.list_available_folders())
instances = loader.load_folder("low_dimensional")
print([p.name for p in instances])
```

**¿Error de importación?**
```powershell
# Verificar que estás en el directorio correcto
cd c:\Users\alfab\Documents\Projects\GAA\projects\KBP-SA
```

**¿Matplotlib no disponible?**
```powershell
# Instalar
pip install matplotlib

# O ejecutar sin visualizaciones (solo JSON)
```

---

## 📝 Próximos Pasos

Después de ejecutar experimentos:
1. ✅ Revisar resultados JSON
2. ✅ Analizar gráficas generadas
3. ✅ Seleccionar top-3 algoritmos
4. ✅ Ejecutar en test set (large_scale)
5. ✅ Generar reporte científico

**¡Listo para empezar! 🚀**
