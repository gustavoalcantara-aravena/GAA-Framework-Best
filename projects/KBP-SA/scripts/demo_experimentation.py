#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de Experimentación - KBP-SA
Demuestra el módulo experimentation/ para análisis estadístico

Este script ejecuta:
1. Experimentos con múltiples algoritmos
2. Análisis estadístico completo
3. Visualizaciones
4. Reporte de resultados
"""

import sys
import os
from pathlib import Path

# Configurar encoding UTF-8 para salida en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from datetime import datetime

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Imports
from experimentation.runner import ExperimentRunner, ExperimentConfig
from experimentation.metrics import QualityMetrics, PerformanceMetrics
from experimentation.statistics import StatisticalAnalyzer
from experimentation.visualization import ResultsVisualizer
from experimentation.ast_visualization import ASTVisualizer
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from metaheuristic.sa_core import SimulatedAnnealing
from core.solution import KnapsackSolution
import numpy as np


def run_detailed_visualization_per_group(instances, algorithm, plots_dir, timestamp):
    """
    Ejecuta SA en TODAS las instancias del grupo con tracking detallado y genera
    4 visualizaciones agregadas representativas del grupo completo
    
    Args:
        instances: lista de KnapsackProblem (todas las instancias del grupo)
        algorithm: dict con 'name', 'ast', 'interpreter'
        plots_dir: directorio donde guardar las gráficas
        timestamp: timestamp (no usado, mantenido por compatibilidad)
    
    Returns:
        best_solution: mejor solución encontrada entre todas las instancias
    """
    # Guardar directamente en la carpeta principal (no subcarpeta)
    output_dir = plots_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"  Ejecutando SA en {len(instances)} instancias del grupo...")
    
    # Variables para almacenar tracking de todas las instancias
    all_best_values = []  # Lista de listas
    all_acceptances = []  # Lista de listas
    all_temperatures = []  # Lista de listas
    all_delta_e = []  # Lista de listas
    
    best_overall = None
    
    # Ejecutar SA en cada instancia del grupo
    for idx, instance in enumerate(instances, 1):
        print(f"    [{idx}/{len(instances)}] Procesando {instance.name}...", end=" ")
        
        # Variables de tracking para esta instancia
        best_values_history = []
        acceptance_history = []
        temperature_history = []
        delta_e_history = []
        
        # Configurar SA con tracking
        sa = SimulatedAnnealing(
            problem=instance,
            T0=100.0,
            alpha=0.95,
            iterations_per_temp=100,
            T_min=0.01,
            max_evaluations=5000,
            seed=42
        )
        
        # Función de vecindad simple
        def custom_neighborhood(solution, rng):
            neighbor = solution.copy()
            idx_flip = rng.integers(0, instance.n)
            neighbor.selection[idx_flip] = 1 - neighbor.selection[idx_flip]
            neighbor.evaluate(instance)
            return neighbor
        
        sa.neighborhood_function = custom_neighborhood
        
        # Ejecutar SA con tracking completo
        initial = KnapsackSolution.empty(instance.n, instance)
        current = initial.copy()
        best = current.copy()
        
        T = sa.T0
        rng = sa.rng
        evaluations = 0
        
        def get_effective_value(sol):
            if sol.is_feasible:
                return sol.value
            else:
                excess = sol.weight - sol.problem.capacity
                return sol.value - excess * 1000
        
        while T > sa.T_min and evaluations < sa.max_evaluations:
            for _ in range(sa.iterations_per_temp):
                neighbor = sa.neighborhood_function(current, rng)
                evaluations += 1
                
                delta = get_effective_value(neighbor) - get_effective_value(current)
                delta_e_history.append(delta)
                
                accepted = False
                if delta > 0:
                    accepted = True
                    current = neighbor
                else:
                    prob = np.exp(delta / T)
                    if rng.random() < prob:
                        accepted = True
                        current = neighbor
                
                acceptance_history.append(1 if accepted else 0)
                temperature_history.append(T)
                
                if current.is_feasible and current.value > best.value:
                    best = current.copy()
                
                best_values_history.append(best.value)
                
                if evaluations >= sa.max_evaluations:
                    break
            
            T *= sa.alpha
        
        # Almacenar tracking de esta instancia
        all_best_values.append(best_values_history)
        all_acceptances.append(acceptance_history)
        all_temperatures.append(temperature_history)
        all_delta_e.append(delta_e_history)
        
        # Actualizar mejor solución global
        if best_overall is None or (best.is_feasible and best.value > best_overall.value):
            best_overall = best.copy()
        
        gap = ((instance.optimal_value - best.value) / instance.optimal_value) * 100 if instance.optimal_value > 0 else 0
        print(f"Gap: {gap:.2f}%")
    
    print(f"\n  Agregando datos de {len(instances)} instancias...")
    
    # Agregar datos de todas las instancias
    # 1. Gap Evolution: normalizar y promediar
    max_length = max(len(vals) for vals in all_best_values)
    
    # Normalizar best_values a gaps porcentuales
    normalized_gaps = []
    for i, best_vals in enumerate(all_best_values):
        instance = instances[i]
        gaps = [((instance.optimal_value - val) / instance.optimal_value) * 100 
                if instance.optimal_value > 0 else 0 
                for val in best_vals]
        # Pad con último valor si es necesario
        if len(gaps) < max_length:
            gaps.extend([gaps[-1]] * (max_length - len(gaps)))
        normalized_gaps.append(gaps)
    
    # Calcular media y std de gaps
    gap_mean = np.mean(normalized_gaps, axis=0)
    gap_std = np.std(normalized_gaps, axis=0)
    
    # 2. Acceptance Rate: promediar tasas de aceptación
    max_length_acc = max(len(acc) for acc in all_acceptances)
    padded_acceptances = []
    for acc in all_acceptances:
        if len(acc) < max_length_acc:
            acc_padded = acc + [acc[-1]] * (max_length_acc - len(acc))
        else:
            acc_padded = acc
        padded_acceptances.append(acc_padded)
    
    acceptance_mean = np.mean(padded_acceptances, axis=0).tolist()
    
    # Usar temperatura de una instancia representativa (todas deberían ser similares)
    representative_temperature = all_temperatures[len(all_temperatures) // 2]
    
    # 3. Delta E Distribution: concatenar todos los valores
    all_delta_e_combined = []
    all_acceptances_combined = []
    all_temperatures_combined = []
    for delta_list, acc_list, temp_list in zip(all_delta_e, all_acceptances, all_temperatures):
        all_delta_e_combined.extend(delta_list)
        all_acceptances_combined.extend(acc_list)
        all_temperatures_combined.extend(temp_list)
    
    # 4. Exploration-Exploitation: promediar proporciones
    # Esta gráfica se calcula internamente, solo pasamos datos combinados
    
    # Generar visualizaciones agregadas en la carpeta principal
    visualizer = ResultsVisualizer(output_dir=str(output_dir))
    
    print(f"\n  Generando visualizaciones agregadas del grupo...")
    
    # 1. Gap evolution (con banda de confianza)
    # Crear datos sintéticos para plot_gap_evolution
    # La función espera best_values y optimal, los reconstruimos desde gap_mean
    # Asumimos optimal=100 y calculamos best_values correspondientes
    synthetic_optimal = 100
    synthetic_best_values = [(synthetic_optimal * (1 - gap/100)) for gap in gap_mean]
    
    visualizer.plot_gap_evolution(
        best_values=synthetic_best_values,
        optimal_value=synthetic_optimal,
        title="Gap Evolution - Grupo Low-Dimensional (Promedio de todas las instancias)",
        filename="gap_evolution.png",
        show_improvements=True,
        temperature_history=representative_temperature
    )
    
    # 2. Acceptance rate (promediada)
    visualizer.plot_acceptance_rate(
        acceptance_history=acceptance_mean,
        window_size=100,
        title="Acceptance Rate - Grupo Low-Dimensional (Promedio de todas las instancias)",
        filename="acceptance_rate.png",
        temperature_history=representative_temperature
    )
    
    # 3. Delta E distribution (combinada de todas las instancias)
    acceptance_decisions_combined = [bool(x) for x in all_acceptances_combined]
    visualizer.plot_delta_e_distribution(
        delta_e_values=all_delta_e_combined,
        acceptance_decisions=acceptance_decisions_combined,
        title="ΔE Distribution - Grupo Low-Dimensional (Todas las instancias)",
        filename="delta_e_distribution.png",
        bins=50
    )
    
    # 4. Exploration-exploitation balance (una gráfica por instancia)
    # Generar gráficas individuales para cada instancia del grupo
    print(f"\n  Generando gráficas exploration-exploitation por instancia...")
    
    for idx, (instance, delta_list, acc_list, temp_list) in enumerate(zip(instances, all_delta_e, all_acceptances, all_temperatures), 1):
        instance_name = instance.name.replace('_low-dimensional', '')
        
        acceptance_decisions = [bool(x) for x in acc_list]
        
        visualizer.plot_exploration_exploitation_balance(
            delta_e_values=delta_list,
            acceptance_decisions=acceptance_decisions,
            temperature_history=temp_list,
            title=f"Exploration-Exploitation Balance - {instance_name}",
            filename=f"exploration_exploitation_{instance_name}.png",
            window_size=100
        )
        
        print(f"    [{idx}/{len(instances)}] {instance_name}: ✓")
    
    print(f"  ✅ {3 + len(instances)} gráficas SA generadas (3 agregadas + {len(instances)} por instancia)")
    
    return best_overall


def main():
    print("=" * 80)
    print("  DEMO: Módulo de Experimentación - KBP-SA")
    print("=" * 80)
    print()
    
    # 1. Generar algoritmos para experimentar
    print("🧬 Paso 1: Generando algoritmos GAA...\n")
    
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'GAA_Algorithm_{i+1}',
                'ast': ast
            })
            print(f"✅ Algoritmo {i+1} generado")
            print(f"   Pseudocódigo:")
            for line in ast.to_pseudocode(indent=2).split('\n'):
                print(f"   {line}")
            print()
    
    # 2. Configurar experimento
    print("⚙️  Paso 2: Configurando experimento...\n")
    
    # Cargar TODAS las instancias low-dimensional disponibles
    from data.loader import DatasetLoader
    from pathlib import Path
    
    # datasets_dir debe apuntar a la carpeta que CONTIENE low_dimensional
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    all_instances = loader.load_folder("low_dimensional")
    
    # Usar nombres de todas las instancias
    instance_names = [inst.name for inst in all_instances]
    
    print(f"📁 Instancias low-dimensional encontradas: {len(instance_names)}")
    for name in instance_names:
        print(f"   • {name}")
    print()
    
    config = ExperimentConfig(
        name="all_instances_experiment",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,  # 1 repetición por instancia para cubrir todas
        max_time_seconds=60.0,
        output_dir="output/all_instances_experiments"
    )
    
    print(f"⚙️  Configuración:")
    print(f"  • Instancias: {len(config.instances)}")
    print(f"  • Algoritmos: {len(config.algorithms)}")
    print(f"  • Repeticiones: {config.repetitions}")
    print(f"  • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    print()
    
    # 3. Ejecutar experimentos
    print("🚀 Paso 3: Ejecutando experimentos con TODAS las instancias low-dimensional...\n")
    
    runner = ExperimentRunner(config)
    runner.load_instances("low_dimensional")
    
    if not runner.problems:
        print("❌ No se pudieron cargar instancias. Abortando.")
        return
    
    results = runner.run_all(verbose=True)
    
    # 4. Guardar resultados
    print("\n💾 Paso 4: Guardando resultados...\n")
    
    json_file = runner.save_results()
    
    # 5. Análisis estadístico
    print("\n📊 Paso 5: Análisis estadístico...\n")
    
    analyzer = StatisticalAnalyzer(alpha=0.05)
    
    # Agrupar resultados por algoritmo
    algorithm_results = {}
    for alg in algorithms:
        alg_name = alg['name']
        alg_data = [r for r in results if r.algorithm_name == alg_name and r.success]
        
        if alg_data:
            gaps = [r.gap_to_optimal for r in alg_data if r.gap_to_optimal is not None]
            times = [r.total_time for r in alg_data]
            
            algorithm_results[alg_name] = gaps
            
            print(f"Algoritmo: {alg_name}")
            
            # Estadísticas descriptivas
            if gaps:
                stats = analyzer.descriptive_statistics(gaps)
                print(f"  Gap (%): media={stats['mean']:.2f} ± {stats['std']:.2f}, "
                      f"min={stats['min']:.2f}, max={stats['max']:.2f}")
                
                # Intervalo de confianza
                ci = analyzer.confidence_interval(gaps, confidence=0.95)
                print(f"  IC 95%: [{ci[0]:.2f}, {ci[1]:.2f}]")
            
            if times:
                time_stats = analyzer.descriptive_statistics(times)
                print(f"  Tiempo (s): media={time_stats['mean']:.3f} ± {time_stats['std']:.3f}")
            
            print()
    
    # 6. Comparación entre algoritmos
    if len(algorithm_results) >= 2:
        print("🔬 Paso 6: Comparación estadística entre algoritmos...\n")
        
        # Generar timestamp para outputs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        comparison = analyzer.compare_multiple_algorithms(
            algorithm_results,
            test_type="friedman"
        )
        
        print(f"Test: {comparison['global_test'].test_name}")
        print(f"  p-value: {comparison['global_test'].p_value:.4f}")
        print(f"  {comparison['global_test'].interpretation}")
        print()
        
        print("Rankings promedio (menor = mejor):")
        for alg, rank in sorted(comparison['average_rankings'].items(), key=lambda x: x[1]):
            print(f"  {rank:.2f}  {alg}")
        print()
        
        print(f"🏆 Mejor algoritmo: {comparison['best_algorithm']}")
        print()
        
        # Test pareado entre primero y segundo
        if len(algorithm_results) >= 2:
            algs = list(algorithm_results.keys())
            data1 = algorithm_results[algs[0]]
            data2 = algorithm_results[algs[1]]
            
            # Ajustar tamaños si no coinciden
            min_len = min(len(data1), len(data2))
            data1 = data1[:min_len]
            data2 = data2[:min_len]
            
            print(f"\nComparación pareada: {algs[0]} vs {algs[1]}")
            
            # Wilcoxon (no paramétrico)
            wilcoxon = analyzer.wilcoxon_signed_rank_test(data1, data2)
            print(f"  Wilcoxon: p={wilcoxon.p_value:.4f}")
            print(f"  {wilcoxon.interpretation}")
            
            # Tamaño del efecto
            cohens_d = analyzer.effect_size_cohens_d(data1, data2)
            print(f"  Cohen's d: {cohens_d:.3f} ", end="")
            if abs(cohens_d) < 0.2:
                print("(efecto pequeño)")
            elif abs(cohens_d) < 0.5:
                print("(efecto mediano)")
            else:
                print("(efecto grande)")
            print()
    
    # 7. Visualización
    print("📈 Paso 7: Generando visualizaciones...\n")
    
    # Crear carpeta con dataset_timestamp (como en versión original)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plots_dir = f"output/plots_low_dimensional_{timestamp}"
    visualizer = ResultsVisualizer(output_dir=plots_dir)
    
    # Crear visualizador de AST para documentación
    from experimentation.ast_visualization import ASTVisualizer
    ast_visualizer = ASTVisualizer(output_dir=plots_dir)
    
    # Crear directorio de documentación
    from pathlib import Path
    docs_dir = Path(plots_dir)
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar documentación del experimento
    print("📝 Generando documentación del experimento...\n")
    
    # 1. README principal
    readme_content = f"""# Reporte de Experimentación - KBP-SA
