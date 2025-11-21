#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de Experimentación Multi-Grupo - KBP-SA
Demuestra el módulo experimentation/ para análisis estadístico

Este script ejecuta experimentos secuencialmente en múltiples grupos de instancias:
1. low_dimensional
2. large_scale

Para cada grupo:
1. Experimentos con múltiples algoritmos
2. Análisis estadístico completo
3. Visualizaciones
4. Reporte de resultados
5. TimeTracker independiente
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
from experimentation.time_tracker import TimeTracker
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from metaheuristic.sa_core import SimulatedAnnealing
from core.solution import KnapsackSolution
from data.loader import DatasetLoader
import numpy as np


def run_detailed_visualization_per_group(instances, algorithm, plots_dir, group_name):
    """
    Ejecuta SA en TODAS las instancias del grupo con tracking detallado y genera
    4 visualizaciones agregadas representativas del grupo completo

    Args:
        instances: lista de KnapsackProblem (todas las instancias del grupo)
        algorithm: dict con 'name', 'ast', 'interpreter'
        plots_dir: directorio donde guardar las gráficas
        group_name: nombre del grupo (para títulos)

    Returns:
        best_solution: mejor solución encontrada entre todas las instancias
    """
    # Guardar directamente en la carpeta principal (no subcarpeta)
    output_dir = plots_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Ejecutando SA en {len(instances)} instancias del grupo...", flush=True)

    # Variables para almacenar tracking de todas las instancias
    all_best_values = []
    all_acceptances = []
    all_temperatures = []
    all_delta_e = []

    best_overall = None

    # Ejecutar SA en cada instancia del grupo
    for idx, instance in enumerate(instances, 1):
        print(f"    [{idx}/{len(instances)}] Procesando {instance.name}...", end=" ", flush=True)

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
        print(f"Gap: {gap:.2f}%", flush=True)

    print(f"\n  Agregando datos de {len(instances)} instancias...", flush=True)

    # Agregar datos de todas las instancias
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

    # Calcular media de gaps
    gap_mean = np.mean(normalized_gaps, axis=0)

    # Acceptance Rate: promediar tasas de aceptación
    max_length_acc = max(len(acc) for acc in all_acceptances)
    padded_acceptances = []
    for acc in all_acceptances:
        if len(acc) < max_length_acc:
            acc_padded = acc + [acc[-1]] * (max_length_acc - len(acc))
        else:
            acc_padded = acc
        padded_acceptances.append(acc_padded)

    acceptance_mean = np.mean(padded_acceptances, axis=0).tolist()

    # Usar temperatura de una instancia representativa
    representative_temperature = all_temperatures[len(all_temperatures) // 2]

    # Delta E Distribution: concatenar todos los valores
    all_delta_e_combined = []
    all_acceptances_combined = []
    for delta_list, acc_list in zip(all_delta_e, all_acceptances):
        all_delta_e_combined.extend(delta_list)
        all_acceptances_combined.extend(acc_list)

    # Generar visualizaciones agregadas
    visualizer = ResultsVisualizer(output_dir=str(output_dir))

    print(f"\n  Generando visualizaciones agregadas del grupo...", flush=True)

    # 1. Gap evolution
    synthetic_optimal = 100
    synthetic_best_values = [(synthetic_optimal * (1 - gap/100)) for gap in gap_mean]

    visualizer.plot_gap_evolution(
        best_values=synthetic_best_values,
        optimal_value=synthetic_optimal,
        title=f"Gap Evolution - {group_name} (Promedio de todas las instancias)",
        filename="gap_evolution.png",
        show_improvements=True,
        temperature_history=representative_temperature
    )

    # 2. Acceptance rate
    visualizer.plot_acceptance_rate(
        acceptance_history=acceptance_mean,
        window_size=100,
        title=f"Acceptance Rate - {group_name} (Promedio de todas las instancias)",
        filename="acceptance_rate.png",
        temperature_history=representative_temperature
    )

    # 3. Delta E distribution
    acceptance_decisions_combined = [bool(x) for x in all_acceptances_combined]
    visualizer.plot_delta_e_distribution(
        delta_e_values=all_delta_e_combined,
        acceptance_decisions=acceptance_decisions_combined,
        title=f"ΔE Distribution - {group_name} (Todas las instancias)",
        filename="delta_e_distribution.png",
        bins=50
    )

    # 4. Exploration-exploitation balance por instancia
    print(f"\n  Generando gráficas exploration-exploitation por instancia...", flush=True)

    for idx, (instance, delta_list, acc_list, temp_list) in enumerate(zip(instances, all_delta_e, all_acceptances, all_temperatures), 1):
        # Limpiar nombre de instancia
        instance_name = instance.name.replace('_low-dimensional', '').replace('_large-scale', '')

        acceptance_decisions = [bool(x) for x in acc_list]

        visualizer.plot_exploration_exploitation_balance(
            delta_e_values=delta_list,
            acceptance_decisions=acceptance_decisions,
            temperature_history=temp_list,
            title=f"Exploration-Exploitation Balance - {instance_name}",
            filename=f"exploration_exploitation_{instance_name}.png",
            window_size=100
        )

        print(f"    [{idx}/{len(instances)}] {instance_name}: ✓", flush=True)

    print(f"  ✅ {3 + len(instances)} gráficas SA generadas (3 agregadas + {len(instances)} por instancia)", flush=True)

    return best_overall


def process_group(group_name, folder_name, algorithms, timestamp, global_tracker):
    """
    Procesa un grupo completo de instancias: ejecuta experimentos, análisis y visualizaciones.

    Args:
        group_name: nombre descriptivo del grupo (ej: "Low-Dimensional")
        folder_name: nombre de la carpeta de datasets (ej: "low_dimensional")
        algorithms: lista de algoritmos generados
        timestamp: timestamp global de la ejecución
        global_tracker: TimeTracker global

    Returns:
        dict con resultados del grupo
    """

    with global_tracker.track(f"Procesando grupo {group_name}"):
        print("\n" + "=" * 80, flush=True)
        print(f"  PROCESANDO GRUPO: {group_name.upper()}", flush=True)
        print("=" * 80, flush=True)
        print(flush=True)

        # Crear directorio de salida específico del grupo
        plots_dir = f"output/plots_{folder_name}_{timestamp}"

        # Inicializar TimeTracker local para este grupo
        tracker = TimeTracker(output_file="time_tracking.md", output_dir=plots_dir)

        with tracker.track(f"Ejecución completa del experimento - {group_name}"):

            # 2. Configurar experimento
            with tracker.track("Paso 2: Configurando experimento"):
                print(f"⚙️  Paso 2: Configurando experimento para {group_name}...\n", flush=True)

                # Cargar instancias del grupo
                datasets_dir = Path(__file__).parent.parent / "datasets"
                loader = DatasetLoader(datasets_dir)
                all_instances = loader.load_folder(folder_name)

                # Usar nombres de todas las instancias
                instance_names = [inst.name for inst in all_instances]

                print(f"📁 Instancias {group_name} encontradas: {len(instance_names)}", flush=True)
                for name in instance_names:
                    print(f"   • {name}", flush=True)
                print(flush=True)

                config = ExperimentConfig(
                    name=f"{folder_name}_experiment",
                    instances=instance_names,
                    algorithms=algorithms,
                    repetitions=1,
                    max_time_seconds=60.0,
                    output_dir=f"output/{folder_name}_experiments"
                )

                print(f"⚙️  Configuración:", flush=True)
                print(f"  • Instancias: {len(config.instances)}", flush=True)
                print(f"  • Algoritmos: {len(config.algorithms)}", flush=True)
                print(f"  • Repeticiones: {config.repetitions}", flush=True)
                print(f"  • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}", flush=True)
                print(flush=True)

                tracker.update_current(
                    instances=len(config.instances),
                    total_experiments=len(config.instances) * len(config.algorithms) * config.repetitions
                )

            # 3. Ejecutar experimentos
            with tracker.track("Paso 3: Ejecutando experimentos",
                             total_ejecuciones=len(config.instances) * len(config.algorithms) * config.repetitions):
                print(f"🚀 Paso 3: Ejecutando experimentos con {group_name}...\n", flush=True)

                runner = ExperimentRunner(config)
                runner.load_instances(folder_name)

                if not runner.problems:
                    print("❌ No se pudieron cargar instancias. Abortando este grupo.", flush=True)
                    tracker.finish_process("Error", error="No se pudieron cargar instancias")
                    return None

                results = runner.run_all(verbose=True)

                tracker.update_current(
                    experiments_completed=len(results),
                    successful=sum(1 for r in results if r.success)
                )

            # 4. Guardar resultados
            with tracker.track("Paso 4: Guardando resultados"):
                print(f"\n💾 Paso 4: Guardando resultados de {group_name}...\n", flush=True)

                json_file = runner.save_results()

                tracker.update_current(output_file=str(json_file))

            # 5. Análisis estadístico
            with tracker.track("Paso 5: Análisis estadístico"):
                print(f"\n📊 Paso 5: Análisis estadístico de {group_name}...\n", flush=True)

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

                        print(f"Algoritmo: {alg_name}", flush=True)

                        # Estadísticas descriptivas
                        if gaps:
                            stats = analyzer.descriptive_statistics(gaps)
                            print(f"  Gap (%): media={stats['mean']:.2f} ± {stats['std']:.2f}, "
                                  f"min={stats['min']:.2f}, max={stats['max']:.2f}", flush=True)

                            # Intervalo de confianza
                            ci = analyzer.confidence_interval(gaps, confidence=0.95)
                            print(f"  IC 95%: [{ci[0]:.2f}, {ci[1]:.2f}]", flush=True)

                        if times:
                            time_stats = analyzer.descriptive_statistics(times)
                            print(f"  Tiempo (s): media={time_stats['mean']:.3f} ± {time_stats['std']:.3f}", flush=True)

                        print(flush=True)

                tracker.update_current(algorithms_analyzed=len(algorithm_results))

            # 6. Comparación entre algoritmos
            comparison = None
            if len(algorithm_results) >= 2:
                with tracker.track("Paso 6: Comparación estadística entre algoritmos"):
                    print(f"🔬 Paso 6: Comparación estadística entre algoritmos ({group_name})...\n", flush=True)

                    comparison = analyzer.compare_multiple_algorithms(
                        algorithm_results,
                        test_type="friedman"
                    )

                    print(f"Test: {comparison['global_test'].test_name}", flush=True)
                    print(f"  p-value: {comparison['global_test'].p_value:.4f}", flush=True)
                    print(f"  {comparison['global_test'].interpretation}", flush=True)
                    print(flush=True)

                    print("Rankings promedio (menor = mejor):", flush=True)
                    for alg, rank in sorted(comparison['average_rankings'].items(), key=lambda x: x[1]):
                        print(f"  {rank:.2f}  {alg}", flush=True)
                    print(flush=True)

                    print(f"🏆 Mejor algoritmo: {comparison['best_algorithm']}", flush=True)
                    print(flush=True)

                    # Test pareado
                    if len(algorithm_results) >= 2:
                        algs = list(algorithm_results.keys())
                        data1 = algorithm_results[algs[0]]
                        data2 = algorithm_results[algs[1]]

                        min_len = min(len(data1), len(data2))
                        data1 = data1[:min_len]
                        data2 = data2[:min_len]

                        print(f"\nComparación pareada: {algs[0]} vs {algs[1]}", flush=True)

                        wilcoxon = analyzer.wilcoxon_signed_rank_test(data1, data2)
                        print(f"  Wilcoxon: p={wilcoxon.p_value:.4f}", flush=True)
                        print(f"  {wilcoxon.interpretation}", flush=True)

                        cohens_d = analyzer.effect_size_cohens_d(data1, data2)
                        print(f"  Cohen's d: {cohens_d:.3f} ", end="", flush=True)
                        if abs(cohens_d) < 0.2:
                            print("(efecto pequeño)", flush=True)
                        elif abs(cohens_d) < 0.5:
                            print("(efecto mediano)", flush=True)
                        else:
                            print("(efecto grande)", flush=True)
                        print(flush=True)

                    tracker.update_current(best_algorithm=comparison['best_algorithm'])

            # 7. Visualización
            if comparison:
                with tracker.track("Paso 7: Generando visualizaciones y documentación"):
                    print(f"📈 Paso 7: Generando visualizaciones de {group_name}...\n", flush=True)

                    visualizer = ResultsVisualizer(output_dir=plots_dir)
                    ast_visualizer = ASTVisualizer(output_dir=plots_dir)

                    docs_dir = Path(plots_dir)
                    docs_dir.mkdir(parents=True, exist_ok=True)

                    print("📝 Generando documentación del experimento...\n", flush=True)

                    # README principal
                    readme_content = f"""# Reporte de Experimentación - {group_name}
**Fecha**: {datetime.now().strftime("%d de %B de %Y, %H:%M:%S")}
**Grupo**: {group_name}

## Resumen Ejecutivo

Este experimento evalúa {len(algorithms)} algoritmos sobre {len(config.instances)} instancias del grupo {group_name}.

### Resultados Principales

- **Mejor algoritmo**: {comparison['best_algorithm']}
- **Instancias procesadas**: {len(config.instances)}
- **Ejecuciones totales**: {len(results)}
- **Tasa de éxito**: {sum(1 for r in results if r.success)}/{len(results)} ({100*sum(1 for r in results if r.success)/len(results):.1f}%)
"""

                    with open(docs_dir / "README.md", "w", encoding="utf-8") as f:
                        f.write(readme_content)

                    # 7.1 Visualización del AST del mejor algoritmo
                    print(f"🌳 Paso 7.1: Visualizando estructura del mejor algoritmo ({group_name})...\n", flush=True)

                    best_algorithm_name = comparison['best_algorithm']
                    best_alg = next(alg for alg in algorithms if alg['name'] == best_algorithm_name)

                    print(f"📊 Estructura del {best_algorithm_name}:\n", flush=True)
                    ast_visualizer.print_ast_ascii(best_alg['ast'])
                    print(flush=True)

                    stats = ast_visualizer.get_ast_statistics(best_alg['ast'])
                    print(f"📈 Estadísticas del AST:", flush=True)
                    print(f"   • Nodos totales: {stats['total_nodes']}", flush=True)
                    print(f"   • Profundidad: {stats['depth']}", flush=True)
                    print(f"   • Operadores usados: {stats['terminal_operators']}", flush=True)
                    print(flush=True)

                    if ast_visualizer.has_graphviz:
                        ast_visualizer.plot_ast_graphviz(
                            ast_node=best_alg['ast'],
                            filename="best_algorithm_ast",
                            title=f"Estructura del Mejor Algoritmo - {best_algorithm_name}",
                            format='png'
                        )

                    # 7.2 Gráficas de comparación estadística
                    print(f"📊 Paso 7.2: Generando gráficas de comparación ({group_name})...\n", flush=True)

                    if visualizer.has_matplotlib and len(algorithm_results) >= 2:
                        # Boxplot
                        visualizer.plot_boxplot_comparison(
                            algorithm_results,
                            title=f"Comparación de Algoritmos - {group_name}",
                            ylabel="Gap (%)",
                            filename="demo_boxplot.png"
                        )

                        # Barras
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
                            title=f"Gap Promedio por Algoritmo - {group_name}",
                            ylabel="Gap Promedio (%)",
                            filename="demo_bars.png",
                            show_error_bars=True
                        )

                        # Scatter
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
                            title=f"Trade-off Tiempo vs Calidad - {group_name}",
                            filename="demo_scatter.png"
                        )

                        # 7.3 Visualizaciones SA
                        print(f"\n📊 Paso 7.3: Generando visualizaciones SA ({group_name})...\n", flush=True)

                        group_instances = loader.load_folder(folder_name)

                        print(f"🔬 Procesando grupo completo: {len(group_instances)} instancias", flush=True)
                        print(f"🔬 Ejecutando {best_alg['name']} con tracking...\n", flush=True)

                        try:
                            run_detailed_visualization_per_group(
                                instances=group_instances,
                                algorithm=best_alg,
                                plots_dir=Path(plots_dir),
                                group_name=group_name
                            )

                            print(f"\n✅ Visualizaciones SA completadas ({len(group_instances)} instancias)", flush=True)
                        except Exception as e:
                            print(f"❌ Error: {e}", flush=True)
                            import traceback
                            traceback.print_exc()

                        print(f"\n✅ Todas las visualizaciones generadas en {plots_dir}/", flush=True)
                        print(flush=True)

                    tracker.update_current(visualizations_generated=True, plots_dir=plots_dir)

            # 8. Resumen final del grupo
            print("\n" + "=" * 80, flush=True)
            print(f"  RESUMEN DEL GRUPO: {group_name.upper()}", flush=True)
            print("=" * 80, flush=True)
            print(flush=True)

            successful = sum(1 for r in results if r.success)
            total = len(results)

            print(f"✅ Experimentos completados: {successful}/{total}", flush=True)
            print(f"📁 Instancias procesadas: {len(config.instances)}", flush=True)
            print(f"📊 Resultados guardados en: {json_file}", flush=True)

            if comparison and len(algorithm_results) > 0:
                best_alg = min(algorithm_results.items(), key=lambda x: sum(x[1])/len(x[1]))
                print(f"\n🏆 Mejor algoritmo: {best_alg[0]}", flush=True)
                print(f"   Gap promedio: {sum(best_alg[1])/len(best_alg[1]):.2f}%", flush=True)
                print(flush=True)

        # Finalizar tracking del grupo
        tracker.finalize()
        print(f"📊 Time tracking del grupo guardado en: {tracker.output_path}\n", flush=True)

        return {
            'group_name': group_name,
            'folder_name': folder_name,
            'plots_dir': plots_dir,
            'results': results,
            'algorithm_results': algorithm_results if comparison else {},
            'comparison': comparison,
            'best_algorithm': comparison['best_algorithm'] if comparison else None,
            'json_file': json_file
        }


