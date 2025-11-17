"""
Acceptance Criteria - KBP-SA
Criterios de aceptación para Simulated Annealing

Referencias:
- Metropolis et al. (1953): Equation of State Calculations
- Kirkpatrick et al. (1983): Optimization by Simulated Annealing
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Optional


class AcceptanceCriterion(ABC):
    """Clase base para criterios de aceptación"""
    
    @abstractmethod
    def accept(self, 
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """
        Decide si aceptar un movimiento
        
        Args:
            delta_E: Diferencia de energía (costo_nuevo - costo_actual)
            temperature: Temperatura actual
            rng: Generador aleatorio
        
        Returns:
            True si acepta, False si rechaza
        """
        pass
    
    def acceptance_probability(self, delta_E: float, temperature: float) -> float:
        """
        Calcula la probabilidad de aceptación (sin decisión)
        
        Args:
            delta_E: Diferencia de energía
            temperature: Temperatura actual
        
        Returns:
            Probabilidad en [0, 1]
        """
        # Por defecto, usa criterio binario
        if delta_E <= 0:
            return 1.0
        if temperature <= 0:
            return 0.0
        return np.exp(-delta_E / temperature)


class MetropolisCriterion(AcceptanceCriterion):
    """
    Criterio de Metropolis (clásico SA)
    
    Acepta siempre si mejora
    Si empeora, acepta con probabilidad exp(-ΔE/T)
    
    Propiedades:
    - T alta: acepta casi todo (exploración)
    - T baja: solo acepta mejoras (explotación)
    - ΔE grande: difícil aceptar empeoramientos
    """
    
    def accept(self, 
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """
        Criterio de Metropolis
        
        Args:
            delta_E: Para MAXIMIZACIÓN: -(f_new - f_current)
                     Negativo = mejora, Positivo = empeora
            temperature: Temperatura actual
            rng: Generador aleatorio
        
        Returns:
            True si acepta
        """
        # Si mejora (delta_E <= 0), siempre acepta
        if delta_E <= 0:
            return True
        
        # Si empeora, acepta con probabilidad de Boltzmann
        if temperature <= 0:
            return False
        
        probability = np.exp(-delta_E / temperature)
        return rng.random() < probability


class ThresholdAcceptance(AcceptanceCriterion):
    """
    Threshold Accepting (variante de SA)
    
    Acepta si la diferencia no excede un umbral
    No usa probabilidades
    
    Ventajas:
    - Determinístico (más reproducible)
    - Computacionalmente más eficiente
    """
    
    def __init__(self, initial_threshold: float):
        """
        Args:
            initial_threshold: Umbral inicial de aceptación
        """
        self.threshold = initial_threshold
    
    def accept(self,
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """Acepta si delta_E <= threshold"""
        # Usar temperatura como umbral dinámico
        return delta_E <= self.threshold
    
    def update_threshold(self, factor: float):
        """Reduce el umbral"""
        self.threshold *= factor


class GreatDelugeAcceptance(AcceptanceCriterion):
    """
    Great Deluge Algorithm
    
    Acepta si no supera un "nivel de agua" que sube gradualmente
    
    Ventajas:
    - Un solo parámetro
    - Fácil de entender
    """
    
    def __init__(self, initial_level: float, rain_speed: float = 0.01):
        """
        Args:
            initial_level: Nivel inicial
            rain_speed: Velocidad de subida del nivel
        """
        self.water_level = initial_level
        self.rain_speed = rain_speed
    
    def accept(self,
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """Acepta si el costo no supera el nivel de agua"""
        # Asumiendo que temperature representa el costo actual
        return temperature - delta_E >= self.water_level
    
    def raise_water_level(self):
        """Sube el nivel de agua"""
        self.water_level += self.rain_speed


class RecordToRecordTravel(AcceptanceCriterion):
    """
    Record-to-Record Travel
    
    Acepta si está dentro de un margen del mejor encontrado
    
    Ventajas:
    - Simple
    - Bueno para problemas con muchos óptimos locales
    """
    
    def __init__(self, deviation: float = 0.05):
        """
        Args:
            deviation: Desviación permitida (fracción del mejor)
        """
        self.deviation = deviation
        self.best_value = float('inf')  # Para minimización
    
    def accept(self,
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """Acepta si está cerca del récord"""
        current_value = temperature  # Usar temperatura como valor actual
        threshold = self.best_value * (1 + self.deviation)
        
        return current_value <= threshold
    
    def update_best(self, value: float):
        """Actualiza mejor valor"""
        if value < self.best_value:
            self.best_value = value


class AlwaysAccept(AcceptanceCriterion):
    """
    Siempre acepta (para testing)
    
    Equivalente a Random Walk
    """
    
    def accept(self,
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """Siempre acepta"""
        return True


class OnlyImproving(AcceptanceCriterion):
    """
    Solo acepta mejoras (Hill Climbing)
    
    No es SA real, pero útil para comparación
    """
    
    def accept(self,
               delta_E: float,
               temperature: float,
               rng: np.random.Generator) -> bool:
        """Solo acepta si mejora"""
        return delta_E <= 0


# Factory function
def get_acceptance_criterion(name: str, **params) -> AcceptanceCriterion:
    """
    Factory para crear criterios de aceptación
    
    Args:
        name: Nombre del criterio
        **params: Parámetros del criterio
    
    Returns:
        Instancia de AcceptanceCriterion
    """
    criteria = {
        'metropolis': MetropolisCriterion,
        'threshold': ThresholdAcceptance,
        'great_deluge': GreatDelugeAcceptance,
        'record_to_record': RecordToRecordTravel,
        'always': AlwaysAccept,
        'improving': OnlyImproving
    }
    
    criterion_class = criteria.get(name.lower())
    
    if criterion_class is None:
        raise ValueError(f"Criterio de aceptación desconocido: {name}")
    
    return criterion_class(**params)
