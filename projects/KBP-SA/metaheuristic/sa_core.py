"""
Simulated Annealing Core - KBP-SA
Motor principal de Simulated Annealing
Fase 4 GAA: Problema Maestro

Referencias:
- Kirkpatrick et al. (1983): Optimization by Simulated Annealing
- Metropolis et al. (1953): Equation of State Calculations
"""

from typing import Optional, Callable, Dict, Any, List
import numpy as np
import time
from pathlib import Path

from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
from metaheuristic.cooling_schedules import CoolingSchedule, GeometricCooling
from metaheuristic.acceptance import AcceptanceCriterion, MetropolisCriterion


class SimulatedAnnealing:
    """
    Simulated Annealing para Knapsack Problem
    
    Parámetros:
    -----------
    T0: Temperatura inicial
    alpha: Factor de enfriamiento (0 < alpha < 1)
    iterations_per_temp: Iteraciones por nivel de temperatura
    T_min: Temperatura mínima
    max_evaluations: Presupuesto máximo de evaluaciones
    
    Esquema de enfriamiento:
    ------------------------
    T_{k+1} = alpha * T_k  (geométrico)
    
    Criterio de aceptación:
    ----------------------
    Metropolis: P(accept) = exp(-ΔE / T) si ΔE > 0
    """
    
    def __init__(self,
                 problem: KnapsackProblem,
                 T0: float = 100.0,
                 alpha: float = 0.95,
                 iterations_per_temp: int = 100,
                 T_min: float = 0.01,
                 max_evaluations: int = 10000,
                 cooling_schedule: Optional[CoolingSchedule] = None,
                 acceptance_criterion: Optional[AcceptanceCriterion] = None,
                 seed: Optional[int] = None):
        """
        Inicializa Simulated Annealing
        
        Args:
            problem: Instancia del problema
            T0: Temperatura inicial
            alpha: Factor de enfriamiento
            iterations_per_temp: Iteraciones por temperatura
            T_min: Temperatura mínima
            max_evaluations: Máximo de evaluaciones
            cooling_schedule: Esquema de enfriamiento personalizado
            acceptance_criterion: Criterio de aceptación personalizado
            seed: Semilla aleatoria
        """
        self.problem = problem
        self.evaluator = KnapsackEvaluator(problem)
        self.rng = np.random.default_rng(seed)
        
        # Parámetros SA
        self.T0 = T0
        self.alpha = alpha
        self.iterations_per_temp = iterations_per_temp
        self.T_min = T_min
        self.max_evaluations = max_evaluations
        
        # Esquema de enfriamiento
        if cooling_schedule is None:
            self.cooling_schedule = GeometricCooling(alpha=alpha)
        else:
            self.cooling_schedule = cooling_schedule
        
        # Criterio de aceptación
        if acceptance_criterion is None:
            self.acceptance_criterion = MetropolisCriterion()
        else:
            self.acceptance_criterion = acceptance_criterion
        
        # Función de vecindario (será proporcionada externamente)
        self.neighborhood_function = None
        
        # Estadísticas de ejecución
        self.reset_statistics()
        
        # Tracking (opcional)
        self.tracker = None
        self.enable_tracking = False
        self.optimal_value = None  # Para calcular gap
    
    def set_tracking(self, tracker, optimal_value: Optional[int] = None):
        """
        Habilita tracking de variables
        
        Args:
            tracker: ExecutionTracker
            optimal_value: Valor óptimo conocido (para calcular gap)
        """
        self.tracker = tracker
        self.enable_tracking = True
        self.optimal_value = optimal_value
    
    def set_neighborhood(self, neighborhood_fn: Callable):
        """
        Establece función de vecindario
        
        Args:
            neighborhood_fn: Función que recibe (solution, rng) y retorna vecino
        """
        self.neighborhood_function = neighborhood_fn
    
    def optimize(self, 
                 initial_solution: KnapsackSolution,
                 verbose: bool = False) -> KnapsackSolution:
        """
        Ejecuta Simulated Annealing
        
        Args:
            initial_solution: Solución inicial
            verbose: Mostrar progreso
        
        Returns:
            Mejor solución encontrada
        """
        if self.neighborhood_function is None:
            raise ValueError("Debe establecer función de vecindario con set_neighborhood()")
        
        # Inicializar
        self.reset_statistics()
        self.start_time = time.time()
        
        current = initial_solution.copy()
        current.evaluate(self.problem)
        
        best = current.copy()
        best_value = current.value
        
        T = self.T0
        iteration = 0
        prev_temp = T
        
        # Bucle principal SA
        while T > self.T_min and self.evaluator.num_evaluations < self.max_evaluations:
            
            for _ in range(self.iterations_per_temp):
                # Generar vecino
                neighbor = self.neighborhood_function(current, self.rng)
                neighbor.evaluate(self.problem)
                
                # Calcular diferencia de energía (minimización: -fitness)
                delta_E = -(neighbor.value - current.value)
                
                # Calcular probabilidad de aceptación
                acceptance_prob = self.acceptance_criterion.acceptance_probability(
                    delta_E=delta_E,
                    temperature=T
                )
                
                # Decidir aceptación
                accept = self.acceptance_criterion.accept(
                    delta_E=delta_E,
                    temperature=T,
                    rng=self.rng
                )
                
                # Registrar decisión de aceptación
                self.acceptance_history.append(1 if accept else 0)
                
                # Tracking de iteración
                is_improvement = False
                if accept:
                    current = neighbor
                    self.accepted_moves += 1
                    
                    # Actualizar mejor solución
                    if current.is_feasible and current.value > best_value:
                        best = current.copy()
                        best_value = current.value
                        self.improvement_iterations.append(iteration)
                        is_improvement = True
                        
                        if self.enable_tracking and self.tracker:
                            self.tracker.track_improvement(iteration)
                        
                        if verbose:
                            print(f"Iter {iteration}, T={T:.2f}: Nueva mejor solución = {best_value}")
                
                # Tracking detallado
                if self.enable_tracking and self.tracker:
                    gap = None
                    if self.optimal_value is not None and best_value > 0:
                        gap = ((self.optimal_value - best_value) / self.optimal_value) * 100
                    
                    self.tracker.track_iteration(iteration, {
                        'temperature': T,
                        'current_value': current.value,
                        'best_value': best_value,
                        'current_weight': current.weight,
                        'best_weight': best.weight,
                        'is_feasible': current.is_feasible,
                        'delta_E': delta_E,
                        'acceptance_prob': acceptance_prob,
                        'accepted': accept,
                        'gap_to_optimal': gap,
                        'is_improvement': is_improvement
                    })
                    
                    self.tracker.track_acceptance(
                        iteration=iteration,
                        temperature=T,
                        delta_E=delta_E,
                        acceptance_prob=acceptance_prob,
                        accepted=accept,
                        improvement=is_improvement
                    )
                
                iteration += 1
                
                # Verificar presupuesto
                if self.evaluator.num_evaluations >= self.max_evaluations:
                    break
            
            # Enfriar temperatura
            new_T = self.cooling_schedule.cool(T, iteration)
            
            # Tracking de cambio de temperatura
            if self.enable_tracking and self.tracker:
                temp_level = len(self.temperature_history)
                self.tracker.track_temperature_change(temp_level, T, new_T)
            
            T = new_T
            self.temperature_history.append(T)
            
            # Registrar valor actual
            self.value_history.append(current.value)
        
        # Finalizar estadísticas
        self.elapsed_time = time.time() - self.start_time
        self.final_temperature = T
        self.total_iterations = iteration
        
        # Finalizar tracking
        if self.enable_tracking and self.tracker:
            self.tracker.calculate_acceptance_windows(self.acceptance_history)
            self.tracker.finalize_tracking(self.get_statistics())
        
        return best
    
    def reset_statistics(self):
        """Reinicia estadísticas de ejecución"""
        self.evaluator.reset_statistics()
        self.accepted_moves = 0
        self.improvement_iterations = []
        self.temperature_history = [self.T0]
        self.value_history = []
        self.acceptance_history = []  # Historial de aceptaciones por iteración
        self.start_time = None
        self.elapsed_time = 0.0
        self.final_temperature = self.T0
        self.total_iterations = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de ejecución
        
        Returns:
            Diccionario con métricas
        """
        acceptance_rate = (self.accepted_moves / self.total_iterations * 100 
                          if self.total_iterations > 0 else 0)
        
        return {
            'total_iterations': self.total_iterations,
            'evaluations': self.evaluator.num_evaluations,
            'elapsed_time': self.elapsed_time,
            'best_value': self.evaluator.best_value,
            'accepted_moves': self.accepted_moves,
            'acceptance_rate': acceptance_rate,
            'improvement_iterations': len(self.improvement_iterations),
            'final_temperature': self.final_temperature,
            'T0': self.T0,
            'T_min': self.T_min,
            'alpha': self.alpha
        }
    
    def get_convergence_data(self) -> Dict[str, List]:
        """
        Obtiene datos de convergencia para gráficos
        
        Returns:
            Diccionario con historiales
        """
        return {
            'temperatures': self.temperature_history,
            'values': self.value_history,
            'improvement_iterations': self.improvement_iterations,
            'acceptance_history': self.acceptance_history
        }
    
    def __repr__(self) -> str:
        """Representación en string"""
        return (f"SimulatedAnnealing(T0={self.T0}, alpha={self.alpha}, "
                f"iter_per_temp={self.iterations_per_temp}, T_min={self.T_min})")