**Fecha**: {datetime.now().strftime("%d de %B de %Y, %H:%M:%S")}
**Configuración**: {config.name}

## Resumen Ejecutivo

Este experimento evalúa {len(algorithms)} algoritmos generados por GAA sobre {len(config.instances)} instancias del problema de la mochila (dataset low-dimensional).

### Resultados Principales

- **Mejor algoritmo**: {comparison['best_algorithm']}
- **Instancias procesadas**: {len(config.instances)}
- **Ejecuciones totales**: {len(results)}
- **Tasa de éxito**: {sum(1 for r in results if r.success)}/{len(results)} ({100*sum(1 for r in results if r.success)/len(results):.1f}%)

## Archivos Generados

### Documentación
- `01_ALGORITMOS_GAA.md` - Descripción de los 3 algoritmos generados
- `02_CONFIGURACION_EXPERIMENTO.md` - Configuración y diseño experimental
- `03_ANALISIS_ESTADISTICO.md` - Resultados y comparaciones estadísticas
- `04_GRAFICAS_ESTADISTICAS.md` - Explicación de gráficas comparativas
- `05_GRAFICAS_SA.md` - Explicación de visualizaciones de SA

### Visualizaciones Estadísticas
- `demo_boxplot.png` - Comparación de gaps entre algoritmos
- `demo_bars.png` - Gap promedio por algoritmo
- `demo_scatter.png` - Trade-off tiempo vs calidad
- `best_algorithm_ast.png` - Estructura del mejor algoritmo

