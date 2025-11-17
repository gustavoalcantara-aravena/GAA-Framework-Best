#!/usr/bin/env python3
"""
Demo End-to-End - KBP-SA
Demostración completa del sistema GAA modular

Este script demuestra:
1. Carga de instancias
2. Generación automática de algoritmos
3. Ejecución con Simulated Annealing
4. Análisis de resultados
"""

import sys
import os
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)  # Cambiar directorio de trabajo

# Imports del sistema modular
import core.problem as problem_module
import core.solution as solution_module
import core.evaluation as evaluation_module
import operators.constructive as constructive_module
import operators.improvement as improvement_module
import gaa.ast_nodes as ast_module
import gaa.grammar as grammar_module
import gaa.generator as generator_module
import gaa.interpreter as interpreter_module
import metaheuristic.sa_core as sa_module
import metaheuristic.cooling_schedules as cooling_module
import data.loader as loader_module
import utils.config as config_module
import utils.logging as logging_module
import utils.random as random_module

# Aliases para compatibilidad
KnapsackProblem = problem_module.KnapsackProblem
KnapsackSolution = solution_module.KnapsackSolution
KnapsackEvaluator = evaluation_module.KnapsackEvaluator
GreedyByRatio = constructive_module.GreedyByRatio
FlipBestItem = improvement_module.FlipBestItem
ASTNode = ast_module.ASTNode
Grammar = grammar_module.Grammar
AlgorithmGenerator = generator_module.AlgorithmGenerator
ASTInterpreter = interpreter_module.ASTInterpreter
SimulatedAnnealing = sa_module.SimulatedAnnealing
GeometricCooling = cooling_module.GeometricCooling
DatasetLoader = loader_module.DatasetLoader
ConfigManager = config_module.ConfigManager
setup_logger = logging_module.setup_logger
RandomManager = random_module.RandomManager


