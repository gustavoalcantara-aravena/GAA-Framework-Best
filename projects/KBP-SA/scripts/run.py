"""
Script Principal de Ejecución - KBP-SA

Ejecuta la generación automática de algoritmos para Knapsack Problem
utilizando Simulated Annealing como metaheurística.
"""

import sys
from pathlib import Path
import yaml
import logging
from datetime import datetime

# Añadir ruta de scripts del framework
framework_scripts = Path(__file__).parent.parent.parent / "04-Generated" / "scripts"
sys.path.insert(0, str(framework_scripts))

from problem import create_problem
from data_loader import DataLoader
from fitness import FitnessEvaluator
from metaheuristic import create_metaheuristic
from ast_nodes import ASTNode


def setup_logging(config: dict) -> logging.Logger:
    """Configura el sistema de logging"""
    log_config = config['logging']
    
    # Crear directorio de logs si no existe
    log_file = Path(log_config['file'])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger('KBP-SA')
    logger.setLevel(getattr(logging, log_config['level']))
    
    # Handler para archivo
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Handler para consola
    if log_config['console']:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    
    return logger


def load_config() -> dict:
    """Carga la configuración del proyecto"""
    config_path = Path(__file__).parent / "config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def main():
    """Función principal"""
    print("=" * 70)
    print("  GAA - Generación Automática de Algoritmos")
    print("  Proyecto: KBP-SA (Knapsack + Simulated Annealing)")
    print("=" * 70)
    print()
    
    # Cargar configuración
    config = load_config()
    logger = setup_logging(config)
    
    logger.info("Iniciando ejecución de KBP-SA")
    logger.info(f"Configuración cargada: {config['project']['name']}")
    
    # Cargar datasets
    print("📊 Cargando datasets...")
    project_dir = Path(__file__).parent
    loader = DataLoader(
        dataset_dir=project_dir / config['datasets']['base_dir'],
        problem_type=config['problem']['type']
    )
    
    training_instances = loader.load_training_set()
    
    if not training_instances:
        logger.error("No se encontraron instancias de entrenamiento")
        print("❌ Error: No hay datasets disponibles")
        print("   Por favor, coloca archivos .txt en datasets/training/")
        return
    
    logger.info(f"Instancias de entrenamiento: {len(training_instances)}")
    
    # Crear problema de referencia
    print("🎯 Configurando problema...")
    problem = create_problem(
        config['problem']['type'],
        training_instances[0]
    )
    logger.info(f"Problema creado: {problem.problem_name}")
    
    # Crear evaluador de fitness
    print("⚖️  Configurando evaluador de fitness...")
    evaluator = FitnessEvaluator(
        problem=problem,
        training_instances=training_instances
    )
    
    # Configurar metaheurística
    print("🔥 Configurando Simulated Annealing...")
    sa_config = config['metaheuristic']['parameters']
    
    metaheuristic = create_metaheuristic(
        name='SA',
        fitness_function=lambda ast: evaluator.evaluate(ast),
        config=sa_config
    )
    
    logger.info(f"Metaheurística: {config['metaheuristic']['name']}")
    logger.info(f"Parámetros: {sa_config}")
    
    # Ejecutar optimización
    print("\n" + "=" * 70)
    print("  INICIANDO OPTIMIZACIÓN")
    print("=" * 70)
    
    start_time = datetime.now()
    
    best_algorithm, best_fitness = metaheuristic.optimize()
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    # Mostrar resultados
    print("\n" + "=" * 70)
    print("  RESULTADOS")
    print("=" * 70)
    print(f"\n✅ Optimización completada en {elapsed:.2f} segundos")
    print(f"📈 Mejor fitness: {best_fitness:.4f}")
    print(f"🔍 Evaluaciones realizadas: {metaheuristic.evaluations}")
    print(f"📏 Tamaño del algoritmo: {best_algorithm.size()} nodos")
    
    print("\n🌳 Algoritmo generado (AST):")
    print("-" * 70)
    print(best_algorithm.to_string())
    print("-" * 70)
    
    # Guardar resultados
    results_dir = project_dir / config['experiments']['output']['directory']
    results_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Guardar AST
    ast_file = results_dir / f"best_algorithm_{timestamp}.txt"
    with open(ast_file, 'w') as f:
        f.write(best_algorithm.to_string())
    
    print(f"\n💾 Algoritmo guardado en: {ast_file}")
    
    # Guardar historial
    import json
    history_file = results_dir / f"history_{timestamp}.json"
    with open(history_file, 'w') as f:
        json.dump(metaheuristic.history, f, indent=2)
    
    print(f"💾 Historial guardado en: {history_file}")
    
    logger.info(f"Mejor fitness: {best_fitness}")
    logger.info(f"Tiempo de ejecución: {elapsed:.2f}s")
    logger.info(f"Tamaño algoritmo: {best_algorithm.size()}")
    
    print("\n✅ Ejecución finalizada exitosamente")


if __name__ == "__main__":
    main()