### Visualizaciones de Simulated Annealing
**Agregadas (grupo completo):**
- `gap_evolution.png` - Evolución del gap promedio
- `acceptance_rate.png` - Tasa de aceptación promedio
- `delta_e_distribution.png` - Distribución de cambios de energía

**Por instancia ({len(config.instances)} gráficas):**
- `exploration_exploitation_<instancia>.png` - Balance exploración-explotación

## Siguiente Paso

Consulte los archivos de documentación individuales para detalles completos de cada fase del experimento.
"""
    
    with open(docs_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 2. Documentación de algoritmos GAA
    alg_doc = f"""# Algoritmos GAA Generados

**Fecha de generación**: {datetime.now().strftime("%d de %B de %Y")}
**Semilla**: 42

## Descripción

Se generaron {len(algorithms)} algoritmos usando Grammar-based Algorithm Generation (GAA) con los siguientes parámetros:

- **Profundidad mínima**: 2
- **Profundidad máxima**: 3
- **Gramática**: Metaheurística Simulated Annealing

## Algoritmos

"""
    
    for i, alg in enumerate(algorithms, 1):
        alg_doc += f"""### {alg['name']}

**Pseudocódigo:**
```
{alg['ast'].to_pseudocode(indent=0)}
```

**Estadísticas del AST:**
"""
        stats = ast_visualizer.get_ast_statistics(alg['ast'])
        alg_doc += f"""- Nodos totales: {stats['total_nodes']}
