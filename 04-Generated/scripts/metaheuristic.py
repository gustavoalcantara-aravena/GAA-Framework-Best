"""
Metaheurística - Template Base GAA

Este archivo se genera automáticamente desde 00-Core/Metaheuristic.md
Implementa la metaheurística seleccionada para evolucionar algoritmos.

AUTO-GENERATED - DO NOT EDIT MANUALLY
Edita: 00-Core/Metaheuristic.md o projects/<proyecto>/problema_metaheuristica.md
"""

from typing import List, Callable, Tuple, Any
from abc import ABC, abstractmethod
import random
import copy
from ast_nodes import ASTNode, random_ast


class Metaheuristic(ABC):
    """Clase base para metaheurísticas"""
    
    def __init__(self, fitness_function: Callable, max_evaluations: int = 10000):
        """
        Args:
            fitness_function: Función que evalúa un individuo (AST)
            max_evaluations: Máximo de evaluaciones permitidas
        """
        self.fitness_func = fitness_function
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.best_solution = None
        self.best_fitness = float('-inf')
        self.history = []
    
    @abstractmethod
    def optimize(self) -> Tuple[ASTNode, float]:
        """
        Ejecuta la metaheurística
        
        Returns:
            (mejor_algoritmo, mejor_fitness)
        """
        pass
    
    def evaluate(self, individual: ASTNode) -> float:
        """Evalúa un individuo y actualiza contador"""
        self.evaluations += 1
        fitness = self.fitness_func(individual)
        
        # Actualizar mejor solución
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = copy.deepcopy(individual)
        
        # Guardar en historial
        self.history.append({
            'evaluation': self.evaluations,
            'fitness': fitness,
            'best_fitness': self.best_fitness
        })
        
        return fitness


# ============================================================================
# SIMULATED ANNEALING
# ============================================================================

class SimulatedAnnealing(Metaheuristic):
    """Simulated Annealing para optimización de AST"""
    
    def __init__(self, fitness_function: Callable, 
                 T0: float = 100.0,
                 alpha: float = 0.95,
                 iterations_per_temp: int = 100,
                 T_min: float = 0.01,
                 max_evaluations: int = 10000):
        """
        Args:
            T0: Temperatura inicial
            alpha: Factor de enfriamiento (0 < alpha < 1)
            iterations_per_temp: Iteraciones por nivel de temperatura
            T_min: Temperatura mínima
        """
        super().__init__(fitness_function, max_evaluations)
        self.T0 = T0
        self.alpha = alpha
        self.iterations_per_temp = iterations_per_temp
        self.T_min = T_min
    
    def optimize(self) -> Tuple[ASTNode, float]:
        """Ejecuta Simulated Annealing"""
        # Solución inicial
        current = random_ast(max_depth=3)
        current_fitness = self.evaluate(current)
        
        # Mejor solución
        best = copy.deepcopy(current)
        best_fitness = current_fitness
        
        # Temperatura
        T = self.T0
        
        print(f"🔥 Simulated Annealing iniciado (T0={self.T0}, α={self.alpha})")
        
        while T > self.T_min and self.evaluations < self.max_evaluations:
            for _ in range(self.iterations_per_temp):
                if self.evaluations >= self.max_evaluations:
                    break
                
                # Generar vecino (mutación)
                neighbor = self._mutate(current)
                neighbor_fitness = self.evaluate(neighbor)
                
                # Criterio de aceptación de Metropolis
                delta = neighbor_fitness - current_fitness
                
                if delta > 0 or random.random() < self._acceptance_probability(delta, T):
                    current = neighbor
                    current_fitness = neighbor_fitness
                    
                    if current_fitness > best_fitness:
                        best = copy.deepcopy(current)
                        best_fitness = current_fitness
            
            # Enfriamiento
            T *= self.alpha
            
            if self.evaluations % 1000 == 0:
                print(f"  Eval {self.evaluations}/{self.max_evaluations} | "
                      f"T={T:.4f} | Best={best_fitness:.4f}")
        
        print(f"✅ SA finalizado: {self.evaluations} evaluaciones")
        return best, best_fitness
    
    def _acceptance_probability(self, delta: float, T: float) -> float:
        """Probabilidad de aceptación de Metropolis"""
        import math
        return math.exp(delta / T)
    
    def _mutate(self, ast: ASTNode) -> ASTNode:
        """Muta un AST (operador básico)"""
        # Implementación simple: regenerar subárbol aleatorio
        mutated = copy.deepcopy(ast)
        
        # Obtener todos los nodos
        nodes = mutated.get_all_nodes()
        
        if len(nodes) > 1:
            # Seleccionar nodo aleatorio (no la raíz)
            idx = random.randint(1, len(nodes) - 1)
            # Reemplazar con nuevo subárbol
            nodes[idx] = random_ast(max_depth=2)
        
        return mutated


