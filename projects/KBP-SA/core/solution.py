"""
Knapsack Solution - Representación de Soluciones
Fase 1 GAA: Estructura de Datos

Representación: Vector binario x = [x_1, x_2, ..., x_n]
donde x_i ∈ {0, 1} indica si el ítem i está en la mochila
"""

from typing import List, Optional, Set
import numpy as np
from copy import deepcopy


class KnapsackSolution:
    """
    Representación de una solución del Knapsack Problem
    
    Attributes:
        selection: Vector binario de selección [0,1]^n
        value: Valor total de la solución
        weight: Peso total de la solución
        is_feasible: Indica si la solución es factible
    """
    
    def __init__(self, 
                 n: int, 
                 selection: Optional[np.ndarray] = None,
                 problem: Optional['KnapsackProblem'] = None):
        """
        Inicializa una solución
        
        Args:
            n: Número de ítems
            selection: Vector binario de selección (None = solución vacía)
            problem: Referencia al problema (para evaluación lazy)
        """
        self.n = n
        self.problem = problem
        
        # Inicializar selección
        if selection is None:
            self.selection = np.zeros(n, dtype=int)
        else:
            self.selection = np.array(selection, dtype=int)
            assert len(self.selection) == n, f"Selección debe tener {n} elementos"
            assert np.all((self.selection == 0) | (self.selection == 1)), "Selección debe ser binaria"
        
        # Atributos calculados (lazy evaluation)
        self._value = None
        self._weight = None
        self._is_feasible = None
    
    @classmethod
    def empty(cls, n: int, problem=None) -> 'KnapsackSolution':
        """Crea solución vacía (ningún ítem seleccionado)"""
        return cls(n=n, selection=np.zeros(n, dtype=int), problem=problem)
    
    @classmethod
    def full(cls, n: int, problem=None) -> 'KnapsackSolution':
        """Crea solución con todos los ítems seleccionados"""
        return cls(n=n, selection=np.ones(n, dtype=int), problem=problem)
    
    @classmethod
    def all(cls, n: int, problem=None) -> 'KnapsackSolution':
        """Alias de full() - Crea solución con todos los ítems seleccionados"""
        return cls.full(n, problem)
    
    @classmethod
    def random(cls, n: int, problem=None, rng: np.random.Generator = None) -> 'KnapsackSolution':
        """
        Crea solución aleatoria
        
        Args:
            n: Número de ítems
            problem: Problema asociado
            rng: Generador aleatorio
        """
        if rng is None:
            rng = np.random.default_rng()
        
        selection = rng.integers(0, 2, size=n, dtype=int)
        return cls(n=n, selection=selection, problem=problem)
    
    def evaluate(self, problem: 'KnapsackProblem') -> None:
        """
        Evalúa la solución respecto al problema
        
        Args:
            problem: Instancia del problema
        """
        self.problem = problem
        self._value = int(np.dot(self.selection, problem.values))
        self._weight = int(np.dot(self.selection, problem.weights))
        self._is_feasible = self._weight <= problem.capacity
    
    @property
    def value(self) -> int:
        """Valor total de la solución"""
        if self._value is None and self.problem is not None:
            self.evaluate(self.problem)
        return self._value if self._value is not None else 0
    
    @property
    def weight(self) -> int:
        """Peso total de la solución"""
        if self._weight is None and self.problem is not None:
            self.evaluate(self.problem)
        return self._weight if self._weight is not None else 0
    
    @property
    def is_feasible(self) -> bool:
        """Verifica si la solución es factible"""
        if self._is_feasible is None and self.problem is not None:
            self.evaluate(self.problem)
        return self._is_feasible if self._is_feasible is not None else True
    
    def get_selected_items(self) -> np.ndarray:
        """
        Obtiene índices de ítems seleccionados
        
        Returns:
            Array de índices donde selection[i] == 1
        """
        return np.where(self.selection == 1)[0]
    
    def get_unselected_items(self) -> np.ndarray:
        """
        Obtiene índices de ítems NO seleccionados
        
        Returns:
            Array de índices donde selection[i] == 0
        """
        return np.where(self.selection == 0)[0]
    
    def num_selected(self) -> int:
        """Número de ítems seleccionados"""
        return int(np.sum(self.selection))
    
    def flip(self, item_idx: int) -> None:
        """
        Cambia el estado de un ítem (0→1 o 1→0)
        
        Args:
            item_idx: Índice del ítem a cambiar
        """
        assert 0 <= item_idx < self.n, f"Índice {item_idx} fuera de rango [0, {self.n})"
        
        self.selection[item_idx] = 1 - self.selection[item_idx]
        
        # Invalidar caché
        self._value = None
        self._weight = None
        self._is_feasible = None
    
    def add_item(self, item_idx: int) -> None:
        """Agrega un ítem a la mochila"""
        if self.selection[item_idx] == 0:
            self.flip(item_idx)
    
    def remove_item(self, item_idx: int) -> None:
        """Remueve un ítem de la mochila"""
        if self.selection[item_idx] == 1:
            self.flip(item_idx)
    
    def copy(self) -> 'KnapsackSolution':
        """Crea copia profunda de la solución"""
        new_sol = KnapsackSolution(
            n=self.n,
            selection=self.selection.copy(),
            problem=self.problem
        )
        new_sol._value = self._value
        new_sol._weight = self._weight
        new_sol._is_feasible = self._is_feasible
        return new_sol
    
    def __eq__(self, other: 'KnapsackSolution') -> bool:
        """Comparación de igualdad"""
        return np.array_equal(self.selection, other.selection)
    
    def __hash__(self) -> int:
        """Hash para usar en sets/dicts"""
        return hash(tuple(self.selection))
    
    def __repr__(self) -> str:
        """Representación en string"""
        feasible_str = "✓" if self.is_feasible else "✗"
        return (f"KnapsackSolution(n={self.n}, selected={self.num_selected()}, "
                f"value={self.value}, weight={self.weight}, feasible={feasible_str})")
    
    def __str__(self) -> str:
        """String legible para humanos"""
        selected = self.get_selected_items()
        return f"Solution: {list(selected)} | Value={self.value}, Weight={self.weight}"
