"""
Random Manager - KBP-SA
Gestión de semillas aleatorias para reproducibilidad
"""

import numpy as np
from typing import Optional


class RandomManager:
    """
    Gestor centralizado de aleatoriedad
    
    Garantiza reproducibilidad en todo el sistema
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa gestor aleatorio
        
        Args:
            seed: Semilla maestra
        """
        self.master_seed = seed
        self.rng = np.random.default_rng(seed)
        self._seed_counter = 0
    
    def get_rng(self) -> np.random.Generator:
        """Obtiene generador aleatorio"""
        return self.rng
    
    def get_child_seed(self) -> int:
        """
        Genera semilla derivada para sub-componentes
        
        Returns:
            Semilla derivada única
        """
        seed = self.rng.integers(0, 2**31)
        self._seed_counter += 1
        return int(seed)
    
    def get_child_rng(self) -> np.random.Generator:
        """
        Crea generador aleatorio derivado
        
        Returns:
            Generador con semilla derivada
        """
        child_seed = self.get_child_seed()
        return np.random.default_rng(child_seed)
    
    def reset(self, seed: Optional[int] = None):
        """Reinicia generador con nueva semilla"""
        self.master_seed = seed if seed is not None else self.master_seed
        self.rng = np.random.default_rng(self.master_seed)
        self._seed_counter = 0
    
    def __repr__(self) -> str:
        return f"RandomManager(seed={self.master_seed}, calls={self._seed_counter})"