def main():
    print("=" * 80, flush=True)
    print("  DEMO: Módulo de Experimentación Multi-Grupo - KBP-SA", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)

    # Generar timestamp global
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Inicializar TimeTracker global
    global_tracker_dir = "output/time_tracker_global"
    global_tracker = TimeTracker(
        output_file=f"time_tracking_global_{timestamp}.md",
        output_dir=global_tracker_dir
    )

    with global_tracker.track("Ejecución completa de experimentos multi-grupo"):

        # 1. Generar algoritmos (UNA SOLA VEZ)
        with global_tracker.track("Paso 1: Generando algoritmos GAA", num_algorithms=3):
            print("🧬 Paso 1: Generando algoritmos GAA (compartidos para todos los grupos)...\n", flush=True)

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
                    print(f"✅ Algoritmo {i+1} generado", flush=True)
                    print(f"   Pseudocódigo:", flush=True)
                    for line in ast.to_pseudocode(indent=2).split('\n'):
                        print(f"   {line}", flush=True)
                    print(flush=True)

            global_tracker.update_current(algorithms_generated=len(algorithms))

        # Lista para almacenar resultados
        all_group_results = []

        # 2. Procesar grupo LOW-DIMENSIONAL
        low_dim_result = process_group(
            group_name="Low-Dimensional",
            folder_name="low_dimensional",
            algorithms=algorithms,
            timestamp=timestamp,
            global_tracker=global_tracker
        )

        if low_dim_result:
            all_group_results.append(low_dim_result)

        # 3. Procesar grupo LARGE-SCALE
        large_scale_result = process_group(
            group_name="Large-Scale",
            folder_name="large_scale",
            algorithms=algorithms,
            timestamp=timestamp,
            global_tracker=global_tracker
        )

        if large_scale_result:
            all_group_results.append(large_scale_result)

        # 4. Resumen global final
        print("\n" + "=" * 80, flush=True)
        print("  RESUMEN GLOBAL DE TODOS LOS GRUPOS", flush=True)
        print("=" * 80, flush=True)
        print(flush=True)

        for group_result in all_group_results:
            print(f"\n📊 {group_result['group_name']}:", flush=True)
            print(f"   • Mejor algoritmo: {group_result['best_algorithm']}", flush=True)
            print(f"   • Resultados guardados en: {group_result['json_file']}", flush=True)
            print(f"   • Visualizaciones en: {group_result['plots_dir']}", flush=True)

        print(f"\n\n✅ TODOS LOS GRUPOS PROCESADOS EXITOSAMENTE", flush=True)
        print(f"📁 Carpetas de salida generadas:", flush=True)
        for group_result in all_group_results:
            print(f"   • {group_result['plots_dir']}", flush=True)

        print(f"\n📊 Time tracking global guardado en: {global_tracker.output_path}", flush=True)
        print(flush=True)

    # Finalizar tracking global
    global_tracker.finalize()

    print("\n" + "=" * 80, flush=True)
    print("  EJECUCIÓN COMPLETADA", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)


if __name__ == '__main__':
    main()
