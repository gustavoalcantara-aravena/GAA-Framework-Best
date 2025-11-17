"""
Script de prueba con UNA SOLA instancia
Para monitorear outputs del sistema KBP-SA
"""

import sys
from pathlib import Path
import numpy as np

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
from metaheuristic.sa_core import SimulatedAnnealing
from metaheuristic.cooling_schedules import GeometricCooling
from metaheuristic.acceptance import MetropolisCriterion
from operators.improvement import OneExchange
from data.loader import DatasetLoader

print("=" * 80)
print("PRUEBA CON UNA SOLA INSTANCIA: f1_l-d_kp_10_269")
print("=" * 80)

# 1. Cargar instancia
print("\n[1] Cargando instancia...")
loader = DatasetLoader(base_dir="datasets")
instances = loader.load_folder("low_dimensional")

# Seleccionar solo f1
f1_instance = None
for inst in instances:
    if "f1_l-d" in inst.name:
        f1_instance = inst
        break

if f1_instance is None:
    print("❌ ERROR: No se encontró la instancia f1")
    sys.exit(1)

print(f"✅ Instancia cargada: {f1_instance.name}")
print(f"   - Ítems (n): {f1_instance.n}")
print(f"   - Capacidad: {f1_instance.capacity}")
print(f"   - Óptimo conocido: {f1_instance.optimal_value}")
print(f"   - Valores: {f1_instance.values}")
print(f"   - Pesos: {f1_instance.weights}")

# 2. Crear problema (ya es KnapsackProblem)
print("\n[2] Usando problema cargado...")
problem = f1_instance
print(f"✅ Problema listo")

# 3. Crear solución inicial (vacía)
print("\n[3] Creando solución inicial...")
initial_solution = KnapsackSolution.empty(problem.n, problem)
initial_solution.evaluate(problem)
print(f"✅ Solución inicial:")
print(f"   - Valor: {initial_solution.value}")
print(f"   - Peso: {initial_solution.weight}")
print(f"   - Factible: {initial_solution.is_feasible}")

# 4. Configurar SA
print("\n[4] Configurando Simulated Annealing...")
sa = SimulatedAnnealing(
    problem=problem,
    T0=100.0,
    alpha=0.95,
    iterations_per_temp=50,  # Reducido para prueba rápida
    T_min=0.01,
    max_evaluations=1000,  # Reducido para prueba rápida
    seed=42
)
print(f"✅ SA configurado:")
print(f"   - T0: {sa.T0}")
print(f"   - alpha: {sa.alpha}")
print(f"   - Iteraciones por temp: {sa.iterations_per_temp}")
print(f"   - Max evaluaciones: {sa.max_evaluations}")

# 5. Configurar operador de vecindario
print("\n[5] Configurando operador de vecindario...")

def neighborhood_fn(solution, rng):
    """Genera vecino aleatorio intercambiando un ítem dentro/fuera"""
    neighbor = solution.copy()
    
    # Obtener ítems dentro y fuera
    selected = solution.get_selected_items()
    unselected = solution.get_unselected_items()
    
    # Si no hay ítems seleccionados, agregar uno aleatorio
    if len(selected) == 0:
        if len(unselected) > 0:
            idx = rng.choice(unselected)
            neighbor.add_item(int(idx))
    # Si todos están seleccionados, remover uno
    elif len(unselected) == 0:
        idx = rng.choice(selected)
        neighbor.remove_item(int(idx))
    # Intercambio normal
    else:
        # 50% agregar, 50% remover, o intercambiar
        action = rng.choice(['add', 'remove', 'swap'])
        
        if action == 'add' and len(unselected) > 0:
            idx = rng.choice(unselected)
            neighbor.add_item(int(idx))
        elif action == 'remove' and len(selected) > 0:
            idx = rng.choice(selected)
            neighbor.remove_item(int(idx))
        else:  # swap
            if len(selected) > 0 and len(unselected) > 0:
                in_idx = rng.choice(selected)
                out_idx = rng.choice(unselected)
                neighbor.remove_item(int(in_idx))
                neighbor.add_item(int(out_idx))
    
    neighbor.evaluate(problem)
    return neighbor

sa.set_neighborhood(neighborhood_fn)
print(f"✅ Operador de vecindario configurado")

# 6. Ejecutar SA con verbose
print("\n[6] Ejecutando Simulated Annealing...")
print("-" * 80)

best_solution = sa.optimize(initial_solution, verbose=True)

print("-" * 80)

# 7. Resultados
print("\n[7] RESULTADOS FINALES:")
print("=" * 80)

evaluator = KnapsackEvaluator(problem)
gap = evaluator.gap_to_optimal(best_solution)
if gap is None:
    gap = 0.0

print(f"Mejor solución encontrada:")
print(f"   - Valor: {best_solution.value}")
print(f"   - Peso: {best_solution.weight}/{problem.capacity}")
print(f"   - Factible: {best_solution.is_feasible}")
print(f"   - Ítems seleccionados: {best_solution.get_selected_items()}")
print(f"   - Número de ítems: {len(best_solution.get_selected_items())}")
print(f"\nComparación con óptimo:")
print(f"   - Óptimo conocido: {f1_instance.optimal_value}")
print(f"   - Gap: {gap:.2f}%")
print(f"\nEstadísticas de ejecución:")
stats = sa.get_statistics()
print(f"   - Total iteraciones: {stats['total_iterations']}")
print(f"   - Evaluaciones: {stats['evaluations']}")
print(f"   - Tiempo: {stats['elapsed_time']:.3f}s")
print(f"   - Movimientos aceptados: {stats['accepted_moves']}")
print(f"   - Tasa de aceptación: {stats['acceptance_rate']:.2f}%")
print(f"   - Mejoras encontradas: {stats['improvement_iterations']}")
print(f"   - Temperatura final: {stats['final_temperature']:.6f}")

print("\n" + "=" * 80)
print("PRUEBA COMPLETADA")
print("=" * 80)