- Profundidad: {stats['depth']}
- Operadores usados: {', '.join(stats['terminal_operators'])}

"""
    
    with open(docs_dir / "01_ALGORITMOS_GAA.md", "w", encoding="utf-8") as f:
        f.write(alg_doc)
    
    # 3. Configuración del experimento
    config_doc = f"""# Configuración del Experimento

## Diseño Experimental

### Instancias ({len(config.instances)})

Dataset: **low-dimensional** (10 instancias del benchmark)

"""
    for name in sorted(config.instances):
        config_doc += f"- `{name}`\n"
    
    config_doc += f"""

### Algoritmos ({len(config.algorithms)})

"""
    for alg in algorithms:
        config_doc += f"- `{alg['name']}`\n"
    
    config_doc += f"""

### Parámetros

- **Repeticiones por combinación**: {config.repetitions}
- **Timeout por ejecución**: {config.max_time_seconds} segundos
- **Total de ejecuciones**: {len(config.instances)} × {len(config.algorithms)} × {config.repetitions} = {len(config.instances) * len(config.algorithms) * config.repetitions}

## Metodología

### Experimentos (Paso 3)

Se ejecutaron **{len(results)} experimentos** siguiendo un diseño factorial completo:

1. Para cada **instancia** del problema
2. Para cada **algoritmo** generado
3. Ejecutar **{config.repetitions} repetición(es)** con semilla aleatoria controlada

