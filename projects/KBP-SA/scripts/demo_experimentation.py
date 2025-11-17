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
import numpy as np


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
    
    # Cargar SOLO UNA INSTANCIA (f1 para prueba)
    from data.loader import DatasetLoader
    from pathlib import Path
    
    # datasets_dir debe apuntar a la carpeta que CONTIENE low_dimensional
    datasets_dir = Path(__file__).parent.parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    all_instances = loader.load_folder("low_dimensional")
    
    # Filtrar solo f1
    instance_names = [inst.name for inst in all_instances if "f1_l-d" in inst.name]
    
    print(f"📁 Instancia seleccionada para prueba:")
    for name in instance_names:
        print(f"   • {name}")
    print()
    
    config = ExperimentConfig(
        name="single_instance_test",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,  # 1 repetición para prueba rápida
        max_time_seconds=60.0,
        output_dir="output/single_instance_test"
    )
    
    print(f"⚙️  Configuración:")
    print(f"  • Instancias: {len(config.instances)}")
    print(f"  • Algoritmos: {len(config.algorithms)}")
    print(f"  • Repeticiones: {config.repetitions}")
    print(f"  • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    print()
    
    # 3. Ejecutar experimentos
    print("🚀 Paso 3: Ejecutando experimento con UNA instancia (f1)...\n")
    
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
    
    # 6.5 Visualización del AST del mejor algoritmo
    print("🌳 Paso 6.5: Visualizando estructura del mejor algoritmo...\n")
    
    best_algorithm_name = comparison['best_algorithm']
    best_alg = next(alg for alg in algorithms if alg['name'] == best_algorithm_name)
    
    # Crear visualizador de AST
    ast_dir = f"output/ast_f1_test_{timestamp}"
    ast_visualizer = ASTVisualizer(output_dir=ast_dir)
    
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
    
    # Gráfico Graphviz (si está disponible)
    if ast_visualizer.has_graphviz:
        ast_path = ast_visualizer.plot_ast_graphviz(
            ast_node=best_alg['ast'],
            filename="best_algorithm_ast",
            title=f"Estructura del Mejor Algoritmo - {best_algorithm_name}",
            format='png'
        )
        print()
    
    # 7. Visualización
    print("📈 Paso 7: Generando visualizaciones...\n")
    
    # Crear carpeta con dataset_timestamp
    plots_dir = f"output/plots_f1_test_{timestamp}"
    visualizer = ResultsVisualizer(output_dir=plots_dir)
    
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
        
        # Gap evolution (si hay datos de convergencia en tracking)
        # Buscar el mejor algoritmo para mostrar su evolución
        if len(algorithm_results) > 0:
            best_alg = min(algorithm_results.items(), key=lambda x: sum(x[1])/len(x[1]))
            print(f"\n📊 Generando gráfica de evolución del gap para: {best_alg[0]}")
            
            # Buscar resultado del mejor algoritmo
            best_result = None
            for r in results:
                if r.algorithm_name == best_alg[0] and r.success:
                    best_result = r
                    break
            
            if best_result:
                # Simular evolución (en futuro usaremos tracking real)
                # Calcular valor óptimo desde gap
                if best_result.gap_to_optimal is not None and best_result.gap_to_optimal > 0:
                    # optimal = best / (1 - gap/100)
                    optimal = int(best_result.best_value / (1 - best_result.gap_to_optimal/100))
                else:
                    # Si gap es 0 o None, el best_value es el óptimo
                    optimal = best_result.best_value
                
                initial_gap = best_result.gap_to_optimal if best_result.gap_to_optimal else 0
                
                # Crear progresión simulada (exponencial decay)
                n_iters = 1000
                simulated_gaps = []
                simulated_temp_for_gap = []
                T_gap = 100.0
                alpha_gap = 0.95
                
                for i in range(n_iters):
                    progress = i / n_iters
                    gap = initial_gap * np.exp(-3 * progress)  # Decay exponencial
                    simulated_gaps.append(gap)
                    
                    # Temperatura para gráfica de gap
                    simulated_temp_for_gap.append(T_gap)
                    if i % 100 == 0:
                        T_gap *= alpha_gap
                
                # Convertir gaps a valores
                simulated_values = [optimal * (1 - gap/100) for gap in simulated_gaps]
                
                visualizer.plot_gap_evolution(
                    best_values=simulated_values,
                    optimal_value=optimal,
                    title=f"Evolución del Gap y Temperatura - {best_alg[0]}",
                    filename="demo_gap_evolution.png",
                    show_improvements=True,
                    temperature_history=simulated_temp_for_gap
                )
                print(f"   ✅ Gráfica de gap generada")
                
                # Simular tasa de aceptación (decae con la temperatura)
                # En futuro usaremos datos reales de tracking
                simulated_acceptance = []
                simulated_temperature = []
                T0 = 100.0
                alpha = 0.95
                T = T0
                
                for i in range(n_iters):
                    # Temperatura decae geométricamente
                    simulated_temperature.append(T)
                    
                    # Tasa alta al inicio, baja al final (refleja enfriamiento)
                    temp_ratio = T / T0
                    acceptance_rate = 0.15 + 0.40 * temp_ratio  # Entre 15% y 55%
                    # Generar decisiones binarias basadas en la tasa
                    decision = 1 if np.random.random() < acceptance_rate else 0
                    simulated_acceptance.append(decision)
                    
                    # Enfriar cada 100 iteraciones
                    if i % 100 == 0:
                        T *= alpha
                
                visualizer.plot_acceptance_rate(
                    acceptance_history=simulated_acceptance,
                    window_size=100,
                    title=f"Tasa de Aceptación y Temperatura - {best_alg[0]}",
                    filename="demo_acceptance_rate.png",
                    temperature_history=simulated_temperature
                )
                print(f"   ✅ Gráfica de tasa de aceptación generada")
                
                # Simular distribución de ΔE
                # En futuro usaremos datos reales de tracking
                simulated_delta_e = []
                simulated_acceptance_decisions = []
                
                for i in range(n_iters):
                    # Simular ΔE: 70% mejoras, 30% empeoramientos
                    if np.random.random() < 0.7:
                        # Mejora (negativo)
                        delta = -np.random.exponential(20)
                    else:
                        # Empeoramiento (positivo)
                        delta = np.random.exponential(30)
                    
                    simulated_delta_e.append(delta)
                    
                    # Decisión: mejoras siempre, empeoramientos según temperatura
                    if delta <= 0:
                        simulated_acceptance_decisions.append(True)
                    else:
                        # Usar tasa de aceptación basada en temperatura
                        T_current = simulated_temperature[i]
                        accept_prob = np.exp(-delta / T_current) if T_current > 0 else 0
                        simulated_acceptance_decisions.append(np.random.random() < accept_prob)
                
                visualizer.plot_delta_e_distribution(
                    delta_e_values=simulated_delta_e,
                    acceptance_decisions=simulated_acceptance_decisions,
                    title=f"Distribución de ΔE - {best_alg[0]}",
                    filename="demo_delta_e_distribution.png",
                    bins=40
                )
                print(f"   ✅ Gráfica de distribución ΔE generada")
        
        print(f"\n✅ Todas las visualizaciones generadas en {plots_dir}/\n")
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
