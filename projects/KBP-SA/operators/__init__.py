"""
Módulo Operators - KBP-SA
Biblioteca de Operadores (Terminales GAA)
Fase 2: Extracción de terminales desde literatura
"""

from .constructive import (
    GreedyByValue,
    GreedyByWeight,
    GreedyByRatio,
    RandomConstruct
)

from .improvement import (
    FlipBestItem,
    FlipWorstItem,
    OneExchange,
    TwoExchange
)

from .perturbation import (
    RandomFlip,
    ShakeByRemoval,
    DestroyRepair
)

from .repair import (
    RepairByRemoval,
    RepairByGreedy
)

__all__ = [
    # Constructivos
    'GreedyByValue',
    'GreedyByWeight',
    'GreedyByRatio',
    'RandomConstruct',
    # Mejora
    'FlipBestItem',
    'FlipWorstItem',
    'OneExchange',
    'TwoExchange',
    # Perturbación
    'RandomFlip',
    'ShakeByRemoval',
    'DestroyRepair',
    # Reparación
    'RepairByRemoval',
    'RepairByGreedy'
]