def print_header(title: str):
    """Imprime encabezado bonito"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_1_load_instance():
    """Demo 1: Carga de instancias"""
    print_header("DEMO 1: Carga de Instancias")
    
    # Cargar instancia pequeña
    loader = DatasetLoader(project_root / "datasets")
    instances = loader.load_folder("low_dimensional")
    
    if not instances:
        print("⚠️  No hay instancias en low_dimensional/")
        return None
    
    # Usar primera instancia
    problem = instances[0]
    
    print(f"✅ Instancia cargada: {problem.name}")
    print(f"   • n = {problem.n} ítems")
    print(f"   • Capacidad = {problem.capacity}")
    print(f"   • Valor óptimo = {problem.optimal_value}")
    
    stats = problem.get_statistics()
    print(f"\n📊 Estadísticas:")
    print(f"   • Valores: min={stats['values']['min']}, max={stats['values']['max']}, "
          f"media={stats['values']['mean']:.1f}")
    print(f"   • Pesos: min={stats['weights']['min']}, max={stats['weights']['max']}, "
          f"media={stats['weights']['mean']:.1f}")
    print(f"   • Ratio capacidad/peso total: {stats['capacity_ratio']:.2f}")
    
    return problem


def demo_2_generate_algorithms():
    """Demo 2: Generación automática de algoritmos"""
    print_header("DEMO 2: Generación Automática de Algoritmos (GAA)")
    
    grammar = Grammar(min_depth=2, max_depth=4)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    print("🌳 Gramática GAA cargada:")
    print(f"   • Terminales constructivos: {len(grammar.CONSTRUCTIVE_TERMINALS)}")
    print(f"   • Terminales de mejora: {len(grammar.IMPROVEMENT_TERMINALS)}")
    print(f"   • Terminales de perturbación: {len(grammar.PERTURBATION_TERMINALS)}")
    print(f"   • Total de terminales: {len(grammar.ALL_TERMINALS)}")
    
    print("\n🎲 Generando 3 algoritmos aleatorios...\n")
    
    algorithms = []
    for i in range(3):
        algorithm = generator.generate_with_validation()
        
        if algorithm:
            stats = generator.get_generation_stats(algorithm)
            algorithms.append(algorithm)
            
            print(f"Algoritmo {i+1}:")
            print(f"   • Profundidad: {stats['depth']}")
            print(f"   • Total nodos: {stats['total_nodes']}")
            print(f"   • Válido: {'✅' if stats['is_valid'] else '❌'}")
            print(f"\n   Pseudocódigo:")
            for line in algorithm.to_pseudocode(indent=2).split('\n'):
                print(f"   {line}")
            print()
    
    return algorithms[0] if algorithms else None


def demo_3_execute_algorithm(problem: KnapsackProblem, algorithm: ASTNode):
    """Demo 3: Ejecución de algoritmo"""
    print_header("DEMO 3: Ejecución de Algoritmo Generado")
    
    print("🚀 Ejecutando algoritmo con intérprete AST...")
    
    interpreter = ASTInterpreter(problem, seed=42)
    best_solution = interpreter.execute(algorithm)
    
    report = interpreter.get_execution_report()
    
    print(f"\n📈 Resultados de ejecución:")
    print(f"   • Iteraciones: {report['iterations']}")
    print(f"   • Evaluaciones: {report['evaluations']}")
    print(f"   • Tiempo: {report['elapsed_time']:.3f}s")
    
    if 'best_solution' in report:
        sol_info = report['best_solution']
        print(f"\n🎯 Mejor solución encontrada:")
        print(f"   • Valor: {sol_info['value']}")
        print(f"   • Peso: {sol_info['weight']}/{problem.capacity}")
        print(f"   • Ítems seleccionados: {sol_info['num_items']}/{problem.n}")
        print(f"   • Factible: {'✅' if sol_info['is_feasible'] else '❌'}")
        
        if report.get('final_gap') is not None:
            print(f"   • Gap vs óptimo: {report['final_gap']:.2f}%")
    
    return best_solution


def demo_4_simulated_annealing(problem: KnapsackProblem):
    """Demo 4: Simulated Annealing tradicional"""
    print_header("DEMO 4: Simulated Annealing Tradicional")
    
    # Configurar SA
    sa = SimulatedAnnealing(
        problem=problem,
        T0=100.0,
        alpha=0.95,
        iterations_per_temp=50,
        T_min=0.1,
        max_evaluations=1000,
        seed=42
    )
    
    # Función de vecindario simple (flip aleatorio)
    def simple_neighborhood(solution, rng):
        neighbor = solution.copy()
        idx = rng.integers(0, problem.n)
        neighbor.flip(idx)
        return neighbor
    
    sa.set_neighborhood(simple_neighborhood)
    
    # Construir solución inicial
    constructor = GreedyByRatio(problem)
    initial = constructor.construct()
    
    print(f"💡 Solución inicial (GreedyByRatio):")
    print(f"   • Valor: {initial.value}")
    print(f"   • Factible: {'✅' if initial.is_feasible else '❌'}")
    
    print(f"\n🔥 Ejecutando SA (T0={sa.T0}, alpha={sa.alpha})...")
    
    best = sa.optimize(initial, verbose=False)
    
    stats = sa.get_statistics()
    
    print(f"\n📊 Estadísticas SA:")
    print(f"   • Iteraciones: {stats['total_iterations']}")
    print(f"   • Evaluaciones: {stats['evaluations']}")
    print(f"   • Tiempo: {stats['elapsed_time']:.3f}s")
    print(f"   • Mejor valor: {stats['best_value']}")
    print(f"   • Tasa de aceptación: {stats['acceptance_rate']:.1f}%")
    print(f"   • Temperatura final: {stats['final_temperature']:.4f}")
    
    evaluator = KnapsackEvaluator(problem)
    gap = evaluator.gap_to_optimal(best)
    
    if gap is not None:
        print(f"   • Gap vs óptimo: {gap:.2f}%")
    
    return best


def demo_5_comparison(problem: KnapsackProblem):
    """Demo 5: Comparación de métodos"""
    print_header("DEMO 5: Comparación de Métodos Constructivos")
    
    GreedyByValue = constructive_module.GreedyByValue
    GreedyByWeight = constructive_module.GreedyByWeight
    GreedyByRatio = constructive_module.GreedyByRatio
    RandomConstruct = constructive_module.RandomConstruct
    
    methods = {
        'GreedyByValue': GreedyByValue(problem),
        'GreedyByWeight': GreedyByWeight(problem),
        'GreedyByRatio': GreedyByRatio(problem),
        'RandomConstruct': RandomConstruct(problem)
    }
    
    evaluator = KnapsackEvaluator(problem)
    
    print(f"Instancia: {problem.name} (n={problem.n}, W={problem.capacity}, "
          f"óptimo={problem.optimal_value})\n")
    
    print(f"{'Método':<20} {'Valor':>8} {'Peso':>8} {'Ítems':>6} {'Gap %':>8} {'Factible':>10}")
    print("-" * 80)
    
    for name, method in methods.items():
        solution = method.construct()
        gap = evaluator.gap_to_optimal(solution)
        gap_str = f"{gap:.2f}" if gap is not None else "N/A"
        feasible = "✅" if solution.is_feasible else "❌"
        
        print(f"{name:<20} {solution.value:>8} {solution.weight:>8} "
              f"{solution.num_selected():>6} {gap_str:>8} {feasible:>10}")


def main():
    """Función principal"""
    print_header("SISTEMA GAA MODULAR - KBP-SA")
    print("Demo End-to-End del Framework de Generación Automática de Algoritmos")
    print("\nMódulos implementados:")
    print("  ✅ core/         - Definición del problema")
    print("  ✅ operators/    - 14 terminales (constructivos, mejora, perturbación, reparación)")
    print("  ✅ gaa/          - Gramática, AST, Generador, Intérprete")
    print("  ✅ metaheuristic/- Simulated Annealing completo")
    print("  ✅ data/         - Carga y validación de instancias")
    print("  ✅ utils/        - Configuración, logging, random")
    
    # Ejecutar demos
    problem = demo_1_load_instance()
    
    if problem is None:
        print("\n❌ No se pudo cargar instancia. Abortando demo.")
        return
    
    algorithm = demo_2_generate_algorithms()
    
    if algorithm:
        solution_gaa = demo_3_execute_algorithm(problem, algorithm)
    
    solution_sa = demo_4_simulated_annealing(problem)
    
    demo_5_comparison(problem)
    
    print_header("DEMO COMPLETADA")
    print("✅ Todos los módulos funcionan correctamente")
    print("✅ Sistema GAA listo para experimentación")
    print("\nPróximos pasos:")
    print("  1. Ejecutar experimentos en large_scale/")
    print("  2. Implementar módulo experimentation/ para análisis estadístico")
    print("  3. Generar población de algoritmos y seleccionar los 3 mejores")
    print("  4. Documentar resultados en formato ESWA")


if __name__ == '__main__':
    main()
