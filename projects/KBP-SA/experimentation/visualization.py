"""
Results Visualizer - KBP-SA
Visualización de resultados experimentales
Fase 5 GAA: Análisis visual

Referencias:
- Tufte (2001): The Visual Display of Quantitative Information
- Cleveland (1993): Visualizing Data
- Dolan & Moré (2002): Performance profiles
"""

from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import numpy as np


class ResultsVisualizer:
    """
    Visualizador de resultados experimentales
    
    Genera gráficas para análisis de algoritmos metaheurísticos.
    
    Referencias:
    - Tufte (2001): Principles of data visualization
    - Dolan & Moré (2002): Performance profiles for benchmarking
    """
    
    def __init__(self, output_dir: str = "output/plots"):
        """
        Args:
            output_dir: Directorio para guardar gráficas
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar si matplotlib está disponible
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')  # Backend sin GUI
            self.plt = plt
            self.has_matplotlib = True
        except ImportError:
            print("⚠️  matplotlib no disponible. Instalar con: pip install matplotlib")
            self.has_matplotlib = False
    
    def plot_convergence(
        self,
        convergence_data: Dict[str, List[float]],
        title: str = "Convergencia de Algoritmos",
        ylabel: str = "Valor Objetivo",
        filename: str = "convergence.png"
    ) -> Optional[Path]:
        """
        Gráfica de convergencia
        
        Args:
            convergence_data: Dict[nombre_algoritmo] -> List[valores_por_iteracion]
            title: Título de la gráfica
            ylabel: Etiqueta del eje Y
            filename: Nombre del archivo
            
        Returns:
            Path del archivo guardado o None si no hay matplotlib
        """
        if not self.has_matplotlib:
            return None
        
        fig, ax = self.plt.subplots(figsize=(10, 6))
        
        for algorithm, values in convergence_data.items():
            iterations = range(len(values))
            ax.plot(iterations, values, label=algorithm, marker='o', 
                   markevery=len(values)//10 if len(values) > 10 else 1)
        
        ax.set_xlabel('Iteraciones', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica guardada: {filepath}")
        return filepath
    
    def plot_boxplot_comparison(
        self,
        algorithm_results: Dict[str, List[float]],
        title: str = "Comparación de Algoritmos",
        ylabel: str = "Valor Objetivo",
        filename: str = "boxplot_comparison.png"
    ) -> Optional[Path]:
        """
        Boxplot para comparar distribuciones
        
        Args:
            algorithm_results: Dict[nombre_algoritmo] -> List[valores]
            title: Título
            ylabel: Etiqueta eje Y
            filename: Nombre del archivo
            
        Returns:
            Path del archivo o None
        """
        if not self.has_matplotlib:
            return None
        
        fig, ax = self.plt.subplots(figsize=(10, 6))
        
        algorithms = list(algorithm_results.keys())
        data = [algorithm_results[alg] for alg in algorithms]
        
        bp = ax.boxplot(data, labels=algorithms, patch_artist=True,
                       showmeans=True, meanline=True)
        
        # Colorear boxes
        colors = self.plt.cm.Set3(range(len(algorithms)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        # Rotar etiquetas si son muchas
        if len(algorithms) > 5:
            self.plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica guardada: {filepath}")
        return filepath
    
    def plot_bar_comparison(
        self,
        algorithm_metrics: Dict[str, Dict[str, float]],
        metric_name: str = "mean_value",
        title: str = "Comparación de Algoritmos",
        ylabel: str = "Valor Promedio",
        filename: str = "bar_comparison.png",
        show_error_bars: bool = True,
        error_metric: str = "std_value"
    ) -> Optional[Path]:
        """
        Gráfica de barras con barras de error
        
        Args:
            algorithm_metrics: Dict[algoritmo] -> Dict[metrica] -> valor
            metric_name: Métrica a graficar
            title: Título
            ylabel: Etiqueta Y
            filename: Nombre archivo
            show_error_bars: Mostrar barras de error
            error_metric: Métrica para barras de error
            
        Returns:
            Path del archivo o None
        """
        if not self.has_matplotlib:
            return None
        
        algorithms = list(algorithm_metrics.keys())
        values = [algorithm_metrics[alg][metric_name] for alg in algorithms]
        
        fig, ax = self.plt.subplots(figsize=(10, 6))
        
        x_pos = np.arange(len(algorithms))
        
        if show_error_bars and error_metric in algorithm_metrics[algorithms[0]]:
            errors = [algorithm_metrics[alg][error_metric] for alg in algorithms]
            bars = ax.bar(x_pos, values, yerr=errors, capsize=5, 
                         alpha=0.7, color=self.plt.cm.Set2(range(len(algorithms))))
        else:
            bars = ax.bar(x_pos, values, alpha=0.7,
                         color=self.plt.cm.Set2(range(len(algorithms))))
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(algorithms)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
        
        if len(algorithms) > 5:
            self.plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica guardada: {filepath}")
        return filepath
    
    def plot_performance_profile(
        self,
        algorithm_results: Dict[str, Dict[str, List[float]]],
        metric: str = "gap",
        title: str = "Performance Profile",
        filename: str = "performance_profile.png"
    ) -> Optional[Path]:
        """
        Performance profile (Dolan & Moré 2002)
        
        Args:
            algorithm_results: Dict[algoritmo] -> Dict[instancia] -> List[valores]
            metric: Métrica a usar ("gap" o "time")
            title: Título
            filename: Nombre archivo
            
        Returns:
            Path del archivo o None
            
        Referencias:
        - Dolan & Moré (2002): Benchmarking optimization software
        """
        if not self.has_matplotlib:
            return None
        
        # Esta es una implementación simplificada
        # La versión completa requiere cálculo de ratios de performance
        
        fig, ax = self.plt.subplots(figsize=(10, 6))
        
        algorithms = list(algorithm_results.keys())
        
        # Para cada algoritmo, calcular proporción de problemas resueltos
        # en función del factor de performance
        
        tau_values = np.logspace(0, 2, 100)  # Factores de 1 a 100
        
        for algorithm in algorithms:
            # Simplificación: usar valores promedio
            proportions = []
            for tau in tau_values:
                # Contar cuántos problemas se resuelven con factor <= tau
                count = 0
                total = len(algorithm_results[algorithm])
                
                for instance_values in algorithm_results[algorithm].values():
                    if len(instance_values) > 0:
                        best = min(instance_values) if metric == "gap" else min(instance_values)
                        if best <= tau:
                            count += 1
                
                proportions.append(count / total if total > 0 else 0)
            
            ax.plot(tau_values, proportions, label=algorithm, linewidth=2)
        
        ax.set_xscale('log')
        ax.set_xlabel('Factor de Performance (τ)', fontsize=12)
        ax.set_ylabel('Proporción de Problemas Resueltos', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([1, 100])
        ax.set_ylim([0, 1.05])
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica guardada: {filepath}")
        return filepath
    
    def plot_scatter_time_vs_quality(
        self,
        results: List[Dict[str, Any]],
        title: str = "Tiempo vs Calidad",
        filename: str = "time_vs_quality.png"
    ) -> Optional[Path]:
        """
        Scatter plot de tiempo vs calidad
        
        Args:
            results: Lista de resultados con 'total_time' y 'gap_to_optimal'
            title: Título
            filename: Nombre archivo
            
        Returns:
            Path del archivo o None
        """
        if not self.has_matplotlib:
            return None
        
        fig, ax = self.plt.subplots(figsize=(10, 6))
        
        # Agrupar por algoritmo
        algorithms = {}
        for r in results:
            alg = r['algorithm_name']
            if alg not in algorithms:
                algorithms[alg] = {'times': [], 'gaps': []}
            
            algorithms[alg]['times'].append(r['total_time'])
            if r['gap_to_optimal'] is not None:
                algorithms[alg]['gaps'].append(r['gap_to_optimal'])
        
        # Plotear cada algoritmo
        for alg, data in algorithms.items():
            ax.scatter(data['times'], data['gaps'], label=alg, alpha=0.6, s=50)
        
        ax.set_xlabel('Tiempo (segundos)', fontsize=12)
        ax.set_ylabel('Gap al Óptimo (%)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica guardada: {filepath}")
        return filepath
    
    def generate_html_report(
        self,
        experiment_data: Dict[str, Any],
        filename: str = "report.html"
    ) -> Path:
        """
        Genera reporte HTML con resultados
        
        Args:
            experiment_data: Datos del experimento
            filename: Nombre del archivo HTML
            
        Returns:
            Path del archivo generado
        """
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Experimentos - KBP-SA</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; background: white; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .metric-label {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <h1>📊 Reporte de Experimentos - KBP-SA</h1>
    <p><strong>Fecha:</strong> {experiment_data.get('timestamp', 'N/A')}</p>
    
    <h2>Resumen General</h2>
    <div class="metric">
        <div class="metric-label">Total Experimentos</div>
        <div class="metric-value">{experiment_data.get('total_experiments', 0)}</div>
    </div>
    <div class="metric">
        <div class="metric-label">Exitosos</div>
        <div class="metric-value">{experiment_data.get('successful', 0)}</div>
    </div>
    
    <h2>Resultados por Algoritmo</h2>
    <p>Los resultados completos están en el archivo JSON.</p>
    
</body>
</html>
"""
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Reporte HTML generado: {filepath}")
        return filepath
    
    def plot_acceptance_rate(
        self,
        acceptance_history: List[int],
        window_size: int = 100,
        title: str = "Tasa de Aceptación vs Iteración",
        filename: str = "acceptance_rate.png"
    ) -> Optional[Path]:
        """
        Genera gráfica de tasa de aceptación vs iteración
        
        Args:
            acceptance_history: Lista de 0/1 indicando aceptación por iteración
            window_size: Tamaño de ventana móvil para calcular tasa
            title: Título de la gráfica
            filename: Nombre del archivo
            
        Returns:
            Path del archivo o None
        """
        if not self.has_matplotlib:
            return None
        
        if not acceptance_history or len(acceptance_history) < window_size:
            print("⚠️  No hay suficientes datos de aceptación")
            return None
        
        # Calcular tasa de aceptación con ventana móvil
        acceptance_rates = []
        iterations = []
        
        for i in range(window_size, len(acceptance_history) + 1):
            window = acceptance_history[i - window_size:i]
            rate = (sum(window) / window_size) * 100  # Porcentaje
            acceptance_rates.append(rate)
            iterations.append(i)
        
        fig, ax = self.plt.subplots(figsize=(12, 6))
        
        # Gráfica principal
        ax.plot(iterations, acceptance_rates, color='#2E86AB', linewidth=1.5, alpha=0.8)
        
        # Línea de referencia (50%)
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% Referencia')
        
        # Configuración
        ax.set_xlabel('Iteración', fontsize=12)
        ax.set_ylabel('Tasa de Aceptación (%)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Añadir información estadística
        mean_rate = np.mean(acceptance_rates)
        ax.axhline(y=mean_rate, color='green', linestyle=':', alpha=0.7, 
                  label=f'Media: {mean_rate:.1f}%')
        ax.legend()
        
        # Añadir anotación con estadísticas
        stats_text = f'Ventana: {window_size} iteraciones\\nMedia: {mean_rate:.2f}%\\nMin: {min(acceptance_rates):.2f}%\\nMax: {max(acceptance_rates):.2f}%'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               fontsize=10)
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica de tasa de aceptación guardada: {filepath}")
        return filepath

