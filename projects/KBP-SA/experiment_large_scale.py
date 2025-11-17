#!/usr/bin/env python3
"""
Experimentos Large Scale - KBP-SA
Ejecuta experimentos en TODAS las instancias large_scale (100-10,000 ítems)

Este script:
- Genera 3 algoritmos GAA
- Ejecuta en las 21 instancias large_scale
- 1 repetición por instancia para cobertura completa
- Análisis y visualizaciones
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Imports
from experimentation.runner import ExperimentRunner, ExperimentConfig
from experimentation.statistics import StatisticalAnalyzer
from experimentation.visualization import ResultsVisualizer
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from data.loader import DatasetLoader


def main():
    print("=" * 80)
    print("  EXPERIMENTOS LARGE SCALE - KBP-SA")
    print("  Instancias: 100 a 10,000 ítems")
    print("=" * 80)
    print()
    
    # 1. Generar algoritmos
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
    
    print(f"\n✅ Total algoritmos generados: {len(algorithms)}\n")
    
    # 2. Cargar instancias large_scale
    print("📁 Paso 2: Cargando instancias large_scale...\n")
    
    datasets_dir = Path(__file__).parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    all_instances = loader.load_folder("large_scale")
    
    instance_names = [inst.name for inst in all_instances]
    
    print(f"📊 Instancias large_scale encontradas: {len(instance_names)}")
    
    # Agrupar por tipo y tamaño
    knapPI_1 = sorted([n for n in instance_names if "knapPI_1_" in n])
    knapPI_2 = sorted([n for n in instance_names if "knapPI_2_" in n])
    knapPI_3 = sorted([n for n in instance_names if "knapPI_3_" in n])
    
    print(f"\n   knapPI_1: {len(knapPI_1)} instancias")
    for name in knapPI_1:
        size = name.split('_')[2]
        print(f"      • {size} ítems")
    
    print(f"\n   knapPI_2: {len(knapPI_2)} instancias")
    print(f"   knapPI_3: {len(knapPI_3)} instancias")
    print()
    
    # 3. Configurar experimento
    print("⚙️  Paso 3: Configurando experimento...\n")
    
    config = ExperimentConfig(
        name="large_scale_full_coverage",
        instances=instance_names,
        algorithms=algorithms,
        repetitions=1,  # 1 repetición por instancia para cobertura
        max_time_seconds=600.0,  # 10 minutos por ejecución
        output_dir="output/large_scale_experiments"
    )
    
    print(f"⚙️  Configuración:")
    print(f"  • Instancias: {len(config.instances)}")
    print(f"  • Algoritmos: {len(config.algorithms)}")
    print(f"  • Repeticiones: {config.repetitions}")
    print(f"  • Total ejecuciones: {len(config.instances) * len(config.algorithms) * config.repetitions}")
    print(f"  • Timeout: {config.max_time_seconds}s por ejecución")
    print()
    
    # 4. Ejecutar experimentos
    print("🚀 Paso 4: Ejecutando experimentos...\n")
    print("⚠️  NOTA: Esto puede tomar varios minutos (~30-60 min)\n")
    
    runner = ExperimentRunner(config)
    runner.load_instances("large_scale")
    
    if not runner.problems:
        print("❌ No se pudieron cargar instancias. Abortando.")
        return
    
    results = runner.run_all(verbose=True)
    
    # 5. Guardar resultados
    print("\n💾 Paso 5: Guardando resultados...\n")
    
    json_file = runner.save_results()
    
    # 6. Análisis por tamaño de instancia
    print("\n📊 Paso 6: Análisis por tamaño de instancia...\n")
    
    # Agrupar resultados por tamaño
    size_groups = {
        '100': [],
        '200': [],
        '500': [],
        '1000': [],
        '2000': [],
        '5000': [],
        '10000': []
    }
    
    for r in results:
        if r.success:
            # Extraer tamaño del nombre
            parts = r.instance_name.split('_')
            if len(parts) >= 3:
                size = parts[2]
                if size in size_groups:
                    size_groups[size].append(r)
    
    print("Rendimiento por tamaño de instancia:")
    print(f"{'Tamaño':<10} {'Ejecuciones':<12} {'Tiempo Prom.':<15} {'Evaluaciones':<15}")
    print("-" * 60)
    
    for size in ['100', '200', '500', '1000', '2000', '5000', '10000']:
        if size_groups[size]:
            times = [r.total_time for r in size_groups[size]]
            evals = [r.evaluations for r in size_groups[size]]
            
            avg_time = sum(times) / len(times)
            avg_evals = sum(evals) / len(evals)
            
            print(f"{size + ' ítems':<10} {len(size_groups[size]):<12} "
                  f"{avg_time:<15.2f} {avg_evals:<15.0f}")
    
    # 7. Ranking de algoritmos
    print("\n🏆 Paso 7: Ranking de algoritmos...\n")
    
    algorithm_results = {}
    for alg in algorithms:
        alg_name = alg['name']
        alg_data = [r for r in results if r.algorithm_name == alg_name and r.success]
        
        if alg_data:
            values = [r.best_value for r in alg_data]
            times = [r.total_time for r in alg_data]
            
            algorithm_results[alg_name] = {
                'runs': len(alg_data),
                'avg_value': sum(values) / len(values),
                'avg_time': sum(times) / len(times),
                'total_time': sum(times)
            }
            
            print(f"Algoritmo: {alg_name}")
            print(f"  Ejecuciones exitosas: {len(alg_data)}/{len(instance_names)}")
            print(f"  Valor promedio: {algorithm_results[alg_name]['avg_value']:.0f}")
            print(f"  Tiempo promedio: {algorithm_results[alg_name]['avg_time']:.2f}s")
            print(f"  Tiempo total: {algorithm_results[alg_name]['total_time']:.2f}s")
            print()
    
    # 8. Visualizaciones
    print("📈 Paso 8: Generando visualizaciones...\n")
    
    # Crear carpeta con dataset_timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plots_dir = f"output/plots_large_scale_{timestamp}"
    visualizer = ResultsVisualizer(output_dir=plots_dir)
    
    if visualizer.has_matplotlib:
        # Gráfica de tiempo por tamaño
        print("⚠️  Generación de gráficas personalizada requerida para large_scale")
        print("    Use los datos en JSON para análisis detallado")
        print(f"📂 Carpeta de plots: {plots_dir}")
    
    # 9. Resumen final
    print("\n" + "=" * 80)
    print("  RESUMEN FINAL - LARGE SCALE")
    print("=" * 80)
    print()
    
    successful = sum(1 for r in results if r.success)
    total = len(results)
    
    print(f"✅ Experimentos completados: {successful}/{total}")
    print(f"📁 Instancias procesadas: {len(config.instances)}")
    print(f"📊 Resultados guardados en: {json_file}")
    
    if algorithm_results:
        best_alg = min(algorithm_results.items(), 
                      key=lambda x: x[1]['avg_time'])
        print(f"\n⚡ Algoritmo más rápido: {best_alg[0]}")
        print(f"   Tiempo promedio: {best_alg[1]['avg_time']:.2f}s")
    
    print()
    print("✅ Cobertura completa del grupo large_scale (21 instancias)")
    print("\nPróximos pasos:")
    print("  1. Analizar escalabilidad por tamaño de instancia")
    print("  2. Comparar rendimiento knapPI_1 vs knapPI_2 vs knapPI_3")
    print("  3. Ejecutar repeticiones múltiples para validación estadística")
    print("  4. Seleccionar mejores algoritmos para reporte final")
    print()


if __name__ == '__main__':
    main()
