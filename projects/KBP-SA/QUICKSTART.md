# 🚀 Guía Rápida - KBP-SA GAA System

## Inicio Rápido (5 minutos)

### 1. Instalación
```bash
pip install numpy scipy matplotlib pandas
```

### 2. Demo Básica
```bash
python demo_complete.py
```

Esto ejecuta:
- ✅ Carga de instancias
- ✅ Generación de 3 algoritmos
- ✅ Ejecución con intérprete
- ✅ Simulated Annealing
- ✅ Comparación de métodos

### 3. Demo de Experimentación
```bash
python demo_experimentation.py
```

Ejecuta experimentos completos con análisis estadístico.

---

## Casos de Uso Comunes

### Caso 1: Resolver una instancia específica

```python
from data.loader import DatasetLoader
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from gaa.interpreter import ASTInterpreter

# Cargar instancia
loader = DatasetLoader()
instances = loader.load_folder("low_dimensional")
problem = instances[0]

# Generar algoritmo
grammar = Grammar()
generator = AlgorithmGenerator(grammar=grammar, seed=42)
algorithm = generator.generate_with_validation()  # Genera automáticamente

# Ejecutar
interpreter = ASTInterpreter(problem, seed=42)
solution = interpreter.execute(algorithm)

print(f"Valor: {solution.value}, Gap: {interpreter.get_execution_report()['final_gap']:.2f}%")
```

### Caso 2: Comparar múltiples algoritmos

```python
from experimentation.runner import ExperimentRunner, ExperimentConfig

# Generar 3 algoritmos
algorithms = []
for i in range(3):
    ast = generator.generate_with_validation()
    algorithms.append({'name': f'Alg{i+1}', 'ast': ast})

# Configurar experimento
config = ExperimentConfig(
    name="comparison",
    instances=["f1_l-d_kp_10_269_low-dimensional"],
    algorithms=algorithms,
    repetitions=30
)

# Ejecutar
runner = ExperimentRunner(config)
runner.load_instances("low_dimensional")
results = runner.run_all()
runner.save_results()
```

### Caso 3: Análisis estadístico

```python
from experimentation.statistics import StatisticalAnalyzer

analyzer = StatisticalAnalyzer(alpha=0.05)

# Datos de dos algoritmos
alg1_gaps = [0.5, 0.8, 0.3, 0.6, 0.4]
alg2_gaps = [1.2, 1.5, 1.0, 1.3, 1.1]

# Test de Wilcoxon
test = analyzer.wilcoxon_signed_rank_test(alg1_gaps, alg2_gaps)
print(test.interpretation)

# Tamaño del efecto
cohens_d = analyzer.effect_size_cohens_d(alg1_gaps, alg2_gaps)
print(f"Cohen's d: {cohens_d:.3f}")
```

### Caso 4: Visualización de resultados

```python
from experimentation.visualization import ResultsVisualizer

visualizer = ResultsVisualizer(output_dir="plots")

# Boxplot
algorithm_results = {
    'Alg1': [0.5, 0.8, 0.3, 0.6, 0.4],
    'Alg2': [1.2, 1.5, 1.0, 1.3, 1.1],
    'Alg3': [0.7, 0.9, 0.5, 0.8, 0.6]
}

visualizer.plot_boxplot_comparison(
    algorithm_results,
    title="Comparación de Gaps",
    filename="comparison.png"
)
```

### Caso 5: Usar Simulated Annealing directamente

```python
from metaheuristic.sa_core import SimulatedAnnealing
from operators.constructive import GreedyByRatio

# Configurar SA
sa = SimulatedAnnealing(
    problem=problem,
    T0=100.0,           # Temperatura inicial
    alpha=0.95,         # Factor de enfriamiento
    iterations_per_temp=100,
    T_min=0.01,
    seed=42
)

# Solución inicial
initial = GreedyByRatio(problem).construct()

# Optimizar
best = sa.optimize(initial, verbose=True)

# Estadísticas
stats = sa.get_statistics()
print(f"Iteraciones: {stats['total_iterations']}")
print(f"Mejor valor: {stats['best_value']}")
print(f"Tiempo: {stats['elapsed_time']:.3f}s")
```

---

## Estructura de Datos Principal

