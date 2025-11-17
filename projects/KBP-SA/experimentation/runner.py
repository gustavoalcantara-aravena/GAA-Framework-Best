"""
Experiment Runner - KBP-SA
Ejecución de experimentos en batch
Fase 5 GAA: Experimentación controlada

Referencias:
- Barr et al. (1995): Designing and reporting on computational experiments
- Hooker (1995): Testing heuristics: We have it all wrong
- Eiben & Jelasity (2002): A critical note on experimental research methodology
"""

from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import json
import time
import numpy as np
from dataclasses import dataclass, asdict
from datetime import datetime

from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
from gaa.interpreter import ASTInterpreter
from gaa.ast_nodes import ASTNode
from data.loader import DatasetLoader


@dataclass
class ExperimentConfig:
    """Configuración de un experimento"""
    name: str
    instances: List[str]  # Nombres de instancias
    algorithms: List[Dict[str, Any]]  # Algoritmos a probar
    repetitions: int = 30  # Repeticiones por combinación
    seeds: Optional[List[int]] = None  # Seeds específicas
    max_time_seconds: float = 300.0  # Timeout por ejecución
    output_dir: str = "output/experiments"
    save_solutions: bool = False  # Guardar soluciones encontradas
    
    def __post_init__(self):
        if self.seeds is None:
            # Generar seeds reproducibles
            rng = np.random.RandomState(42)
            # Convertir a int Python nativo para JSON
            self.seeds = [int(x) for x in rng.randint(0, 2**31, self.repetitions)]


@dataclass
class ExperimentResult:
    """Resultado de una ejecución individual"""
    instance_name: str
    algorithm_name: str
    seed: int
    repetition: int
    
    # Resultados de calidad
    best_value: int
    best_weight: int
    is_feasible: bool
    gap_to_optimal: Optional[float]  # Porcentaje
    
    # Métricas de rendimiento
    total_time: float  # segundos
    iterations: int
    evaluations: int
    
    # Estadísticas de convergencia
    initial_value: int
    improvement: int  # best_value - initial_value
    improvement_ratio: float  # improvement / initial_value
    
    # Metadata
    timestamp: str
    success: bool
    error_message: Optional[str] = None


