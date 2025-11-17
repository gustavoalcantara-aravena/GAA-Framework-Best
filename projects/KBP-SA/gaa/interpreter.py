"""
AST Interpreter - KBP-SA
Ejecución de algoritmos representados como AST
Fase 3 GAA: Interpretación y ejecución
"""

from typing import Dict, Any, Optional, Callable
import time
import numpy as np

from gaa.ast_nodes import ASTNode
from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator

# Import operators
from operators.constructive import *
from operators.improvement import *
from operators.perturbation import *
from operators.repair import *


class ExecutionContext:
    """
    Contexto de ejecución para el intérprete
    
    Mantiene:
    - Solución actual
    - Mejor solución encontrada
    - Estadísticas de ejecución
    - Presupuesto consumido
    """
    
    def __init__(self, 
                 problem: KnapsackProblem,
                 rng: Optional[np.random.Generator] = None):
        self.problem = problem
        self.evaluator = KnapsackEvaluator(problem)
        self.rng = rng if rng else np.random.default_rng()
        
        # Estado de ejecución
        self.current_solution = None
        self.best_solution = None
        self.best_value = 0
        
        # Estadísticas
        self.iterations = 0
        self.evaluations = 0
        self.start_time = None
        self.elapsed_time = 0.0
        self.improvement_iterations = []
        
        # Control de estancamiento
        self.iterations_without_improvement = 0
        self.last_improvement_iter = 0
    
    def update_solution(self, new_solution: KnapsackSolution):
        """Actualiza solución actual"""
        self.current_solution = new_solution
        self.evaluations += 1
        
        # Actualizar mejor solución
        if new_solution.is_feasible and new_solution.value > self.best_value:
            self.best_value = new_solution.value
            self.best_solution = new_solution.copy()
            self.improvement_iterations.append(self.iterations)
            self.iterations_without_improvement = 0
            self.last_improvement_iter = self.iterations
        else:
            self.iterations_without_improvement += 1
    
    def check_stagnation(self, threshold: int = 10) -> bool:
        """Verifica si hay estancamiento"""
        return self.iterations_without_improvement >= threshold
    
    def get_elapsed_time(self) -> float:
        """Obtiene tiempo transcurrido"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def start_timer(self):
        """Inicia cronómetro"""
        self.start_time = time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de ejecución"""
        return {
            'iterations': self.iterations,
            'evaluations': self.evaluations,
            'elapsed_time': self.get_elapsed_time(),
            'best_value': self.best_value,
            'improvement_iterations': len(self.improvement_iterations),
            'final_gap': self.evaluator.gap_to_optimal(self.best_solution) 
                        if self.best_solution else None
        }


