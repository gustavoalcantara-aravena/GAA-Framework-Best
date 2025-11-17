"""
Dataset Validator - KBP-SA
Validación de instancias
"""

from pathlib import Path
from typing import List, Tuple
from core.problem import KnapsackProblem


class DatasetValidator:
    """Validador de instancias del problema"""
    
    @staticmethod
    def validate_instance(problem: KnapsackProblem) -> Tuple[bool, List[str]]:
        """
        Valida una instancia
        
        Args:
            problem: Instancia a validar
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        # Validaciones básicas
        if problem.n <= 0:
            errors.append("n debe ser positivo")
        
        if problem.capacity <= 0:
            errors.append("Capacidad debe ser positiva")
        
        if len(problem.values) != problem.n:
            errors.append(f"Número de valores ({len(problem.values)}) != n ({problem.n})")
        
        if len(problem.weights) != problem.n:
            errors.append(f"Número de pesos ({len(problem.weights)}) != n ({problem.n})")
        
        if any(problem.values < 0):
            errors.append("Valores deben ser no negativos")
        
        if any(problem.weights <= 0):
            errors.append("Pesos deben ser positivos")
        
        return len(errors) == 0, errors
