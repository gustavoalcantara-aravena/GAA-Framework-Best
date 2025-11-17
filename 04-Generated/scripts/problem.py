"""
Módulo de Problema - Template Base GAA

Este archivo se genera automáticamente desde 00-Core/Problem.md
Define la estructura del problema de optimización.

AUTO-GENERATED - DO NOT EDIT MANUALLY
Edita: 00-Core/Problem.md o projects/<proyecto>/problema_metaheuristica.md
"""

from typing import List, Dict, Any, Tuple
from abc import ABC, abstractmethod
import numpy as np


class Solution:
    """Representación abstracta de una solución"""
    
    def __init__(self, representation: Any):
        """
        Args:
            representation: Estructura de datos que representa la solución
                           (vector binario, permutación, grafo, etc.)
        """
        self.representation = representation
        self.fitness_value = None
        self.is_feasible = None
        self.metadata = {}
    
    def copy(self) -> 'Solution':
        """Crea una copia profunda de la solución"""
        import copy
        return copy.deepcopy(self)
    
    def __repr__(self):
        return f"Solution(fitness={self.fitness_value}, feasible={self.is_feasible})"


class Problem(ABC):
    """Clase abstracta para definir problemas de optimización"""
    
    def __init__(self, instance_data: Dict[str, Any]):
        """
        Args:
            instance_data: Diccionario con los datos de la instancia
        """
        self.instance_data = instance_data
        self.problem_name = "Undefined"
        self.optimization_type = "minimize"  # 'minimize' o 'maximize'
        
    @abstractmethod
    def evaluate(self, solution: Solution) -> float:
        """
        Evalúa la función objetivo de una solución
        
        Args:
            solution: Solución a evaluar
            
        Returns:
            Valor de la función objetivo
        """
        pass
    
    @abstractmethod
    def is_feasible(self, solution: Solution) -> bool:
        """
        Verifica si una solución cumple todas las restricciones
        
        Args:
            solution: Solución a verificar
            
        Returns:
            True si es factible, False en caso contrario
        """
        pass
    
    @abstractmethod
    def repair(self, solution: Solution) -> Solution:
        """
        Repara una solución infactible para hacerla factible
        
        Args:
            solution: Solución a reparar
            
        Returns:
            Solución factible
        """
        pass
    
    @abstractmethod
    def random_solution(self) -> Solution:
        """
        Genera una solución aleatoria factible
        
        Returns:
            Solución aleatoria
        """
        pass
    
    def get_problem_size(self) -> int:
        """Retorna el tamaño del problema (número de variables)"""
        return len(self.instance_data.get('variables', []))
    
    def get_bounds(self) -> Tuple[Any, Any]:
        """Retorna los límites del espacio de búsqueda"""
        return None, None


# ============================================================================
# EJEMPLO: Knapsack Problem (KBP)
# ============================================================================

class KnapsackProblem(Problem):
    """Problema de la Mochila (0/1 Knapsack)"""
    
    def __init__(self, instance_data: Dict[str, Any]):
        super().__init__(instance_data)
        self.problem_name = "Knapsack Problem"
        self.optimization_type = "maximize"
        
        # Extraer datos de la instancia
        self.n = instance_data['n']  # Número de ítems
        self.values = np.array(instance_data['values'])  # Valores v_i
        self.weights = np.array(instance_data['weights'])  # Pesos w_i
        self.capacity = instance_data['capacity']  # Capacidad W
    
    def evaluate(self, solution: Solution) -> float:
        """Evalúa el valor total de los ítems seleccionados"""
        x = np.array(solution.representation)
        return np.sum(self.values * x)
    
    def is_feasible(self, solution: Solution) -> bool:
        """Verifica que el peso total no exceda la capacidad"""
        x = np.array(solution.representation)
        total_weight = np.sum(self.weights * x)
        return total_weight <= self.capacity
    
    def repair(self, solution: Solution) -> Solution:
        """Repara removiendo ítems hasta cumplir restricción de capacidad"""
        x = np.array(solution.representation).copy()
        
        # Calcular ratios valor/peso
        ratios = self.values / (self.weights + 1e-10)
        
        # Mientras exceda capacidad, remover ítem con peor ratio
        while np.sum(self.weights * x) > self.capacity:
            # Encontrar ítems seleccionados
            selected = np.where(x == 1)[0]
            if len(selected) == 0:
                break
            
            # Remover el de peor ratio
            worst_idx = selected[np.argmin(ratios[selected])]
            x[worst_idx] = 0
        
        solution.representation = x.tolist()
        return solution
    
    def random_solution(self) -> Solution:
        """Genera una solución aleatoria factible"""
        x = np.zeros(self.n, dtype=int)
        
        # Orden aleatorio de ítems
        items = np.random.permutation(self.n)
        
        # Añadir ítems mientras quepan
        current_weight = 0
        for i in items:
            if current_weight + self.weights[i] <= self.capacity:
                x[i] = 1
                current_weight += self.weights[i]
        
        return Solution(x.tolist())
    
    def get_problem_size(self) -> int:
        return self.n


# ============================================================================
# Factory para crear problemas
# ============================================================================

def create_problem(problem_type: str, instance_data: Dict[str, Any]) -> Problem:
    """
    Factory para crear instancias de problemas
    
    Args:
        problem_type: Tipo de problema ('knapsack', 'graph_coloring', 'vrp', etc.)
        instance_data: Datos de la instancia
        
    Returns:
        Instancia del problema
    """
    problems = {
        'knapsack': KnapsackProblem,
        # Añadir otros problemas aquí según se implementen
        # 'graph_coloring': GraphColoringProblem,
        # 'vrp': VRPProblem,
    }
    
    if problem_type not in problems:
        raise ValueError(f"Problema desconocido: {problem_type}")
    
    return problems[problem_type](instance_data)


if __name__ == "__main__":
    # Ejemplo de uso
    instance = {
        'n': 5,
        'values': [10, 20, 30, 15, 25],
        'weights': [5, 10, 15, 8, 12],
        'capacity': 30
    }
    
    problem = create_problem('knapsack', instance)
    sol = problem.random_solution()
    
    print(f"Solución: {sol.representation}")
    print(f"Valor: {problem.evaluate(sol)}")
    print(f"Factible: {problem.is_feasible(sol)}")
