"""
Función de Fitness - Template Base GAA

Este archivo se genera automáticamente desde 02-Components/Fitness-Function.md
Define cómo evaluar un algoritmo (AST) en instancias del problema.

AUTO-GENERATED - DO NOT EDIT MANUALLY
Edita: 02-Components/Fitness-Function.md
"""

from typing import List, Dict, Any
import numpy as np
from problem import Problem, Solution
from ast_nodes import ASTNode


class FitnessEvaluator:
    """Evalúa la calidad de un algoritmo representado como AST"""
    
    def __init__(self, problem: Problem, training_instances: List[Dict]):
        """
        Args:
            problem: Problema de optimización
            training_instances: Lista de instancias para entrenamiento
        """
        self.problem = problem
        self.training_instances = training_instances
        self.evaluation_count = 0
        
    def evaluate(self, algorithm_ast: ASTNode, max_evaluations: int = 1000) -> float:
        """
        Evalúa un algoritmo en las instancias de entrenamiento
        
        Args:
            algorithm_ast: AST que representa el algoritmo
            max_evaluations: Máximo de evaluaciones permitidas
            
        Returns:
            Fitness promedio del algoritmo
        """
        self.evaluation_count += 1
        
        results = []
        for instance_data in self.training_instances:
            # Crear problema específico para esta instancia
            problem_instance = type(self.problem)(instance_data)
            
            # Ejecutar algoritmo en esta instancia
            result = self._run_algorithm(algorithm_ast, problem_instance, max_evaluations)
            results.append(result)
        
        # Fitness = promedio de resultados en todas las instancias
        return np.mean(results)
    
    def _run_algorithm(self, algorithm_ast: ASTNode, problem: Problem, 
                       max_evals: int) -> float:
        """
        Ejecuta el algoritmo en una instancia específica
        
        Args:
            algorithm_ast: AST del algoritmo
            problem: Instancia del problema
            max_evals: Máximo de evaluaciones
            
        Returns:
            Mejor fitness encontrado
        """
        # Inicializar contexto de ejecución
        context = {
            'problem': problem,
            'current_solution': problem.random_solution(),
            'best_solution': None,
            'best_fitness': float('-inf') if problem.optimization_type == 'maximize' else float('inf'),
            'evaluations': 0,
            'max_evaluations': max_evals,
            'iteration': 0,
            'terminals': self._get_terminals(problem),
            'history': []
        }
        
        # Ejecutar AST
        try:
            algorithm_ast.execute(context)
        except Exception as e:
            # Si hay error en ejecución, penalizar
            print(f"Error ejecutando AST: {e}")
            return float('-inf') if problem.optimization_type == 'maximize' else float('inf')
        
        # Retornar mejor fitness encontrado
        return context['best_fitness']
    
    def _get_terminals(self, problem: Problem) -> Dict[str, callable]:
        """
        Retorna diccionario de terminales (operadores del dominio)
        
        Args:
            problem: Problema de optimización
            
        Returns:
            Diccionario {nombre: función}
        """
        # Estos terminales deben ser específicos del problema
        # Por ahora, incluimos algunos genéricos como ejemplo
        
        def greedy_construct(context: dict) -> None:
            """Construcción voraz básica"""
            context['current_solution'] = problem.random_solution()
            self._update_best(context)
        
        def local_search(context: dict) -> None:
            """Búsqueda local básica"""
            current = context['current_solution']
            improved = True
            
            while improved and context['evaluations'] < context['max_evaluations']:
                improved = False
                # Generar vecinos y seleccionar el mejor
                for _ in range(10):
                    neighbor = self._generate_neighbor(current, problem)
                    
                    if problem.is_feasible(neighbor):
                        f_current = problem.evaluate(current)
                        f_neighbor = problem.evaluate(neighbor)
                        context['evaluations'] += 2
                        
                        if self._is_better(f_neighbor, f_current, problem):
                            current = neighbor
                            improved = True
                            break
            
            context['current_solution'] = current
            self._update_best(context)
        
        def random_restart(context: dict) -> None:
            """Reinicio aleatorio"""
            context['current_solution'] = problem.random_solution()
            self._update_best(context)
        
        def perturbation(context: dict) -> None:
            """Perturbación de la solución actual"""
            context['current_solution'] = self._perturb(
                context['current_solution'], 
                problem
            )
        
        return {
            'GreedyConstruct': greedy_construct,
            'LocalSearch': local_search,
            'RandomRestart': random_restart,
            'Perturbation': perturbation,
        }
    
    def _update_best(self, context: dict) -> None:
        """Actualiza la mejor solución encontrada"""
        problem = context['problem']
        current = context['current_solution']
        
        if not problem.is_feasible(current):
            return
        
        f_current = problem.evaluate(current)
        context['evaluations'] += 1
        
        if context['best_solution'] is None:
            context['best_solution'] = current.copy()
            context['best_fitness'] = f_current
        else:
            if self._is_better(f_current, context['best_fitness'], problem):
                context['best_solution'] = current.copy()
                context['best_fitness'] = f_current
    
    def _is_better(self, f1: float, f2: float, problem: Problem) -> bool:
        """Compara dos fitness según el tipo de optimización"""
        if problem.optimization_type == 'maximize':
            return f1 > f2
        else:
            return f1 < f2
    
    def _generate_neighbor(self, solution: Solution, problem: Problem) -> Solution:
        """Genera un vecino de la solución (implementación básica)"""
        import copy
        neighbor = copy.deepcopy(solution)
        
        # Ejemplo: flip de un bit aleatorio para representación binaria
        if isinstance(neighbor.representation, list):
            idx = np.random.randint(0, len(neighbor.representation))
            neighbor.representation[idx] = 1 - neighbor.representation[idx]
        
        return neighbor
    
    def _perturb(self, solution: Solution, problem: Problem) -> Solution:
        """Perturba la solución (implementación básica)"""
        import copy
        perturbed = copy.deepcopy(solution)
        
        # Perturbar múltiples elementos
        if isinstance(perturbed.representation, list):
            n_changes = max(1, len(perturbed.representation) // 10)
            for _ in range(n_changes):
                idx = np.random.randint(0, len(perturbed.representation))
                perturbed.representation[idx] = 1 - perturbed.representation[idx]
        
        return perturbed


class MultiObjectiveFitness(FitnessEvaluator):
    """Evaluador para problemas multi-objetivo"""
    
    def __init__(self, problem: Problem, training_instances: List[Dict],
                 objectives: List[str]):
        super().__init__(problem, training_instances)
        self.objectives = objectives
    
    def evaluate(self, algorithm_ast: ASTNode, max_evaluations: int = 1000) -> List[float]:
        """
        Retorna vector de fitness para múltiples objetivos
        
        Returns:
            Lista de valores de fitness (uno por objetivo)
        """
        # TODO: Implementar evaluación multi-objetivo
        # Por ahora, retorna fitness simple
        single_fitness = super().evaluate(algorithm_ast, max_evaluations)
        return [single_fitness]


if __name__ == "__main__":
    # Ejemplo de uso
    from problem import create_problem
    from ast_nodes import random_ast
    
    # Crear problema de ejemplo
    instance = {
        'n': 10,
        'values': [10, 20, 30, 15, 25, 5, 12, 18, 22, 8],
        'weights': [5, 10, 15, 8, 12, 3, 6, 9, 11, 4],
        'capacity': 50
    }
    
    problem = create_problem('knapsack', instance)
    
    # Crear evaluador
    evaluator = FitnessEvaluator(problem, [instance])
    
    # Generar algoritmo aleatorio
    algorithm = random_ast(max_depth=2, terminals=['GreedyConstruct', 'LocalSearch'])
    
    # Evaluar
    fitness = evaluator.evaluate(algorithm, max_evaluations=100)
    print(f"Fitness del algoritmo: {fitness}")
    print(f"AST:\n{algorithm.to_string()}")
