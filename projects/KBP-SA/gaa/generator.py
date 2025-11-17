"""
Algorithm Generator - KBP-SA
Generación aleatoria de algoritmos
Fase 3 GAA: Creación de AST aleatorios válidos
"""

from typing import Optional, List
import numpy as np
from .ast_nodes import *
from .grammar import Grammar


class AlgorithmGenerator:
    """
    Generador de algoritmos aleatorios para KBP
    
    Genera AST válidos según la gramática GAA
    con control de profundidad y diversidad
    """
    
    def __init__(self, 
                 grammar: Optional[Grammar] = None,
                 seed: Optional[int] = None):
        """
        Inicializa generador
        
        Args:
            grammar: Gramática a usar (default: nueva instancia)
            seed: Semilla aleatoria para reproducibilidad
        """
        self.grammar = grammar if grammar else Grammar()
        self.rng = np.random.default_rng(seed)
        self.seed = seed
    
    def generate(self, max_depth: Optional[int] = None) -> ASTNode:
        """
        Genera algoritmo aleatorio completo
        
        Args:
            max_depth: Profundidad máxima (default: desde grammar)
        
        Returns:
            AST raíz del algoritmo
        """
        if max_depth is None:
            max_depth = self.grammar.max_depth
        
        # Estructura típica de un algoritmo:
        # 1. Construcción inicial
        # 2. Bucle de mejora
        # 3. (Opcional) Perturbación/diversificación
        
        algorithm_structure = self.rng.choice([
            'simple',      # Construcción + mejora
            'iterative',   # Construcción + bucle con mejora
            'multistart',  # Múltiples construcciones
            'complex'      # Estructura completa con perturbación
        ])
        
        if algorithm_structure == 'simple':
            return self._generate_simple_algorithm()
        elif algorithm_structure == 'iterative':
            return self._generate_iterative_algorithm()
        elif algorithm_structure == 'multistart':
            return self._generate_multistart_algorithm()
        else:
            return self._generate_complex_algorithm()
    
    def _generate_simple_algorithm(self) -> Seq:
        """
        Genera algoritmo simple: construcción + mejora
        
        Estructura:
        1. GreedyConstruct
        2. LocalSearch o mejora
        """
        construction = self._generate_construction()
        improvement = self._generate_improvement()
        
        return Seq(body=[construction, improvement])
    
    def _generate_iterative_algorithm(self) -> Seq:
        """
        Genera algoritmo iterativo con bucle
        
        Estructura:
        1. Construcción inicial
        2. While/For con mejora iterativa
        """
        construction = self._generate_construction()
        
        # Bucle de mejora
        budget_type = self.rng.choice(['IterBudget', 'TimeBudget'])
        if budget_type == 'IterBudget':
            budget_value = int(self.rng.choice([100, 500, 1000]))
        else:
            budget_value = float(self.rng.choice([1.0, 5.0, 10.0]))
        
        loop_body = self._generate_improvement_sequence()
        
        loop = While(
            budget_type=budget_type,
            budget_value=budget_value,
            body=loop_body
        )
        
        return Seq(body=[construction, loop])
    
    def _generate_multistart_algorithm(self) -> Seq:
        """
        Genera algoritmo multi-start
        
        Estructura:
        ChooseBestOf(n, construcción + mejora)
        """
        n_tries = int(self.rng.choice([5, 10, 20]))
        
        trial_body = Seq(body=[
            self._generate_construction(),
            self._generate_improvement()
        ])
        
        multistart = ChooseBestOf(n_tries=n_tries, body=trial_body)
        
        return Seq(body=[multistart])
    
    def _generate_complex_algorithm(self) -> Seq:
        """
        Genera algoritmo complejo con todas las fases
        
        Estructura:
        1. Construcción
        2. Mejora inicial
        3. Bucle con perturbación y mejora
        """
        construction = self._generate_construction()
        initial_improvement = self._generate_improvement()
        
        # Bucle principal
        iterations = int(self.rng.choice([50, 100, 200]))
        
        # Cuerpo del bucle: perturbación + mejora + condicional
        perturbation = self._generate_perturbation()
        improvement = self._generate_improvement()
        
        # Condicional de aceptación
        condition = self.rng.choice(['Improves', 'Prob'])
        if condition == 'Prob':
            params = {'p': float(self.rng.uniform(0.1, 0.5))}
        else:
            params = {}
        
        conditional = If(
            condition=condition,
            then_branch=Call(name='Accept'),
            else_branch=Call(name='Reject'),
            params=params
        )
        
        loop_body = Seq(body=[perturbation, improvement, conditional])
        
        main_loop = For(iterations=iterations, body=loop_body)
        
        return Seq(body=[construction, initial_improvement, main_loop])
    
    def _generate_construction(self) -> GreedyConstruct:
        """Genera paso de construcción aleatorio"""
        heuristic = self.rng.choice(list(self.grammar.CONSTRUCTIVE_TERMINALS))
        return GreedyConstruct(heuristic=heuristic)
    
    def _generate_improvement(self) -> ASTNode:
        """Genera paso de mejora aleatorio"""
        improvement_type = self.rng.choice([
            'local_search',
            'apply_until_no_improve',
            'single_operator'
        ])
        
        if improvement_type == 'local_search':
            neighborhood = self.rng.choice(list(self.grammar.NEIGHBORHOODS))
            acceptance = self.rng.choice(list(self.grammar.ACCEPTANCE_CRITERIA))
            return LocalSearch(neighborhood=neighborhood, acceptance=acceptance)
        
        elif improvement_type == 'apply_until_no_improve':
            operator = self.rng.choice(list(self.grammar.IMPROVEMENT_TERMINALS))
            return ApplyUntilNoImprove(
                body=Call(name=operator),
                stop_condition='Stagnation',
                stop_value=int(self.rng.choice([5, 10, 20]))
            )
        
        else:
            operator = self.rng.choice(list(self.grammar.IMPROVEMENT_TERMINALS))
            return Call(name=operator)
    
    def _generate_improvement_sequence(self) -> Seq:
        """Genera secuencia de operadores de mejora"""
        n_operators = int(self.rng.choice([1, 2, 3]))
        operators = []
        
        for _ in range(n_operators):
            operators.append(self._generate_improvement())
        
        return Seq(body=operators)
    
    def _generate_perturbation(self) -> ASTNode:
        """Genera paso de perturbación aleatorio"""
        perturbation_type = self.rng.choice([
            'simple',
            'destroy_repair'
        ])
        
        if perturbation_type == 'destroy_repair':
            destroy = self.rng.choice(['ShakeByRemoval', 'RandomFlip'])
            repair = self.rng.choice(list(self.grammar.REPAIR_TERMINALS))
            rate = float(self.rng.uniform(0.1, 0.5))
            return DestroyRepair(
                destroy_op=destroy,
                repair_op=repair,
                destruction_rate=rate
            )
        else:
            operator = self.rng.choice(list(self.grammar.PERTURBATION_TERMINALS))
            return Call(name=operator)
    
    def generate_population(self, 
                          size: int, 
                          max_depth: Optional[int] = None) -> List[ASTNode]:
        """
        Genera población de algoritmos
        
        Args:
            size: Tamaño de la población
            max_depth: Profundidad máxima
        
        Returns:
            Lista de AST
        """
        population = []
        
        for _ in range(size):
            algorithm = self.generate(max_depth)
            population.append(algorithm)
        
        return population
    
    def generate_with_validation(self, 
                                max_attempts: int = 100,
                                max_depth: Optional[int] = None) -> Optional[ASTNode]:
        """
        Genera algoritmo válido con validación
        
        Args:
            max_attempts: Intentos máximos
            max_depth: Profundidad máxima
        
        Returns:
            AST válido o None si falla
        """
        for attempt in range(max_attempts):
            algorithm = self.generate(max_depth)
            errors = self.grammar.validate_ast(algorithm)
            
            if not errors:
                return algorithm
        
        return None
    
    def get_generation_stats(self, algorithm: ASTNode) -> dict:
        """
        Obtiene estadísticas del algoritmo generado
        
        Args:
            algorithm: AST generado
        
        Returns:
            Diccionario con estadísticas
        """
        stats = self.grammar.get_statistics(algorithm)
        stats['seed'] = self.seed
        return stats
