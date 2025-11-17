# Plan de Implementación: SAVisualizer

Sistema completo de visualizaciones especializadas para análisis de Simulated Annealing en KBP-SA.

---

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Especificaciones Técnicas](#especificaciones-técnicas)
4. [Implementación por Fases](#implementación-por-fases)
5. [Integración con Sistema Existente](#integración-con-sistema-existente)
6. [Plan de Pruebas](#plan-de-pruebas)

---

## 📐 Arquitectura del Sistema

### Componentes Principales

```
experimentation/
├── visualization.py          # Existente (visualizaciones generales)
├── sa_visualizations.py      # NUEVO (visualizaciones SA específicas)
├── tracking.py               # Existente (sistema de tracking)
└── plotter_utils.py          # NUEVO (utilidades de plotting)
```

### Flujo de Datos

```
SA Execution → Tracking System → Logs (CSV/JSON) → SAVisualizer → Gráficas (PNG)
     ↓              ↓                    ↓               ↓
  sa_core.py   tracking.py      output/{inst}/   sa_visualizations.py
```

---

## 📁 Estructura de Archivos

### Nuevo archivo: `experimentation/sa_visualizations.py`

**Propósito**: Visualizaciones especializadas para análisis de Simulated Annealing.

**Clases**:
- `SAVisualizer`: Clase principal de visualizaciones
- `SADashboard`: Dashboard multi-panel
- `SAParameterAnalyzer`: Análisis de sensibilidad de parámetros

**Dependencias**:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
```

---

### Nuevo archivo: `experimentation/plotter_utils.py`

**Propósito**: Utilidades compartidas para plotting.

**Funciones**:
- `setup_publication_style()`: Configurar estilo profesional
- `save_figure()`: Guardar con múltiples formatos
- `create_color_palette()`: Paletas de colores consistentes
- `add_grid_lines()`: Grillas profesionales

---

## 🔧 Especificaciones Técnicas

### Clase: `SAVisualizer`

```python
class SAVisualizer:
    """
    Visualizador especializado para Simulated Annealing
    
    Genera visualizaciones avanzadas usando datos de tracking
    del sistema SA.
    
    Attributes:
        output_dir: Directorio para guardar gráficas
        style: Estilo de matplotlib ('seaborn', 'ggplot', etc.)
        dpi: Resolución de imágenes (default: 300)
        figsize: Tamaño default de figuras
        colors: Paleta de colores
    """
    
    def __init__(self, 
                 output_dir: str = "output/visualizations",
                 style: str = "seaborn-v0_8-darkgrid",
                 dpi: int = 300,
                 figsize: Tuple[int, int] = (12, 8)):
        pass
```

---

## 📊 Implementación por Fases

---

## **FASE 1: Dashboard Multi-Variable** (PRIORIDAD ALTA)

### Método: `plot_convergence_dashboard()`

**Entrada**:
```python
tracking_data = {
    'iterations': [0, 1, 2, ...],
    'best_values': [150, 150, 160, ...],
    'temperatures': [100.0, 100.0, 95.0, ...],
    'acceptance_windows': {
        'window_50': [0.68, 0.64, ...],
        'window_100': [0.65, 0.62, ...],
        'window_200': [0.63, 0.60, ...]
    },
    'gaps': [44.24, 44.24, 40.52, ...]
}

metadata = {
    'instance_name': 'f1_l-d_kp_10_269',
    'optimal': 295,
    'T0': 100.0,
    'alpha': 0.95,
    'seed': 42
}
```

**Output**: Figura con 4 subplots (2×2)

**Implementación**:

```python
def plot_convergence_dashboard(self,
                               tracking_data: Dict,
                               metadata: Dict,
                               filename: str = "sa_dashboard.png") -> str:
    """
    Dashboard completo de convergencia SA (4 subplots)
    
    Subplots:
    1. (Top-left) Best Value vs Iteration
    2. (Top-right) Temperature vs Iteration  
    3. (Bottom-left) Acceptance Rate vs Iteration
    4. (Bottom-right) Gap vs Time
    
    Args:
        tracking_data: Datos de convergence.json
        metadata: Información del experimento
        filename: Nombre del archivo de salida
    
    Returns:
        Path al archivo guardado
    """
    
    # Crear figura con GridSpec
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # --- SUBPLOT 1: Best Value vs Iteration ---
    ax1 = fig.add_subplot(gs[0, 0])
    
    iterations = tracking_data['iterations']
    best_values = tracking_data['best_values']
    optimal = metadata['optimal']
    
    # Línea principal
    ax1.plot(iterations, best_values, 
             linewidth=2, color='#2E86AB', label='Best Value')
    
    # Línea del óptimo
    ax1.axhline(y=optimal, color='red', linestyle='--', 
                linewidth=1.5, alpha=0.7, label=f'Optimal ({optimal})')
    
    # Zona de gap aceptable (< 1%)
    gap_threshold = optimal * 0.99
    ax1.axhspan(gap_threshold, optimal, alpha=0.1, color='green',
                label='Gap < 1%')
    
    # Marcadores de mejoras
    improvements = tracking_data.get('improvement_markers', [])
    if improvements:
        improvement_values = [best_values[i] for i in improvements if i < len(best_values)]
        ax1.scatter(improvements[:len(improvement_values)], improvement_values, 
                   color='orange', s=50, zorder=5, alpha=0.6,
                   label='Improvements')
    
    ax1.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Best Value', fontsize=12, fontweight='bold')
    ax1.set_title('Convergence: Best Value', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # --- SUBPLOT 2: Temperature vs Iteration ---
    ax2 = fig.add_subplot(gs[0, 1])
    
    temperatures = tracking_data['temperatures']
    
    # Temperatura en escala logarítmica
    ax2.plot(iterations, temperatures, 
             linewidth=2, color='#FF6B35', label='Temperature')
    
    ax2.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Temperature', fontsize=12, fontweight='bold')
    ax2.set_title('Cooling Schedule', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3, which='both')
    
    # Anotación de parámetros
    ax2.text(0.05, 0.95, f"T₀ = {metadata['T0']}\nα = {metadata['alpha']}", 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # --- SUBPLOT 3: Acceptance Rate vs Iteration ---
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Usar ventana de 100 iteraciones por default
    acceptance_rates = tracking_data['acceptance_windows']['window_100']
    
    ax3.plot(iterations, acceptance_rates, 
             linewidth=2, color='#06A77D', label='Acceptance Rate (window=100)')
    
    # Línea de referencia (50%)
    ax3.axhline(y=0.5, color='gray', linestyle='--', 
                linewidth=1, alpha=0.5, label='50% threshold')
    
    ax3.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Acceptance Rate', fontsize=12, fontweight='bold')
    ax3.set_title('Exploration vs Exploitation', fontsize=14, fontweight='bold')
    ax3.set_ylim(0, 1)
    ax3.legend(loc='upper right', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Sombrear regiones
    ax3.axhspan(0.7, 1.0, alpha=0.1, color='blue', label='High Exploration')
    ax3.axhspan(0.0, 0.3, alpha=0.1, color='red', label='High Exploitation')
    
    # --- SUBPLOT 4: Gap vs Time ---
    ax4 = fig.add_subplot(gs[1, 1])
    
    gaps = tracking_data['gaps']
    # Calcular tiempo acumulado (asumiendo tiempo uniforme por iteración)
    total_time = metadata.get('elapsed_time', len(iterations) * 0.001)
    times = np.linspace(0, total_time, len(iterations))
    
    ax4.plot(times, gaps, 
             linewidth=2, color='#A23B72', label='Gap to Optimal')
    
    ax4.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Gap (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Efficiency: Gap vs Time', fontsize=14, fontweight='bold')
    ax4.legend(loc='upper right', fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Línea de gap objetivo (1%)
    ax4.axhline(y=1.0, color='green', linestyle='--', 
                linewidth=1.5, alpha=0.7, label='Target (1%)')
    
    # Título general
    instance_name = metadata.get('instance_name', 'Unknown')
    fig.suptitle(f'Simulated Annealing Dashboard: {instance_name}', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

**Datos requeridos**:
- `convergence.json` (del sistema de tracking)
- `summary.json` (metadata)

**Prueba unitaria**:
```python
# En tests/test_sa_visualizations.py
def test_convergence_dashboard():
    visualizer = SAVisualizer(output_dir="tests/output")
    
    # Mock data
    tracking_data = load_json("fixtures/convergence_f1.json")
    metadata = load_json("fixtures/metadata_f1.json")
    
    path = visualizer.plot_convergence_dashboard(tracking_data, metadata)
    
    assert Path(path).exists()
    assert Path(path).suffix == '.png'
```

---

## **FASE 2: Análisis de Aceptación** (PRIORIDAD ALTA)

### Método: `plot_acceptance_analysis()`

**Entrada**:
```python
acceptance_log = pd.read_csv("tracking_acceptance.csv")
# Columnas: iteration, temperature, delta_E, acceptance_prob, accepted, move_type, improvement
```

**Output**: Figura con 3 subplots (1×3)

**Implementación**:

```python
def plot_acceptance_analysis(self,
                             acceptance_log: pd.DataFrame,
                             filename: str = "acceptance_analysis.png") -> str:
    """
    Análisis detallado de decisiones de aceptación
    
    Subplots:
    1. Decisiones por tipo de movimiento (barras apiladas)
    2. Distribución de ΔE (histograma)
    3. Probabilidad calculada vs observada (scatter)
    
    Args:
        acceptance_log: DataFrame de tracking_acceptance.csv
        filename: Nombre del archivo
    
    Returns:
        Path al archivo guardado
    """
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # --- SUBPLOT 1: Decisiones por Tipo ---
    ax1 = axes[0]
    
    # Agrupar por tipo de movimiento
    types = ['improving', 'worsening', 'neutral']
    type_counts = {}
    
    for move_type in types:
        mask = acceptance_log['move_type'] == move_type
        total = mask.sum()
        accepted = (mask & acceptance_log['accepted']).sum()
        rejected = total - accepted
        
        type_counts[move_type] = {
            'accepted': accepted,
            'rejected': rejected,
            'total': total,
            'rate': accepted / total if total > 0 else 0
        }
    
    # Barras apiladas
    x_pos = np.arange(len(types))
    accepted_vals = [type_counts[t]['accepted'] for t in types]
    rejected_vals = [type_counts[t]['rejected'] for t in types]
    
    ax1.bar(x_pos, accepted_vals, label='Accepted', color='#06A77D', alpha=0.8)
    ax1.bar(x_pos, rejected_vals, bottom=accepted_vals, 
            label='Rejected', color='#D62828', alpha=0.8)
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([t.capitalize() for t in types])
    ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax1.set_title('Acceptance Decisions by Move Type', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Anotaciones de tasa
    for i, move_type in enumerate(types):
        rate = type_counts[move_type]['rate']
        total = type_counts[move_type]['total']
        ax1.text(i, total + total * 0.05, f'{rate*100:.1f}%', 
                ha='center', fontsize=10, fontweight='bold')
    
    # --- SUBPLOT 2: Distribución de ΔE ---
    ax2 = axes[1]
    
    # Separar aceptados y rechazados
    accepted_mask = acceptance_log['accepted']
    delta_e_accepted = acceptance_log.loc[accepted_mask, 'delta_E']
    delta_e_rejected = acceptance_log.loc[~accepted_mask, 'delta_E']
    
    # Histogramas superpuestos
    bins = 50
    ax2.hist(delta_e_accepted, bins=bins, alpha=0.6, 
             color='#06A77D', label='Accepted', edgecolor='black')
    ax2.hist(delta_e_rejected, bins=bins, alpha=0.6, 
             color='#D62828', label='Rejected', edgecolor='black')
    
    # Línea vertical en ΔE=0
    ax2.axvline(x=0, color='black', linestyle='--', linewidth=2, 
                label='ΔE = 0 (neutral)')
    
    ax2.set_xlabel('ΔE (Energy Difference)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Distribution of Energy Differences', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Anotaciones
    ax2.text(0.05, 0.95, f'Improvements (ΔE≤0): {(delta_e_accepted <= 0).sum()}\n'
                         f'Worsening (ΔE>0): {(delta_e_accepted > 0).sum()}',
             transform=ax2.transAxes, fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # --- SUBPLOT 3: Probabilidad Calculada vs Observada ---
    ax3 = axes[2]
    
    # Crear bins de probabilidad
    prob_bins = np.linspace(0, 1, 21)  # 20 bins de 0.05
    bin_centers = (prob_bins[:-1] + prob_bins[1:]) / 2
    
    observed_rates = []
    bin_counts = []
    
    for i in range(len(prob_bins) - 1):
        # Filtrar movimientos en este rango de probabilidad
        mask = (acceptance_log['acceptance_prob'] >= prob_bins[i]) & \
               (acceptance_log['acceptance_prob'] < prob_bins[i+1])
        
        count = mask.sum()
        bin_counts.append(count)
        
        if count > 0:
            observed_rate = acceptance_log.loc[mask, 'accepted'].mean()
            observed_rates.append(observed_rate)
        else:
            observed_rates.append(np.nan)
    
    # Scatter plot
    valid_mask = ~np.isnan(observed_rates)
    ax3.scatter(bin_centers[valid_mask], np.array(observed_rates)[valid_mask], 
               s=np.array(bin_counts)[valid_mask] * 2,  # Tamaño proporcional a conteo
               alpha=0.6, color='#2E86AB', edgecolors='black', linewidth=0.5)
    
    # Línea y=x (ideal)
    ax3.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Ideal (y=x)')
    
    ax3.set_xlabel('Calculated Probability', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Observed Acceptance Rate', fontsize=12, fontweight='bold')
    ax3.set_title('Metropolis Criterion Validation', fontsize=13, fontweight='bold')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')
    
    # Anotación
    ax3.text(0.95, 0.05, 'Bubble size = sample size', 
             transform=ax3.transAxes, fontsize=9, 
             ha='right', style='italic')
    
    plt.tight_layout()
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

**Datos requeridos**:
- `tracking_acceptance.csv`

---

## **FASE 3: Landscape de Búsqueda** (PRIORIDAD MEDIA)

### Método: `plot_landscape_exploration()`

**Entrada**:
```python
# Cargar soluciones visitadas durante la búsqueda
solutions_df = pd.read_csv("tracking_full.csv")
# Columnas: iteration, current_value, current_weight, best_value, temperature, accepted
```

**Output**: Scatter plot 2D

**Implementación**:

```python
def plot_landscape_exploration(self,
                               solutions_df: pd.DataFrame,
                               metadata: Dict,
                               filename: str = "landscape_exploration.png") -> str:
    """
    Visualización del landscape de búsqueda (2D)
    
    Muestra trayectoria en espacio Peso × Valor
    - Color = Temperatura
    - Tamaño = Calidad relativa
    - Marca inicial/final
    
    Args:
        solutions_df: DataFrame de tracking_full.csv
        metadata: Información (capacity, optimal)
        filename: Nombre del archivo
    
    Returns:
        Path al archivo guardado
    """
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extraer datos
    weights = solutions_df['current_weight'].values
    values = solutions_df['current_value'].values
    temperatures = solutions_df['temperature'].values
    iterations = solutions_df['iteration'].values
    
    capacity = metadata['capacity']
    optimal = metadata['optimal']
    
    # Normalizar temperatura para color
    temp_norm = (temperatures - temperatures.min()) / (temperatures.max() - temperatures.min())
    
    # Scatter plot principal
    scatter = ax.scatter(weights, values, 
                        c=temp_norm, 
                        cmap='coolwarm',  # Frío (azul) = baja T, Caliente (rojo) = alta T
                        s=30, 
                        alpha=0.6,
                        edgecolors='black',
                        linewidth=0.3)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Temperature (normalized)', fontsize=11, fontweight='bold')
    
    # Marcar solución inicial (verde)
    ax.scatter(weights[0], values[0], 
              s=200, color='green', marker='*', 
              edgecolors='black', linewidth=2,
              label='Initial', zorder=5)
    
    # Marcar solución final (azul)
    ax.scatter(weights[-1], values[-1], 
              s=200, color='blue', marker='s', 
              edgecolors='black', linewidth=2,
              label='Final', zorder=5)
    
    # Marcar mejor solución global (dorado)
    best_idx = values.argmax()
    ax.scatter(weights[best_idx], values[best_idx], 
              s=250, color='gold', marker='D', 
              edgecolors='black', linewidth=2,
              label='Best', zorder=6)
    
    # Línea de capacidad (vertical)
    ax.axvline(x=capacity, color='red', linestyle='--', 
              linewidth=2, alpha=0.7, label=f'Capacity ({capacity})')
    
    # Zona infactible (sombreada)
    ax.axvspan(capacity, weights.max() * 1.1, alpha=0.1, color='red')
    
    # Línea de óptimo (horizontal)
    ax.axhline(y=optimal, color='green', linestyle='--', 
              linewidth=2, alpha=0.7, label=f'Optimal ({optimal})')
    
    # Conectar puntos con líneas finas (trayectoria)
    ax.plot(weights, values, 
           color='gray', alpha=0.2, linewidth=0.5, zorder=1)
    
    ax.set_xlabel('Weight', fontsize=13, fontweight='bold')
    ax.set_ylabel('Value', fontsize=13, fontweight='bold')
    ax.set_title('Search Space Landscape Exploration', fontsize=15, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Anotaciones
    instance_name = metadata.get('instance_name', 'Unknown')
    ax.text(0.02, 0.98, f'Instance: {instance_name}\nIterations: {len(iterations)}', 
           transform=ax.transAxes, fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

**Datos requeridos**:
- `tracking_full.csv`
- `metadata.json`

---

## **FASE 4: Performance Profiles** (PRIORIDAD ALTA - Multi-Algoritmo)

### Método: `plot_performance_profiles()`

**Entrada**:
```python
# Resultados de múltiples algoritmos en múltiples instancias
results = {
    'Algorithm_1': {
        'f1': 0.34,  # gaps
        'f2': 1.25,
        'f3': 0.00,
        # ...
    },
    'Algorithm_2': {
        'f1': 2.15,
        'f2': 0.50,
        # ...
    }
}
```

**Output**: Gráfica CDF de performance

**Implementación**:

```python
def plot_performance_profiles(self,
                              algorithm_results: Dict[str, Dict[str, float]],
                              filename: str = "performance_profiles.png") -> str:
    """
    Performance Profiles (Dolan & Moré, 2002)
    
    Muestra robustez de algoritmos mediante CDF de ratios de performance.
    
    Args:
        algorithm_results: {alg_name: {instance: gap}}
        filename: Nombre del archivo
    
    Returns:
        Path al archivo guardado
    """
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Convertir a DataFrame
    df = pd.DataFrame(algorithm_results).T
    
    # Calcular performance ratios
    # ratio[alg, inst] = gap[alg, inst] / min_gap[inst]
    min_gaps = df.min(axis=0)
    ratios = df.div(min_gaps, axis=1)
    
    # Reemplazar 0/0 = NaN con 1.0 (óptimo encontrado)
    ratios = ratios.fillna(1.0)
    
    # Crear tau values (eje X)
    tau_max = ratios.max().max() * 1.1
    tau_values = np.linspace(1.0, tau_max, 100)
    
    # Calcular CDF para cada algoritmo
    colors = plt.cm.tab10(np.linspace(0, 1, len(algorithm_results)))
    
    for i, (alg_name, color) in enumerate(zip(algorithm_results.keys(), colors)):
        alg_ratios = ratios.loc[alg_name].values
        
        # CDF: P(ratio <= tau)
        cdf_values = []
        for tau in tau_values:
            prob = (alg_ratios <= tau).sum() / len(alg_ratios)
            cdf_values.append(prob)
        
        ax.plot(tau_values, cdf_values, 
               linewidth=2.5, color=color, label=alg_name, 
               marker='o', markersize=4, markevery=10)
    
    ax.set_xlabel('Performance Ratio (τ)', fontsize=13, fontweight='bold')
    ax.set_ylabel('P(ratio ≤ τ)', fontsize=13, fontweight='bold')
    ax.set_title('Performance Profiles', fontsize=15, fontweight='bold')
    ax.set_xlim(1.0, tau_max)
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Líneas de referencia
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(x=1.0, color='green', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Anotación
    ax.text(0.98, 0.02, 'Higher curve = more robust algorithm', 
           transform=ax.transAxes, fontsize=10, 
           ha='right', style='italic',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

**Datos requeridos**:
- Resultados de experimentos multi-algoritmo

---

## **FASE 5: Análisis de Parámetros** (PRIORIDAD MEDIA)

### Método: `plot_parameter_sensitivity()`

**Entrada**:
```python
# Resultados de grid search sobre parámetros
param_results = {
    'T0': [50, 75, 100, 125, 150],
    'alpha': [0.85, 0.90, 0.95, 0.99],
    'gaps': [
        [5.2, 3.1, 2.4, 1.8, 1.5],  # Para cada T0 con alpha=0.85
        [4.8, 2.7, 1.9, 1.2, 0.9],  # alpha=0.90
        # ...
    ]
}
```

**Output**: Heatmap 2D

**Implementación**:

```python
def plot_parameter_sensitivity(self,
                               param_grid: Dict,
                               filename: str = "parameter_sensitivity.png") -> str:
    """
    Análisis de sensibilidad de parámetros (heatmap)
    
    Muestra gap promedio para combinaciones de T0 × alpha
    
    Args:
        param_grid: Resultados de grid search
        filename: Nombre del archivo
    
    Returns:
        Path al archivo guardado
    """
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Preparar datos
    T0_values = param_grid['T0']
    alpha_values = param_grid['alpha']
    gap_matrix = np.array(param_grid['gaps']).T  # Transponer para T0 (filas) × alpha (cols)
    
    # Heatmap
    im = ax.imshow(gap_matrix, cmap='RdYlGn_r', aspect='auto', 
                   vmin=gap_matrix.min(), vmax=gap_matrix.max())
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Average Gap (%)', fontsize=12, fontweight='bold')
    
    # Configurar ejes
    ax.set_xticks(np.arange(len(alpha_values)))
    ax.set_yticks(np.arange(len(T0_values)))
    ax.set_xticklabels(alpha_values)
    ax.set_yticklabels(T0_values)
    
    ax.set_xlabel('Alpha (α)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Initial Temperature (T₀)', fontsize=13, fontweight='bold')
    ax.set_title('Parameter Sensitivity Heatmap', fontsize=15, fontweight='bold')
    
    # Anotaciones en celdas
    for i in range(len(T0_values)):
        for j in range(len(alpha_values)):
            text = ax.text(j, i, f'{gap_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    # Marcar mejor combinación
    min_idx = np.unravel_index(gap_matrix.argmin(), gap_matrix.shape)
    rect = plt.Rectangle((min_idx[1] - 0.5, min_idx[0] - 0.5), 1, 1,
                         fill=False, edgecolor='blue', linewidth=3)
    ax.add_patch(rect)
    
    # Anotación
    ax.text(0.02, 0.98, f'Best: T₀={T0_values[min_idx[0]]}, α={alpha_values[min_idx[1]]}\n'
                        f'Gap: {gap_matrix[min_idx]:.2f}%', 
           transform=ax.transAxes, fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

---

## **FASE 6: Temperatura vs Acceptance Rate** (PRIORIDAD ALTA)

### Método: `plot_temperature_acceptance_relationship()`

**Entrada**:
```python
temp_log = pd.read_csv("tracking_temperature.csv")
# Columnas: temperature_level, temperature, acceptance_rate, iterations
```

**Output**: Scatter plot con línea de tendencia

**Implementación**:

```python
def plot_temperature_acceptance_relationship(self,
                                            temp_log: pd.DataFrame,
                                            filename: str = "temp_acceptance.png") -> str:
    """
    Relación Temperatura vs Tasa de Aceptación
    
    Muestra cómo la temperatura afecta la probabilidad de aceptar
    movimientos empeorados.
    
    Args:
        temp_log: DataFrame de tracking_temperature.csv
        filename: Nombre del archivo
    
    Returns:
        Path al archivo guardado
    """
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    temperatures = temp_log['temperature'].values
    acceptance_rates = temp_log['acceptance_rate'].values
    
    # Scatter plot (tamaño proporcional a iteraciones)
    iterations = temp_log['iterations'].values
    scatter = ax.scatter(temperatures, acceptance_rates, 
                        s=iterations * 0.5,
                        alpha=0.6, c=temperatures, cmap='coolwarm',
                        edgecolors='black', linewidth=0.5)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Temperature', fontsize=11, fontweight='bold')
    
    # Línea de tendencia (regresión polinómica)
    from numpy.polynomial import Polynomial
    
    # Usar log(T) para mejor ajuste
    log_temps = np.log10(temperatures + 1e-10)  # Evitar log(0)
    p = Polynomial.fit(log_temps, acceptance_rates, deg=3)
    
    # Generar curva suave
    log_temps_smooth = np.linspace(log_temps.min(), log_temps.max(), 100)
    temps_smooth = 10 ** log_temps_smooth
    rates_smooth = p(log_temps_smooth)
    
    ax.plot(temps_smooth, rates_smooth, 
           'r--', linewidth=2, label='Trend (polynomial fit)', alpha=0.8)
    
    ax.set_xlabel('Temperature', fontsize=13, fontweight='bold')
    ax.set_ylabel('Acceptance Rate', fontsize=13, fontweight='bold')
    ax.set_title('Temperature vs Acceptance Rate', fontsize=15, fontweight='bold')
    ax.set_xscale('log')
    ax.set_ylim(0, 1)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, which='both')
    
    # Anotaciones de fases
    ax.axhspan(0.7, 1.0, alpha=0.05, color='blue')
    ax.text(temperatures.max() * 0.8, 0.85, 'Exploration Phase', 
           fontsize=10, style='italic', color='blue')
    
    ax.axhspan(0.0, 0.3, alpha=0.05, color='red')
    ax.text(temperatures.max() * 0.8, 0.15, 'Exploitation Phase', 
           fontsize=10, style='italic', color='red')
    
    # Anotación
    ax.text(0.02, 0.98, 'Bubble size = iterations at this temperature', 
           transform=ax.transAxes, fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Guardar
    output_path = Path(self.output_dir) / filename
    plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

---

## 🔗 Integración con Sistema Existente

### Modificaciones en `sa_core.py`

**Habilitar tracking automático**:

```python
# En sa_core.py, método optimize()

def optimize(self, initial_solution, verbose=False, enable_tracking=False, 
             output_dir=None):
    """
    Args:
        enable_tracking: Si True, activa tracking completo
        output_dir: Carpeta para guardar tracking logs
    """
    
    if enable_tracking:
        from experimentation.tracking import ExecutionTracker, TrackingConfig
        
        config = TrackingConfig(level="full")
        tracker = ExecutionTracker(config)
        
        # Iniciar tracking
        tracker.start_tracking(
            instance_info={'name': self.problem.name, 
                          'optimal': self.problem.optimal_value},
            algorithm_info={'T0': self.T0, 'alpha': self.alpha},
            seed=self.rng.bit_generator.state['state']['state']
        )
        
        self.set_tracking(tracker, self.problem.optimal_value)
```

### Script de Uso Completo

**Nuevo archivo**: `scripts/demo_sa_visualizations.py`

```python
"""
Demo completo de visualizaciones SA
"""

from pathlib import Path
from experimentation.sa_visualizations import SAVisualizer
from experimentation.tracking import ExecutionTracker, TrackingConfig
from metaheuristic.sa_core import SimulatedAnnealing
from data.loader import DatasetLoader
import json
import pandas as pd

# 1. Ejecutar SA con tracking
loader = DatasetLoader("datasets")
instances = loader.load_folder("low_dimensional")
f1 = [inst for inst in instances if "f1" in inst.name][0]

sa = SimulatedAnnealing(f1, T0=100, alpha=0.95, seed=42)
initial = KnapsackSolution.empty(f1.n, f1)

# Habilitar tracking
best = sa.optimize(initial, verbose=True, enable_tracking=True, 
                  output_dir="output/f1_visualization")

# 2. Crear visualizador
visualizer = SAVisualizer(output_dir="output/f1_plots")

# 3. Cargar datos de tracking
output_path = Path("output/f1_visualization")
convergence = json.load(open(output_path / "convergence.json"))
metadata = json.load(open(output_path / "metadata.json"))
acceptance_log = pd.read_csv(output_path / "tracking_acceptance.csv")
temp_log = pd.read_csv(output_path / "tracking_temperature.csv")
full_log = pd.read_csv(output_path / "tracking_full.csv")

# 4. Generar todas las visualizaciones
print("Generando visualizaciones...")

# Dashboard principal
visualizer.plot_convergence_dashboard(convergence, metadata)
print("✅ Dashboard generado")

# Análisis de aceptación
visualizer.plot_acceptance_analysis(acceptance_log)
print("✅ Análisis de aceptación generado")

# Landscape
visualizer.plot_landscape_exploration(full_log, metadata)
print("✅ Landscape generado")

# Temperatura vs Aceptación
visualizer.plot_temperature_acceptance_relationship(temp_log)
print("✅ Temperatura vs Aceptación generado")

print(f"\n✅ Todas las visualizaciones en: output/f1_plots/")
```

---

## 🧪 Plan de Pruebas

### Test Suite: `tests/test_sa_visualizations.py`

```python
import pytest
from experimentation.sa_visualizations import SAVisualizer
from pathlib import Path
import json
import pandas as pd

@pytest.fixture
def visualizer():
    return SAVisualizer(output_dir="tests/output/viz")

@pytest.fixture
def mock_tracking_data():
    return {
        'iterations': list(range(1000)),
        'best_values': [100 + i * 0.1 for i in range(1000)],
        'temperatures': [100 * 0.95**i for i in range(1000)],
        'gaps': [10 - i * 0.01 for i in range(1000)],
        'acceptance_windows': {
            'window_100': [0.5] * 1000
        },
        'improvement_markers': [0, 50, 100, 200]
    }

@pytest.fixture
def mock_metadata():
    return {
        'instance_name': 'test_instance',
        'optimal': 200,
        'T0': 100,
        'alpha': 0.95,
        'elapsed_time': 1.5
    }

def test_convergence_dashboard(visualizer, mock_tracking_data, mock_metadata):
    """Test dashboard generation"""
    path = visualizer.plot_convergence_dashboard(
        mock_tracking_data, mock_metadata
    )
    
    assert Path(path).exists()
    assert Path(path).suffix == '.png'

def test_acceptance_analysis(visualizer):
    """Test acceptance analysis"""
    # Mock data
    df = pd.DataFrame({
        'iteration': range(100),
        'temperature': [100 * 0.95**i for i in range(100)],
        'delta_E': np.random.randn(100) * 10,
        'acceptance_prob': np.random.rand(100),
        'accepted': np.random.choice([True, False], 100),
        'move_type': np.random.choice(['improving', 'worsening', 'neutral'], 100),
        'improvement': np.random.choice([True, False], 100)
    })
    
    path = visualizer.plot_acceptance_analysis(df)
    
    assert Path(path).exists()

# ... más tests
```

---

## 📅 Timeline de Implementación

### Semana 1: Infraestructura
- Día 1-2: Crear `plotter_utils.py`
- Día 3-4: Crear clase `SAVisualizer` base
- Día 5: Setup de tests

### Semana 2: Visualizaciones Core (Prioridad Alta)
- Día 1-2: `plot_convergence_dashboard()`
- Día 3-4: `plot_acceptance_analysis()`
- Día 5: `plot_temperature_acceptance_relationship()`

### Semana 3: Visualizaciones Avanzadas
- Día 1-2: `plot_landscape_exploration()`
- Día 3-4: `plot_performance_profiles()`
- Día 5: Integración con `sa_core.py`

### Semana 4: Parámetros y Finalización
- Día 1-2: `plot_parameter_sensitivity()`
- Día 3: Script `demo_sa_visualizations.py`
- Día 4-5: Tests y documentación

---

## 📚 Documentación Adicional

### Docstrings Completos

Cada método debe incluir:
```python
def plot_method(self, data, metadata, **kwargs):
    """
    Descripción breve en una línea.
    
    Descripción detallada de qué hace la visualización,
    qué insights provee, y cuándo usarla.
    
    Args:
        data: Descripción del formato esperado
        metadata: Información adicional
        **kwargs: Parámetros opcionales
    
    Returns:
        str: Path al archivo generado
    
    Raises:
        ValueError: Si los datos están incompletos
        FileNotFoundError: Si output_dir no existe
    
    Examples:
        >>> visualizer = SAVisualizer()
        >>> path = visualizer.plot_method(data, metadata)
        >>> print(f"Saved to: {path}")
    
    Notes:
        - Requiere matplotlib >= 3.4.0
        - Los datos deben tener al menos 100 puntos
    
    References:
        - Kirkpatrick et al. (1983)
        - Dolan & Moré (2002) para performance profiles
    """
```

---

## ✅ Checklist de Implementación

### Fase 1: Dashboard
- [ ] Crear `experimentation/plotter_utils.py`
- [ ] Crear `experimentation/sa_visualizations.py`
- [ ] Implementar clase `SAVisualizer.__init__()`
- [ ] Implementar `plot_convergence_dashboard()`
- [ ] Crear test `test_convergence_dashboard()`
- [ ] Documentar con ejemplos
- [ ] Validar con datos reales de f1

### Fase 2: Aceptación
- [ ] Implementar `plot_acceptance_analysis()`
- [ ] Crear test `test_acceptance_analysis()`
- [ ] Validar distribución de ΔE
- [ ] Validar probabilidad calculada vs observada

### Fase 3: Landscape
- [ ] Implementar `plot_landscape_exploration()`
- [ ] Crear test `test_landscape_exploration()`
- [ ] Validar con diferentes instancias

### Fase 4: Performance
- [ ] Implementar `plot_performance_profiles()`
- [ ] Crear test con múltiples algoritmos
- [ ] Validar cálculo de ratios

### Fase 5: Parámetros
- [ ] Implementar `plot_parameter_sensitivity()`
- [ ] Crear test con grid search mock
- [ ] Validar heatmap y anotaciones

### Fase 6: Temperatura
- [ ] Implementar `plot_temperature_acceptance_relationship()`
- [ ] Crear test con datos de tracking
- [ ] Validar ajuste polinómico

### Integración
- [ ] Modificar `sa_core.optimize()` para soportar tracking
- [ ] Crear `scripts/demo_sa_visualizations.py`
- [ ] Ejecutar demo completo end-to-end
- [ ] Actualizar `TRACKING_LOGS.md` con ejemplos de visualizaciones
- [ ] Crear tutorial en `docs/SA_VISUALIZATIONS.md`

---

## 🎯 Criterios de Éxito

1. **Funcionalidad**:
   - ✅ Todas las visualizaciones se generan sin errores
   - ✅ Archivos PNG guardados en output_dir
   - ✅ Datos correctamente procesados y mostrados

2. **Calidad**:
   - ✅ Gráficas profesionales (DPI 300)
   - ✅ Etiquetas claras y legibles
   - ✅ Colores consistentes y accesibles
   - ✅ Leyendas informativas

3. **Performance**:
   - ✅ Dashboard generado en < 2 segundos
   - ✅ Soporta datasets con 10,000+ iteraciones
   - ✅ Memoria eficiente (< 500 MB)

4. **Usabilidad**:
   - ✅ API simple y consistente
   - ✅ Parámetros con defaults sensibles
   - ✅ Mensajes de error claros
   - ✅ Documentación completa

5. **Testing**:
   - ✅ Coverage > 80%
   - ✅ Tests unitarios para cada método
   - ✅ Tests de integración
   - ✅ Validación con datos reales

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0  
**Estado**: Listo para implementación
