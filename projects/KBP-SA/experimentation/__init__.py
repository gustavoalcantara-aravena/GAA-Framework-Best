"""
Módulo Experimentation - KBP-SA
Análisis estadístico y experimentación
Fase 5 GAA: Diseño y ejecución de experimentos
"""

from .runner import ExperimentRunner
from .metrics import QualityMetrics, PerformanceMetrics
from .statistics import StatisticalAnalyzer
from .visualization import ResultsVisualizer

__all__ = [
    'ExperimentRunner',
    'QualityMetrics',
    'PerformanceMetrics',
    'StatisticalAnalyzer',
    'ResultsVisualizer'
]
