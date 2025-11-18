"""
Test de Visualización de Tasa de Aceptación
Prueba el gráfico de Tasa de Aceptación vs Iteración
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


def test_acceptance_and_gap_visualization():
    """
    Ejecuta SA y genera gráficas de aceptación y gap
    """
    print("="*70)
    print("TEST: VISUALIZACIÓN DE TASA DE ACEPTACIÓN Y GAP")
    print("TEST CON TODAS LAS INSTANCIAS LOW-DIMENSIONAL")
    print("="*70)
    
    # 1. Cargar TODAS las instancias low-dimensional
    print("\n📂 Cargando instancias low-dimensional...")
    loader = DatasetLoader(base_dir=project_root / "datasets")
    instances = loader.load_folder("low_dimensional")
    
    print(f"✅ {len(instances)} instancias cargadas:")
    for inst in sorted(instances, key=lambda x: x.n):
        print(f"   • {inst.name}: n={inst.n}, capacity={inst.capacity}, optimal={inst.optimal_value}")
    
    # Seleccionar primera instancia para demostración detallada
    test_instance = sorted(instances, key=lambda x: x.n)[0]
    
    print(f"\n📊 Generando visualizaciones detalladas para: {test_instance.name}")
    print(f"   n={test_instance.n}, capacity={test_instance.capacity}, optimal={test_instance.optimal_value}")
    
    # 2. Configurar SA
    print("\n🔧 Configurando Simulated Annealing...")
    sa = SimulatedAnnealing(
        problem=test_instance,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=100,
        T_min=0.01,
        max_evaluations=5000,
        seed=42
    )
    sa.neighborhood_function = custom_neighborhood
    
    # 3. Ejecutar SA con tracking detallado
    print("\n🚀 Ejecutando SA con tracking...")
    initial = KnapsackSolution.empty(test_instance.n, test_instance)
    
    # Variables de tracking
    best_values_history = []
    acceptance_history = []
    temperature_history = []
    delta_e_history = []
    
    # Implementación de SA con tracking completo
    def optimize_with_full_tracking(initial_solution, verbose=False):
        current = initial_solution.copy()
        best = current.copy()
        
        T = sa.T0
        rng = sa.rng
        evaluations = 0
        
        # Función para obtener valor efectivo (penalizar infactibles)
        def get_effective_value(sol):
            if sol.is_feasible:
                return sol.value
            else:
                excess = sol.weight - sol.problem.capacity
                return sol.value - excess * 1000
        
        while T > sa.T_min and evaluations < sa.max_evaluations:
            for _ in range(sa.iterations_per_temp):
                # Generar vecino
                neighbor = sa.neighborhood_function(current, rng)
                evaluations += 1
                
                # Evaluar
                delta = get_effective_value(neighbor) - get_effective_value(current)
                
                # Guardar ΔE
                delta_e_history.append(delta)
                
                # Decisión de aceptación
                accepted = False
                if delta > 0:
                    # Mejora: siempre aceptar
                    accepted = True
                    current = neighbor
                else:
                    # Empeoramiento: aplicar criterio de Metropolis
                    prob = np.exp(delta / T)
                    if rng.random() < prob:
                        accepted = True
                        current = neighbor
                
                # Registrar decisión
                acceptance_history.append(1 if accepted else 0)
                temperature_history.append(T)
                
                # Actualizar mejor (solo factibles)
                if current.is_feasible and current.value > best.value:
                    best = current.copy()
                    if verbose and evaluations % 500 == 0:
                        gap = ((test_instance.optimal_value - best.value) / test_instance.optimal_value) * 100
                        acc_rate = (sum(acceptance_history[-100:]) / min(100, len(acceptance_history))) * 100
                        print(f"Eval {evaluations:5d}: best={best.value:3.0f}, gap={gap:5.2f}%, "
                              f"T={T:.4f}, acc={acc_rate:.1f}%")
                
                # Guardar mejor valor
                best_values_history.append(best.value)
                
                if evaluations >= sa.max_evaluations:
                    break
            
            # Enfriar
            T *= sa.alpha
        
        return best
    
    sa.optimize = optimize_with_full_tracking
    best = sa.optimize(initial, verbose=True)
    
    print(f"\n✅ Optimización completada")
    print(f"   Mejor valor: {best.value}")
    print(f"   Óptimo: {test_instance.optimal_value}")
    gap = ((test_instance.optimal_value - best.value) / test_instance.optimal_value) * 100
    print(f"   Gap final: {gap:.2f}%")
    print(f"   Iteraciones: {len(acceptance_history)}")
    print(f"   Aceptaciones: {sum(acceptance_history)}")
    print(f"   Tasa global: {(sum(acceptance_history)/len(acceptance_history))*100:.2f}%")
    print(f"   ΔE registrados: {len(delta_e_history)}")
    
    # 4. Generar visualizaciones
    print("\n📊 Generando visualizaciones...")
    visualizer = ResultsVisualizer(output_dir=project_root / "output" / "test_acceptance")
    
    # 4.1 Gráfica de Gap
    print("\n📈 Gráfica 1: Evolución del Gap con Temperatura")
    gap_path = visualizer.plot_gap_evolution(
        best_values=best_values_history,
        optimal_value=test_instance.optimal_value,
        title=f"Evolución del Gap y Temperatura - {test_instance.name}",
        filename="gap_evolution.png",
        show_improvements=True,
        temperature_history=temperature_history
    )
    if gap_path:
        print(f"   ✅ Generada: {gap_path}")
    
    # 4.2 Gráfica de Tasa de Aceptación
    print("\n📈 Gráfica 2: Tasa de Aceptación con Temperatura")
    
    # Probar con diferentes tamaños de ventana
    for window in [50, 100, 200]:
        acc_path = visualizer.plot_acceptance_rate(
            acceptance_history=acceptance_history,
            window_size=window,
            title=f"Tasa de Aceptación y Temperatura - {test_instance.name} (ventana={window})",
            filename=f"acceptance_rate_w{window}.png",
            temperature_history=temperature_history
        )
        if acc_path:
            print(f"   ✅ Generada (ventana={window}): {acc_path}")
    
    # 4.3 Gráfica de Distribución de ΔE
    print("\n📈 Gráfica 3: Distribución de ΔE")
    
    # Convertir acceptance_history a lista de booleanos
    acceptance_decisions = [bool(x) for x in acceptance_history]
    
    delta_path = visualizer.plot_delta_e_distribution(
        delta_e_values=delta_e_history,
        acceptance_decisions=acceptance_decisions,
        title=f"Distribución de ΔE - {test_instance.name}",
        filename="delta_e_distribution.png",
        bins=50
    )
    if delta_path:
        print(f"   ✅ Generada: {delta_path}")
    
    # 4.4 Gráfica de Balance Exploración-Explotación
    print("\n📈 Gráfica 4: Balance Exploración-Explotación")
    
    balance_path = visualizer.plot_exploration_exploitation_balance(
        delta_e_values=delta_e_history,
        acceptance_decisions=acceptance_decisions,
        temperature_history=temperature_history,
        title=f"Balance Exploración-Explotación - {test_instance.name}",
        filename="exploration_exploitation_balance.png",
        window_size=100
    )
    if balance_path:
        print(f"   ✅ Generada: {balance_path}")

    
    # 4.5 Estadísticas detalladas
    print("\n📊 Estadísticas detalladas:")
    print(f"   Gap inicial: {((test_instance.optimal_value - best_values_history[0]) / test_instance.optimal_value) * 100:.2f}%")
    print(f"   Gap final: {gap:.2f}%")
    print(f"   Mejoras: {sum(1 for i in range(1, len(best_values_history)) if best_values_history[i] > best_values_history[i-1])}")
    
    # Dividir en fases (exploración vs explotación)
    n_iters = len(acceptance_history)
    phase1 = acceptance_history[:n_iters//3]
    phase2 = acceptance_history[n_iters//3:2*n_iters//3]
    phase3 = acceptance_history[2*n_iters//3:]
    
    print(f"\n   Tasa de aceptación por fase:")
    print(f"   • Fase 1 (exploración):  {(sum(phase1)/len(phase1))*100:.2f}%")
    print(f"   • Fase 2 (transición):   {(sum(phase2)/len(phase2))*100:.2f}%")
    print(f"   • Fase 3 (explotación):  {(sum(phase3)/len(phase3))*100:.2f}%")
    
    # Temperatura inicial vs final
    print(f"\n   Temperatura:")
    print(f"   • Inicial: {temperature_history[0]:.4f}")
    print(f"   • Final:   {temperature_history[-1]:.4f}")
    print(f"   • Ratio:   {temperature_history[-1]/temperature_history[0]:.6f}")
    
    # Estadísticas de ΔE
    print(f"\n   ΔE (Diferencias de energía):")
    delta_e_array = np.array(delta_e_history)
    improvements_mask = delta_e_array <= 0
    worsenings_mask = delta_e_array > 0
    
    print(f"   • Total movimientos: {len(delta_e_array)}")
    print(f"   • Mejoras (ΔE≤0): {improvements_mask.sum()} ({improvements_mask.sum()/len(delta_e_array)*100:.1f}%)")
    print(f"   • Empeoramientos (ΔE>0): {worsenings_mask.sum()} ({worsenings_mask.sum()/len(delta_e_array)*100:.1f}%)")
    
    improvements = delta_e_array[improvements_mask]
    worsenings = delta_e_array[worsenings_mask]
    
    if len(improvements) > 0:
        print(f"   • ΔE promedio (mejoras): {improvements.mean():.2f}")
    if len(worsenings) > 0:
        print(f"   • ΔE promedio (empeoramientos): {worsenings.mean():.2f}")
        # Contar cuántos empeoramientos fueron aceptados
        worsenings_accepted = sum(1 for i, delta in enumerate(delta_e_history) 
                                 if delta > 0 and acceptance_history[i] == 1)
        print(f"   • Empeoramientos aceptados: {worsenings_accepted} ({worsenings_accepted/len(worsenings)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("TEST COMPLETADO")
    print("="*70)
    print(f"\n📁 Todas las gráficas en: output/test_acceptance/")


if __name__ == "__main__":
    test_acceptance_and_gap_visualization()
