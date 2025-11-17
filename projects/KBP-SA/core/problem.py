"""
Knapsack Problem - Definición del Problema
Fase 1 GAA: Modelado Matemático

Referencia: Pisinger (2005) - "Where are the hard knapsack problems?"
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class KnapsackProblem:
    """
    Definición del Knapsack Problem (0/1)
    
    Modelo Matemático:
    ------------------
    Maximizar: Z = Σ(v_i * x_i)  para i=1..n
    
    Sujeto a:
        Σ(w_i * x_i) ≤ W         (restricción de capacidad)
        x_i ∈ {0, 1}             (decisión binaria)
    
    Donde:
        n: número de ítems
        v_i: valor del ítem i
        w_i: peso del ítem i
        W: capacidad máxima de la mochila
        x_i: variable de decisión (1=seleccionado, 0=no seleccionado)
    """
    
    n: int                    # Número de ítems
    capacity: int             # Capacidad W de la mochila
    values: np.ndarray        # Vector de valores [v_1, ..., v_n]
    weights: np.ndarray       # Vector de pesos [w_1, ..., w_n]
    optimal_value: int = None # Valor óptimo conocido (si existe)
    name: str = "KBP"         # Nombre de la instancia
    
    def __post_init__(self):
        """Validación y conversión de tipos"""
        # Validaciones básicas
        if self.n <= 0:
            raise ValueError(f"Número de ítems debe ser positivo, recibido: {self.n}")
        if self.capacity <= 0:
            raise ValueError(f"Capacidad debe ser positiva, recibida: {self.capacity}")
        
        # Convertir a numpy arrays si es necesario
        if not isinstance(self.values, np.ndarray):
            self.values = np.array(self.values, dtype=int)
        if not isinstance(self.weights, np.ndarray):
            self.weights = np.array(self.weights, dtype=int)
        
        # Validaciones de arrays
        if len(self.values) == 0 or len(self.weights) == 0:
            raise ValueError("Arrays de valores y pesos no pueden estar vacíos")
        
        assert len(self.values) == self.n, f"Número de valores ({len(self.values)}) != n ({self.n})"
        assert len(self.weights) == self.n, f"Número de pesos ({len(self.weights)}) != n ({self.n})"
        
        # Verificar que todos los valores y pesos sean válidos
        if not np.all(self.values >= 0):
            invalid_indices = np.where(self.values < 0)[0].tolist()
            raise ValueError(f"Todos los valores deben ser no negativos. Valores inválidos en índices: {invalid_indices}")
        if not np.all(self.weights > 0):
            invalid_indices = np.where(self.weights <= 0)[0].tolist()
            raise ValueError(f"Todos los pesos deben ser positivos. Pesos inválidos en índices: {invalid_indices}")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnapsackProblem':
        """
        Crea instancia desde diccionario
        
        Args:
            data: Diccionario con claves 'n', 'capacity', 'values', 'weights'
        
        Returns:
            Instancia de KnapsackProblem
        """
        return cls(
            n=data['n'],
            capacity=data['capacity'],
            values=np.array(data['values'], dtype=int),
            weights=np.array(data['weights'], dtype=int),
            optimal_value=data.get('optimal_value'),
            name=data.get('filename', 'KBP')
        )
    
    def get_ratio(self) -> np.ndarray:
        """
        Calcula ratio valor/peso para cada ítem
        
        Returns:
            Array de ratios [v_1/w_1, ..., v_n/w_n]
        """
        return self.values / self.weights
    
    def get_efficiency_order(self) -> np.ndarray:
        """
        Obtiene índices ordenados por ratio v/w decreciente
        
        Returns:
            Array de índices ordenados
        """
        return np.argsort(self.get_ratio())[::-1]
    
    def total_value(self) -> int:
        """Suma total de todos los valores"""
        return int(np.sum(self.values))
    
    def total_weight(self) -> int:
        """Suma total de todos los pesos"""
        return int(np.sum(self.weights))
    
    def is_trivial(self) -> bool:
        """
        Verifica si el problema es trivial (caben todos los ítems)
        
        Returns:
            True si Σw_i ≤ W
        """
        return self.total_weight() <= self.capacity
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Estadísticas descriptivas de la instancia
        
        Returns:
            Diccionario con estadísticas
        """
        ratios = self.get_ratio()
        
        return {
            'n': self.n,
            'capacity': self.capacity,
            'total_value': self.total_value(),
            'total_weight': self.total_weight(),
            'optimal_value': self.optimal_value,
            'is_trivial': self.is_trivial(),
            'capacity_ratio': self.capacity / self.total_weight(),
            'values': {
                'min': int(np.min(self.values)),
                'max': int(np.max(self.values)),
                'mean': float(np.mean(self.values)),
                'std': float(np.std(self.values))
            },
            'weights': {
                'min': int(np.min(self.weights)),
                'max': int(np.max(self.weights)),
                'mean': float(np.mean(self.weights)),
                'std': float(np.std(self.weights))
            },
            'ratios': {
                'min': float(np.min(ratios)),
                'max': float(np.max(ratios)),
                'mean': float(np.mean(ratios)),
                'std': float(np.std(ratios))
            }
        }
    
    def __repr__(self) -> str:
        """Representación en string"""
        return (f"KnapsackProblem(name='{self.name}', n={self.n}, "
                f"W={self.capacity}, optimal={self.optimal_value})")
