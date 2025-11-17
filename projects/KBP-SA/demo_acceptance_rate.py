#!/usr/bin/env python3
"""
Demo: Visualización de Tasa de Aceptación - KBP-SA
Demuestra el tracking de tasa de aceptación durante SA

Este script:
1. Ejecuta SA directamente sobre una instancia
2. Captura el historial de aceptaciones
3. Genera gráfica de tasa de aceptación vs iteración
"""

import sys
from pathlib import Path
from datetime import datetime

# Agregar proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Imports
from data.loader import DatasetLoader
from metaheuristic.sa_core import SimulatedAnnealing
from operators.constructive import GreedyByRatio
from operators.improvement import OneExchange
from experimentation.visualization import ResultsVisualizer


def main():
    print("=" * 80)
    print("  DEMO: Visualización de Tasa de Aceptación - SA")
    print("=" * 80)
    print()
    
    # 1. Cargar instancia
    print("📁 Paso 1: Cargando instancia de prueba...\n")
    
    datasets_dir = Path(__file__).parent / "datasets"
    loader = DatasetLoader(datasets_dir)
    instances = loader.load_folder("low_dimensional")
    
    # Usar instancia f8 (23 ítems, 10000 capacidad)
    problem = None
    for inst in instances:
        if "f8" in inst.name:
            problem = inst
            break
    
    if not problem:
        print("❌ No se encontró instancia f8")
        return
    
    print(f"✅ Instancia cargada: {problem.name}")
    print(f"   Ítems: {problem.n}")
    print(f"   Capacidad: {problem.capacity}")
    print()
    
    # 2. Crear solución inicial
    print("🏗️  Paso 2: Generando solución inicial...\n")
    
    constructor = GreedyByRatio(problem)
    initial_solution = constructor.construct()
    
    print(f"✅ Solución inicial:")
    print(f"   Valor: {initial_solution.value}")
    print(f"   Peso: {initial_solution.weight}/{problem.capacity}")
    print(f"   Factible: {initial_solution.is_feasible}")
    print()
    
    # 3. Configurar y ejecutar SA
    print("🔥 Paso 3: Configurando y ejecutando Simulated Annealing...\n")
    
    sa = SimulatedAnnealing(
        problem=problem,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=100,
        T_min=0.01,
        max_evaluations=10000,
        seed=42
    )
    
    # Función de vecindario (OneExchange)
    def neighborhood_fn(solution, rng):
        """
        Genera un vecino ALEATORIO usando OneExchange.
        IMPORTANTE: No usar improve() porque siempre retorna el mejor vecino.
        """
        selected = solution.get_selected_items()
        unselected = solution.get_unselected_items()
        
        if len(selected) == 0 or len(unselected) == 0:
            return solution.copy()
        
        # Seleccionar ALEATORIAMENTE un ítem para intercambiar
        in_idx = rng.choice(selected)
        out_idx = rng.choice(unselected)
        
        # Crear vecino
        neighbor = solution.copy()
        neighbor.remove_item(int(in_idx))
        neighbor.add_item(int(out_idx))
        neighbor.evaluate(problem)
        
        return neighbor
    
    sa.set_neighborhood(neighborhood_fn)
    
    print("⚙️  Parámetros SA:")
    print(f"   T0: {sa.T0}")
    print(f"   Alpha: {sa.alpha}")
    print(f"   Iteraciones por temperatura: {sa.iterations_per_temp}")
    print(f"   T_min: {sa.T_min}")
    print(f"   Max evaluaciones: {sa.max_evaluations}")
    print()
    
    print("🚀 Ejecutando SA...")
    best_solution = sa.optimize(initial_solution, verbose=False)
    print()
    
    # 4. Resultados
    print("📊 Paso 4: Resultados de SA...\n")
    
    stats = sa.get_statistics()
    
    print(f"✅ Optimización completada:")
    print(f"   Valor inicial: {initial_solution.value}")
    print(f"   Mejor valor: {best_solution.value}")
    print(f"   Mejora: {best_solution.value - initial_solution.value} ({((best_solution.value - initial_solution.value) / initial_solution.value * 100):.2f}%)")
    print(f"   Iteraciones: {stats['total_iterations']}")
    print(f"   Evaluaciones: {stats['evaluations']}")
    print(f"   Tiempo: {stats['elapsed_time']:.2f}s")
    print(f"   Movimientos aceptados: {stats['accepted_moves']}")
    print(f"   Tasa de aceptación global: {stats['acceptance_rate']:.2f}%")
    print()
    
    # 5. Obtener datos de convergencia
    print("📈 Paso 5: Obteniendo datos de convergencia...\n")
    
    convergence_data = sa.get_convergence_data()
    
    if 'acceptance_history' not in convergence_data or not convergence_data['acceptance_history']:
        print("⚠️  No hay datos de aceptación disponibles")
        return
    
    acceptance_history = convergence_data['acceptance_history']
    
    print(f"✅ Datos de convergencia recopilados:")
    print(f"   Total decisiones: {len(acceptance_history)}")
    print(f"   Aceptaciones: {sum(acceptance_history)}")
    print(f"   Rechazos: {len(acceptance_history) - sum(acceptance_history)}")
    print()
    
    # 6. Generar visualización
    print("📊 Paso 6: Generando visualizaciones...\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plots_dir = f"output/plots_acceptance_{timestamp}"
    visualizer = ResultsVisualizer(output_dir=plots_dir)
    
    if not visualizer.has_matplotlib:
        print("❌ matplotlib no disponible")
        return
    
    # Gráfica de tasa de aceptación con diferentes ventanas
    window_sizes = [50, 100, 200]
    
    for window_size in window_sizes:
        if len(acceptance_history) >= window_size:
            visualizer.plot_acceptance_rate(
                acceptance_history=acceptance_history,
                window_size=window_size,
                title=f"Tasa de Aceptación vs Iteración - {problem.name}",
                filename=f"acceptance_rate_w{window_size}.png"
            )
    
    print()
    
    # 7. Resumen final
    print("=" * 80)
    print("  RESUMEN")
    print("=" * 80)
    print()
    print(f"✅ Instancia: {problem.name}")
    print(f"✅ Solución inicial: {initial_solution.value}")
    print(f"✅ Mejor solución: {best_solution.value}")
    print(f"✅ Mejora absoluta: {best_solution.value - initial_solution.value}")
    print(f"✅ Mejora relativa: {((best_solution.value - initial_solution.value) / initial_solution.value * 100):.2f}%")
    print(f"✅ Iteraciones: {stats['total_iterations']}")
    print(f"✅ Tasa de aceptación: {stats['acceptance_rate']:.2f}%")
    print(f"✅ Gráficas guardadas en: {plots_dir}/")
    print()
    print("💡 Interpretación de la tasa de aceptación:")
    print("  • Alta al inicio (>50%): Fase de exploración con T alta")
    print("  • Decreciente gradual: Transición exploración → explotación")
    print("  • Baja al final (<10%): Fase de refinamiento con T baja")
    print("  • Oscilaciones: Enfriamiento por etapas (geométrico)")
    print()


if __name__ == '__main__':
    main()