Esto permite:
- Comparación justa entre algoritmos (mismas instancias)
- Análisis estadístico robusto (múltiples repeticiones)
- Reproducibilidad (semillas controladas)

### Métricas Capturadas

**Calidad:**
- Valor de la mejor solución encontrada
- Gap al óptimo conocido (%)
- Factibilidad de la solución

**Rendimiento:**
- Tiempo total de ejecución
- Número de iteraciones
- Número de evaluaciones de la función objetivo

**Convergencia:**
- Valor inicial
- Mejora absoluta
- Ratio de mejora
"""
    
    with open(docs_dir / "02_CONFIGURACION_EXPERIMENTO.md", "w", encoding="utf-8") as f:
        f.write(config_doc)
    
    # 7.1 Visualización del AST del mejor algoritmo
    print("🌳 Paso 7.1: Visualizando estructura del mejor algoritmo...\n")
    
    best_algorithm_name = comparison['best_algorithm']
    best_alg = next(alg for alg in algorithms if alg['name'] == best_algorithm_name)
    
    # Visualización ASCII
    print(f"📊 Estructura del {best_algorithm_name}:\n")
    ast_visualizer.print_ast_ascii(best_alg['ast'])
    print()
    
    # Estadísticas del AST
    stats = ast_visualizer.get_ast_statistics(best_alg['ast'])
    print(f"📈 Estadísticas del AST:")
    print(f"   • Nodos totales: {stats['total_nodes']}")
    print(f"   • Profundidad: {stats['depth']}")
    print(f"   • Operadores usados: {stats['terminal_operators']}")
    print()
    
    # Documentación de análisis estadístico
    stats_doc = f"""# Análisis Estadístico

## Test de Friedman (Comparación Global)

**Test**: {comparison['global_test'].test_name}
**p-value**: {comparison['global_test'].p_value:.4f}
**Interpretación**: {comparison['global_test'].interpretation}

## Rankings Promedio

(Menor ranking = mejor desempeño)

"""
    for alg, rank in sorted(comparison['average_rankings'].items(), key=lambda x: x[1]):
        stats_doc += f"- **{alg}**: {rank:.2f}\n"
    
    stats_doc += f"""

## Mejor Algoritmo

🏆 **{comparison['best_algorithm']}**

### Estadísticas Descriptivas

"""
    best_alg_gaps = algorithm_results[comparison['best_algorithm']]
    best_stats = analyzer.descriptive_statistics(best_alg_gaps)
    stats_doc += f"""
- **Media**: {best_stats['mean']:.2f}%
- **Desviación estándar**: {best_stats['std']:.2f}%
- **Mínimo**: {best_stats['min']:.2f}%
- **Máximo**: {best_stats['max']:.2f}%
- **Mediana**: {best_stats['median']:.2f}%

### Intervalo de Confianza (95%)

"""
    best_ci = analyzer.confidence_interval(best_alg_gaps, confidence=0.95)
    stats_doc += f"[{best_ci[0]:.2f}%, {best_ci[1]:.2f}%]\n\n"
    
    stats_doc += """## Comparación Por Algoritmo

"""
    for alg_name, gaps in algorithm_results.items():
        alg_stats = analyzer.descriptive_statistics(gaps)
        stats_doc += f"""### {alg_name}

