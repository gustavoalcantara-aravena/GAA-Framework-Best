"""
Cooling Schedules - KBP-SA
Esquemas de enfriamiento para Simulated Annealing

Referencias:
- Kirkpatrick et al. (1983): Geometric cooling
- Aarts & Korst (1989): Simulated Annealing and Boltzmann Machines
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class CoolingSchedule(ABC):
    """Clase base para esquemas de enfriamiento"""
    
    @abstractmethod
    def cool(self, current_temp: float, iteration: int) -> float:
        """
        Calcula nueva temperatura
        
        Args:
            current_temp: Temperatura actual
            iteration: Iteración actual
        
        Returns:
            Nueva temperatura
        """
        pass
    
    def __repr__(self) -> str:
        return self.__class__.__name__


class GeometricCooling(CoolingSchedule):
    """
    Enfriamiento geométrico (más común)
    
    T_{k+1} = alpha * T_k
    
    Parámetros:
    - alpha: factor de enfriamiento (típicamente 0.8-0.99)
    
    Ventajas:
    - Simple y efectivo
    - Ampliamente utilizado
    - Buen balance exploración/explotación
    """
    
    def __init__(self, alpha: float = 0.95):
        """
        Args:
            alpha: Factor de enfriamiento (0 < alpha < 1)
        """
        assert 0 < alpha < 1, "Alpha debe estar en (0, 1)"
        self.alpha = alpha
    
    def cool(self, current_temp: float, iteration: int) -> float:
        """Enfriamiento geométrico"""
        return self.alpha * current_temp
    
    def __repr__(self) -> str:
        return f"GeometricCooling(alpha={self.alpha})"


class LinearCooling(CoolingSchedule):
    """
    Enfriamiento lineal
    
    T_k = T_0 - k * delta
    
    Parámetros:
    - T0: temperatura inicial
    - delta: decremento por iteración
    
    Ventajas:
    - Predecible
    - Fácil control del tiempo de ejecución
    """
    
    def __init__(self, T0: float, delta: float):
        """
        Args:
            T0: Temperatura inicial
            delta: Decremento por iteración
        """
        self.T0 = T0
        self.delta = delta
    
    def cool(self, current_temp: float, iteration: int) -> float:
        """Enfriamiento lineal"""
        new_temp = self.T0 - iteration * self.delta
        return max(new_temp, 0.01)  # Evitar temperatura negativa
    
    def __repr__(self) -> str:
        return f"LinearCooling(T0={self.T0}, delta={self.delta})"


class ExponentialCooling(CoolingSchedule):
    """
    Enfriamiento exponencial
    
    T_k = T_0 * exp(-k * rate)
    
    Parámetros:
    - T0: temperatura inicial
    - rate: tasa de enfriamiento
    
    Ventajas:
    - Enfriamiento rápido inicial
    - Desaceleración gradual
    """
    
    def __init__(self, T0: float, rate: float = 0.01):
        """
        Args:
            T0: Temperatura inicial
            rate: Tasa de enfriamiento
        """
        self.T0 = T0
        self.rate = rate
    
    def cool(self, current_temp: float, iteration: int) -> float:
        """Enfriamiento exponencial"""
        return self.T0 * np.exp(-iteration * self.rate)
    
    def __repr__(self) -> str:
        return f"ExponentialCooling(T0={self.T0}, rate={self.rate})"


class LogarithmicCooling(CoolingSchedule):
    """
    Enfriamiento logarítmico (muy lento)
    
    T_k = c / log(1 + k)
    
    Parámetros:
    - c: constante de enfriamiento
    
    Ventajas:
    - Garantías teóricas de convergencia
    - Muy lento (no práctico para aplicaciones reales)
    """
    
    def __init__(self, c: float = 100.0):
        """
        Args:
            c: Constante de enfriamiento
        """
        self.c = c
    
    def cool(self, current_temp: float, iteration: int) -> float:
        """Enfriamiento logarítmico"""
        return self.c / np.log(1 + iteration + 1)  # +1 para evitar log(0)
    
    def __repr__(self) -> str:
        return f"LogarithmicCooling(c={self.c})"


class AdaptiveCooling(CoolingSchedule):
    """
    Enfriamiento adaptativo
    
    Ajusta alpha según tasa de aceptación:
    - Si muchas aceptaciones: enfría más rápido
    - Si pocas aceptaciones: enfría más lento
    
    Ventajas:
    - Auto-ajuste según progreso
    - Mejor adaptación a diferentes problemas
    """
    
    def __init__(self, 
                 alpha_min: float = 0.90,
                 alpha_max: float = 0.99,
                 target_acceptance: float = 0.5):
        """
        Args:
            alpha_min: Alpha mínimo
            alpha_max: Alpha máximo
            target_acceptance: Tasa de aceptación objetivo
        """
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.target_acceptance = target_acceptance
        self.current_alpha = (alpha_min + alpha_max) / 2
        
        # Historial de aceptaciones (ventana deslizante)
        self.acceptance_window = []
        self.window_size = 100
    
    def update_acceptance(self, accepted: bool):
        """
        Actualiza historial de aceptaciones
        
        Args:
            accepted: Si el movimiento fue aceptado
        """
        self.acceptance_window.append(1 if accepted else 0)
        
        # Mantener ventana de tamaño fijo
        if len(self.acceptance_window) > self.window_size:
            self.acceptance_window.pop(0)
    
    def cool(self, current_temp: float, iteration: int) -> float:
        """Enfriamiento adaptativo"""
        if len(self.acceptance_window) >= 10:
            # Calcular tasa de aceptación actual
            acceptance_rate = sum(self.acceptance_window) / len(self.acceptance_window)
            
            # Ajustar alpha
            if acceptance_rate > self.target_acceptance:
                # Muchas aceptaciones: enfría más rápido
                self.current_alpha = max(self.alpha_min, 
                                        self.current_alpha - 0.01)
            else:
                # Pocas aceptaciones: enfría más lento
                self.current_alpha = min(self.alpha_max,
                                        self.current_alpha + 0.01)
        
        return self.current_alpha * current_temp
    
    def __repr__(self) -> str:
        return (f"AdaptiveCooling(alpha_range=[{self.alpha_min}, {self.alpha_max}], "
                f"current={self.current_alpha:.3f})")


# Factory function
def get_cooling_schedule(name: str, **params) -> CoolingSchedule:
    """
    Factory para crear esquemas de enfriamiento
    
    Args:
        name: Nombre del esquema ('geometric', 'linear', 'exponential', etc.)
        **params: Parámetros del esquema
    
    Returns:
        Instancia de CoolingSchedule
    """
    schedules = {
        'geometric': GeometricCooling,
        'linear': LinearCooling,
        'exponential': ExponentialCooling,
        'logarithmic': LogarithmicCooling,
        'adaptive': AdaptiveCooling
    }
    
    schedule_class = schedules.get(name.lower())
    
    if schedule_class is None:
        raise ValueError(f"Esquema de enfriamiento desconocido: {name}")
    
    return schedule_class(**params)
