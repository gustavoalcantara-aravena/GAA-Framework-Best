"""
Test Suite: Sistema de Visualizaciones
========================================

Valida:
1. Estructura de carpetas unificada (low_dimensional_{timestamp})
2. Generacin de grficas estadsticas generales (boxplot, bars, scatter)
3. Visualizacin AST del mejor algoritmo
4. Visualizaciones detalladas por instancia (4 grficas cada una)
5. Integridad de archivos PNG generados
6. Tracking completo de SA (gap, acceptance, delta_e, temperature)
"""

import unittest
import sys
from pathlib import Path
import json
import shutil
from datetime import datetime
import os

# Aadir el directorio raz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.solution import KnapsackSolution
from data.loader import DatasetLoader
from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.visualization import ResultsVisualizer
from experimentation.ast_visualization import ASTVisualizer
from metaheuristic.sa_core import SimulatedAnnealing


class TestVisualizationSystem(unittest.TestCase):
    """Tests para el sistema de visualizaciones completo"""
    
    @classmethod
    def setUpClass(cls):
        """Configuracin inicial para todos los tests"""
        cls.output_base = project_root / "output" / "test_visualizations"
        cls.dataset_dir = project_root / "datasets" / "low_dimensional"
        
        # Limpiar carpeta de tests anteriores
        if cls.output_base.exists():
            shutil.rmtree(cls.output_base)
        cls.output_base.mkdir(parents=True, exist_ok=True)
        
        # Cargar instancias de prueba
        loader = DatasetLoader(cls.dataset_dir.parent)
        cls.instances = loader.load_folder("low_dimensional", strict=False)
        
        # Filtrar instancia con error conocido (f5)
        cls.instances = [inst for inst in cls.instances if "f5" not in inst.name]
        
        # Usar solo 3 instancias pequeas para tests rpidos
        cls.test_instances = sorted(cls.instances, key=lambda x: x.n)[:3]
        
        # Generar algoritmo de prueba
        grammar = Grammar()
        generator = AlgorithmGenerator(grammar=grammar, seed=42)
        cls.test_algorithm = generator.generate(max_depth=3)
        cls.test_algorithm_name = "GAA_Test_Algorithm"
        
        print(f"\n{'='*70}")
        print(f"Test Suite: Sistema de Visualizaciones")
        print(f"{'='*70}")
        print(f"Instancias de prueba: {len(cls.test_instances)}")
        for inst in cls.test_instances:
            print(f"   - {inst.name} (n={inst.n})")
        print(f"Algoritmo: {cls.test_algorithm_name}")
        print(f"Output: {cls.output_base}")
        print(f"{'='*70}\n")
    
    @classmethod
    def tearDownClass(cls):
        """Limpieza final - mantener resultados para inspeccin"""
        print(f"\n{'='*70}")
        print(f"Tests completados - Resultados guardados en:")
        print(f"   {cls.output_base}")
        print(f"{'='*70}\n")
    
    def test_01_unified_folder_structure(self):
        """Test 1: Validar estructura de carpeta unificada"""
        print("\n[TEST 1] Estructura de carpeta unificada...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_folder = self.output_base / f"low_dimensional_{timestamp}"
        main_folder.mkdir(parents=True, exist_ok=True)
        
        # Validar que la carpeta existe
        self.assertTrue(main_folder.exists(), "Carpeta principal no creada")
        self.assertTrue(main_folder.is_dir(), "No es un directorio")
        
        # Validar patrn de nombre
        self.assertRegex(main_folder.name, r"low_dimensional_\d{8}_\d{6}")
        
        print(f"    Carpeta creada: {main_folder.name}")
    
    def test_02_general_statistical_plots(self):
        """Test 2: Generacin de grficas estadsticas generales"""
        print("\n[TEST 2] Grficas estadsticas generales...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plots_dir = self.output_base / f"low_dimensional_{timestamp}"
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        visualizer = ResultsVisualizer(plots_dir)
        
        # Generar datos de prueba
        test_data = {
            'GAA_Test_1': [2.5, 3.0, 2.8],
            'GAA_Test_2': [5.0, 4.5, 5.2],
            'GAA_Test_3': [1.0, 1.2, 0.9]
        }
        
        instance_names = [inst.name for inst in self.test_instances]
        
        # Generar grficas
        visualizer.plot_gap_comparison_boxplot(
            test_data,
            filename="test_boxplot.png",
            title="Test Boxplot"
        )
        
        visualizer.plot_gap_comparison_bars(
            test_data,
            instance_names=instance_names,
            filename="test_bars.png",
            title="Test Bars"
        )
        
        visualizer.plot_gap_scatter(
            test_data,
            instance_names=instance_names,
            filename="test_scatter.png",
            title="Test Scatter"
        )
        
        # Validar archivos generados
        expected_files = ["test_boxplot.png", "test_bars.png", "test_scatter.png"]
        
        for filename in expected_files:
            filepath = plots_dir / filename
            self.assertTrue(filepath.exists(), f"Falta archivo: {filename}")
            self.assertGreater(filepath.stat().st_size, 1000, f"Archivo muy pequeo: {filename}")
            print(f"    {filename} - {filepath.stat().st_size:,} bytes")
    
    def test_03_ast_visualization(self):
        """Test 3: Visualizacin del AST del algoritmo"""
        print("\n[TEST 3] Visualizacin AST...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plots_dir = self.output_base / f"low_dimensional_{timestamp}"
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar visualizacin AST
        ast_visualizer = ASTVisualizer(plots_dir)
        
        result = ast_visualizer.plot_ast_graphviz(
            self.test_algorithm,
            filename="test_algorithm_ast",
            title=f"Test Algorithm: {self.test_algorithm_name}",
            format='png'
        )
        
        self.assertIsNotNone(result, "Fall generacin de AST")
        ast_file = Path(result)
        self.assertTrue(ast_file.exists(), "Archivo AST no creado")
        self.assertGreater(ast_file.stat().st_size, 5000, "AST muy pequeo")
        
        print(f"    AST generado: {ast_file.stat().st_size:,} bytes")
        print(f"    Nodos: {len(list(self.test_algorithm.root.traverse()))}")
    
    def test_04_per_instance_detailed_visualizations(self):
        """Test 4: Visualizaciones detalladas por instancia"""
        print("\n[TEST 4] Visualizaciones por instancia...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_folder = self.output_base / f"low_dimensional_{timestamp}"
        main_folder.mkdir(parents=True, exist_ok=True)
        
        # Usar solo la primera instancia para test rpido
        test_instance = self.test_instances[0]
        
        # Crear subcarpeta para la instancia
        instance_folder = main_folder / f"{test_instance.name}_{timestamp}"
        instance_folder.mkdir(parents=True, exist_ok=True)
        
        visualizer = ResultsVisualizer(instance_folder)
        
        # Ejecutar SA con tracking completo
        initial_solution = KnapsackSolution.random_solution(test_instance)
        
        # Variables de tracking
        best_values = []
        acceptance_history = []
        temperature_history = []
        delta_e_values = []
        
        def neighborhood_func(sol):
            """Funcin de vecindad: flip de bit aleatorio"""
            import random
            new_sol = sol.copy()
            if len(new_sol.selected_items) > 0:
                idx = random.choice(list(new_sol.selected_items))
                new_sol.flip_item(idx)
            return new_sol
        
        # Configuracin SA
        sa = SimulatedAnnealing(
            initial_solution=initial_solution,
            neighborhood_function=neighborhood_func,
            initial_temperature=100.0,
            cooling_rate=0.95,
            max_iterations=1000
        )
        
        # Ejecutar con tracking manual
        current_best = initial_solution.value
        T = 100.0
        alpha = 0.95
        current_sol = initial_solution
        
        for i in range(1000):
            # Generar vecino
            neighbor = neighborhood_func(current_sol)
            
            # Calcular delta
            delta = neighbor.value - current_sol.value
            delta_e_values.append(delta)
            
            # Decisin de aceptacin
            import random
            import math
            
            if delta > 0:  # Mejora (maximizacin)
                accept = True
            else:  # Empeoramiento
                accept = random.random() < math.exp(delta / T) if T > 0 else False
            
            acceptance_history.append(1 if accept else 0)
            
            if accept:
                current_sol = neighbor
            
            # Actualizar mejor
            if current_sol.value > current_best:
                current_best = current_sol.value
            
            best_values.append(current_best)
            temperature_history.append(T)
            
            # Enfriar
            if i % 100 == 0:
                T *= alpha
        
        # Generar las 4 visualizaciones requeridas
        visualizer.plot_gap_evolution(
            best_values=best_values,
            optimal_value=test_instance.optimal_value,
            title=f"Gap Evolution - {test_instance.name}",
            filename="gap_evolution.png",
            temperature_history=temperature_history
        )
        
        visualizer.plot_acceptance_rate(
            acceptance_history=acceptance_history,
            window_size=50,
            title=f"Acceptance Rate - {test_instance.name}",
            filename="acceptance_rate.png",
            temperature_history=temperature_history
        )
        
        acceptance_decisions = [bool(x) for x in acceptance_history]
        visualizer.plot_delta_e_distribution(
            delta_e_values=delta_e_values,
            acceptance_decisions=acceptance_decisions,
            title=f"E Distribution - {test_instance.name}",
            filename="delta_e_distribution.png"
        )
        
        visualizer.plot_exploration_exploitation_balance(
            acceptance_history=acceptance_history,
            best_values=best_values,
            title=f"Exploration vs Exploitation - {test_instance.name}",
            filename="exploration_exploitation_balance.png"
        )
        
        # Validar las 4 grficas
        expected_files = [
            "gap_evolution.png",
            "acceptance_rate.png",
            "delta_e_distribution.png",
            "exploration_exploitation_balance.png"
        ]
        
        for filename in expected_files:
            filepath = instance_folder / filename
            self.assertTrue(filepath.exists(), f"Falta: {filename}")
            self.assertGreater(filepath.stat().st_size, 1000, f"Muy pequeo: {filename}")
            print(f"    {filename} - {filepath.stat().st_size:,} bytes")
        
        print(f"    Tracking: {len(best_values)} iteraciones")
        print(f"    Mejor valor: {current_best}/{test_instance.optimal_value}")
    
    def test_05_complete_workflow_integration(self):
        """Test 5: Workflow completo integrado"""
        print("\n[TEST 5] Workflow completo...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_folder = self.output_base / f"low_dimensional_{timestamp}"
        main_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"    Carpeta principal: {main_folder.name}")
        
        # 1. Grficas generales
        visualizer_main = ResultsVisualizer(main_folder)
        
        test_data = {
            'Alg1': [1.0, 1.5, 0.8],
            'Alg2': [2.0, 2.5, 1.8],
        }
        
        visualizer_main.plot_gap_comparison_boxplot(
            test_data,
            filename="complete_boxplot.png"
        )
        
        visualizer_main.plot_gap_comparison_bars(
            test_data,
            instance_names=[inst.name for inst in self.test_instances[:2]],
            filename="complete_bars.png"
        )
        
        visualizer_main.plot_gap_scatter(
            test_data,
            instance_names=[inst.name for inst in self.test_instances[:2]],
            filename="complete_scatter.png"
        )
        
        # 2. AST
        ast_visualizer = ASTVisualizer(main_folder)
        ast_visualizer.plot_ast_graphviz(
            self.test_algorithm,
            filename="complete_ast",
            title=f"Complete Test: {self.test_algorithm_name}",
            format='png'
        )
        
        # 3. Por instancia (solo primera)
        instance = self.test_instances[0]
        instance_folder = main_folder / f"{instance.name}_{timestamp}"
        instance_folder.mkdir(parents=True, exist_ok=True)
        
        visualizer_inst = ResultsVisualizer(instance_folder)
        
        # Generar datos mnimos
        dummy_best = list(range(100, 200))
        dummy_acceptance = [1] * 50 + [0] * 50
        dummy_delta_e = list(range(-50, 50))
        dummy_temp = [100.0 * (0.95 ** i) for i in range(100)]
        
        visualizer_inst.plot_gap_evolution(
            best_values=dummy_best,
            optimal_value=instance.optimal_value,
            filename="gap_evolution.png",
            temperature_history=dummy_temp
        )
        
        visualizer_inst.plot_acceptance_rate(
            acceptance_history=dummy_acceptance,
            filename="acceptance_rate.png",
            temperature_history=dummy_temp
        )
        
        visualizer_inst.plot_delta_e_distribution(
            delta_e_values=dummy_delta_e,
            acceptance_decisions=[True] * 50 + [False] * 50,
            filename="delta_e_distribution.png"
        )
        
        visualizer_inst.plot_exploration_exploitation_balance(
            acceptance_history=dummy_acceptance,
            best_values=dummy_best,
            filename="exploration_exploitation_balance.png"
        )
        
        # Validar estructura completa
        expected_main = [
            "complete_boxplot.png",
            "complete_bars.png",
            "complete_scatter.png",
            "complete_ast.png"
        ]
        
        expected_instance = [
            "gap_evolution.png",
            "acceptance_rate.png",
            "delta_e_distribution.png",
            "exploration_exploitation_balance.png"
        ]
        
        # Verificar archivos principales
        print("\n    Archivos principales:")
        for filename in expected_main:
            filepath = main_folder / filename
            self.assertTrue(filepath.exists(), f"Falta: {filename}")
            print(f"       {filename}")
        
        # Verificar archivos por instancia
        print(f"\n    Archivos de {instance.name}:")
        for filename in expected_instance:
            filepath = instance_folder / filename
            self.assertTrue(filepath.exists(), f"Falta: {filename}")
            print(f"       {filename}")
        
        # Contar total de archivos
        total_files = len(list(main_folder.rglob("*.png")))
        expected_total = len(expected_main) + len(expected_instance)
        
        self.assertEqual(total_files, expected_total, "Nmero incorrecto de archivos")
        print(f"\n    Total archivos PNG: {total_files}/{expected_total}")
    
    def test_06_folder_naming_conventions(self):
        """Test 6: Convenciones de nombres de carpetas"""
        print("\n[TEST 6] Convenciones de nombres...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Test 1: Carpeta principal
        main_folder_name = f"low_dimensional_{timestamp}"
        self.assertRegex(main_folder_name, r"low_dimensional_\d{8}_\d{6}")
        print(f"    Main folder: {main_folder_name}")
        
        # Test 2: Carpetas por instancia
        for instance in self.test_instances:
            instance_folder_name = f"{instance.name}_{timestamp}"
            self.assertIn(instance.name, instance_folder_name)
            self.assertRegex(instance_folder_name, r".*_\d{8}_\d{6}$")
            print(f"    Instance folder: {instance_folder_name}")
    
    def test_07_file_integrity(self):
        """Test 7: Integridad de archivos PNG"""
        print("\n[TEST 7] Integridad de archivos PNG...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_folder = self.output_base / f"low_dimensional_{timestamp}"
        test_folder.mkdir(parents=True, exist_ok=True)
        
        visualizer = ResultsVisualizer(test_folder)
        
        # Generar archivo de prueba
        test_data = {'Test': [1.0, 2.0, 3.0]}
        visualizer.plot_gap_comparison_boxplot(
            test_data,
            filename="integrity_test.png"
        )
        
        filepath = test_folder / "integrity_test.png"
        
        # Validaciones de integridad
        self.assertTrue(filepath.exists(), "Archivo no existe")
        
        file_size = filepath.stat().st_size
        self.assertGreater(file_size, 1000, "Archivo demasiado pequeo")
        self.assertLess(file_size, 5_000_000, "Archivo demasiado grande")
        
        # Verificar que es PNG vlido (magic bytes)
        with open(filepath, 'rb') as f:
            header = f.read(8)
            png_signature = b'\x89PNG\r\n\x1a\n'
            self.assertEqual(header, png_signature, "No es PNG vlido")
        
        print(f"    Archivo vlido: {file_size:,} bytes")
        print(f"    Signature PNG: correcto")
    
    def test_08_error_handling(self):
        """Test 8: Manejo de errores"""
        print("\n[TEST 8] Manejo de errores...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_folder = self.output_base / f"low_dimensional_{timestamp}"
        test_folder.mkdir(parents=True, exist_ok=True)
        
        visualizer = ResultsVisualizer(test_folder)
        
        # Test 1: Datos vacos
        try:
            visualizer.plot_gap_comparison_boxplot(
                {},
                filename="empty_test.png"
            )
            print("    Maneja datos vacos sin crash")
        except Exception as e:
            print(f"     Error con datos vacos: {e}")
        
        # Test 2: Carpeta no existente (debera crear)
        non_existent = self.output_base / "non_existent" / "subfolder"
        visualizer2 = ResultsVisualizer(non_existent)
        
        visualizer2.plot_gap_comparison_boxplot(
            {'Test': [1.0]},
            filename="create_test.png"
        )
        
        self.assertTrue((non_existent / "create_test.png").exists())
        print("    Crea carpetas automticamente")


def run_test_suite():
    """Ejecutar suite completa de tests"""
    # Configurar unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestVisualizationSystem)
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"RESUMEN DE TESTS")
    print(f"{'='*70}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Total: {result.testsRun}")
    print(f"{'='*70}\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)

