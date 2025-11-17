"""
Metrics - KBP-SA
Métricas de calidad y rendimiento
Fase 5 GAA: Evaluación de algoritmos

Referencias:
- Reinelt (1991): TSPLIB - A traveling salesman problem library
- Hansen & Mladenović (2001): Variable neighborhood search metrics
- Ribeiro & Rosseti (2007): Performance evaluation of heuristics
"""

from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass

from core.problem import KnapsackProblem
from core.solution import KnapsackSolution


@dataclass
class QualityMetrics:
    """
    Métricas de calidad de soluciones
    
    Referencias:
    - Reinelt (1991): Standard benchmarking metrics
    - Hansen & Mladenović (2001): Solution quality assessment
    """
    
    best_value: int
    optimal_value: Optional[int]
    gap_to_optimal: Optional[float]  # Porcentaje
    
    # Estadísticas de múltiples ejecuciones
    mean_value: float
    std_value: float
    min_value: int
    max_value: int
    median_value: float
    
    # Robustez
    coefficient_of_variation: float  # std / mean
    success_rate: float  # Porcentaje de soluciones factibles
    
    @staticmethod
    def from_solutions(
        solutions: List[KnapsackSolution],
        optimal_value: Optional[int] = None
    ) -> 'QualityMetrics':
        """
        Calcula métricas desde lista de soluciones
        
        Args:
            solutions: Lista de soluciones
            optimal_value: Valor óptimo conocido
            
        Returns:
            Métricas de calidad
        """
        values = np.array([s.value for s in solutions])
        feasible = [s.is_feasible for s in solutions]
        
        best_value = int(np.max(values))
        mean_value = float(np.mean(values))
        std_value = float(np.std(values))
        
        # Gap al óptimo
        gap = None
        if optimal_value is not None and optimal_value > 0:
            gap = 100.0 * (optimal_value - best_value) / optimal_value
        
        # Coeficiente de variación
        cv = std_value / mean_value if mean_value > 0 else 0.0
        
        # Tasa de éxito
        success_rate = 100.0 * sum(feasible) / len(feasible)
        
        return QualityMetrics(
            best_value=best_value,
            optimal_value=optimal_value,
            gap_to_optimal=gap,
            mean_value=mean_value,
            std_value=std_value,
            min_value=int(np.min(values)),
            max_value=int(np.max(values)),
            median_value=float(np.median(values)),
            coefficient_of_variation=cv,
            success_rate=success_rate
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'best_value': self.best_value,
            'optimal_value': self.optimal_value,
            'gap_to_optimal': self.gap_to_optimal,
            'mean_value': self.mean_value,
            'std_value': self.std_value,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'median_value': self.median_value,
            'coefficient_of_variation': self.coefficient_of_variation,
            'success_rate': self.success_rate
        }
    
    def __str__(self) -> str:
        """Representación legible"""
        gap_str = f"{self.gap_to_optimal:.2f}%" if self.gap_to_optimal else "N/A"
        
        return (
            f"QualityMetrics:\n"
            f"  Best: {self.best_value} (gap: {gap_str})\n"
            f"  Mean ± Std: {self.mean_value:.2f} ± {self.std_value:.2f}\n"
            f"  Range: [{self.min_value}, {self.max_value}]\n"
            f"  CV: {self.coefficient_of_variation:.4f}\n"
            f"  Success rate: {self.success_rate:.1f}%"
        )


