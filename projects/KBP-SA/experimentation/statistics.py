"""
Statistical Analyzer - KBP-SA
Análisis estadístico de resultados experimentales
Fase 5 GAA: Validación estadística

Referencias:
- Barr et al. (1995): Guidelines for designing and reporting computational experiments
- Derrac et al. (2011): A practical tutorial on statistical tests
- García & Herrera (2008): An extension on statistical comparisons
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from scipy import stats


@dataclass
class StatisticalTest:
    """Resultado de un test estadístico"""
    test_name: str
    statistic: float
    p_value: float
    is_significant: bool  # p < alpha
    alpha: float
    interpretation: str


class StatisticalAnalyzer:
    """
    Analizador estadístico para experimentos computacionales
    
    Implementa tests estadísticos estándar para comparación de algoritmos.
    
    Referencias:
    - Derrac et al. (2011): Statistical comparison methodology
    - García & Herrera (2008): Multiple comparison procedures
    """
    
    def __init__(self, alpha: float = 0.05):
        """
        Args:
            alpha: Nivel de significancia (típicamente 0.05)
        """
        self.alpha = alpha
    
    def descriptive_statistics(
        self,
        data: List[float]
    ) -> Dict[str, float]:
        """
        Calcula estadísticas descriptivas
        
        Args:
            data: Lista de valores numéricos
            
        Returns:
            Diccionario con estadísticas
        """
        arr = np.array(data)
        
        return {
            'n': len(arr),
            'mean': float(np.mean(arr)),
            'std': float(np.std(arr, ddof=1)),  # Sample std
            'stderr': float(np.std(arr, ddof=1) / np.sqrt(len(arr))),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'median': float(np.median(arr)),
            'q1': float(np.percentile(arr, 25)),
            'q3': float(np.percentile(arr, 75)),
            'iqr': float(np.percentile(arr, 75) - np.percentile(arr, 25)),
            'cv': float(np.std(arr, ddof=1) / np.mean(arr)) if np.mean(arr) > 0 else 0.0
        }
    
    def confidence_interval(
        self,
        data: List[float],
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calcula intervalo de confianza
        
        Args:
            data: Lista de valores
            confidence: Nivel de confianza (0.95 = 95%)
            
        Returns:
            (lower_bound, upper_bound)
        """
        arr = np.array(data)
        n = len(arr)
        mean = np.mean(arr)
        stderr = np.std(arr, ddof=1) / np.sqrt(n)
        
        # t-distribution para muestras pequeñas
        t_critical = stats.t.ppf((1 + confidence) / 2, n - 1)
        margin = t_critical * stderr
        
        return (mean - margin, mean + margin)
    
    def normality_test(
        self,
        data: List[float]
    ) -> StatisticalTest:
        """
        Test de normalidad (Shapiro-Wilk)
        
        Args:
            data: Lista de valores
            
        Returns:
            Resultado del test
            
        Referencias:
        - Shapiro & Wilk (1965): Analysis of variance test for normality
        """
        arr = np.array(data)
        
        if len(arr) < 3:
            return StatisticalTest(
                test_name="Shapiro-Wilk",
                statistic=0.0,
                p_value=1.0,
                is_significant=False,
                alpha=self.alpha,
                interpretation="Muestra muy pequeña para test de normalidad"
            )
        
        statistic, p_value = stats.shapiro(arr)
        is_significant = p_value < self.alpha
        
        interpretation = (
            "Los datos NO siguen distribución normal" if is_significant
            else "No se rechaza normalidad (datos pueden ser normales)"
        )
        
        return StatisticalTest(
            test_name="Shapiro-Wilk",
            statistic=float(statistic),
            p_value=float(p_value),
            is_significant=is_significant,
            alpha=self.alpha,
            interpretation=interpretation
        )
    
    def paired_t_test(
        self,
        data1: List[float],
        data2: List[float]
    ) -> StatisticalTest:
        """
        T-test pareado (datos apareados)
        
        Args:
            data1: Primera muestra
            data2: Segunda muestra (mismo orden que data1)
            
        Returns:
            Resultado del test
            
        Referencias:
        - Student (1908): The probable error of a mean
        """
        arr1 = np.array(data1)
        arr2 = np.array(data2)
        
        if len(arr1) != len(arr2):
            raise ValueError("Las muestras deben tener el mismo tamaño")
        
        statistic, p_value = stats.ttest_rel(arr1, arr2)
        is_significant = p_value < self.alpha
        
        mean_diff = np.mean(arr1 - arr2)
        
        interpretation = (
            f"Diferencia significativa (Δ={mean_diff:.3f})" if is_significant
            else f"No hay diferencia significativa (Δ={mean_diff:.3f})"
        )
        
        return StatisticalTest(
            test_name="Paired t-test",
            statistic=float(statistic),
            p_value=float(p_value),
            is_significant=is_significant,
            alpha=self.alpha,
            interpretation=interpretation
        )
    
    def wilcoxon_signed_rank_test(
        self,
        data1: List[float],
        data2: List[float]
    ) -> StatisticalTest:
        """
        Test de Wilcoxon (no paramétrico, alternativa a t-test pareado)
        
        Args:
            data1: Primera muestra
            data2: Segunda muestra
            
        Returns:
            Resultado del test
            
        Referencias:
        - Wilcoxon (1945): Individual comparisons by ranking methods
        """
        arr1 = np.array(data1)
        arr2 = np.array(data2)
        
        if len(arr1) != len(arr2):
            raise ValueError("Las muestras deben tener el mismo tamaño")
        
        # Filtrar empates (diferencias = 0)
        diff = arr1 - arr2
        non_zero = diff[diff != 0]
        
        if len(non_zero) < 1:
            return StatisticalTest(
                test_name="Wilcoxon signed-rank",
                statistic=0.0,
                p_value=1.0,
                is_significant=False,
                alpha=self.alpha,
                interpretation="No hay diferencias entre las muestras"
            )
        
        statistic, p_value = stats.wilcoxon(non_zero)
        is_significant = p_value < self.alpha
        
        median_diff = np.median(arr1 - arr2)
        
        interpretation = (
            f"Diferencia significativa (mediana Δ={median_diff:.3f})" if is_significant
            else f"No hay diferencia significativa (mediana Δ={median_diff:.3f})"
        )
        
        return StatisticalTest(
            test_name="Wilcoxon signed-rank",
            statistic=float(statistic),
            p_value=float(p_value),
            is_significant=is_significant,
            alpha=self.alpha,
            interpretation=interpretation
        )
    
    def mann_whitney_u_test(
        self,
        data1: List[float],
        data2: List[float]
    ) -> StatisticalTest:
        """
        Test de Mann-Whitney U (no paramétrico, muestras independientes)
        
        Args:
            data1: Primera muestra
            data2: Segunda muestra
            
        Returns:
            Resultado del test
            
        Referencias:
        - Mann & Whitney (1947): On a test of whether one of two random variables
        """
        arr1 = np.array(data1)
        arr2 = np.array(data2)
        
        statistic, p_value = stats.mannwhitneyu(arr1, arr2, alternative='two-sided')
        is_significant = p_value < self.alpha
        
        median1 = np.median(arr1)
        median2 = np.median(arr2)
        
        interpretation = (
            f"Diferencia significativa (med1={median1:.3f}, med2={median2:.3f})" 
            if is_significant
            else f"No hay diferencia significativa (med1={median1:.3f}, med2={median2:.3f})"
        )
        
        return StatisticalTest(
            test_name="Mann-Whitney U",
            statistic=float(statistic),
            p_value=float(p_value),
            is_significant=is_significant,
            alpha=self.alpha,
            interpretation=interpretation
        )
    
    def friedman_test(
        self,
        *groups: List[float]
    ) -> StatisticalTest:
        """
        Test de Friedman (ANOVA no paramétrico para k muestras relacionadas)
        
        Args:
            *groups: Múltiples grupos de datos (mismo tamaño)
            
        Returns:
            Resultado del test
            
        Referencias:
        - Friedman (1937): The use of ranks to avoid the assumption of normality
        """
        if len(groups) < 3:
            raise ValueError("Se necesitan al menos 3 grupos para test de Friedman")
        
        # Verificar mismo tamaño
        sizes = [len(g) for g in groups]
        if len(set(sizes)) > 1:
            raise ValueError("Todos los grupos deben tener el mismo tamaño")
        
        statistic, p_value = stats.friedmanchisquare(*groups)
        is_significant = p_value < self.alpha
        
        interpretation = (
            f"Hay diferencias significativas entre los {len(groups)} algoritmos"
            if is_significant
            else f"No hay diferencias significativas entre los {len(groups)} algoritmos"
        )
        
        return StatisticalTest(
            test_name="Friedman",
            statistic=float(statistic),
            p_value=float(p_value),
            is_significant=is_significant,
            alpha=self.alpha,
            interpretation=interpretation
        )
    
    def effect_size_cohens_d(
        self,
        data1: List[float],
        data2: List[float]
    ) -> float:
        """
        Calcula tamaño del efecto (Cohen's d)
        
        Args:
            data1: Primera muestra
            data2: Segunda muestra
            
        Returns:
            Cohen's d (small: 0.2, medium: 0.5, large: 0.8)
            
        Referencias:
        - Cohen (1988): Statistical power analysis for the behavioral sciences
        """
        arr1 = np.array(data1)
        arr2 = np.array(data2)
        
        mean1 = np.mean(arr1)
        mean2 = np.mean(arr2)
        
        # Pooled standard deviation
        n1 = len(arr1)
        n2 = len(arr2)
        var1 = np.var(arr1, ddof=1)
        var2 = np.var(arr2, ddof=1)
        
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        cohens_d = (mean1 - mean2) / pooled_std
        return float(cohens_d)
    
    def compare_multiple_algorithms(
        self,
        algorithm_results: Dict[str, List[float]],
        test_type: str = "friedman"
    ) -> Dict[str, Any]:
        """
        Compara múltiples algoritmos
        
        Args:
            algorithm_results: Dict[nombre_algoritmo] -> List[valores]
            test_type: "friedman" o "kruskal"
            
        Returns:
            Diccionario con resultados del análisis
        """
        algorithms = list(algorithm_results.keys())
        
        # Estadísticas descriptivas por algoritmo
        descriptives = {}
        for alg, data in algorithm_results.items():
            descriptives[alg] = self.descriptive_statistics(data)
        
        # Test global
        if test_type == "friedman":
            global_test = self.friedman_test(*algorithm_results.values())
        else:
            # Kruskal-Wallis (para muestras independientes)
            statistic, p_value = stats.kruskal(*algorithm_results.values())
            is_significant = p_value < self.alpha
            
            global_test = StatisticalTest(
                test_name="Kruskal-Wallis",
                statistic=float(statistic),
                p_value=float(p_value),
                is_significant=is_significant,
                alpha=self.alpha,
                interpretation=(
                    f"Hay diferencias significativas entre los {len(algorithms)} algoritmos"
                    if is_significant else 
                    f"No hay diferencias significativas entre los {len(algorithms)} algoritmos"
                )
            )
        
        # Rankings promedio
        rankings = self._compute_average_rankings(algorithm_results)
        
        return {
            'algorithms': algorithms,
            'descriptive_stats': descriptives,
            'global_test': global_test,
            'average_rankings': rankings,
            'best_algorithm': min(rankings, key=rankings.get)  # Menor ranking = mejor
        }
    
    def _compute_average_rankings(
        self,
        algorithm_results: Dict[str, List[float]]
    ) -> Dict[str, float]:
        """
        Calcula rankings promedio (para test de Friedman)
        
        Args:
            algorithm_results: Resultados por algoritmo
            
        Returns:
            Dict con ranking promedio de cada algoritmo
        """
        algorithms = list(algorithm_results.keys())
        n_algorithms = len(algorithms)
        n_instances = len(list(algorithm_results.values())[0])
        
        rankings = {alg: 0.0 for alg in algorithms}
        
        # Para cada instancia, rankear algoritmos
        for i in range(n_instances):
            instance_values = {alg: results[i] for alg, results in algorithm_results.items()}
            
            # Ordenar por valor (descendente = mejor para maximización)
            sorted_algs = sorted(instance_values.items(), key=lambda x: x[1], reverse=True)
            
            # Asignar rankings (1 = mejor)
            for rank, (alg, _) in enumerate(sorted_algs, start=1):
                rankings[alg] += rank
        
        # Promediar
        for alg in rankings:
            rankings[alg] /= n_instances
        
        return rankings