class ASTInterpreter:
    """
    Intérprete de AST para KBP
    
    Ejecuta algoritmos representados como AST
    sobre instancias del problema
    """
    
    def __init__(self, problem: KnapsackProblem, seed: Optional[int] = None):
        """
        Inicializa intérprete
        
        Args:
            problem: Instancia del problema
            seed: Semilla aleatoria
        """
        self.problem = problem
        self.rng = np.random.default_rng(seed)
        self.context = None
        self.sa_instance = None  # Referencia al SA si se usa
        
        # Mapeo de operadores
        self._operator_map = self._build_operator_map()
    
    def _build_operator_map(self) -> Dict[str, Callable]:
        """Construye mapeo de nombres a operadores"""
        return {
            # Constructivos
            'GreedyByValue': GreedyByValue(self.problem),
            'GreedyByWeight': GreedyByWeight(self.problem),
            'GreedyByRatio': GreedyByRatio(self.problem),
            'RandomConstruct': RandomConstruct(self.problem),
            # Mejora
            'FlipBestItem': FlipBestItem(self.problem),
            'FlipWorstItem': FlipWorstItem(self.problem),
            'OneExchange': OneExchange(self.problem),
            'TwoExchange': TwoExchange(self.problem),
            # Perturbación
            'RandomFlip': RandomFlip(self.problem),
            'ShakeByRemoval': ShakeByRemoval(self.problem),
            'DestroyRepair': DestroyRepair(self.problem),
            # Reparación
            'RepairByRemoval': RepairByRemoval(self.problem),
            'RepairByGreedy': RepairByGreedy(self.problem)
        }
    
    def execute(self, algorithm: ASTNode) -> KnapsackSolution:
        """
        Ejecuta algoritmo completo
        
        Args:
            algorithm: AST del algoritmo
        
        Returns:
            Mejor solución encontrada
        """
        # Inicializar contexto
        self.context = ExecutionContext(self.problem, self.rng)
        self.context.start_timer()
        
        # Ejecutar AST
        self._execute_node(algorithm)
        
        # Retornar mejor solución
        return self.context.best_solution if self.context.best_solution else \
               KnapsackSolution.empty(self.problem.n, self.problem)
    
    def _execute_node(self, node: ASTNode) -> Optional[KnapsackSolution]:
        """
        Ejecuta un nodo del AST
        
        Args:
            node: Nodo a ejecutar
        
        Returns:
            Solución resultante (puede ser None)
        """
        node_type = node.__class__.__name__
        
        if node_type == 'Seq':
            return self._execute_seq(node)
        elif node_type == 'If':
            return self._execute_if(node)
        elif node_type == 'While':
            return self._execute_while(node)
        elif node_type == 'For':
            return self._execute_for(node)
        elif node_type == 'Call':
            return self._execute_call(node)
        elif node_type == 'GreedyConstruct':
            return self._execute_greedy_construct(node)
        elif node_type == 'LocalSearch':
            return self._execute_local_search(node)
        elif node_type == 'ChooseBestOf':
            return self._execute_choose_best_of(node)
        elif node_type == 'ApplyUntilNoImprove':
            return self._execute_apply_until_no_improve(node)
        elif node_type == 'DestroyRepair':
            return self._execute_destroy_repair(node)
        else:
            raise ValueError(f"Nodo no soportado: {node_type}")
    
    def _execute_seq(self, node) -> KnapsackSolution:
        """Ejecuta secuencia de operaciones"""
        solution = None
        for stmt in node.body:
            result = self._execute_node(stmt)
            if result is not None:
                solution = result
                self.context.update_solution(solution)
        return solution
    
    def _execute_if(self, node) -> KnapsackSolution:
        """Ejecuta condicional"""
        condition_met = self._evaluate_condition(node.condition, node.params)
        
        if condition_met:
            return self._execute_node(node.then_branch)
        elif node.else_branch:
            return self._execute_node(node.else_branch)
        
        return self.context.current_solution
    
    def _execute_while(self, node) -> KnapsackSolution:
        """Ejecuta bucle con presupuesto"""
        if node.budget_type == 'IterBudget':
            max_iter = int(node.budget_value)
            for _ in range(max_iter):
                self.context.iterations += 1
                self._execute_node(node.body)
        
        elif node.budget_type == 'TimeBudget':
            max_time = float(node.budget_value)
            while self.context.get_elapsed_time() < max_time:
                self.context.iterations += 1
                self._execute_node(node.body)
        
        return self.context.current_solution
    
    def _execute_for(self, node) -> KnapsackSolution:
        """Ejecuta bucle for"""
        for _ in range(node.iterations):
            self.context.iterations += 1
            self._execute_node(node.body)
        
        return self.context.current_solution
    
    def _execute_call(self, node) -> KnapsackSolution:
        """Ejecuta llamada a operador"""
        operator = self._operator_map.get(node.name)
        
        if operator is None:
            raise ValueError(f"Operador no encontrado: {node.name}")
        
        # Ejecutar operador
        if self.context.current_solution is None:
            # Si es constructivo, crear nueva solución
            if hasattr(operator, 'construct'):
                solution = operator.construct(self.rng)
            else:
                solution = KnapsackSolution.empty(self.problem.n, self.problem)
        else:
            # Aplicar operador a solución actual
            solution = operator(self.context.current_solution, self.rng)
        
        return solution
    
    def _execute_greedy_construct(self, node) -> KnapsackSolution:
        """Ejecuta construcción voraz"""
        constructor = self._operator_map.get(node.heuristic)
        
        if constructor is None:
            raise ValueError(f"Heurística no encontrada: {node.heuristic}")
        
        solution = constructor.construct(self.rng)
        return solution
    
    def _execute_local_search(self, node) -> KnapsackSolution:
        """Ejecuta búsqueda local"""
        if self.context.current_solution is None:
            return None
        
        operator = self._operator_map.get(node.neighborhood)
        
        if operator is None:
            raise ValueError(f"Vecindario no encontrado: {node.neighborhood}")
        
        # Aplicar búsqueda local
        improved_solution, improved = operator.improve(
            self.context.current_solution, 
            self.rng
        )
        
        # Criterio de aceptación
        if node.acceptance == 'Improving':
            return improved_solution if improved else self.context.current_solution
        elif node.acceptance == 'AlwaysAccept':
            return improved_solution
        else:  # Metropolis u otros
            return improved_solution
    
    def _execute_choose_best_of(self, node) -> KnapsackSolution:
        """Ejecuta multi-start"""
        best_solution = None
        best_value = -float('inf')
        
        for _ in range(node.n_tries):
            solution = self._execute_node(node.body)
            
            if solution and solution.is_feasible:
                if solution.value > best_value:
                    best_value = solution.value
                    best_solution = solution.copy()
        
        return best_solution
    
    def _execute_apply_until_no_improve(self, node) -> KnapsackSolution:
        """Ejecuta operador hasta no mejorar"""
        if self.context.current_solution is None:
            return None
        
        solution = self.context.current_solution.copy()
        iterations_without_improvement = 0
        
        while iterations_without_improvement < node.stop_value:
            new_solution = self._execute_node(node.body)
            
            if new_solution and new_solution.value > solution.value:
                solution = new_solution.copy()
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1
        
        return solution
    
    def _execute_destroy_repair(self, node) -> KnapsackSolution:
        """Ejecuta destrucción y reparación"""
        if self.context.current_solution is None:
            return None
        
        # Destruir
        destroyer = self._operator_map.get(node.destroy_op)
        destroyed = destroyer(self.context.current_solution, self.rng)
        
        # Reparar
        repairer = self._operator_map.get(node.repair_op)
        repaired = repairer(destroyed, self.rng)
        
        return repaired
    
    def _evaluate_condition(self, condition: str, params: Dict[str, Any]) -> bool:
        """Evalúa condición"""
        if condition == 'IsFeasible':
            return self.context.current_solution.is_feasible if self.context.current_solution else False
        
        elif condition == 'Improves':
            if self.context.current_solution is None:
                return False
            return self.context.current_solution.value > self.context.best_value
        
        elif condition == 'Prob':
            p = params.get('p', 0.5)
            return self.rng.random() < p
        
        elif condition == 'Stagnation':
            threshold = params.get('threshold', 10)
            return self.context.check_stagnation(threshold)
        
        else:
            return False
    
    def get_execution_report(self) -> Dict[str, Any]:
        """
        Genera reporte de ejecución
        
        Returns:
            Diccionario con estadísticas y resultados
        """
        if self.context is None:
            return {}
        
        stats = self.context.get_statistics()
        
        if self.context.best_solution:
            stats['best_solution'] = {
                'value': self.context.best_solution.value,
                'weight': self.context.best_solution.weight,
                'num_items': self.context.best_solution.num_selected(),
                'is_feasible': self.context.best_solution.is_feasible
            }
        
        return stats
    
    def get_convergence_data(self) -> Dict[str, Any]:
        """
        Obtiene datos de convergencia para visualización
        
        Returns:
            Diccionario con historiales de convergencia
        """
        if self.context is None:
            return {}
        
        data = {
            'iterations': self.context.iterations,
            'evaluations': self.context.evaluations,
            'improvement_iterations': self.context.improvement_iterations,
            'acceptance_history': []
        }
        
        # Si se usó SA, obtener sus datos de convergencia
        if self.sa_instance is not None:
            sa_data = self.sa_instance.get_convergence_data()
            data.update(sa_data)
        
        return data