@dataclass
class PerformanceMetrics:
    """
    Métricas de rendimiento computacional
    
    Referencias:
    - Barr et al. (1995): Computational efficiency metrics
    - Ribeiro & Rosseti (2007): Time-to-target analysis
    """
    
    # Tiempo
    mean_time: float  # segundos
    std_time: float
    min_time: float
    max_time: float
    median_time: float
    
    # Esfuerzo computacional
    mean_iterations: float
    mean_evaluations: float
    
    # Eficiencia (valor / tiempo)
    mean_efficiency: float
    std_efficiency: float
    
    # Velocidad de convergencia
    mean_improvement: float  # Mejora promedio desde inicial
    mean_improvement_ratio: float  # Mejora relativa
    
    @staticmethod
    def from_results(results: List[Dict[str, Any]]) -> 'PerformanceMetrics':
        """
        Calcula métricas desde lista de resultados de experimentos
        
        Args:
            results: Lista de diccionarios con resultados
            
        Returns:
            Métricas de rendimiento
        """
        times = np.array([r['total_time'] for r in results])
        iterations = np.array([r['iterations'] for r in results])
        evaluations = np.array([r['evaluations'] for r in results])
        values = np.array([r['best_value'] for r in results])
        improvements = np.array([r['improvement'] for r in results])
        improvement_ratios = np.array([r['improvement_ratio'] for r in results])
        
        # Eficiencia (valor por segundo)
        efficiencies = values / np.maximum(times, 1e-6)
        
        return PerformanceMetrics(
            mean_time=float(np.mean(times)),
            std_time=float(np.std(times)),
            min_time=float(np.min(times)),
            max_time=float(np.max(times)),
            median_time=float(np.median(times)),
            mean_iterations=float(np.mean(iterations)),
            mean_evaluations=float(np.mean(evaluations)),
            mean_efficiency=float(np.mean(efficiencies)),
            std_efficiency=float(np.std(efficiencies)),
            mean_improvement=float(np.mean(improvements)),
            mean_improvement_ratio=float(np.mean(improvement_ratios))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'mean_time': self.mean_time,
            'std_time': self.std_time,
            'min_time': self.min_time,
            'max_time': self.max_time,
            'median_time': self.median_time,
            'mean_iterations': self.mean_iterations,
            'mean_evaluations': self.mean_evaluations,
            'mean_efficiency': self.mean_efficiency,
            'std_efficiency': self.std_efficiency,
            'mean_improvement': self.mean_improvement,
            'mean_improvement_ratio': self.mean_improvement_ratio
        }
    
    def __str__(self) -> str:
        """Representación legible"""
        return (
            f"PerformanceMetrics:\n"
            f"  Time: {self.mean_time:.3f} ± {self.std_time:.3f}s\n"
            f"  Range: [{self.min_time:.3f}, {self.max_time:.3f}]s\n"
            f"  Iterations: {self.mean_iterations:.1f}\n"
            f"  Evaluations: {self.mean_evaluations:.1f}\n"
            f"  Efficiency: {self.mean_efficiency:.2f} value/sec\n"
            f"  Improvement: {self.mean_improvement:.1f} ({self.mean_improvement_ratio:.2%})"
        )


def compute_relative_performance(
    algorithm_results: Dict[str, List[float]],
    reference_algorithm: Optional[str] = None
) -> Dict[str, float]:
    """
    Calcula rendimiento relativo entre algoritmos
    
    Args:
        algorithm_results: Dict[nombre_algoritmo] -> List[valores]
        reference_algorithm: Algoritmo de referencia (None = mejor promedio)
        
    Returns:
        Dict con ratios relativos para cada algoritmo
        
    Referencias:
    - Dolan & Moré (2002): Benchmarking optimization software with performance profiles
    """
    relative_performance = {}
    
    # Calcular promedios
    means = {alg: np.mean(values) for alg, values in algorithm_results.items()}
    
    # Determinar referencia
    if reference_algorithm is None:
        reference_algorithm = max(means, key=means.get)
    
    reference_value = means[reference_algorithm]
    
    # Calcular ratios
    for alg, mean_value in means.items():
        if reference_value > 0:
            relative_performance[alg] = mean_value / reference_value
        else:
            relative_performance[alg] = 0.0
    
    return relative_performance


def compute_convergence_rate(
    values_over_time: List[float],
    optimal_value: Optional[float] = None
) -> Dict[str, float]:
    """
    Calcula tasa de convergencia
    
    Args:
        values_over_time: Lista de valores a lo largo del tiempo
        optimal_value: Valor óptimo conocido
        
    Returns:
        Métricas de convergencia
    """
    values = np.array(values_over_time)
    
    # Mejora total
    total_improvement = values[-1] - values[0]
    
    # Encontrar punto de convergencia (95% de mejora)
    if total_improvement > 0:
        threshold = values[0] + 0.95 * total_improvement
        convergence_point = np.argmax(values >= threshold)
        convergence_ratio = convergence_point / len(values)
    else:
        convergence_point = 0
        convergence_ratio = 0.0
    
    metrics = {
        'total_improvement': float(total_improvement),
        'convergence_point': int(convergence_point),
        'convergence_ratio': float(convergence_ratio),
        'final_value': float(values[-1])
    }
    
    if optimal_value is not None:
        final_gap = 100.0 * (optimal_value - values[-1]) / optimal_value
        metrics['final_gap'] = float(final_gap)
    
    return metrics