class ExperimentRunner:
    """
    Ejecutor de experimentos en batch
    
    Permite ejecutar múltiples algoritmos sobre múltiples instancias
    con repeticiones independientes para análisis estadístico.
    
    References:
    - Barr et al. (1995): Factor-screening experiments
    - Hooker (1995): Statistical testing methodology
    """
    
    def __init__(self, config: ExperimentConfig):
        """
        Args:
            config: Configuración del experimento
        """
        self.config = config
        self.results: List[ExperimentResult] = []
        self.output_path = Path(config.output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Cargar datasets - usar directorio por defecto
        datasets_dir = Path(__file__).parent.parent / "datasets"
        self.loader = DatasetLoader(datasets_dir)
        self.problems: Dict[str, KnapsackProblem] = {}
        
    def load_instances(self, folder: str = "low_dimensional") -> None:
        """
        Carga instancias desde una carpeta
        
        Args:
            folder: Nombre de la carpeta de datasets
        """
        all_instances = self.loader.load_folder(folder)
        
        # Filtrar solo las instancias especificadas en config
        for instance in all_instances:
            if instance.name in self.config.instances:
                self.problems[instance.name] = instance
        
        loaded = len(self.problems)
        expected = len(self.config.instances)
        
        if loaded < expected:
            missing = set(self.config.instances) - set(self.problems.keys())
            print(f"⚠️  Advertencia: {len(missing)} instancias no encontradas: {missing}")
    
    def run_single(
        self,
        problem: KnapsackProblem,
        algorithm: Dict[str, Any],
        seed: int,
        repetition: int
    ) -> ExperimentResult:
        """
        Ejecuta una sola combinación instancia-algoritmo-seed
        
        Args:
            problem: Instancia del problema
            algorithm: Diccionario con 'name' y 'ast' (o función 'executor')
            seed: Semilla aleatoria
            repetition: Número de repetición (para tracking)
            
        Returns:
            Resultado del experimento
        """
        start_time = time.time()
        
        try:
            # Ejecutar algoritmo
            if 'ast' in algorithm:
                # Algoritmo GAA (AST)
                ast_node = algorithm['ast']
                interpreter = ASTInterpreter(problem, seed=seed)
                best_solution = interpreter.execute(ast_node)
                report = interpreter.get_execution_report()
                
                iterations = report.get('iterations', 0)
                evaluations = report.get('evaluations', 0)
                initial_value = report.get('initial_value', 0)
                
            elif 'executor' in algorithm:
                # Función custom
                executor_func = algorithm['executor']
                result = executor_func(problem, seed)
                
                best_solution = result['solution']
                iterations = result.get('iterations', 0)
                evaluations = result.get('evaluations', 0)
                initial_value = result.get('initial_value', 0)
            else:
                raise ValueError("Algoritmo debe tener 'ast' o 'executor'")
            
            elapsed_time = time.time() - start_time
            
            # Verificar timeout
            if elapsed_time > self.config.max_time_seconds:
                raise TimeoutError(f"Excedido timeout de {self.config.max_time_seconds}s")
            
            # Calcular métricas
            evaluator = KnapsackEvaluator(problem)
            gap = evaluator.gap_to_optimal(best_solution)
            
            improvement = best_solution.value - initial_value
            improvement_ratio = improvement / initial_value if initial_value > 0 else 0.0
            
            return ExperimentResult(
                instance_name=problem.name,
                algorithm_name=algorithm['name'],
                seed=seed,
                repetition=repetition,
                best_value=best_solution.value,
                best_weight=best_solution.weight,
                is_feasible=best_solution.is_feasible,
                gap_to_optimal=gap,
                total_time=elapsed_time,
                iterations=iterations,
                evaluations=evaluations,
                initial_value=initial_value,
                improvement=improvement,
                improvement_ratio=improvement_ratio,
                timestamp=datetime.now().isoformat(),
                success=True
            )
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            
            return ExperimentResult(
                instance_name=problem.name,
                algorithm_name=algorithm['name'],
                seed=seed,
                repetition=repetition,
                best_value=0,
                best_weight=0,
                is_feasible=False,
                gap_to_optimal=None,
                total_time=elapsed_time,
                iterations=0,
                evaluations=0,
                initial_value=0,
                improvement=0,
                improvement_ratio=0.0,
                timestamp=datetime.now().isoformat(),
                success=False,
                error_message=str(e)
            )
    
    def run_all(self, verbose: bool = True) -> List[ExperimentResult]:
        """
        Ejecuta todos los experimentos configurados
        
        Args:
            verbose: Mostrar progreso
            
        Returns:
            Lista de todos los resultados
        """
        total_experiments = (
            len(self.problems) * 
            len(self.config.algorithms) * 
            self.config.repetitions
        )
        
        if verbose:
            print(f"🧪 Iniciando experimentos:")
            print(f"   • Instancias: {len(self.problems)}")
            print(f"   • Algoritmos: {len(self.config.algorithms)}")
            print(f"   • Repeticiones: {self.config.repetitions}")
            print(f"   • Total ejecuciones: {total_experiments}\n")
        
        experiment_count = 0
        start_time = time.time()
        
        for instance_name, problem in self.problems.items():
            for algorithm in self.config.algorithms:
                for rep in range(self.config.repetitions):
                    seed = self.config.seeds[rep]
                    
                    if verbose:
                        experiment_count += 1
                        print(f"[{experiment_count}/{total_experiments}] "
                              f"{instance_name} × {algorithm['name']} (rep {rep+1})", 
                              end=" ... ")
                    
                    result = self.run_single(problem, algorithm, seed, rep)
                    self.results.append(result)
                    
                    if verbose:
                        if result.success:
                            gap_str = f"{result.gap_to_optimal:.2f}%" if result.gap_to_optimal else "N/A"
                            print(f"✅ valor={result.best_value}, gap={gap_str}, "
                                  f"tiempo={result.total_time:.3f}s")
                        else:
                            print(f"❌ Error: {result.error_message}")
        
        total_time = time.time() - start_time
        
        if verbose:
            successful = sum(1 for r in self.results if r.success)
            print(f"\n✅ Experimentos completados:")
            print(f"   • Exitosos: {successful}/{total_experiments}")
            print(f"   • Tiempo total: {total_time:.1f}s")
            print(f"   • Tiempo promedio: {total_time/total_experiments:.3f}s por ejecución")
        
        return self.results
    
    def save_results(self, filename: Optional[str] = None) -> Path:
        """
        Guarda resultados en JSON
        
        Args:
            filename: Nombre del archivo (auto-generado si None)
            
        Returns:
            Path del archivo guardado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"experiment_{self.config.name}_{timestamp}.json"
        
        filepath = self.output_path / filename
        
        data = {
            'config': asdict(self.config),
            'results': [asdict(r) for r in self.results],
            'summary': self._compute_summary()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados guardados en: {filepath}")
        return filepath
    
    def _compute_summary(self) -> Dict[str, Any]:
        """Calcula resumen estadístico de resultados"""
        if not self.results:
            return {}
        
        summary = {
            'total_experiments': len(self.results),
            'successful': sum(1 for r in self.results if r.success),
            'by_algorithm': {},
            'by_instance': {}
        }
        
        # Agrupar por algoritmo
        for algorithm in self.config.algorithms:
            alg_name = algorithm['name']
            alg_results = [r for r in self.results if r.algorithm_name == alg_name and r.success]
            
            if alg_results:
                gaps = [r.gap_to_optimal for r in alg_results if r.gap_to_optimal is not None]
                times = [r.total_time for r in alg_results]
                
                summary['by_algorithm'][alg_name] = {
                    'runs': len(alg_results),
                    'avg_gap': float(np.mean(gaps)) if gaps else None,
                    'std_gap': float(np.std(gaps)) if gaps else None,
                    'avg_time': float(np.mean(times)),
                    'std_time': float(np.std(times))
                }
        
        # Agrupar por instancia
        for instance_name in self.problems.keys():
            inst_results = [r for r in self.results if r.instance_name == instance_name and r.success]
            
            if inst_results:
                gaps = [r.gap_to_optimal for r in inst_results if r.gap_to_optimal is not None]
                
                summary['by_instance'][instance_name] = {
                    'runs': len(inst_results),
                    'avg_gap': float(np.mean(gaps)) if gaps else None,
                    'best_gap': float(np.min(gaps)) if gaps else None,
                    'worst_gap': float(np.max(gaps)) if gaps else None
                }
        
        return summary
    
    def get_results_dataframe(self):
        """
        Convierte resultados a pandas DataFrame (si pandas disponible)
        
        Returns:
            DataFrame con todos los resultados
        """
        try:
            import pandas as pd
            return pd.DataFrame([asdict(r) for r in self.results])
        except ImportError:
            print("⚠️  pandas no disponible. Instalar con: pip install pandas")
            return None
