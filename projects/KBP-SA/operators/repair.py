"""
Operadores de Reparación - KBP-SA
Fase 2 GAA: Terminales para restaurar factibilidad

Referencias:
- Chu & Beasley (1998): A genetic algorithm for the multidimensional knapsack problem
- Pisinger (1999): An exact algorithm for large multiple knapsack problems
"""

from typing import Optional
import numpy as np
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution


class RepairByRemoval:
    """
    Elimina ítems hasta factibilidad [Chu1998]
    
    Algoritmo:
    1. Mientras solución sea infactible:
       a. Identificar ítem seleccionado con menor ratio v/w
       b. Removerlo
    
    Ventajas:
    - Garantiza factibilidad
    - Preserva ítems eficientes
    
    Complejidad: O(n log n) peor caso
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def repair(self, solution: KnapsackSolution,
               rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """
        Repara solución infactible removiendo ítems
        
        Args:
            solution: Solución posiblemente infactible
            rng: No usado (compatibilidad de interfaz)
        
        Returns:
            Solución factible
        """
        if solution.is_feasible:
            return solution.copy()
        
        repaired = solution.copy()
        ratios = self.problem.get_ratio()
        
        # Remover ítems hasta ser factible
        while not repaired.is_feasible:
            selected = repaired.get_selected_items()
            
            if len(selected) == 0:
                break
            
            # Encontrar ítem con peor ratio entre los seleccionados
            selected_ratios = ratios[selected]
            worst_idx_in_selected = np.argmin(selected_ratios)
            worst_item = selected[worst_idx_in_selected]
            
            # Remover
            repaired.remove_item(int(worst_item))
            repaired.evaluate(self.problem)
        
        return repaired
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.repair(solution, rng)


class RepairByGreedy:
    """
    Reconstrucción voraz tras destrucción [Pisinger1999]
    
    Algoritmo:
    1. Si solución es infactible: aplicar RepairByRemoval
    2. Intentar agregar ítems no seleccionados por ratio decreciente
    3. Agregar mientras quede capacidad
    
    Ventajas:
    - Garantiza factibilidad
    - Maximiza utilización de capacidad
    - Usa heurística greedy probada
    
    Complejidad: O(n log n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
        self.repair_removal = RepairByRemoval(problem)
    
    def repair(self, solution: KnapsackSolution,
               rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """
        Repara solución y completa con greedy
        
        Args:
            solution: Solución a reparar
            rng: No usado (compatibilidad)
        
        Returns:
            Solución factible mejorada
        """
        # Paso 1: Asegurar factibilidad
        repaired = self.repair_removal.repair(solution, rng)
        
        # Paso 2: Completar con greedy
        ratios = self.problem.get_ratio()
        unselected = repaired.get_unselected_items()
        
        if len(unselected) == 0:
            return repaired
        
        # Ordenar ítems no seleccionados por ratio decreciente
        sorted_unselected = unselected[np.argsort(ratios[unselected])[::-1]]
        
        # Intentar agregar ítems
        for idx in sorted_unselected:
            test_solution = repaired.copy()
            test_solution.add_item(int(idx))
            test_solution.evaluate(self.problem)
            
            if test_solution.is_feasible:
                repaired = test_solution
            else:
                # Si uno no cabe, los siguientes tampoco (están ordenados por ratio)
                break
        
        repaired.evaluate(self.problem)
        return repaired
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.repair(solution, rng)


# Función auxiliar para reparación automática
def auto_repair(solution: KnapsackSolution, 
                problem: KnapsackProblem,
                method: str = 'greedy',
                rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
    """
    Repara solución automáticamente
    
    Args:
        solution: Solución a reparar
        problem: Problema
        method: 'greedy' o 'removal'
        rng: Generador aleatorio
    
    Returns:
        Solución factible
    """
    if method == 'greedy':
        repairer = RepairByGreedy(problem)
    elif method == 'removal':
        repairer = RepairByRemoval(problem)
    else:
        raise ValueError(f"Método de reparación desconocido: {method}")
    
    return repairer.repair(solution, rng)
