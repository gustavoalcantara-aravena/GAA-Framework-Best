"""
Módulo Core - KBP-SA
Definición matemática del problema de la mochila
"""

from .problem import KnapsackProblem
from .solution import KnapsackSolution
from .evaluation import KnapsackEvaluator

__all__ = ['KnapsackProblem', 'KnapsackSolution', 'KnapsackEvaluator']
