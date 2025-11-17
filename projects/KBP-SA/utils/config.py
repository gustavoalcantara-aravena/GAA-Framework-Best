"""
Configuration Manager - KBP-SA
Gestión centralizada de configuración
"""

from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigManager:
    """
    Gestor de configuración del proyecto
    
    Carga desde config.yaml y permite acceso estructurado
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Inicializa gestor de configuración
        
        Args:
            config_path: Ruta al archivo config.yaml
        """
        if config_path is None:
            # Buscar config.yaml en directorio del proyecto
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde YAML"""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Configuración por defecto"""
        return {
            'problem': {'type': 'knapsack'},
            'metaheuristic': {
                'name': 'SA',
                'parameters': {
                    'T0': 100.0,
                    'alpha': 0.95,
                    'iterations_per_temp': 100,
                    'T_min': 0.01
                }
            },
            'datasets': {'base_dir': './datasets'},
            'output': {'base_dir': './output'}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene valor de configuración con notación de punto"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Acceso directo con []"""
        return self.config[key]
    
    def __repr__(self) -> str:
        return f"ConfigManager(config_path='{self.config_path}')"
