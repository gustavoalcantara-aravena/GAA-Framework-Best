#!/usr/bin/env python3
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


def run_detailed_visualization_per_instance(instance, algorithm, plots_dir, timestamp):
    """
    Ejecuta SA con tracking detallado y genera 4 visualizaciones por instancia
    
    Args:
        instance: KnapsackProblem
        algorithm: dict con 'name', 'ast', 'interpreter'
        plots_dir: directorio base
        timestamp: timestamp para subcarpetas
    """
    # Crear subcarpeta para esta instancia
    instance_dir = plots_dir / f"{instance.name}_{timestamp}"
    instance_dir.mkdir(parents=True, exist_ok=True)
    
    # Variables de tracking
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
        idx = rng.integers(0, instance.n)
        neighbor.selection[idx] = 1 - neighbor.selection[idx]
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
    
    # Generar visualizaciones
    visualizer = ResultsVisualizer(output_dir=str(instance_dir))
    
    # 1. Gap evolution
    visualizer.plot_gap_evolution(
        best_values=best_values_history,
        optimal_value=instance.optimal_value,
        title=f"Gap Evolution - {instance.name}",
        filename="gap_evolution.png",
        show_improvements=True,
        temperature_history=temperature_history
    )
    
    # 2. Acceptance rate
    visualizer.plot_acceptance_rate(
        acceptance_history=acceptance_history,
        window_size=100,
        title=f"Acceptance Rate - {instance.name}",
        filename="acceptance_rate.png",
        temperature_history=temperature_history
    )
    
    # 3. Delta E distribution
    acceptance_decisions = [bool(x) for x in acceptance_history]
    visualizer.plot_delta_e_distribution(
        delta_e_values=delta_e_history,
        acceptance_decisions=acceptance_decisions,
        title=f"ΔE Distribution - {instance.name}",
        filename="delta_e_distribution.png",
        bins=50
    )
    
    # 4. Exploration-exploitation balance
    visualizer.plot_exploration_exploitation_balance(
        delta_e_values=delta_e_history,
        acceptance_decisions=acceptance_decisions,
        temperature_history=temperature_history,
        title=f"Exploration-Exploitation Balance - {instance.name}",
        filename="exploration_exploitation_balance.png",
        window_size=100
    )
    
    return best


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
    
    # Cargar TODAS las instancias low-dimensional
    from data.loader import DatasetLoader
    from pathlib import Path
    
    # datasets_dir debe apuntar a la carpeta que CONTIENE low_dimensional
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    all_instances = loader.load_folder("low_dimensional")
    
    # Usar TODAS las instancias low-dimensional
    instance_names = [inst.name for inst in all_instances]
    
    print(f"📁 Instancias low-dimensional cargadas: {len(instance_names)}")
    for name in sorted(instance_names):
        print(f"   • {name}")
    print()
    
    config = ExperimentConfig(
        name="low_dimensional_full_test",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=3,  # 3 repeticiones para análisis estadístico
        max_time_seconds=120.0,
        output_dir="output/low_dimensional_full_test"
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
    
    # Crear carpeta UNIFICADA con dataset_timestamp para TODAS las visualizaciones
    plots_dir = f"output/low_dimensional_{timestamp}"
    visualizer = ResultsVisualizer(output_dir=plots_dir)
    
    # 7.1 Visualización del AST del mejor algoritmo (en la MISMA carpeta)
    print("🌳 Paso 7.1: Visualizando estructura del mejor algoritmo...\n")
    
    best_algorithm_name = comparison['best_algorithm']
    best_alg = next(alg for alg in algorithms if alg['name'] == best_algorithm_name)
    
    # Crear visualizador de AST en la MISMA carpeta plots_dir
    ast_visualizer = ASTVisualizer(output_dir=plots_dir)
    
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
    
    # Gráfico Graphviz (si está disponible) - guardado en plots_dir
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
        
        # 7.3 Visualizaciones detalladas POR CADA INSTANCIA
        print("\n📊 Paso 7.3: Generando visualizaciones detalladas por instancia...\n")
        
        # Obtener mejor algoritmo
        best_alg_name = comparison['best_algorithm']
        best_alg = next(alg for alg in algorithms if alg['name'] == best_alg_name)
        
        # Cargar instancias
        from data.loader import DatasetLoader
        from pathlib import Path as PathLib
        
        datasets_dir = PathLib(__file__).parent.parent / "datasets"
        loader = DatasetLoader(datasets_dir)
        all_instances = loader.load_folder("low_dimensional")
        
        print(f"🔬 Ejecutando {best_alg_name} en cada instancia con tracking completo...\n")
        
        for i, instance in enumerate(sorted(all_instances, key=lambda x: x.n), 1):
            print(f"[{i}/{len(all_instances)}] {instance.name} (n={instance.n})...", end=" ", flush=True)
            
            try:
                best_solution = run_detailed_visualization_per_instance(
                    instance=instance,
                    algorithm=best_alg,
                    plots_dir=Path(plots_dir),
                    timestamp=timestamp
                )
                
                gap = ((instance.optimal_value - best_solution.value) / instance.optimal_value) * 100 if instance.optimal_value > 0 else 0
                status = "✅ ÓPTIMO" if gap == 0 else f"Gap: {gap:.2f}%"
                print(f"{status} - 4 gráficas generadas")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n✅ Visualizaciones por instancia completadas")
        
        print(f"\n✅ Todas las visualizaciones generadas en {plots_dir}/")
        print(f"   📊 Gráficas estadísticas: boxplot, bars, scatter")
        print(f"   🌳 AST del mejor algoritmo: best_algorithm_ast.png")
        print(f"   📁 Carpetas por instancia: {len(all_instances)} carpetas con 4 gráficas cada una")
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
