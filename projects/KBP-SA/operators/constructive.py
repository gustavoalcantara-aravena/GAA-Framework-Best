"""
Operadores Constructivos - KBP-SA
Fase 2 GAA: Terminales para construcción de soluciones iniciales

Referencias:
- Dantzig (1957): Greedy algorithms for linear programming relaxation
- Martello & Toth (1990): Knapsack Problems: Algorithms and Computer Implementations
- Pisinger (2005): Where are the hard knapsack problems?
- Khuri et al. (1994): The zero/one knapsack problem and genetic algorithms
"""

from typing import Optional
import numpy as np
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution


class GreedyByValue:
    """
    Construcción voraz por valor decreciente [Dantzig1957]
    
    Algoritmo:
    1. Ordenar ítems por valor decreciente
    2. Insertar ítems mientras quede capacidad
    
    Complejidad: O(n log n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def construct(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """
        Construye solución greedy por valor
        
        Returns:
            Solución factible construida
        """
        solution = KnapsackSolution.empty(self.problem.n, self.problem)
        
        # Ordenar ítems por valor decreciente
        sorted_indices = np.argsort(self.problem.values)[::-1]
        
        current_weight = 0
        
        for idx in sorted_indices:
            weight = self.problem.weights[idx]
            
            # Agregar ítem si cabe
            if current_weight + weight <= self.problem.capacity:
                solution.add_item(int(idx))
                current_weight += weight
        
        solution.evaluate(self.problem)
        return solution
    
    def __call__(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.construct(rng)


class GreedyByWeight:
    """
    Construcción voraz por peso creciente [Martello1990]
    
    Algoritmo:
    1. Ordenar ítems por peso creciente
    2. Insertar ítems ligeros primero
    
    Complejidad: O(n log n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def construct(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """Construye solución greedy por peso"""
        solution = KnapsackSolution.empty(self.problem.n, self.problem)
        
        # Ordenar ítems por peso creciente
        sorted_indices = np.argsort(self.problem.weights)
        
        current_weight = 0
        
        for idx in sorted_indices:
            weight = self.problem.weights[idx]
            
            if current_weight + weight <= self.problem.capacity:
                solution.add_item(int(idx))
                current_weight += weight
        
        solution.evaluate(self.problem)
        return solution
    
    def __call__(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.construct(rng)


class GreedyByRatio:
    """
    Construcción voraz por ratio valor/peso [Pisinger2005]
    
    Algoritmo:
    1. Calcular ratio v_i/w_i para cada ítem
    2. Ordenar por ratio decreciente
    3. Insertar ítems con mejor eficiencia
    
    Nota: Esta es la heurística clásica para KBP con mejor garantía teórica
    
    Complejidad: O(n log n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def construct(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """Construye solución greedy por ratio v/w"""
        solution = KnapsackSolution.empty(self.problem.n, self.problem)
        
        # Calcular ratios y ordenar decreciente
        ratios = self.problem.get_ratio()
        sorted_indices = np.argsort(ratios)[::-1]
        
        current_weight = 0
        
        for idx in sorted_indices:
            weight = self.problem.weights[idx]
            
            if current_weight + weight <= self.problem.capacity:
                solution.add_item(int(idx))
                current_weight += weight
        
        solution.evaluate(self.problem)
        return solution
    
    def __call__(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.construct(rng)


class RandomConstruct:
    """
    Construcción aleatoria respetando capacidad [Khuri1994]
    
    Algoritmo:
    1. Barajar ítems aleatoriamente
    2. Insertar ítems en orden aleatorio mientras quede capacidad
    
    Útil para:
    - Diversificación en población inicial
    - Multi-start methods
    
    Complejidad: O(n)
    """
    
    def __init__(self, problem: KnapsackProblem):
        self.problem = problem
    
    def construct(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        """
        Construye solución aleatoria factible
        
        Args:
            rng: Generador aleatorio (para reproducibilidad)
        """
        if rng is None:
            rng = np.random.default_rng()
        
        solution = KnapsackSolution.empty(self.problem.n, self.problem)
        
        # Permutación aleatoria de índices
        shuffled_indices = rng.permutation(self.problem.n)
        
        current_weight = 0
        
        for idx in shuffled_indices:
            weight = self.problem.weights[idx]
            
            if current_weight + weight <= self.problem.capacity:
                solution.add_item(int(idx))
                current_weight += weight
        
        solution.evaluate(self.problem)
        return solution
    
    def __call__(self, rng: Optional[np.random.Generator] = None) -> KnapsackSolution:
        return self.construct(rng)


# Alias para compatibilidad con gramática GAA
def construct_greedy_value(problem: KnapsackProblem, rng=None) -> KnapsackSolution:
    """Helper function para uso en AST"""
    return GreedyByValue(problem).construct(rng)

def construct_greedy_weight(problem: KnapsackProblem, rng=None) -> KnapsackSolution:
    """Helper function para uso en AST"""
    return GreedyByWeight(problem).construct(rng)

def construct_greedy_ratio(problem: KnapsackProblem, rng=None) -> KnapsackSolution:
    """Helper function para uso en AST"""
    return GreedyByRatio(problem).construct(rng)

def construct_random(problem: KnapsackProblem, rng=None) -> KnapsackSolution:
    """Helper function para uso en AST"""
    return RandomConstruct(problem).construct(rng)