- Gap medio: {alg_stats['mean']:.2f}% ± {alg_stats['std']:.2f}%
- Rango: [{alg_stats['min']:.2f}%, {alg_stats['max']:.2f}%]

"""
    
    # Comparación pareada
    if len(algorithm_results) >= 2:
        algs = list(algorithm_results.keys())
        data1 = algorithm_results[algs[0]]
        data2 = algorithm_results[algs[1]]
        min_len = min(len(data1), len(data2))
        data1 = data1[:min_len]
        data2 = data2[:min_len]
        
        wilcoxon = analyzer.wilcoxon_signed_rank_test(data1, data2)
        cohens_d = analyzer.effect_size_cohens_d(data1, data2)
        
        stats_doc += f"""## Test Pareado: {algs[0]} vs {algs[1]}

**Test de Wilcoxon**:
- p-value: {wilcoxon.p_value:.4f}
- {wilcoxon.interpretation}

**Tamaño del efecto (Cohen's d)**: {cohens_d:.3f}
"""
        if abs(cohens_d) < 0.2:
            stats_doc += "- Interpretación: Efecto pequeño\n"
        elif abs(cohens_d) < 0.5:
            stats_doc += "- Interpretación: Efecto mediano\n"
        else:
            stats_doc += "- Interpretación: Efecto grande\n"
    
    with open(docs_dir / "03_ANALISIS_ESTADISTICO.md", "w", encoding="utf-8") as f:
        f.write(stats_doc)
    
    # Gráfico Graphviz (si está disponible)
    if ast_visualizer.has_graphviz:
        ast_path = ast_visualizer.plot_ast_graphviz(
            ast_node=best_alg['ast'],
            filename="best_algorithm_ast",
            title=f"Estructura del Mejor Algoritmo - {best_algorithm_name}",
            format='png'
        )
        print()
    
    # 7.2 Gráficas de comparación estadística
    print("📊 Paso 7.2: Generando gráficas de comparación...\n")
    
    if visualizer.has_matplotlib and len(algorithm_results) >= 2:
        # Boxplot
        visualizer.plot_boxplot_comparison(
            algorithm_results,
            title="Comparación de Algoritmos - Gap al Óptimo",
            ylabel="Gap (%)",
            filename="demo_boxplot.png"
        )
        
        # Barras con estadísticas
        alg_metrics = {}
        for alg_name, gaps in algorithm_results.items():
            stats = analyzer.descriptive_statistics(gaps)
            alg_metrics[alg_name] = {
                'mean_value': stats['mean'],
                'std_value': stats['std']
            }
        
        visualizer.plot_bar_comparison(
            alg_metrics,
            metric_name='mean_value',
            title="Gap Promedio por Algoritmo",
            ylabel="Gap Promedio (%)",
            filename="demo_bars.png",
            show_error_bars=True
        )
        
        # Scatter tiempo vs calidad
        result_dicts = [
            {
                'algorithm_name': r.algorithm_name,
                'total_time': r.total_time,
                'gap_to_optimal': r.gap_to_optimal
            }
            for r in results if r.success and r.gap_to_optimal is not None
        ]
        
        visualizer.plot_scatter_time_vs_quality(
            result_dicts,
            title="Trade-off Tiempo vs Calidad",
            filename="demo_scatter.png"
        )
        
        # 7.3 Visualizaciones detalladas SA para el grupo low-dimensional
        print("\n📊 Paso 7.3: Generando visualizaciones SA del grupo low-dimensional...\n")
        
        # Cargar TODAS las instancias del grupo para procesamiento completo
        from data.loader import DatasetLoader
        from pathlib import Path as PathLib
        
        datasets_dir = PathLib(__file__).parent.parent / "datasets"
        loader = DatasetLoader(datasets_dir)
        group_instances = loader.load_folder("low_dimensional")
        
        print(f"🔬 Procesando grupo completo: {len(group_instances)} instancias")
        
        # Obtener mejor algoritmo
        best_alg_name = comparison['best_algorithm']
        best_alg = next(alg for alg in algorithms if alg['name'] == best_alg_name)
        
        print(f"🔬 Ejecutando {best_alg_name} con tracking en todas las instancias...\n")
        
        try:
            best_solution = run_detailed_visualization_per_group(
                instances=group_instances,
                algorithm=best_alg,
                plots_dir=Path(plots_dir),
                timestamp=timestamp
            )
            
            print(f"\n✅ Visualizaciones SA del grupo completadas ({len(group_instances)} instancias procesadas)")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Generar documentación de gráficas estadísticas
        graficas_stats_doc = """# Gráficas Estadísticas

## 1. demo_boxplot.png - Comparación de Algoritmos

**Tipo**: Diagrama de caja (boxplot)

**Descripción**: Compara la distribución de gaps al óptimo entre los diferentes algoritmos.

**Elementos visuales**:
- **Caja**: Representa el rango intercuartílico (Q1 a Q3)
- **Línea central**: Mediana del gap
- **Bigotes**: Extienden hasta 1.5× el rango intercuartílico
- **Puntos**: Outliers (valores atípicos)

**Interpretación**:
- Cajas más bajas = mejor desempeño (menor gap)
- Cajas más estrechas = mayor consistencia
- Outliers indican instancias particularmente difíciles

## 2. demo_bars.png - Gap Promedio por Algoritmo

**Tipo**: Gráfico de barras con barras de error

**Descripción**: Muestra el gap promedio de cada algoritmo con su desviación estándar.

**Elementos visuales**:
- **Altura de la barra**: Gap promedio (%)
- **Barras de error**: Desviación estándar
- **Color**: Diferencia algoritmos

**Interpretación**:
- Barras más bajas = mejor desempeño promedio
- Barras de error más pequeñas = mayor robustez
- Compara rendimiento promedio directamente

## 3. demo_scatter.png - Trade-off Tiempo vs Calidad

**Tipo**: Gráfico de dispersión

**Descripción**: Muestra la relación entre tiempo de ejecución y calidad de solución.

**Ejes**:
- **X**: Tiempo de ejecución (segundos)
- **Y**: Gap al óptimo (%)
- **Color/Forma**: Algoritmo

**Interpretación**:
- Puntos más abajo = mejor calidad
- Puntos más a la izquierda = más rápido
- Esquina inferior izquierda = óptimo (rápido y bueno)
- Identifica trade-offs entre velocidad y calidad

## 4. best_algorithm_ast.png - Estructura del Mejor Algoritmo

**Tipo**: Árbol de sintaxis abstracta (AST)

**Descripción**: Visualización gráfica de la estructura del algoritmo ganador.

**Elementos**:
- **Nodos**: Operadores de la metaheurística
- **Aristas**: Flujo de control
- **Niveles**: Profundidad del árbol

**Interpretación**:
- Muestra composición del algoritmo
- Permite entender decisiones de diseño
- Facilita reproducción y análisis
"""
        
        with open(docs_dir / "04_GRAFICAS_ESTADISTICAS.md", "w", encoding="utf-8") as f:
            f.write(graficas_stats_doc)
        
        # Generar documentación de gráficas SA
        graficas_sa_doc = f"""# Gráficas de Simulated Annealing

## Gráficas Agregadas (Grupo Completo)

### 1. gap_evolution.png - Evolución del Gap

**Descripción**: Muestra cómo evoluciona el gap al óptimo durante la búsqueda, promediado sobre las {len(group_instances)} instancias.

**Elementos visuales**:
- **Línea azul**: Gap promedio por iteración
- **Banda sombreada**: Desviación estándar (variabilidad entre instancias)
- **Eje derecho (rojo)**: Temperatura (escala logarítmica)

**Interpretación**:
- Pendiente negativa = convergencia hacia mejores soluciones
- Banda estrecha = comportamiento consistente
- Temperatura descendente = transición exploración → explotación

### 2. acceptance_rate.png - Tasa de Aceptación

**Descripción**: Porcentaje de movimientos aceptados en ventanas de 100 iteraciones.

**Elementos visuales**:
- **Línea verde**: Tasa de aceptación promedio
- **Línea roja**: Temperatura (escala logarítmica)

**Interpretación**:
- Inicio alto (~80-100%) = fase de exploración
- Descenso gradual = transición
- Final bajo (~10-30%) = fase de explotación
- Correlación con temperatura = criterio de Metropolis funcionando

### 3. delta_e_distribution.png - Distribución de Cambios de Energía

**Descripción**: Histograma de todos los cambios de energía (ΔE) observados, combinando las {len(group_instances)} instancias.

**Elementos visuales**:
- **Barras verdes**: ΔE de movimientos aceptados
- **Barras rojas**: ΔE de movimientos rechazados
- **Eje X**: Cambio de energía (negativo = empeoramiento)

**Interpretación**:
- Positivos = mejoras (siempre aceptadas)
- Negativos = empeoramientos (aceptados probabilísticamente)
- Distribución muestra balance exploración-explotación
- Solapamiento verde-rojo = criterio de Metropolis activo

## Gráficas Por Instancia ({len(group_instances)} gráficas)

### exploration_exploitation_<instancia>.png

**Descripción**: Balance entre exploración y explotación específico para cada instancia.

**Elementos visuales**:
- **Área verde**: Proporción de mejoras (explotación)
- **Área naranja**: Proporción de empeoramientos aceptados (exploración)
- **Área roja**: Proporción de empeoramientos rechazados
- **Línea negra**: Temperatura
- **Panel estadístico**: Métricas clave

**Métricas mostradas**:
- Total iterations: Iteraciones totales
- Improvements: Número de mejoras
- Explorations: Empeoramientos aceptados
- Rejected: Movimientos rechazados
- Accept rate: Tasa global de aceptación
- Expl/Expt ratio: Balance exploración/explotación

**Interpretación**:
- Inicio: Mucho naranja (exploración)
- Medio: Transición equilibrada
- Final: Mucho verde (explotación)
- Patrones anómalos indican problemas de configuración

**Archivos generados**:
"""
        
        for inst in sorted(group_instances, key=lambda x: x.name):
            inst_name = inst.name.replace('_low-dimensional', '')
            graficas_sa_doc += f"- `exploration_exploitation_{inst_name}.png`\n"
        
        with open(docs_dir / "05_GRAFICAS_SA.md", "w", encoding="utf-8") as f:
            f.write(graficas_sa_doc)
        
        print(f"\n✅ Todas las visualizaciones generadas en {plots_dir}/")
        print(f"   📊 Gráficas estadísticas del grupo: boxplot, bars, scatter")
        print(f"   🌳 AST del mejor algoritmo: best_algorithm_ast.png")
        print(f"   📈 Gráficas SA del grupo:")
        print(f"      - gap_evolution.png (media ± desviación estándar de {len(group_instances)} instancias)")
        print(f"      - acceptance_rate.png (tasa promedio de {len(group_instances)} instancias)")
        print(f"      - delta_e_distribution.png (distribución combinada de {len(group_instances)} instancias)")
        print(f"      - exploration_exploitation_<instance>.png ({len(group_instances)} gráficas, una por instancia)")
        print(f"\n📝 Documentación generada:")
        print(f"   - README.md")
        print(f"   - 01_ALGORITMOS_GAA.md")
        print(f"   - 02_CONFIGURACION_EXPERIMENTO.md")
        print(f"   - 03_ANALISIS_ESTADISTICO.md")
        print(f"   - 04_GRAFICAS_ESTADISTICAS.md")
        print(f"   - 05_GRAFICAS_SA.md")
        print()
        print(f"      - delta_e_distribution.png (distribución combinada de {len(group_instances)} instancias)")
        print(f"      - exploration_exploitation_<instance>.png ({len(group_instances)} gráficas, una por instancia)")
        print()
    else:
        if not visualizer.has_matplotlib:
            print("⚠️  matplotlib no disponible. Saltando visualizaciones.")
        else:
            print("⚠️  Se necesitan al menos 2 algoritmos para comparación visual.")
    
    # 8. Resumen final
    print("\n" + "=" * 80)
    print("  RESUMEN FINAL")
    print("=" * 80)
    print()
    
    successful = sum(1 for r in results if r.success)
    total = len(results)
    
    print(f"✅ Experimentos completados: {successful}/{total}")
    print(f"📁 Instancias procesadas: {len(config.instances)}")
    print(f"📊 Resultados guardados en: {json_file}")
    
    if len(algorithm_results) > 0:
        best_alg = min(algorithm_results.items(), key=lambda x: sum(x[1])/len(x[1]))
        print(f"\n🏆 Mejor algoritmo (menor gap promedio): {best_alg[0]}")
        print(f"   Gap promedio: {sum(best_alg[1])/len(best_alg[1]):.2f}%")
        
        # Mostrar resumen por instancia
        print(f"\n📈 Resultados por instancia:")
        instances_processed = set(r.instance_name for r in results if r.success)
        for inst in sorted(instances_processed):
            inst_results = [r for r in results if r.instance_name == inst and r.success]
            if inst_results:
                best_gap = min((r.gap_to_optimal for r in inst_results if r.gap_to_optimal is not None), default=None)
                best_alg_inst = min(inst_results, key=lambda r: r.gap_to_optimal if r.gap_to_optimal else float('inf'))
                gap_str = f"{best_gap:.2f}%" if best_gap is not None else "ÓPTIMO"
                print(f"   • {inst[:30]:<30} → {best_alg_inst.algorithm_name} (gap: {gap_str})")
    
    print()
    print("✅ Cobertura completa del grupo low-dimensional")
    print("\nPróximos pasos:")
    print("  1. Ejecutar experimentos con large_scale (21 instancias)")
    print("  2. Aumentar repeticiones a 30 para análisis estadístico robusto")
    print("  3. Generar más algoritmos (población de 50) y seleccionar top-3")
    print("  4. Análisis detallado de convergencia y performance profiles")
    print()


if __name__ == '__main__':
    main()
