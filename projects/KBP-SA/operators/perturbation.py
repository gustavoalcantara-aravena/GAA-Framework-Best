"""
Operadores de Perturbación - KBP-SA
Fase 2 GAA: Terminales para diversificación

Referencias:
- Glover (1998): A Template for Scatter Search and Path Relinking
- Lourenço et al. (2003): Iterated Local Search
- Shaw (1998): Using Constraint Programming and Local Search Methods
"""

from typing import Optional
import numpy as np
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution


class RandomFlip:
    """
    Cambia aleatoriamente el estado de k ítems [Glover1998]
    
    Algoritmo:
    1. Seleccionar k ítems aleatoriamente
    2. Cambiar su estado (0→1 o 1→0)
    
    Parámetro:
    - k: intensidad de perturbación (default: 10% de n)
    
    Complejidad: O(k)
    """
    
    def __init__(self, problem: KnapsackProblem, k: Optional[int] = None):
        self.problem = problem
        self.k = k if k is not None else max(1, problem.n // 10)
    
    def perturb(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """
        Perturba solución cambiando k ítems aleatorios
        
        Args:
            solution: Solución a perturbar
            rng: Generador aleatorio
        
        Returns:
            Solución perturbada
        """
        if rng is None:
            rng = np.random.default_rng()
        
        perturbed = solution.copy()
        
        # Seleccionar k ítems aleatorios
        items_to_flip = rng.choice(self.problem.n, size=min(self.k, self.problem.n), replace=False)
        
        # Cambiar estado
        for idx in items_to_flip:
            perturbed.flip(int(idx))
        
        perturbed.evaluate(self.problem)
        return perturbed
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.perturb(solution, rng)


class ShakeByRemoval:
    """
    Remueve aleatoriamente k ítems de la mochila [Lourenco2003]
    
    Algoritmo:
    1. Identificar ítems seleccionados
    2. Remover k ítems aleatoriamente
    
    Útil para:
    - Escapar de óptimos locales
    - Diversificación en ILS
    
    Complejidad: O(k)
    """
    
    def __init__(self, problem: KnapsackProblem, k: Optional[int] = None):
        self.problem = problem
        self.k = k if k is not None else max(1, problem.n // 20)
    
    def perturb(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """Remueve k ítems aleatoriamente"""
        if rng is None:
            rng = np.random.default_rng()
        
        perturbed = solution.copy()
        
        selected = perturbed.get_selected_items()
        
        if len(selected) == 0:
            return perturbed
        
        # Número de ítems a remover
        num_to_remove = min(self.k, len(selected))
        
        # Seleccionar ítems a remover
        items_to_remove = rng.choice(selected, size=num_to_remove, replace=False)
        
        # Remover
        for idx in items_to_remove:
            perturbed.remove_item(int(idx))
        
        perturbed.evaluate(self.problem)
        return perturbed
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.perturb(solution, rng)


class DestroyRepair:
    """
    Destruye porción de solución y reconstruye vorazmente [Shaw1998]
    
    Algoritmo:
    1. Remover d% de ítems seleccionados aleatoriamente
    2. Reconstruir usando greedy por ratio
    
    Parámetros:
    - destruction_rate: proporción a destruir (default: 0.3)
    
    Complejidad: O(n log n)
    """
    
    def __init__(self, problem: KnapsackProblem, destruction_rate: float = 0.3):
        self.problem = problem
        self.destruction_rate = destruction_rate
    
    def perturb(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """Destruye y repara solución"""
        if rng is None:
            rng = np.random.default_rng()
        
        perturbed = solution.copy()
        
        selected = perturbed.get_selected_items()
        
        if len(selected) == 0:
            return perturbed
        
        # Fase de destrucción
        num_to_destroy = max(1, int(len(selected) * self.destruction_rate))
        items_to_destroy = rng.choice(selected, size=num_to_destroy, replace=False)
        
        for idx in items_to_destroy:
            perturbed.remove_item(int(idx))
        
        # Fase de reparación (greedy por ratio)
        ratios = self.problem.get_ratio()
        unselected = perturbed.get_unselected_items()
        sorted_unselected = unselected[np.argsort(ratios[unselected])[::-1]]
        
        for idx in sorted_unselected:
            test_solution = perturbed.copy()
            test_solution.add_item(int(idx))
            test_solution.evaluate(self.problem)
            
            if test_solution.is_feasible:
                perturbed = test_solution
            else:
                break
        
        perturbed.evaluate(self.problem)
        return perturbed
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.perturb(solution, rng)
