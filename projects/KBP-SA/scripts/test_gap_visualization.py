"""
Test de Visualización de Gap
Prueba el gráfico de Gap (%) vs Iteración
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from experimentation.visualization import ResultsVisualizer
from data.loader import DatasetLoader
from metaheuristic.sa_core import SimulatedAnnealing
from core.solution import KnapsackSolution
import numpy as np


def custom_neighborhood(solution, rng):
    """Función de vecindad simple - flip bit"""
    neighbor = solution.copy()
    problem = solution.problem
    
    # Simplemente hacer flip de un bit aleatorio
    idx = rng.integers(0, problem.n)
    neighbor.selection[idx] = 1 - neighbor.selection[idx]
    
    # Re-evaluar
    neighbor.evaluate(problem)
    
    return neighbor


def test_gap_visualization():
    """
    Ejecuta SA y genera gráfica de gap
    """
    print("="*70)
    print("TEST: VISUALIZACIÓN DE GAP (%) vs ITERACIÓN")
    print("="*70)
    
    # 1. Cargar instancia f1
    print("\n📂 Cargando instancia f1...")
    loader = DatasetLoader(base_dir=project_root / "datasets")
    instances = loader.load_folder("low_dimensional")
    f1 = [inst for inst in instances if "f1_l-d" in inst.name][0]
    
    print(f"✅ Instancia cargada: {f1.name}")
    print(f"   n={f1.n}, capacity={f1.capacity}, optimal={f1.optimal_value}")
    
    # 2. Configurar SA
    print("\n🔧 Configurando Simulated Annealing...")
    sa = SimulatedAnnealing(
        problem=f1,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=100,
        T_min=0.01,
        max_evaluations=5000,
        seed=42
    )
    sa.neighborhood_function = custom_neighborhood
    
    # 3. Ejecutar SA con tracking
    print("\n🚀 Ejecutando SA...")
    initial = KnapsackSolution.empty(f1.n, f1)
    
    # Lista para almacenar el mejor valor en cada iteración
    best_values_history = []
    
    # Monkey patch para capturar valores
    original_optimize = sa.optimize
    
    def tracked_optimize(initial_solution, verbose=False):
        """Versión modificada que captura best_values"""
        # Ejecutar optimización original
        best = original_optimize(initial_solution, verbose=verbose)
        
        # Copiar historial de best_values
        if hasattr(sa, '_best_values_history'):
            best_values_history.extend(sa._best_values_history)
        
        return best
    
    # Modificar sa.optimize para trackear
    def optimize_with_tracking(initial_solution, verbose=False):
        import copy
        current = initial_solution.copy()
        best = current.copy()
        
        T = sa.T0
        rng = sa.rng
        
        sa._best_values_history = []
        evaluations = 0
        
        # Función para obtener valor efectivo (penalizar infactibles)
        def get_effective_value(sol):
            if sol.is_feasible:
                return sol.value
            else:
                # Penalizar soluciones infactibles
                excess = sol.weight - sol.problem.capacity
                return sol.value - excess * 1000  # Penalización fuerte
        
        while T > sa.T_min and evaluations < sa.max_evaluations:
            for _ in range(sa.iterations_per_temp):
                # Generar vecino
                neighbor = sa.neighborhood_function(current, rng)
                evaluations += 1
                
                # Evaluar con penalización
                delta = get_effective_value(neighbor) - get_effective_value(current)
                
                # Criterio de aceptación
                if delta > 0 or rng.random() < np.exp(delta / T):
                    current = neighbor
                
                # Actualizar mejor (solo si es factible)
                if current.is_feasible and current.value > best.value:
                    best = current.copy()
                    if verbose and evaluations % 500 == 0:
                        gap = ((f1.optimal_value - best.value) / f1.optimal_value) * 100
                        print(f"Eval {evaluations:5d}: best={best.value:3.0f}, gap={gap:5.2f}%, T={T:.4f}")
                
                # Guardar mejor valor actual
                sa._best_values_history.append(best.value)
                
                if evaluations >= sa.max_evaluations:
                    break
            
            # Enfriar
            T *= sa.alpha
        
        return best
    
    sa.optimize = optimize_with_tracking
    
    best = sa.optimize(initial, verbose=True)
    best_values_history = sa._best_values_history
    
    print(f"\n✅ Optimización completada")
    print(f"   Mejor valor: {best.value}")
    print(f"   Óptimo: {f1.optimal_value}")
    gap = ((f1.optimal_value - best.value) / f1.optimal_value) * 100
    print(f"   Gap final: {gap:.2f}%")
    print(f"   Iteraciones registradas: {len(best_values_history)}")
    
    # 4. Generar visualización
    print("\n📊 Generando visualización de gap...")
    visualizer = ResultsVisualizer(output_dir=project_root / "output" / "test_gap")
    
    filepath = visualizer.plot_gap_evolution(
        best_values=best_values_history,
        optimal_value=f1.optimal_value,
        title=f"Evolución del Gap - {f1.name}",
        filename="gap_evolution_test.png",
        show_improvements=True
    )
    
    if filepath:
        print(f"✅ Gráfica generada: {filepath}")
        print(f"\n📈 Estadísticas del gap:")
        gaps = [((f1.optimal_value - v) / f1.optimal_value) * 100 for v in best_values_history]
        print(f"   Gap inicial: {gaps[0]:.2f}%")
        print(f"   Gap final: {gaps[-1]:.2f}%")
        print(f"   Gap mínimo: {min(gaps):.2f}%")
        print(f"   Gap promedio: {np.mean(gaps):.2f}%")
        print(f"   Mejoras detectadas: {sum(1 for i in range(1, len(best_values_history)) if best_values_history[i] > best_values_history[i-1])}")
    else:
        print("❌ No se pudo generar la gráfica")
    
    print("\n" + "="*70)
    print("TEST COMPLETADO")
    print("="*70)


if __name__ == "__main__":
    test_gap_visualization()