### KnapsackProblem
```python
problem = KnapsackProblem(
    n=10,                      # Número de ítems
    capacity=50,               # Capacidad de la mochila
    values=[10, 20, ...],      # Valores de ítems
    weights=[5, 10, ...],      # Pesos de ítems
    optimal_value=100,         # Valor óptimo (opcional)
    name="instance_1"          # Nombre
)
```

### KnapsackSolution
```python
solution = KnapsackSolution(problem, [1, 0, 1, 0, ...])
print(solution.value)          # Valor total
print(solution.weight)         # Peso total
print(solution.is_feasible)    # ¿Es factible?
print(solution.num_selected()) # Ítems seleccionados
```

### AST Algorithm
```python
algorithm = Seq([
    GreedyConstruct(method="GreedyByRatio"),
    ApplyUntilNoImprove(
        operator=Call(name="FlipBestItem"),
        stop_condition="Stagnation=10"
    )
])

print(algorithm.to_pseudocode())
print(algorithm.to_dict())  # Para JSON
```

---

## Flujo de Trabajo Típico

### Para Experimentos

1. **Generar población de algoritmos**
   ```python
   population = generator.generate_population(size=50)
   ```

2. **Evaluar en instancias de validación**
   ```python
   config = ExperimentConfig(
       name="validation",
       instances=[...],
       algorithms=population[:10],  # Top 10
       repetitions=30
   )
   ```

3. **Análisis estadístico**
   ```python
   comparison = analyzer.compare_multiple_algorithms(results)
   print(f"Mejor: {comparison['best_algorithm']}")
   ```

4. **Seleccionar top-3**
   ```python
   rankings = comparison['average_rankings']
   top3 = sorted(rankings.items(), key=lambda x: x[1])[:3]
   ```

5. **Validar en test set**
   ```python
   final_config = ExperimentConfig(
       name="test",
       instances=test_instances,
       algorithms=top3_algorithms,
       repetitions=30
   )
   ```

---

## Tips y Mejores Prácticas

### 🎯 Para Experimentos
- Use al menos **30 repeticiones** para validez estadística
- Establezca **seeds fijas** para reproducibilidad
- Configure **timeout** apropiado (max_time_seconds)
- Guarde resultados en **JSON** para análisis posterior

### 🔬 Para Análisis
- Verifique **normalidad** antes de tests paramétricos
- Use tests **no paramétricos** para datos no normales
- Reporte **tamaño del efecto** (Cohen's d)
- Incluya **intervalos de confianza** (95%)

### 📊 Para Visualización
- Use **boxplots** para mostrar distribución completa
- **Scatter plots** revelan trade-offs
- **Curvas de convergencia** muestran comportamiento dinámico
- Guarde en **alta resolución** (dpi=300) para publicaciones

### ⚙️ Para Algoritmos
- Comience con **profundidad 2-3** (más simple)
- Use **validation** para asegurar AST válido
- Prefiera operadores con **referencias bibliográficas**
- Balancee **exploración vs explotación**

---

## Solución de Problemas

### Importaciones fallan
```bash
# Verificar que está en el directorio correcto
cd KBP-SA
python demo_complete.py
```

### No encuentra instancias
```python
# Verificar ruta de datasets
loader = DatasetLoader(base_path="datasets")
folders = loader.list_available_folders()
print(folders)  # ['low_dimensional', 'large_scale']
```

### Matplotlib no disponible
```bash
pip install matplotlib
# O ejecutar sin visualizaciones
```

### Experimentos muy lentos
```python
# Reducir repeticiones para testing
config.repetitions = 5
# O usar instancias más pequeñas
config.instances = instances[:3]
```

---

## Recursos Adicionales

- **README_SISTEMA.md**: Documentación completa
- **demo_complete.py**: Demo end-to-end
- **demo_experimentation.py**: Demo de experimentación
- Código fuente con **docstrings** detalladas
- **Referencias bibliográficas** en cada módulo

---

## Contacto y Soporte

Para dudas o problemas:
1. Revisar documentación en archivos fuente
2. Ejecutar demos para verificar funcionamiento
3. Verificar logs en `logs/`

**¡Buena suerte con tus experimentos!** 🚀