# ============================================================================
# GENETIC PROGRAMMING
# ============================================================================

class GeneticProgramming(Metaheuristic):
    """Genetic Programming para evolucionar algoritmos"""
    
    def __init__(self, fitness_function: Callable,
                 population_size: int = 100,
                 n_generations: int = 50,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.2,
                 tournament_size: int = 3,
                 max_evaluations: int = 10000):
        super().__init__(fitness_function, max_evaluations)
        self.pop_size = population_size
        self.n_generations = n_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
    
    def optimize(self) -> Tuple[ASTNode, float]:
        """Ejecuta Genetic Programming"""
        # Población inicial
        population = [random_ast(max_depth=3) for _ in range(self.pop_size)]
        fitnesses = [self.evaluate(ind) for ind in population]
        
        print(f"🧬 Genetic Programming iniciado (Pop={self.pop_size}, Gen={self.n_generations})")
        
        for gen in range(self.n_generations):
            if self.evaluations >= self.max_evaluations:
                break
            
            # Nueva generación
            new_population = []
            
            while len(new_population) < self.pop_size:
                if self.evaluations >= self.max_evaluations:
                    break
                
                # Selección
                parent1 = self._tournament_selection(population, fitnesses)
                parent2 = self._tournament_selection(population, fitnesses)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
                
                # Mutación
                if random.random() < self.mutation_rate:
                    child1 = self._mutate(child1)
                if random.random() < self.mutation_rate:
                    child2 = self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Evaluar nueva generación
            population = new_population[:self.pop_size]
            fitnesses = [self.evaluate(ind) for ind in population]
            
            if gen % 10 == 0:
                print(f"  Gen {gen}/{self.n_generations} | "
                      f"Best={max(fitnesses):.4f} | Avg={sum(fitnesses)/len(fitnesses):.4f}")
        
        # Retornar mejor individuo
        best_idx = fitnesses.index(max(fitnesses))
        print(f"✅ GP finalizado: {self.evaluations} evaluaciones")
        return population[best_idx], fitnesses[best_idx]
    
    def _tournament_selection(self, population: List[ASTNode], 
                             fitnesses: List[float]) -> ASTNode:
        """Selección por torneo"""
        tournament = random.sample(list(zip(population, fitnesses)), self.tournament_size)
        winner = max(tournament, key=lambda x: x[1])
        return winner[0]
    
    def _crossover(self, parent1: ASTNode, parent2: ASTNode) -> Tuple[ASTNode, ASTNode]:
        """Crossover de subárboles"""
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Obtener nodos de ambos padres
        nodes1 = child1.get_all_nodes()
        nodes2 = child2.get_all_nodes()
        
        if len(nodes1) > 1 and len(nodes2) > 1:
            # Seleccionar puntos de crossover
            idx1 = random.randint(1, len(nodes1) - 1)
            idx2 = random.randint(1, len(nodes2) - 1)
            
            # Intercambiar subárboles
            nodes1[idx1], nodes2[idx2] = nodes2[idx2], nodes1[idx1]
        
        return child1, child2
    
    def _mutate(self, ast: ASTNode) -> ASTNode:
        """Mutación de AST"""
        mutated = copy.deepcopy(ast)
        nodes = mutated.get_all_nodes()
        
        if len(nodes) > 1:
            idx = random.randint(1, len(nodes) - 1)
            nodes[idx] = random_ast(max_depth=2)
        
        return mutated


# ============================================================================
# FACTORY
# ============================================================================

def create_metaheuristic(name: str, fitness_function: Callable, 
                        config: dict) -> Metaheuristic:
    """
    Factory para crear metaheurísticas
    
    Args:
        name: Nombre de la metaheurística
        fitness_function: Función de fitness
        config: Configuración específica
        
    Returns:
        Instancia de metaheurística
    """
    metaheuristics = {
        'SA': SimulatedAnnealing,
        'simulated_annealing': SimulatedAnnealing,
        'GP': GeneticProgramming,
        'genetic_programming': GeneticProgramming,
    }
    
    if name not in metaheuristics:
        raise ValueError(f"Metaheurística desconocida: {name}")
    
    return metaheuristics[name](fitness_function, **config)


if __name__ == "__main__":
    # Ejemplo de uso
    def dummy_fitness(ast: ASTNode) -> float:
        """Fitness dummy para testing"""
        return random.random() * ast.size()
    
    # Simulated Annealing
    sa = SimulatedAnnealing(
        fitness_function=dummy_fitness,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=50,
        max_evaluations=1000
    )
    
    best_ast, best_fitness = sa.optimize()
    print(f"\nMejor algoritmo encontrado:")
    print(best_ast.to_string())
    print(f"Fitness: {best_fitness:.4f}")
