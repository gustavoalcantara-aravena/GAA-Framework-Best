"""
Operadores de Mejora Local - KBP-SA
Fase 2 GAA: Terminales para mejora de soluciones

Referencias:
- Martello (1999): Dynamic programming and strong bounds for the 0-1 knapsack problem
- Pisinger (2007): The quadratic knapsack problem—a survey
- Kellerer et al. (2004): Knapsack problems
- Vazirani (2001): Approximation Algorithms
"""

from typing import Optional, List, Tuple
import numpy as np
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator


class FlipBestItem:
    """
    Mejora local: cambia el ítem que más mejore [Martello1999]
    
    Algoritmo:
    1. Para cada ítem, evaluar cambio de estado (flip)
    2. Seleccionar el flip que más mejore
    3. Aplicar si mejora y mantiene factibilidad
    
    Complejidad: O(n) por iteración
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
        self.evaluator = KnapsackEvaluator(problem)
    
    def improve(self, solution: KnapsackSolution, 
                rng: Optional[np.random.Generator] = None) -> Tuple[KnapsackSolution, bool]:
        """
        Aplica mejora FlipBestItem
        
        Returns:
            (solución mejorada, True si hubo mejora)
        """
        best_solution = solution.copy()
        best_value = solution.value
        improved = False
        best_idx = -1
        
        for idx in range(self.problem.n):
            # Probar flip
            test_solution = solution.copy()
            test_solution.flip(idx)
            test_solution.evaluate(self.problem)
            
            # Verificar si mejora y es factible
            if test_solution.is_feasible and test_solution.value > best_value:
                best_value = test_solution.value
                best_solution = test_solution
                best_idx = idx
                improved = True
        
        return best_solution, improved
    
    def __call__(self, solution: KnapsackSolution, 
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        improved_sol, _ = self.improve(solution, rng)
        return improved_sol


class FlipWorstItem:
    """
    Remueve ítem con peor contribución (menor ratio v/w) [Pisinger2007]
    
    Algoritmo:
    1. Entre ítems seleccionados, identificar el de menor ratio
    2. Removerlo de la solución
    3. Intentar agregar ítems no seleccionados por ratio decreciente
    
    Complejidad: O(n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def improve(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> Tuple[KnapsackSolution, bool]:
        """Remueve peor ítem y reinserta mejores no seleccionados"""
        new_solution = solution.copy()
        
        selected = solution.get_selected_items()
        
        if len(selected) == 0:
            return new_solution, False
        
        # Encontrar ítem seleccionado con peor ratio
        ratios = self.problem.get_ratio()
        selected_ratios = ratios[selected]
        worst_idx_in_selected = np.argmin(selected_ratios)
        worst_item = selected[worst_idx_in_selected]
        
        # Remover peor ítem
        new_solution.remove_item(int(worst_item))
        new_solution.evaluate(self.problem)
        
        # Intentar agregar ítems no seleccionados por ratio decreciente
        unselected = new_solution.get_unselected_items()
        unselected_ratios = ratios[unselected]
        sorted_unselected = unselected[np.argsort(unselected_ratios)[::-1]]
        
        for idx in sorted_unselected:
            test_solution = new_solution.copy()
            test_solution.add_item(int(idx))
            test_solution.evaluate(self.problem)
            
            if test_solution.is_feasible:
                new_solution = test_solution
        
        new_solution.evaluate(self.problem)
        improved = new_solution.value > solution.value
        
        return new_solution, improved
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        improved_sol, _ = self.improve(solution, rng)
        return improved_sol


class OneExchange:
    """
    Intercambia un ítem dentro por uno fuera [Kellerer2004]
    
    Algoritmo:
    1. Para cada par (ítem_dentro, ítem_fuera)
    2. Evaluar intercambio
    3. Aplicar el mejor intercambio que mejore
    
    Complejidad: O(n²)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def improve(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> Tuple[KnapsackSolution, bool]:
        """Aplica mejor intercambio 1-1"""
        best_solution = solution.copy()
        best_value = solution.value
        improved = False
        
        selected = solution.get_selected_items()
        unselected = solution.get_unselected_items()
        
        # Probar todos los intercambios
        for in_idx in selected:
            for out_idx in unselected:
                test_solution = solution.copy()
                test_solution.remove_item(int(in_idx))
                test_solution.add_item(int(out_idx))
                test_solution.evaluate(self.problem)
                
                if test_solution.is_feasible and test_solution.value > best_value:
                    best_value = test_solution.value
                    best_solution = test_solution
                    improved = True
        
        return best_solution, improved
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        improved_sol, _ = self.improve(solution, rng)
        return improved_sol


class TwoExchange:
    """
    Intercambia dos ítems simultáneamente [Vazirani2001]
    
    Algoritmo:
    1. Remover 2 ítems seleccionados
    2. Agregar 2 ítems no seleccionados
    3. Aplicar mejor intercambio factible que mejore
    
    Complejidad: O(n⁴) - muy costoso, usar con cautela
    """
    
    def __init__(self, problem: KnapsackProblem, max_iterations: int = 100):
        self.problem = problem
        self.max_iterations = max_iterations
    
    def improve(self, solution: KnapsackSolution,
                rng: Optional[np.random.Generator] = None) -> Tuple[KnapsackSolution, bool]:
        """Aplica mejor intercambio 2-2"""
        if rng is None:
            rng = np.random.default_rng()
        
        best_solution = solution.copy()
        best_value = solution.value
        improved = False
        
        selected = solution.get_selected_items()
        unselected = solution.get_unselected_items()
        
        if len(selected) < 2 or len(unselected) < 2:
            return best_solution, False
        
        # Limitar búsqueda para evitar O(n^4)
        iterations = 0
        
        # Muestreo aleatorio de intercambios
        for _ in range(min(self.max_iterations, len(selected) * len(unselected))):
            # Seleccionar 2 ítems dentro y 2 fuera aleatoriamente
            in_pair = rng.choice(selected, size=min(2, len(selected)), replace=False)
            out_pair = rng.choice(unselected, size=min(2, len(unselected)), replace=False)
            
            test_solution = solution.copy()
            
            # Intercambiar
            for idx in in_pair:
                test_solution.remove_item(int(idx))
            for idx in out_pair:
                test_solution.add_item(int(idx))
            
            test_solution.evaluate(self.problem)
            
            if test_solution.is_feasible and test_solution.value > best_value:
                best_value = test_solution.value
                best_solution = test_solution
                improved = True
            
            iterations += 1
            if iterations >= self.max_iterations:
                break
        
        return best_solution, improved
    
    def __call__(self, solution: KnapsackSolution,
                 rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        improved_sol, _ = self.improve(solution, rng)
        return improved_sol
