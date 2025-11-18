#!/usr/bin/env python3
"""
Test Suite Completo: Todas las Instancias Low-Dimensional
Ejecuta SA con todas las instancias y genera reporte comparativo
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.loader import DatasetLoader
from metaheuristic.sa_core import SimulatedAnnealing
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
import numpy as np


def custom_neighborhood(solution, rng):
    """Función de vecindad simple - flip bit"""
    neighbor = solution.copy()
    problem = solution.problem
    
    # Flip de un bit aleatorio
    idx = rng.integers(0, problem.n)
    neighbor.selection[idx] = 1 - neighbor.selection[idx]
    
    # Re-evaluar
    neighbor.evaluate(problem)
    
    return neighbor


def run_sa_on_instance(instance, seed=42, max_evals=5000):
    """
    Ejecuta SA en una instancia y retorna resultados
    
    Args:
        instance: Instancia KnapsackProblem
        seed: Semilla aleatoria
        max_evals: Máximo de evaluaciones
        
    Returns:
        dict con resultados
    """
    # Configurar SA
    sa = SimulatedAnnealing(
        problem=instance,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=100,
        T_min=0.01,
        max_evaluations=max_evals,
        seed=seed
    )
    sa.neighborhood_function = custom_neighborhood
    
    # Ejecutar
    initial = KnapsackSolution.empty(instance.n, instance)
    best = sa.optimize(initial, verbose=False)
    
    # Calcular métricas
    evaluator = KnapsackEvaluator(instance)
    gap = evaluator.gap_to_optimal(best)
    
    stats = sa.get_statistics()
    
    return {
        'instance_name': instance.name,
        'n': instance.n,
        'capacity': instance.capacity,
        'optimal': instance.optimal_value,
        'best_value': best.value,
        'gap': gap if gap is not None else 0.0,
        'is_optimal': gap == 0.0 if gap is not None else False,
        'is_feasible': best.is_feasible,
        'evaluations': stats['evaluations'],
        'time': stats['elapsed_time'],
        'acceptance_rate': stats['acceptance_rate'],
        'improvements': stats['improvement_iterations']
    }


def main():
    print("=" * 80)
    print("  TEST COMPLETO: TODAS LAS INSTANCIAS LOW-DIMENSIONAL")
    print("=" * 80)
    print()
    
    # 1. Cargar instancias
    print("📂 Cargando instancias...")
    loader = DatasetLoader(base_dir=project_root / "datasets")
    instances = loader.load_folder("low_dimensional")
    
    # Ordenar por tamaño
    instances = sorted(instances, key=lambda x: x.n)
    
    print(f"✅ {len(instances)} instancias cargadas\n")
    
    # 2. Ejecutar SA en cada instancia
    results = []
    
    print("🚀 Ejecutando SA en cada instancia...\n")
    print("-" * 80)
    
    for i, instance in enumerate(instances, 1):
        print(f"[{i}/{len(instances)}] {instance.name} (n={instance.n})...", end=" ", flush=True)
        
        result = run_sa_on_instance(instance, seed=42)
        results.append(result)
        
        # Mostrar resultado
        status = "✅ ÓPTIMO" if result['is_optimal'] else f"Gap: {result['gap']:.2f}%"
        print(f"{status} ({result['time']:.3f}s)")
    
    print("-" * 80)
    print()
    
    # 3. Generar reporte
    print("📊 REPORTE DE RESULTADOS")
    print("=" * 80)
    print()
    
    # Tabla de resultados
    print(f"{'Instancia':<30} {'n':>4} {'Óptimo':>8} {'Mejor':>8} {'Gap %':>8} {'Tiempo':>10}")
    print("-" * 80)
    
    for r in results:
        gap_str = f"{r['gap']:.2f}" if r['gap'] > 0 else "0.00"
        optimal_marker = " ✅" if r['is_optimal'] else ""
        print(f"{r['instance_name']:<30} {r['n']:>4} {r['optimal']:>8} "
              f"{r['best_value']:>8} {gap_str:>8}{optimal_marker} {r['time']:>9.3f}s")
    
    print("-" * 80)
    print()
    
    # 4. Estadísticas agregadas
    print("📈 ESTADÍSTICAS AGREGADAS")
    print("=" * 80)
    print()
    
    gaps = [r['gap'] for r in results]
    times = [r['time'] for r in results]
    n_optimal = sum(1 for r in results if r['is_optimal'])
    
    print(f"Total instancias:         {len(results)}")
    print(f"Óptimos encontrados:      {n_optimal} ({n_optimal/len(results)*100:.1f}%)")
    print(f"Gap promedio:             {np.mean(gaps):.2f}%")
    print(f"Gap máximo:               {np.max(gaps):.2f}%")
    print(f"Gap mínimo:               {np.min(gaps):.2f}%")
    print(f"Tiempo total:             {sum(times):.3f}s")
    print(f"Tiempo promedio:          {np.mean(times):.3f}s")
    print()
    
    # Desglose por tamaño
    print("Desglose por tamaño:")
    print(f"  • n ≤ 10:  {sum(1 for r in results if r['n'] <= 10 and r['is_optimal'])}/{sum(1 for r in results if r['n'] <= 10)} óptimos")
    print(f"  • n ≤ 20:  {sum(1 for r in results if r['n'] <= 20 and r['is_optimal'])}/{sum(1 for r in results if r['n'] <= 20)} óptimos")
    print(f"  • n > 20:  {sum(1 for r in results if r['n'] > 20 and r['is_optimal'])}/{sum(1 for r in results if r['n'] > 20)} óptimos")
    print()
    
    # 5. Guardar resultados
    output_dir = project_root / "output" / "test_all_low_dimensional"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = output_dir / f"results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_instances': len(results),
                'optimal_found': n_optimal,
                'success_rate': n_optimal / len(results) * 100,
                'avg_gap': float(np.mean(gaps)),
                'max_gap': float(np.max(gaps)),
                'total_time': sum(times)
            },
            'results': results
        }, f, indent=2)
    
    print(f"💾 Resultados guardados: {results_file}")
    print()
    
    # 6. Conclusiones
    print("=" * 80)
    print("✅ TEST COMPLETADO")
    print("=" * 80)
    print()
    
    if n_optimal == len(results):
        print("🎉 ¡ÉXITO TOTAL! Todos los óptimos encontrados")
    elif n_optimal >= len(results) * 0.8:
        print(f"✅ Muy buen desempeño: {n_optimal}/{len(results)} óptimos ({n_optimal/len(results)*100:.1f}%)")
    else:
        print(f"⚠️  Desempeño moderado: {n_optimal}/{len(results)} óptimos ({n_optimal/len(results)*100:.1f}%)")
        print("   Considera ajustar parámetros de SA para mejorar")
    
    print()


if __name__ == "__main__":
    main()
