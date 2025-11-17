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
        filename: str = "acceptance_rate.png",
        temperature_history: Optional[List[float]] = None
    ) -> Optional[Path]:
        """
        Genera gráfica de tasa de aceptación vs iteración
        
        Args:
            acceptance_history: Lista de 0/1 indicando aceptación por iteración
            window_size: Tamaño de ventana móvil para calcular tasa
            title: Título de la gráfica
            filename: Nombre del archivo
            temperature_history: Lista opcional con temperatura en cada iteración
            
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
        
        fig, ax1 = self.plt.subplots(figsize=(12, 6))
        
        # Eje Y izquierdo: Tasa de aceptación
        color_acceptance = '#2E86AB'
        ax1.set_xlabel('Iteración', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Tasa de Aceptación (%)', fontsize=12, fontweight='bold', color=color_acceptance)
        ax1.plot(iterations, acceptance_rates, color=color_acceptance, linewidth=2, alpha=0.8, label='Tasa de Aceptación')
        ax1.tick_params(axis='y', labelcolor=color_acceptance)
        ax1.set_ylim(0, 105)
        
        # Línea de referencia (50%)
        ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5, linewidth=1, label='50% Referencia')
        
        # Media de tasa de aceptación
        mean_rate = np.mean(acceptance_rates)
        ax1.axhline(y=mean_rate, color='green', linestyle=':', alpha=0.7, linewidth=1.5,
                   label=f'Media: {mean_rate:.1f}%')
        
        # Eje Y derecho: Temperatura (si está disponible)
        if temperature_history is not None and len(temperature_history) >= window_size:
            ax2 = ax1.twinx()
            color_temp = '#FF6B35'  # Naranja
            
            # Alinear temperatura con las iteraciones de acceptance_rates
            temp_aligned = temperature_history[window_size-1:len(temperature_history)]
            temp_aligned = temp_aligned[:len(iterations)]  # Asegurar mismo tamaño
            
            ax2.set_ylabel('Temperatura', fontsize=12, fontweight='bold', color=color_temp)
            ax2.plot(iterations[:len(temp_aligned)], temp_aligned, color=color_temp, 
                    linewidth=2, alpha=0.7, linestyle='-', label='Temperatura')
            ax2.tick_params(axis='y', labelcolor=color_temp)
            
            # Escala logarítmica para temperatura (mejor visualización)
            ax2.set_yscale('log')
            ax2.grid(False)  # Evitar conflicto con grid del eje 1
        
        # Título y grid
        ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax1.grid(True, alpha=0.3, axis='both')
        
        # Leyendas combinadas
        lines1, labels1 = ax1.get_legend_handles_labels()
        if temperature_history is not None and len(temperature_history) >= window_size:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
        else:
            ax1.legend(loc='upper right', fontsize=10)
        
        # Añadir anotación con estadísticas
        stats_text = f'Ventana: {window_size} iteraciones\nMedia: {mean_rate:.2f}%\nMin: {min(acceptance_rates):.2f}%\nMax: {max(acceptance_rates):.2f}%'
        if temperature_history is not None and len(temperature_history) >= window_size:
            temp_min = min(temp_aligned)
            temp_max = max(temp_aligned)
            stats_text += f'\n\nT inicial: {temp_max:.2f}\nT final: {temp_min:.4f}'
        
        ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, edgecolor='black'),
               fontsize=9, family='monospace')
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica de tasa de aceptación guardada: {filepath}")
        return filepath
    
    def plot_gap_evolution(
        self,
        best_values: List[float],
        optimal_value: float,
        title: str = "Evolución del Gap al Óptimo",
        filename: str = "gap_evolution.png",
        show_improvements: bool = True,
        temperature_history: Optional[List[float]] = None
    ) -> Optional[Path]:
        """
        Gráfica de Gap (%) vs Iteración
        
        Muestra la evolución del gap al óptimo conocido a lo largo
        de las iteraciones del algoritmo.
        
        Args:
            best_values: Lista con el mejor valor en cada iteración
            optimal_value: Valor óptimo conocido
            title: Título de la gráfica
            filename: Nombre del archivo
            show_improvements: Marcar iteraciones con mejora
            temperature_history: Lista opcional con temperatura en cada iteración
            
        Returns:
            Path del archivo guardado o None
        """
        if not self.has_matplotlib:
            return None
        
        if not best_values or optimal_value <= 0:
            print("⚠️  Datos insuficientes para gráfica de gap")
            return None
        
        # Calcular gaps en porcentaje
        gaps = []
        for value in best_values:
            gap = ((optimal_value - value) / optimal_value) * 100
            gaps.append(max(0, gap))  # Evitar gaps negativos
        
        iterations = list(range(len(gaps)))
        
        fig, ax1 = self.plt.subplots(figsize=(12, 7))
        
        # Eje Y izquierdo: Gap
        color_gap = '#D62828'
        ax1.set_xlabel('Iteración', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Gap (%)', fontsize=13, fontweight='bold', color=color_gap)
        ax1.plot(iterations, gaps, color=color_gap, linewidth=2.5, 
               label='Gap (%)', alpha=0.9)
        ax1.tick_params(axis='y', labelcolor=color_gap)
        
        # Línea del 0% (óptimo alcanzado)
        ax1.axhline(y=0, color='green', linestyle='--', linewidth=2,
                  alpha=0.7, label='Óptimo (0%)')
        
        # Zona de gap aceptable (< 1%)
        ax1.axhspan(0, 1, alpha=0.1, color='green', label='Gap < 1%')
        
        # Marcar mejoras si se solicita
        if show_improvements:
            improvements = [0]  # Primera iteración siempre es mejora
            for i in range(1, len(best_values)):
                if best_values[i] > best_values[i-1]:
                    improvements.append(i)
            
            if improvements:
                improvement_gaps = [gaps[i] for i in improvements]
                ax1.scatter(improvements, improvement_gaps, 
                         color='orange', s=80, zorder=5, 
                         alpha=0.7, edgecolors='black', linewidth=0.5,
                         label=f'Mejoras ({len(improvements)})')
        
        # Configurar límites del eje Y izquierdo
        max_gap = max(gaps)
        ax1.set_ylim(-0.5, min(max_gap * 1.1, 100))
        ax1.grid(True, alpha=0.3)
        
        # Eje Y derecho: Temperatura (si está disponible)
        if temperature_history is not None and len(temperature_history) == len(gaps):
            ax2 = ax1.twinx()
            color_temp = '#FF6B35'  # Naranja
            
            ax2.set_ylabel('Temperatura', fontsize=13, fontweight='bold', color=color_temp)
            ax2.plot(iterations, temperature_history, color=color_temp, 
                    linewidth=2.5, alpha=0.8, linestyle='-', label='Temperatura')
            ax2.tick_params(axis='y', labelcolor=color_temp)
            
            # Escala logarítmica para temperatura (mejor visualización)
            ax2.set_yscale('log')
            ax2.grid(False)  # Evitar conflicto con grid del eje 1
        
        # Título
        ax1.set_title(title, fontsize=15, fontweight='bold', pad=20)
        
        # Leyendas combinadas
        lines1, labels1 = ax1.get_legend_handles_labels()
        if temperature_history is not None and len(temperature_history) == len(gaps):
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=11)
        else:
            ax1.legend(loc='upper right', fontsize=11)
        
        # Añadir estadísticas
        final_gap = gaps[-1]
        min_gap = min(gaps)
        mean_gap = np.mean(gaps)
        
        stats_text = (f'Gap Inicial: {gaps[0]:.2f}%\n'
                     f'Gap Final: {final_gap:.2f}%\n'
                     f'Gap Mínimo: {min_gap:.2f}%\n'
                     f'Gap Promedio: {mean_gap:.2f}%\n'
                     f'Valor Óptimo: {optimal_value}')
        
        if temperature_history is not None and len(temperature_history) == len(gaps):
            temp_min = min(temperature_history)
            temp_max = max(temperature_history)
            stats_text += f'\n\nT Inicial: {temp_max:.2f}\nT Final: {temp_min:.4f}'
        
        ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
               verticalalignment='top', 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, 
                        edgecolor='black', linewidth=1.5),
               fontsize=9, family='monospace')
        
        # Añadir línea de tendencia si hay suficientes datos
        if len(iterations) > 10:
            z = np.polyfit(iterations, gaps, 3)  # Polinomio de grado 3
            p = np.poly1d(z)
            ax1.plot(iterations, p(iterations), "b:", linewidth=1.5, 
                   alpha=0.5, label='Tendencia')
            # Actualizar leyenda
            lines1, labels1 = ax1.get_legend_handles_labels()
            if temperature_history is not None and len(temperature_history) == len(gaps):
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=11)
            else:
                ax1.legend(loc='upper right', fontsize=11)
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica de gap guardada: {filepath}")
        return filepath
    
    def plot_delta_e_distribution(
        self,
        delta_e_values: List[float],
        acceptance_decisions: List[bool],
        title: str = "Distribución de ΔE (Diferencias de Energía)",
        filename: str = "delta_e_distribution.png",
        bins: int = 50
    ) -> Optional[Path]:
        """
        Gráfica de distribución de ΔE (diferencias de energía)
        
        Muestra histograma de cambios de energía, separando movimientos
        aceptados y rechazados, mejoras (ΔE < 0) y empeoramientos (ΔE > 0).
        
        Args:
            delta_e_values: Lista de diferencias de energía (neighbor - current)
            acceptance_decisions: Lista de booleanos (True=aceptado, False=rechazado)
            title: Título de la gráfica
            filename: Nombre del archivo
            bins: Número de bins para histograma
            
        Returns:
            Path del archivo guardado o None
        """
        if not self.has_matplotlib:
            return None
        
        if not delta_e_values or len(delta_e_values) != len(acceptance_decisions):
            print("⚠️  Datos insuficientes o inconsistentes para distribución de ΔE")
            return None
        
        # Convertir a arrays numpy
        delta_e = np.array(delta_e_values)
        accepted = np.array(acceptance_decisions)
        
        # Separar en aceptados y rechazados
        delta_e_accepted = delta_e[accepted]
        delta_e_rejected = delta_e[~accepted]
        
        # Separar en mejoras (ΔE ≤ 0) y empeoramientos (ΔE > 0)
        improvements = delta_e[delta_e <= 0]
        worsenings = delta_e[delta_e > 0]
        
        improvements_accepted = delta_e_accepted[delta_e_accepted <= 0]
        worsenings_accepted = delta_e_accepted[delta_e_accepted > 0]
        worsenings_rejected = delta_e_rejected[delta_e_rejected > 0]
        
        # Crear figura con 2 subplots
        fig, (ax1, ax2) = self.plt.subplots(1, 2, figsize=(16, 6))
        
        # --- SUBPLOT 1: Histograma general (aceptados vs rechazados) ---
        
        # Determinar rango común para bins
        min_delta = min(delta_e)
        max_delta = max(delta_e)
        bin_edges = np.linspace(min_delta, max_delta, bins + 1)
        
        # Histogramas superpuestos
        ax1.hist(delta_e_accepted, bins=bin_edges, alpha=0.7, 
                color='#06A77D', label=f'Aceptados ({len(delta_e_accepted)})', 
                edgecolor='black', linewidth=0.5)
        ax1.hist(delta_e_rejected, bins=bin_edges, alpha=0.7, 
                color='#D62828', label=f'Rechazados ({len(delta_e_rejected)})', 
                edgecolor='black', linewidth=0.5)
        
        # Línea vertical en ΔE = 0
        ax1.axvline(x=0, color='black', linestyle='--', linewidth=2.5, 
                   alpha=0.8, label='ΔE = 0 (neutral)', zorder=10)
        
        # Sombrear zonas
        ax1.axvspan(min_delta, 0, alpha=0.05, color='green', label='Mejoras (ΔE ≤ 0)')
        ax1.axvspan(0, max_delta, alpha=0.05, color='red', label='Empeoramientos (ΔE > 0)')
        
        ax1.set_xlabel('ΔE (Diferencia de Energía)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax1.set_title('Distribución: Aceptados vs Rechazados', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=9)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Estadísticas en subplot 1
        stats1_text = (f'Total movimientos: {len(delta_e)}\n'
                      f'Aceptados: {len(delta_e_accepted)} ({len(delta_e_accepted)/len(delta_e)*100:.1f}%)\n'
                      f'Rechazados: {len(delta_e_rejected)} ({len(delta_e_rejected)/len(delta_e)*100:.1f}%)\n'
                      f'\nΔE promedio: {np.mean(delta_e):.2f}\n'
                      f'ΔE mediana: {np.median(delta_e):.2f}')
        
        ax1.text(0.02, 0.98, stats1_text, transform=ax1.transAxes,
                verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'),
                fontsize=9, family='monospace')
        
        # --- SUBPLOT 2: Desglose por tipo de movimiento ---
        
        # Histogramas apilados para mejoras y empeoramientos
        
        # Solo empeoramientos (ΔE > 0)
        worsening_bin_edges = np.linspace(0, max_delta, bins//2 + 1) if max_delta > 0 else [0, 1]
        
        if len(worsenings) > 0:
            ax2.hist(worsenings_accepted, bins=worsening_bin_edges, alpha=0.7,
                    color='#FF9F1C', label=f'Empeoramientos Aceptados ({len(worsenings_accepted)})',
                    edgecolor='black', linewidth=0.5)
            ax2.hist(worsenings_rejected, bins=worsening_bin_edges, alpha=0.7,
                    color='#D62828', label=f'Empeoramientos Rechazados ({len(worsenings_rejected)})',
                    edgecolor='black', linewidth=0.5)
        
        # Mejoras en otra zona (ΔE ≤ 0)
        improvement_bin_edges = np.linspace(min_delta, 0, bins//2 + 1)
        
        if len(improvements) > 0:
            # Usar barras para mejoras (siempre aceptadas en SA estándar)
            ax2.hist(improvements_accepted, bins=improvement_bin_edges, alpha=0.8,
                    color='#06A77D', label=f'Mejoras (siempre aceptadas) ({len(improvements_accepted)})',
                    edgecolor='black', linewidth=0.5)
        
        # Línea vertical en ΔE = 0
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=2.5, 
                   alpha=0.8, zorder=10)
        
        ax2.set_xlabel('ΔE (Diferencia de Energía)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax2.set_title('Desglose: Mejoras vs Empeoramientos', fontsize=13, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Estadísticas en subplot 2
        improvement_rate = len(improvements) / len(delta_e) * 100 if len(delta_e) > 0 else 0
        worsening_accept_rate = len(worsenings_accepted) / len(worsenings) * 100 if len(worsenings) > 0 else 0
        
        stats2_text = (f'Mejoras (ΔE≤0): {len(improvements)} ({improvement_rate:.1f}%)\n'
                      f'  • Promedio: {np.mean(improvements):.2f}\n'
                      f'\nEmpeoramientos (ΔE>0): {len(worsenings)} ({100-improvement_rate:.1f}%)\n'
                      f'  • Aceptados: {len(worsenings_accepted)} ({worsening_accept_rate:.1f}%)\n'
                      f'  • Rechazados: {len(worsenings_rejected)} ({100-worsening_accept_rate:.1f}%)\n'
                      f'  • Promedio: {np.mean(worsenings):.2f}')
        
        ax2.text(0.02, 0.98, stats2_text, transform=ax2.transAxes,
                verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'),
                fontsize=9, family='monospace')
        
        # Título general
        fig.suptitle(title, fontsize=15, fontweight='bold', y=0.98)
        
        filepath = self.output_dir / filename
        self.plt.tight_layout()
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica de distribución ΔE guardada: {filepath}")
        return filepath
    
    def plot_exploration_exploitation_balance(
        self, delta_e_values, acceptance_decisions, temperature_history,
        title, filename, window_size=100
    ):
        """
        Genera un área apilada mostrando el balance exploración-explotación
        
        Exploración = movimientos que empeoran pero son aceptados (ΔE>0 aceptados)
        Explotación = movimientos que mejoran (ΔE≤0)
        
        Args:
            delta_e_values: Lista de diferencias de energía
            acceptance_decisions: Lista de decisiones (True/False)
            temperature_history: Lista de temperaturas
            title: Título del gráfico
            filename: Nombre del archivo de salida
            window_size: Tamaño de ventana para suavizado
            
        Returns:
            str: Ruta del archivo generado
        """
        if not self.has_matplotlib:
            print("⚠️  matplotlib no disponible")
            return None
        
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Rectangle
        
        # Convertir a arrays numpy
        delta_e = np.array(delta_e_values)
        accepted = np.array(acceptance_decisions, dtype=bool)
        temperature = np.array(temperature_history)
        
        n_iters = len(delta_e)
        
        # Clasificar movimientos por tipo
        # Explotación (mejoras): ΔE ≤ 0
        # Exploración (empeoramientos aceptados): ΔE > 0 y aceptado
        
        improving = delta_e <= 0
        worsening = delta_e > 0
        
        # Crear series binarias para cada tipo
        exploitation = improving.astype(int)  # Mejoras (siempre explotación)
        exploration = (worsening & accepted).astype(int)  # Empeoramientos aceptados
        rejected = (worsening & ~accepted).astype(int)  # Empeoramientos rechazados
        
        # Calcular proporciones con ventana móvil
        def moving_proportion(data, window):
            """Calcula proporción móvil"""
            if window < 1:
                window = 1
            result = np.zeros(len(data))
            for i in range(len(data)):
                start = max(0, i - window + 1)
                end = i + 1
                result[i] = np.mean(data[start:end]) * 100
            return result
        
        exploitation_prop = moving_proportion(exploitation, window_size)
        exploration_prop = moving_proportion(exploration, window_size)
        rejected_prop = moving_proportion(rejected, window_size)
        
        # Crear figura con área apilada
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        iterations = np.arange(1, n_iters + 1)
        
        # Área apilada
        ax1.fill_between(
            iterations, 0, exploitation_prop,
            color='#06A77D', alpha=0.7, label='Explotación (mejoras ΔE≤0)',
            linewidth=0
        )
        ax1.fill_between(
            iterations, exploitation_prop, exploitation_prop + exploration_prop,
            color='#FF9F1C', alpha=0.7, label='Exploración (empeoramientos aceptados)',
            linewidth=0
        )
        ax1.fill_between(
            iterations, exploitation_prop + exploration_prop, 100,
            color='#D62828', alpha=0.5, label='Rechazados (empeoramientos)',
            linewidth=0
        )
        
        # Línea de referencia 50%
        ax1.axhline(y=50, color='black', linestyle='--', linewidth=1.5, alpha=0.5, label='50%')
        
        # Configurar eje Y principal
        ax1.set_xlabel('Iteración', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Proporción de Movimientos (%)', fontsize=12, fontweight='bold', color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
        
        # Segundo eje Y para temperatura
        ax2 = ax1.twinx()
        
        # Línea de temperatura
        temp_line = ax2.plot(
            iterations, temperature,
            color='#FF6B35', linewidth=2.5, alpha=0.8,
            label='Temperatura', linestyle='-', marker=None
        )
        
        ax2.set_ylabel('Temperatura (escala log)', fontsize=12, fontweight='bold', color='#FF6B35')
        ax2.tick_params(axis='y', labelcolor='#FF6B35')
        ax2.set_yscale('log')
        
        # Título
        ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Combinar leyendas
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(
            lines1 + lines2, labels1 + labels2,
            loc='upper right', framealpha=0.95, fontsize=10
        )
        
        # Panel de estadísticas
        total_improving = np.sum(improving)
        total_worsening_accepted = np.sum(worsening & accepted)
        total_worsening_rejected = np.sum(worsening & ~accepted)
        total_moves = len(delta_e)
        
        exploitation_rate = (total_improving / total_moves) * 100
        exploration_rate = (total_worsening_accepted / total_moves) * 100
        rejection_rate = (total_worsening_rejected / total_moves) * 100
        
        # Calcular punto de transición (donde exploración cae por debajo de cierto umbral)
        # Transición = cuando exploración cae por debajo de 10%
        transition_threshold = 10.0
        transition_iter = None
        for i in range(len(exploration_prop)):
            if exploration_prop[i] < transition_threshold:
                transition_iter = i + 1
                break
        
        stats_text = f"Ventana: {window_size} iter\n"
        stats_text += f"Explotación: {exploitation_rate:.1f}%\n"
        stats_text += f"Exploración: {exploration_rate:.1f}%\n"
        stats_text += f"Rechazados: {rejection_rate:.1f}%\n"
        stats_text += f"T inicial: {temperature[0]:.2f}\n"
        stats_text += f"T final: {temperature[-1]:.4f}\n"
        if transition_iter:
            stats_text += f"Transición: iter {transition_iter}"
        
        # Recuadro de estadísticas
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=1.5)
        ax1.text(
            0.02, 0.98, stats_text,
            transform=ax1.transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=props,
            family='monospace'
        )
        
        # Ajustar layout
        plt.tight_layout()
        
        # Guardar
        output_path = self.output_dir / filename
        self.plt.savefig(output_path, dpi=300, bbox_inches='tight')
        self.plt.close(fig)
        
        print(f"📊 Gráfica de balance exploración-explotación guardada: {output_path}")
        return str(output_path)


