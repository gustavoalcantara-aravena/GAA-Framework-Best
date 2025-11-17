"""
Knapsack Evaluator - Evaluación y Fitness
Fase 1 GAA: Función de Evaluación

Criterios de evaluación:
- Maximización del valor total
- Penalización por infactibilidad
- Métricas de calidad
"""

from typing import Dict, Any, Optional
import numpy as np
from .problem import KnapsackProblem
from .solution import KnapsackSolution


class KnapsackEvaluator:
    """
    Evaluador de soluciones del Knapsack Problem
    
    Función de fitness:
    -------------------
    Si factible:   fitness = Σ(v_i * x_i)
    Si infactible: fitness = Σ(v_i * x_i) - penalty * exceso_peso
    
    donde penalty controla la severidad de la penalización
    """
    
    def __init__(self, 
                 problem: KnapsackProblem,
                 penalty_factor: float = 1000.0,
                 use_penalty: bool = True):
        """
        Inicializa el evaluador
        
        Args:
            problem: Instancia del problema
            penalty_factor: Factor de penalización por infactibilidad
            use_penalty: Si False, solo acepta soluciones factibles
        """
        self.problem = problem
        self.penalty_factor = penalty_factor
        self.use_penalty = use_penalty
        
        # Estadísticas de evaluación
        self.num_evaluations = 0
        self.best_value = 0
        self.best_solution = None
    
    def evaluate(self, solution: KnapsackSolution) -> float:
        """
        Evalúa una solución y retorna su fitness
        
        Args:
            solution: Solución a evaluar
        
        Returns:
            Valor de fitness
        """
        self.num_evaluations += 1
        
        # Asegurar que la solución esté evaluada
        if solution.problem is None:
            solution.evaluate(self.problem)
        
        value = solution.value
        weight = solution.weight
        capacity = self.problem.capacity
        
        # Calcular fitness
        if solution.is_feasible:
            fitness = float(value)
        else:
            if self.use_penalty:
                excess = weight - capacity
                fitness = float(value) - self.penalty_factor * excess
            else:
                # Solución infactible = fitness muy bajo
                fitness = -float('inf')
        
        # Actualizar mejor solución encontrada
        if solution.is_feasible and value > self.best_value:
            self.best_value = value
            self.best_solution = solution.copy()
        
        return fitness
    
    def gap_to_optimal(self, solution: KnapsackSolution) -> Optional[float]:
        """
        Calcula gap respecto al óptimo conocido
        
        Args:
            solution: Solución a evaluar
        
        Returns:
            Gap porcentual (%) o None si no hay óptimo conocido
        """
        if self.problem.optimal_value is None:
            return None
        
        if not solution.is_feasible:
            return float('inf')
        
        if self.problem.optimal_value == 0:
            return 0.0
        
        gap = (self.problem.optimal_value - solution.value) / self.problem.optimal_value * 100
        return gap
    
    def utilization_rate(self, solution: KnapsackSolution) -> float:
        """
        Calcula tasa de utilización de capacidad
        
        Args:
            solution: Solución a evaluar
        
        Returns:
            Porcentaje de capacidad utilizada (0-100+)
        """
        return (solution.weight / self.problem.capacity) * 100
    
    def efficiency(self, solution: KnapsackSolution) -> float:
        """
        Calcula eficiencia: valor por unidad de peso usado
        
        Args:
            solution: Solución a evaluar
        
        Returns:
            Ratio valor/peso o 0 si peso=0
        """
        if solution.weight == 0:
            return 0.0
        return solution.value / solution.weight
    
    def get_metrics(self, solution: KnapsackSolution) -> Dict[str, Any]:
        """
        Calcula todas las métricas de calidad
        
        Args:
            solution: Solución a evaluar
        
        Returns:
            Diccionario con métricas
        """
        metrics = {
            'value': solution.value,
            'weight': solution.weight,
            'capacity': self.problem.capacity,
            'is_feasible': solution.is_feasible,
            'num_items': solution.num_selected(),
            'total_items': self.n,
            'utilization': self.utilization_rate(solution),
            'efficiency': self.efficiency(solution),
            'fitness': self.evaluate(solution)
        }
        
        gap = self.gap_to_optimal(solution)
        if gap is not None:
            metrics['gap_percent'] = gap
            metrics['optimal_value'] = self.problem.optimal_value
        
        return metrics
    
    def compare(self, sol1: KnapsackSolution, sol2: KnapsackSolution) -> int:
        """
        Compara dos soluciones
        
        Args:
            sol1: Primera solución
            sol2: Segunda solución
        
        Returns:
            1 si sol1 es mejor, -1 si sol2 es mejor, 0 si iguales
        """
        # Priorizar factibilidad
        if sol1.is_feasible and not sol2.is_feasible:
            return 1
        if not sol1.is_feasible and sol2.is_feasible:
            return -1
        
        # Comparar por valor
        if sol1.value > sol2.value:
            return 1
        elif sol1.value < sol2.value:
            return -1
        else:
            return 0
    
    def is_better(self, sol1: KnapsackSolution, sol2: KnapsackSolution) -> bool:
        """Verifica si sol1 es mejor que sol2"""
        return self.compare(sol1, sol2) > 0
    
    def reset_statistics(self):
        """Reinicia estadísticas de evaluación"""
        self.num_evaluations = 0
        self.best_value = 0
        self.best_solution = None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del evaluador
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'num_evaluations': self.num_evaluations,
            'best_value': self.best_value,
            'best_solution': str(self.best_solution) if self.best_solution else None,
            'problem': str(self.problem)
        }
    
    def __repr__(self) -> str:
        """Representación en string"""
        return (f"KnapsackEvaluator(evals={self.num_evaluations}, "
                f"best={self.best_value})")
