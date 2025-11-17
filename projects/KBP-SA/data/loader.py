"""
Dataset Loader - KBP-SA
Carga de instancias del problema
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import logging

from core.problem import KnapsackProblem

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Cargador de datasets para KBP
    
    Soporta formato estándar:
    optimal_value
    n W
    v_1 w_1
    ...
    """
    
    def __init__(self, base_dir: Path):
        """
        Inicializa loader
        
        Args:
            base_dir: Directorio base de datasets
        """
        self.base_dir = Path(base_dir)
    
    def load_instance(self, file_path: Path) -> KnapsackProblem:
        """
        Carga una instancia desde archivo
        
        Args:
            file_path: Ruta al archivo
        
        Returns:
            Instancia de KnapsackProblem
        """
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # Detectar formato
        first_parts = lines[0].split()
        
        if len(first_parts) == 1:
            # Formato con optimal_value
            optimal_value = int(float(first_parts[0]))
            n, capacity = map(int, lines[1].split())
            start_idx = 2
        else:
            # Formato sin optimal_value
            optimal_value = None
            n, capacity = map(int, lines[0].split())
            start_idx = 1
        
        # Leer ítems
        values = []
        weights = []
        
        for i in range(start_idx, start_idx + n):
            v, w = map(float, lines[i].split())
            values.append(int(v))
            weights.append(int(w))
        
        return KnapsackProblem(
            n=n,
            capacity=capacity,
            values=np.array(values),
            weights=np.array(weights),
            optimal_value=optimal_value,
            name=file_path.stem
        )
    
    def load_folder(self, folder_name: str, strict: bool = False) -> List[KnapsackProblem]:
        """
        Carga todas las instancias de una carpeta
        
        Args:
            folder_name: Nombre de la carpeta (low_dimensional, large_scale, etc.)
            strict: Si True, lanza excepción en cualquier error. Si False, continúa.
        
        Returns:
            Lista de instancias
        """
        folder_path = self.base_dir / folder_name
        
        if not folder_path.exists():
            logger.warning(f"Carpeta no existe: {folder_path}")
            return []
        
        instances = []
        errors = []
        
        for file_path in sorted(folder_path.glob('*.txt')):
            try:
                instance = self.load_instance(file_path)
                instances.append(instance)
                logger.debug(f"Cargada instancia: {file_path.name}")
            except Exception as e:
                error_msg = f"Error cargando {file_path.name}: {e}"
                logger.error(error_msg)
                errors.append((file_path.name, str(e)))
                print(f"Error cargando {file_path.name}: {e}")
                if strict:
                    raise
        
        if errors:
            logger.warning(f"Se encontraron {len(errors)} errores al cargar {folder_name}")
        
        return instances
    
    def list_available_folders(self) -> List[str]:
        """Lista carpetas disponibles"""
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]
