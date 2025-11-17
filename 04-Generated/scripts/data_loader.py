"""
Cargador de Datos - Template Base GAA

Este archivo se genera automáticamente desde 06-Datasets/Dataset-Specification.md
Gestiona la carga y validación de instancias del problema.

AUTO-GENERATED - DO NOT EDIT MANUALLY
Edita: 06-Datasets/Dataset-Specification.md
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
import json
import re


class DataLoader:
    """Cargador de datasets para problemas de optimización"""
    
    def __init__(self, dataset_dir: Path, problem_type: str):
        """
        Args:
            dataset_dir: Directorio raíz de datasets
            problem_type: Tipo de problema ('knapsack', 'graph_coloring', etc.)
        """
        self.dataset_dir = Path(dataset_dir)
        self.problem_type = problem_type
        self.parsers = {
            'knapsack': self._parse_knapsack,
            'graph_coloring': self._parse_graph_coloring,
            'vrptw': self._parse_vrptw,
        }
    
    def load_training_set(self) -> List[Dict[str, Any]]:
        """Carga instancias de entrenamiento"""
        return self._load_instances('training')
    
    def load_validation_set(self) -> List[Dict[str, Any]]:
        """Carga instancias de validación"""
        return self._load_instances('validation')
    
    def load_test_set(self) -> List[Dict[str, Any]]:
        """Carga instancias de test"""
        return self._load_instances('test')
    
    def load_benchmark_set(self) -> List[Dict[str, Any]]:
        """Carga instancias benchmark"""
        return self._load_instances('benchmark')
    
    def _load_instances(self, subset: str) -> List[Dict[str, Any]]:
        """
        Carga todas las instancias de un subset
        
        Args:
            subset: 'training', 'validation', 'test', o 'benchmark'
            
        Returns:
            Lista de diccionarios con datos de instancias
        """
        subset_dir = self.dataset_dir / subset
        
        if not subset_dir.exists():
            print(f"⚠️  Directorio {subset_dir} no existe")
            return []
        
        instances = []
        for file_path in subset_dir.glob('*.txt'):
            try:
                instance = self._parse_file(file_path)
                instance['filename'] = file_path.name
                instance['subset'] = subset
                instances.append(instance)
            except Exception as e:
                print(f"Error cargando {file_path.name}: {e}")
        
        print(f"✅ Cargadas {len(instances)} instancias de {subset}")
        return instances
    
    def _parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parsea un archivo de instancia según el tipo de problema
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            Diccionario con datos de la instancia
        """
        if self.problem_type not in self.parsers:
            raise ValueError(f"Parser no disponible para: {self.problem_type}")
        
        return self.parsers[self.problem_type](file_path)
    
    # ========================================================================
    # PARSERS ESPECÍFICOS POR PROBLEMA
    # ========================================================================
    
    def _parse_knapsack(self, file_path: Path) -> Dict[str, Any]:
        """
        Parser para Knapsack Problem
        
        Formato esperado (con valor óptimo):
        optimal_value
        n W
        v_1 w_1
        v_2 w_2
        ...
        v_n w_n
        
        O formato sin valor óptimo:
        n W
        v_1 w_1
        ...
        """
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # Detectar formato: si la primera línea tiene un solo número, es optimal_value
        first_line_parts = lines[0].split()
        
        if len(first_line_parts) == 1:
            # Formato con optimal_value
            optimal_value = float(first_line_parts[0])
            n, capacity = map(int, lines[1].split())
            start_idx = 2
        else:
            # Formato sin optimal_value
            optimal_value = None
            n, capacity = map(int, lines[0].split())
            start_idx = 1
        
        values = []
        weights = []
        
        for i in range(start_idx, start_idx + n):
            if i >= len(lines):
                break
            parts = lines[i].split()
            # Manejar valores decimales (convertir a int)
            values.append(int(float(parts[0])))
            weights.append(int(float(parts[1])))
        
        result = {
            'n': n,
            'capacity': capacity,
            'values': values,
            'weights': weights,
            'problem_type': 'knapsack'
        }
        
        if optimal_value is not None:
            result['optimal_value'] = int(optimal_value)
        
        return result
    
    def _parse_graph_coloring(self, file_path: Path) -> Dict[str, Any]:
        """
        Parser para Graph Coloring Problem
        
        Formato DIMACS (.col):
        p edge <n_vertices> <n_edges>
        e <v1> <v2>
        ...
        
        O formato simplificado:
        n m
        v1 v2
        ...
        """
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('c')]
        
        edges = []
        n_vertices = 0
        n_edges = 0
        
        for line in lines:
            if line.startswith('p edge'):
                # Formato DIMACS
                parts = line.split()
                n_vertices = int(parts[2])
                n_edges = int(parts[3])
            elif line.startswith('e'):
                # Arista en formato DIMACS
                parts = line.split()
                v1, v2 = int(parts[1]), int(parts[2])
                edges.append((v1 - 1, v2 - 1))  # Convertir a 0-indexed
            else:
                # Formato simplificado
                parts = line.split()
                if len(parts) == 2 and n_vertices == 0:
                    n_vertices = int(parts[0])
                    n_edges = int(parts[1])
                elif len(parts) == 2:
                    v1, v2 = int(parts[0]), int(parts[1])
                    edges.append((v1, v2))
        
        return {
            'n_vertices': n_vertices,
            'n_edges': n_edges,
            'edges': edges,
            'problem_type': 'graph_coloring'
        }
    
    def _parse_vrptw(self, file_path: Path) -> Dict[str, Any]:
        """
        Parser para Vehicle Routing Problem with Time Windows
        
        Formato Solomon:
        VEHICLE
        NUMBER     CAPACITY
        <K>        <Q>
        
        CUSTOMER
        CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
        0         40        50         0        0           230        0
        1         45        68         10       0           100        10
        ...
        """
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extraer información de vehículos
        vehicle_match = re.search(r'VEHICLE.*?NUMBER\s+CAPACITY\s+(\d+)\s+(\d+)', content, re.DOTALL)
        if vehicle_match:
            n_vehicles = int(vehicle_match.group(1))
            capacity = int(vehicle_match.group(2))
        else:
            n_vehicles = 10  # Default
            capacity = 200
        
        # Extraer información de clientes
        customer_section = re.search(r'CUSTOMER.*', content, re.DOTALL)
        if customer_section:
            customer_text = customer_section.group(0)
            lines = customer_text.split('\n')[2:]  # Saltar encabezados
            
            customers = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 7:
                        customers.append({
                            'id': int(parts[0]),
                            'x': float(parts[1]),
                            'y': float(parts[2]),
                            'demand': int(parts[3]),
                            'ready_time': int(parts[4]),
                            'due_date': int(parts[5]),
                            'service_time': int(parts[6])
                        })
        
        return {
            'n_vehicles': n_vehicles,
            'capacity': capacity,
            'customers': customers,
            'n_customers': len(customers),
            'problem_type': 'vrptw'
        }
    
    def save_results(self, results: List[Dict[str, Any]], output_path: Path):
        """
        Guarda resultados de experimentos
        
        Args:
            results: Lista de resultados
            output_path: Ruta donde guardar
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Resultados guardados en {output_path}")
    
    def validate_instance(self, instance: Dict[str, Any]) -> bool:
        """
        Valida que una instancia tenga todos los campos requeridos
        
        Args:
            instance: Diccionario con datos de instancia
            
        Returns:
            True si es válida, False en caso contrario
        """
        required_fields = {
            'knapsack': ['n', 'capacity', 'values', 'weights'],
            'graph_coloring': ['n_vertices', 'n_edges', 'edges'],
            'vrptw': ['n_vehicles', 'capacity', 'customers']
        }
        
        prob_type = instance.get('problem_type', self.problem_type)
        
        if prob_type not in required_fields:
            return False
        
        for field in required_fields[prob_type]:
            if field not in instance:
                print(f"⚠️  Campo faltante: {field}")
                return False
        
        return True


if __name__ == "__main__":
    # Ejemplo de uso
    
    # Knapsack
    print("=== KNAPSACK ===")
    loader = DataLoader(
        dataset_dir=Path("../../projects/KBP-SA/datasets"),
        problem_type='knapsack'
    )
    training = loader.load_training_set()
    print(f"Instancias cargadas: {len(training)}")
    
    if training:
        print(f"Primera instancia: {training[0]}")
        print(f"Válida: {loader.validate_instance(training[0])}")
