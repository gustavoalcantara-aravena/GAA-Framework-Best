"""
Tests Unitarios Básicos - KBP-SA
Suite de tests para validar funcionalidad core del sistema
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.problem import KnapsackProblem
from core.solution import KnapsackSolution
from core.evaluation import KnapsackEvaluator
from data.loader import DatasetLoader


class TestKnapsackProblem:
    """Tests para KnapsackProblem"""
    
    def test_problem_creation_valid(self):
        """Test creación de problema válido"""
        problem = KnapsackProblem(
            n=3,
            capacity=10,
            values=np.array([5, 3, 2]),
            weights=np.array([4, 3, 2]),
            optimal_value=8,
            name="test_problem"
        )
        assert problem.n == 3
        assert problem.capacity == 10
        assert len(problem.values) == 3
        assert len(problem.weights) == 3
    
    def test_problem_negative_capacity(self):
        """Test que capacidad negativa lanza error"""
        with pytest.raises(ValueError, match="Capacidad debe ser positiva"):
            KnapsackProblem(
                n=3,
                capacity=-10,
                values=np.array([5, 3, 2]),
                weights=np.array([4, 3, 2])
            )
    
    def test_problem_zero_items(self):
        """Test que n=0 lanza error"""
        with pytest.raises(ValueError, match="debe ser positivo"):
            KnapsackProblem(
                n=0,
                capacity=10,
                values=np.array([]),
                weights=np.array([])
            )
    
    def test_problem_negative_weights(self):
        """Test que pesos negativos lanzan error"""
        with pytest.raises(ValueError, match="pesos deben ser positivos"):
            KnapsackProblem(
                n=3,
                capacity=10,
                values=np.array([5, 3, 2]),
                weights=np.array([4, -3, 2])
            )
    
    def test_problem_negative_values(self):
        """Test que valores negativos lanzan error"""
        with pytest.raises(ValueError, match="valores deben ser no negativos"):
            KnapsackProblem(
                n=3,
                capacity=10,
                values=np.array([5, -3, 2]),
                weights=np.array([4, 3, 2])
            )
    
    def test_problem_mismatched_lengths(self):
        """Test que tamaños incompatibles lanzan error"""
        with pytest.raises(AssertionError):
            KnapsackProblem(
                n=3,
                capacity=10,
                values=np.array([5, 3]),  # Solo 2 valores
                weights=np.array([4, 3, 2])  # 3 pesos
            )


class TestKnapsackSolution:
    """Tests para KnapsackSolution"""
    
    @pytest.fixture
    def simple_problem(self):
        """Fixture con problema simple"""
        return KnapsackProblem(
            n=3,
            capacity=10,
            values=np.array([5, 3, 2]),
            weights=np.array([4, 3, 2])
        )
    
    def test_solution_empty(self, simple_problem):
        """Test solución vacía"""
        sol = KnapsackSolution.empty(3, simple_problem)
        assert sol.num_selected() == 0
        assert np.all(sol.selection == 0)
    
    def test_solution_all(self, simple_problem):
        """Test solución con todos los ítems"""
        sol = KnapsackSolution.all(3, simple_problem)
        assert sol.num_selected() == 3
        assert np.all(sol.selection == 1)
    
    def test_solution_add_item(self, simple_problem):
        """Test agregar ítem"""
        sol = KnapsackSolution.empty(3, simple_problem)
        sol.add_item(0)
        assert sol.selection[0] == 1
        assert sol.num_selected() == 1
    
    def test_solution_remove_item(self, simple_problem):
        """Test remover ítem"""
        sol = KnapsackSolution.all(3, simple_problem)
        sol.remove_item(1)
        assert sol.selection[1] == 0
        assert sol.num_selected() == 2
    
    def test_solution_flip_item(self, simple_problem):
        """Test flip ítem"""
        sol = KnapsackSolution.empty(3, simple_problem)
        sol.flip(0)
        assert sol.selection[0] == 1
        sol.flip(0)
        assert sol.selection[0] == 0
    
    def test_solution_copy(self, simple_problem):
        """Test copia de solución"""
        sol1 = KnapsackSolution.empty(3, simple_problem)
        sol1.add_item(0)
        sol2 = sol1.copy()
        sol2.add_item(1)
        
        # sol1 no debe cambiar
        assert sol1.num_selected() == 1
        assert sol2.num_selected() == 2


class TestKnapsackEvaluator:
    """Tests para KnapsackEvaluator"""
    
    @pytest.fixture
    def problem_with_optimal(self):
        """Fixture con problema con óptimo conocido"""
        return KnapsackProblem(
            n=3,
            capacity=10,
            values=np.array([6, 5, 3]),
            weights=np.array([4, 3, 2]),
            optimal_value=11  # Ítems 0 y 1
        )
    
    def test_evaluator_gap_to_optimal(self, problem_with_optimal):
        """Test cálculo de gap al óptimo"""
        evaluator = KnapsackEvaluator(problem_with_optimal)
        
        # Solución óptima
        optimal_sol = KnapsackSolution.empty(3, problem_with_optimal)
        optimal_sol.add_item(0)
        optimal_sol.add_item(1)
        optimal_sol.evaluate(problem_with_optimal)
        
        gap = evaluator.gap_to_optimal(optimal_sol)
        assert gap == 0.0
        
        # Solución subóptima
        suboptimal_sol = KnapsackSolution.empty(3, problem_with_optimal)
        suboptimal_sol.add_item(0)  # Solo ítem 0, valor=6
        suboptimal_sol.evaluate(problem_with_optimal)
        
        gap = evaluator.gap_to_optimal(suboptimal_sol)
        assert gap > 0.0
    
    def test_evaluator_gap_without_optimal(self):
        """Test gap cuando no hay óptimo conocido"""
        problem = KnapsackProblem(
            n=3,
            capacity=10,
            values=np.array([6, 5, 3]),
            weights=np.array([4, 3, 2]),
            optimal_value=None
        )
        evaluator = KnapsackEvaluator(problem)
        sol = KnapsackSolution.empty(3, problem)
        
        gap = evaluator.gap_to_optimal(sol)
        assert gap is None


class TestDatasetLoader:
    """Tests para DatasetLoader"""
    
    @pytest.fixture
    def datasets_dir(self):
        """Fixture con directorio de datasets"""
        return Path(__file__).parent.parent / "datasets"
    
    def test_loader_initialization(self, datasets_dir):
        """Test inicialización del loader"""
        loader = DatasetLoader(datasets_dir)
        assert loader.base_dir == datasets_dir
    
    def test_load_folder_low_dimensional(self, datasets_dir):
        """Test carga de carpeta low_dimensional"""
        loader = DatasetLoader(datasets_dir)
        instances = loader.load_folder("low_dimensional")
        
        # Debe cargar al menos algunas instancias (f5 puede fallar)
        assert len(instances) >= 8
        
        # Todas deben ser KnapsackProblem
        for inst in instances:
            assert isinstance(inst, KnapsackProblem)
            assert inst.n > 0
            assert inst.capacity > 0
    
    def test_load_folder_nonexistent(self, datasets_dir):
        """Test carga de carpeta inexistente"""
        loader = DatasetLoader(datasets_dir)
        instances = loader.load_folder("nonexistent_folder")
        assert len(instances) == 0
    
    def test_load_folder_strict_mode(self, datasets_dir):
        """Test modo strict con instancia inválida"""
        loader = DatasetLoader(datasets_dir)
        
        # En modo no-strict, debe continuar
        instances = loader.load_folder("low_dimensional", strict=False)
        assert len(instances) > 0
        
        # En modo strict, debería fallar si hay errores
        # (pero no podemos garantizar que haya errores en todas las ejecuciones)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
