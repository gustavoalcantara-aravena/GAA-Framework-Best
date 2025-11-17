"""
Tracking System - KBP-SA
Sistema de logging y trackeo de variables durante experimentación
Fase 5 GAA: Monitoreo y análisis de ejecución

Referencias:
- Barr et al. (1995): Experimental methodology
- Eiben & Jelasity (2002): Tracking convergence behavior
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import csv
import time
from datetime import datetime
import numpy as np


class TrackingConfig:
    """Configuración del sistema de tracking"""
    
    MINIMAL = "minimal"
    MODERATE = "moderate"
    FULL = "full"
    
    def __init__(self, 
                 level: str = "moderate",
                 save_summary: bool = True,
                 save_full_log: bool = False,
                 save_temperature_log: bool = True,
                 save_acceptance_log: bool = True,
                 save_convergence: bool = True,
                 sampling_rate: int = 1):
        """
        Args:
            level: Nivel de detalle ('minimal', 'moderate', 'full')
            save_summary: Guardar resumen ejecutivo
            save_full_log: Guardar log completo por iteración
            save_temperature_log: Guardar log por temperatura
            save_acceptance_log: Guardar log de aceptaciones
            save_convergence: Guardar datos de convergencia
            sampling_rate: Frecuencia de muestreo (1 = todas las iteraciones)
        """
        self.level = level
        self.save_summary = save_summary
        self.save_full_log = save_full_log
        self.save_temperature_log = save_temperature_log
        self.save_acceptance_log = save_acceptance_log
        self.save_convergence = save_convergence
        self.sampling_rate = sampling_rate
        
        # Configurar según nivel
        if level == self.MINIMAL:
            self.save_full_log = False
            self.save_temperature_log = False
            self.save_acceptance_log = False
            self.save_convergence = False
        elif level == self.MODERATE:
            self.save_full_log = False
            self.sampling_rate = max(10, sampling_rate)
        elif level == self.FULL:
            self.save_full_log = True
            self.save_temperature_log = True
            self.save_acceptance_log = True
            self.save_convergence = True


class ExecutionTracker:
    """
    Tracker de ejecución de algoritmos
    
    Registra todas las variables de interés durante la optimización
    y las guarda en archivos estructurados.
    """
    
    def __init__(self, config: TrackingConfig = None):
        """
        Args:
            config: Configuración de tracking
        """
        if config is None:
            config = TrackingConfig(level="moderate")
        
        self.config = config
        self.reset()
    
    def reset(self):
        """Reinicia el tracker"""
        # Logs por iteración
        self.iteration_log = []
        
        # Logs por temperatura
        self.temperature_log = []
        
        # Log de aceptaciones
        self.acceptance_log = []
        
        # Historial de convergencia
        self.convergence_data = {
            'iterations': [],
            'best_values': [],
            'temperatures': [],
            'gaps': [],
            'acceptance_windows': {
                'window_50': [],
                'window_100': [],
                'window_200': []
            },
            'improvement_markers': []
        }
        
        # Metadata
        self.metadata = {}
        
        # Estado temporal
        self.current_temp_level = 0
        self.current_temp_iterations = []
        self.start_time = None
    
    def start_tracking(self, instance_info: Dict, algorithm_info: Dict, seed: int):
        """
        Inicia el tracking de una ejecución
        
        Args:
            instance_info: Información de la instancia
            algorithm_info: Información del algoritmo
            seed: Semilla aleatoria
        """
        self.reset()
        self.start_time = time.time()
        
        self.metadata = {
            'experiment': {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'start_time': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            },
            'instance': instance_info,
            'algorithm': algorithm_info,
            'execution': {
                'seed': seed
            },
            'tracking': {
                'level': self.config.level,
                'full_log': self.config.save_full_log,
                'temperature_log': self.config.save_temperature_log,
                'acceptance_log': self.config.save_acceptance_log,
                'sampling_rate': self.config.sampling_rate
            }
        }
    
    def track_iteration(self, iteration: int, data: Dict[str, Any]):
        """
        Registra una iteración
        
        Args:
            iteration: Número de iteración
            data: Diccionario con variables de la iteración
                - temperature: float
                - current_value: int
                - best_value: int
                - current_weight: int
                - best_weight: int
                - is_feasible: bool
                - delta_E: float
                - acceptance_prob: float
                - accepted: bool
                - gap_to_optimal: float (opcional)
        """
        # Muestreo según configuración
        if iteration % self.config.sampling_rate != 0:
            return
        
        elapsed = time.time() - self.start_time if self.start_time else 0.0
        
        # Log completo por iteración
        if self.config.save_full_log:
            self.iteration_log.append({
                'iteration': iteration,
                'temperature': data.get('temperature', 0.0),
                'current_value': data.get('current_value', 0),
                'best_value': data.get('best_value', 0),
                'current_weight': data.get('current_weight', 0),
                'best_weight': data.get('best_weight', 0),
                'is_feasible': data.get('is_feasible', False),
                'delta_E': data.get('delta_E', 0.0),
                'acceptance_prob': data.get('acceptance_prob', 0.0),
                'accepted': data.get('accepted', False),
                'elapsed_time': elapsed,
                'gap_to_optimal': data.get('gap_to_optimal', None)
            })
        
        # Actualizar datos de convergencia
        if self.config.save_convergence:
            self.convergence_data['iterations'].append(iteration)
            self.convergence_data['best_values'].append(data.get('best_value', 0))
            self.convergence_data['temperatures'].append(data.get('temperature', 0.0))
            if data.get('gap_to_optimal') is not None:
                self.convergence_data['gaps'].append(data['gap_to_optimal'])
        
        # Acumular para nivel de temperatura
        if self.config.save_temperature_log:
            self.current_temp_iterations.append(data)
    
    def track_acceptance(self, iteration: int, temperature: float, 
                        delta_E: float, acceptance_prob: float, 
                        accepted: bool, improvement: bool):
        """
        Registra una decisión de aceptación
        
        Args:
            iteration: Número de iteración
            temperature: Temperatura actual
            delta_E: Diferencia de energía
            acceptance_prob: Probabilidad de aceptación
            accepted: ¿Fue aceptado?
            improvement: ¿Resultó en mejora al best?
        """
        if not self.config.save_acceptance_log:
            return
        
        # Determinar tipo de movimiento
        if delta_E <= 0:  # Mejora (delta_E es negativo para mejoras en maximización)
            move_type = "improving"
        elif delta_E == 0:
            move_type = "neutral"
        else:
            move_type = "worsening"
        
        self.acceptance_log.append({
            'iteration': iteration,
            'temperature': temperature,
            'delta_E': delta_E,
            'acceptance_prob': acceptance_prob,
            'accepted': accepted,
            'move_type': move_type,
            'improvement': improvement
        })
    
    def track_temperature_change(self, temp_level: int, old_temp: float, new_temp: float):
        """
        Registra cambio de nivel de temperatura
        
        Args:
            temp_level: Nivel de temperatura
            old_temp: Temperatura anterior
            new_temp: Nueva temperatura
        """
        if not self.config.save_temperature_log or not self.current_temp_iterations:
            return
        
        # Calcular estadísticas del nivel anterior
        values = [d['current_value'] for d in self.current_temp_iterations]
        weights = [d['current_weight'] for d in self.current_temp_iterations]
        acceptances = [d['accepted'] for d in self.current_temp_iterations]
        best_value = max([d['best_value'] for d in self.current_temp_iterations])
        
        improvements = sum(1 for d in self.current_temp_iterations 
                          if d.get('is_improvement', False))
        
        elapsed = time.time() - self.start_time if self.start_time else 0.0
        
        self.temperature_log.append({
            'temperature_level': self.current_temp_level,
            'temperature': old_temp,
            'avg_value': np.mean(values),
            'best_value': best_value,
            'avg_weight': np.mean(weights),
            'acceptance_rate': np.mean(acceptances) if acceptances else 0.0,
            'improvements': improvements,
            'iterations': len(self.current_temp_iterations),
            'elapsed_time': elapsed
        })
        
        # Reiniciar para nuevo nivel
        self.current_temp_level += 1
        self.current_temp_iterations = []
    
    def track_improvement(self, iteration: int):
        """
        Marca una iteración donde hubo mejora
        
        Args:
            iteration: Número de iteración
        """
        if self.config.save_convergence:
            self.convergence_data['improvement_markers'].append(iteration)
    
    def calculate_acceptance_windows(self, acceptance_history: List[int]):
        """
        Calcula ventanas móviles de aceptación
        
        Args:
            acceptance_history: Lista de aceptaciones (1/0)
        """
        if not self.config.save_convergence:
            return
        
        windows = [50, 100, 200]
        for window_size in windows:
            window_rates = []
            for i in range(len(acceptance_history)):
                start = max(0, i - window_size + 1)
                window = acceptance_history[start:i+1]
                if window:
                    rate = sum(window) / len(window)
                    window_rates.append(rate)
                else:
                    window_rates.append(0.0)
            
            self.convergence_data['acceptance_windows'][f'window_{window_size}'] = window_rates
    
    def finalize_tracking(self, final_stats: Dict[str, Any]):
        """
        Finaliza el tracking y prepara resumen
        
        Args:
            final_stats: Estadísticas finales de la ejecución
        """
        end_time = time.time()
        elapsed = end_time - self.start_time if self.start_time else 0.0
        
        self.metadata['execution']['end_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.metadata['execution']['elapsed_time'] = elapsed
        self.metadata['results'] = final_stats
    
    def save(self, output_dir: Path, instance_name: str):
        """
        Guarda todos los logs en disco
        
        Args:
            output_dir: Directorio de salida
            instance_name: Nombre de la instancia
        """
        # Crear directorio si no existe
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Guardar resumen
        if self.config.save_summary:
            summary_path = output_dir / "summary.json"
            with open(summary_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        
        # 2. Guardar log completo por iteración
        if self.config.save_full_log and self.iteration_log:
            full_log_path = output_dir / "tracking_full.csv"
            self._save_csv(full_log_path, self.iteration_log)
        
        # 3. Guardar log por temperatura
        if self.config.save_temperature_log and self.temperature_log:
            temp_log_path = output_dir / "tracking_temperature.csv"
            self._save_csv(temp_log_path, self.temperature_log)
        
        # 4. Guardar log de aceptaciones
        if self.config.save_acceptance_log and self.acceptance_log:
            acc_log_path = output_dir / "tracking_acceptance.csv"
            self._save_csv(acc_log_path, self.acceptance_log)
        
        # 5. Guardar datos de convergencia
        if self.config.save_convergence:
            conv_path = output_dir / "convergence.json"
            with open(conv_path, 'w') as f:
                json.dump(self.convergence_data, f, indent=2)
        
        # 6. Guardar metadata
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _save_csv(self, path: Path, data: List[Dict]):
        """
        Guarda lista de diccionarios como CSV
        
        Args:
            path: Ruta del archivo
            data: Lista de diccionarios
        """
        if not data:
            return
        
        fieldnames = list(data[0].keys())
        
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen del tracking
        
        Returns:
            Diccionario con resumen
        """
        return {
            'total_iterations_logged': len(self.iteration_log),
            'temperature_levels': len(self.temperature_log),
            'acceptance_decisions': len(self.acceptance_log),
            'improvements': len(self.convergence_data.get('improvement_markers', [])),
            'tracking_config': {
                'level': self.config.level,
                'sampling_rate': self.config.sampling_rate
            }
        }
