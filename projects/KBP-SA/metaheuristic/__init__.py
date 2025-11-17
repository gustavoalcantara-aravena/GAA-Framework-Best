"""
Módulo Metaheuristic - KBP-SA
Simulated Annealing para el Problema Maestro GAA
Fase 4: Optimización de parámetros de algoritmos
"""

from .sa_core import SimulatedAnnealing
from .cooling_schedules import (
    GeometricCooling,
    LinearCooling,
    ExponentialCooling,
    AdaptiveCooling
)
from .acceptance import MetropolisCriterion, AcceptanceCriterion

__all__ = [
    'SimulatedAnnealing',
    'GeometricCooling',
    'LinearCooling',
    'ExponentialCooling',
    'AdaptiveCooling',
    'MetropolisCriterion',
    'AcceptanceCriterion'
]
