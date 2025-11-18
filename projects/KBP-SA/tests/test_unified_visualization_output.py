"""
Test: Validacion del Sistema Unificado de Visualizaciones
===========================================================

Valida que el sistema genere correctamente:
1. Carpeta unificada low_dimensional_{timestamp}
2. Graficas estadisticas generales (3 archivos)
3. AST del mejor algoritmo (1 archivo)
4. Subcarpetas por instancia con 4 graficas cada una

Este test ejecuta demo_experimentation.py y valida la estructura de salida.
"""

import unittest
import subprocess
import sys
from pathlib import Path
import time
import re


class TestUnifiedVisualizationOutput(unittest.TestCase):
    """Test de integracion para validar output completo"""
    
    @classmethod
    def setUpClass(cls):
        """Configuracion inicial"""
        cls.project_root = Path(__file__).parent.parent
        cls.script_path = cls.project_root / "scripts" / "demo_experimentation.py"
        cls.output_base = cls.project_root / "output"
        
        print("\n" + "="*70)
        print("TEST: Sistema Unificado de Visualizaciones")
        print("="*70)
        print(f"Proyecto: {cls.project_root}")
        print(f"Script: {cls.script_path.name}")
        print(f"Output: {cls.output_base}")
        print("="*70 + "\n")
    
    def test_01_execute_demo_experimentation(self):
        """Test 1: Ejecutar demo_experimentation.py exitosamente"""
        print("\n[TEST 1] Ejecutando demo_experimentation.py...")
        
        # Verificar que el script existe
        self.assertTrue(
            self.script_path.exists(),
            f"Script no encontrado: {self.script_path}"
        )
        
        # Ejecutar script
        result = subprocess.run(
            [sys.executable, str(self.script_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minutos max
        )
        
        # Validar ejecucion exitosa
        self.assertEqual(
            result.returncode, 0,
            f"Script fallo con codigo {result.returncode}\n{result.stderr}"
        )
        
        print("   Script ejecutado exitosamente")
        
        # Buscar mensaje de confirmacion en output
        self.assertIn(
            "Todas las visualizaciones generadas",
            result.stdout,
            "No se encontro mensaje de confirmacion"
        )
        
        print("   Confirmacion encontrada en output")
    
    def test_02_validate_unified_folder_structure(self):
        """Test 2: Validar estructura de carpeta unificada"""
        print("\n[TEST 2] Validando estructura de carpeta unificada...")
        
        # Buscar la carpeta mas reciente low_dimensional_*
        pattern = re.compile(r"low_dimensional_\d{8}_\d{6}")
        low_dim_folders = [
            f for f in self.output_base.iterdir()
            if f.is_dir() and pattern.match(f.name)
        ]
        
        self.assertGreater(
            len(low_dim_folders), 0,
            "No se encontro carpeta low_dimensional_YYYYMMDD_HHMMSS"
        )
        
        # Usar la mas reciente
        latest_folder = max(low_dim_folders, key=lambda f: f.stat().st_mtime)
        
        print(f"   Carpeta encontrada: {latest_folder.name}")
        
        # Validar patron de nombre
        self.assertRegex(
            latest_folder.name,
            r"low_dimensional_\d{8}_\d{6}",
            "Patron de nombre incorrecto"
        )
        
        # Guardar para otros tests
        self.__class__.latest_output = latest_folder
    
    def test_03_validate_main_folder_files(self):
        """Test 3: Validar archivos en carpeta principal"""
        print("\n[TEST 3] Validando archivos en carpeta principal...")
        
        if not hasattr(self.__class__, 'latest_output'):
            self.skipTest("Test 02 no ejecutado correctamente")
        
        folder = self.__class__.latest_output
        
        # Archivos esperados
        expected_files = [
            "best_algorithm_ast.png",      # AST del mejor
            "demo_boxplot.png",             # Estadisticas
            "demo_bars.png",
            "demo_scatter.png"
        ]
        
        found_files = []
        for filename in expected_files:
            filepath = folder / filename
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"   OK: {filename} ({size:,} bytes)")
                found_files.append(filename)
                
                # Validar que no esta vacio
                self.assertGreater(
                    size, 1000,
                    f"{filename} muy pequeno (< 1KB)"
                )
            else:
                print(f"   FALTA: {filename}")
        
        # Al menos debe haber el AST y alguna grafica estadistica
        self.assertIn(
            "best_algorithm_ast.png", found_files,
            "Falta AST del mejor algoritmo"
        )
        
        self.assertGreaterEqual(
            len(found_files), 2,
            f"Solo {len(found_files)} archivos principales encontrados"
        )
    
    def test_04_validate_instance_subfolders(self):
        """Test 4: Validar subcarpetas por instancia"""
        print("\n[TEST 4] Validando subcarpetas por instancia...")
        
        if not hasattr(self.__class__, 'latest_output'):
            self.skipTest("Test 02 no ejecutado correctamente")
        
        folder = self.__class__.latest_output
        
        # Buscar subcarpetas (patron: nombre_instancia_timestamp)
        instance_pattern = re.compile(r"f\d+_.*_\d{8}_\d{6}")
        instance_folders = [
            f for f in folder.iterdir()
            if f.is_dir() and instance_pattern.match(f.name)
        ]
        
        print(f"   Subcarpetas encontradas: {len(instance_folders)}")
        
        self.assertGreater(
            len(instance_folders), 0,
            "No se encontraron subcarpetas de instancias"
        )
        
        # Listar subcarpetas
        for instance_folder in sorted(instance_folders):
            print(f"   - {instance_folder.name}")
        
        # Guardar para siguiente test
        self.__class__.instance_folders = instance_folders
    
    def test_05_validate_instance_plots(self):
        """Test 5: Validar 4 graficas por instancia"""
        print("\n[TEST 5] Validando graficas por instancia...")
        
        if not hasattr(self.__class__, 'instance_folders'):
            self.skipTest("Test 04 no ejecutado correctamente")
        
        expected_plots = [
            "gap_evolution.png",
            "acceptance_rate.png",
            "delta_e_distribution.png",
            "exploration_exploitation_balance.png"
        ]
        
        total_checked = 0
        total_found = 0
        
        for instance_folder in self.__class__.instance_folders:
            print(f"\n   {instance_folder.name}:")
            
            instance_found = 0
            for plot_name in expected_plots:
                filepath = instance_folder / plot_name
                total_checked += 1
                
                if filepath.exists():
                    size = filepath.stat().st_size
                    print(f"      OK: {plot_name} ({size:,} bytes)")
                    instance_found += 1
                    total_found += 1
                    
                    # Validar tamano
                    self.assertGreater(
                        size, 1000,
                        f"{plot_name} muy pequeno"
                    )
                else:
                    print(f"      FALTA: {plot_name}")
            
            # Cada instancia debe tener las 4 graficas
            self.assertEqual(
                instance_found, 4,
                f"{instance_folder.name}: solo {instance_found}/4 graficas"
            )
        
        print(f"\n   Total validado: {total_found}/{total_checked} graficas")
    
    def test_06_validate_total_file_count(self):
        """Test 6: Validar numero total de archivos PNG"""
        print("\n[TEST 6] Validando numero total de archivos...")
        
        if not hasattr(self.__class__, 'latest_output'):
            self.skipTest("Test 02 no ejecutado correctamente")
        
        folder = self.__class__.latest_output
        
        # Contar todos los PNG recursivamente
        all_pngs = list(folder.rglob("*.png"))
        
        print(f"   Total archivos PNG: {len(all_pngs)}")
        
        # Separar por ubicacion
        main_pngs = [f for f in all_pngs if f.parent == folder]
        instance_pngs = [f for f in all_pngs if f.parent != folder]
        
        print(f"   - En carpeta principal: {len(main_pngs)}")
        print(f"   - En subcarpetas: {len(instance_pngs)}")
        
        # Validaciones
        self.assertGreaterEqual(
            len(main_pngs), 2,
            "Deben haber al menos 2 graficas principales (AST + 1 estadistica)"
        )
        
        if hasattr(self.__class__, 'instance_folders'):
            expected_instance_pngs = len(self.__class__.instance_folders) * 4
            self.assertEqual(
                len(instance_pngs), expected_instance_pngs,
                f"Esperados {expected_instance_pngs} graficas de instancia, "
                f"encontrados {len(instance_pngs)}"
            )
    
    def test_07_validate_png_integrity(self):
        """Test 7: Validar integridad de archivos PNG"""
        print("\n[TEST 7] Validando integridad de PNG...")
        
        if not hasattr(self.__class__, 'latest_output'):
            self.skipTest("Test 02 no ejecutado correctamente")
        
        folder = self.__class__.latest_output
        all_pngs = list(folder.rglob("*.png"))
        
        png_signature = b'\x89PNG\r\n\x1a\n'
        valid_count = 0
        
        for png_file in all_pngs:
            with open(png_file, 'rb') as f:
                header = f.read(8)
            
            if header == png_signature:
                valid_count += 1
            else:
                print(f"   INVALIDO: {png_file.name}")
        
        print(f"   PNG validos: {valid_count}/{len(all_pngs)}")
        
        self.assertEqual(
            valid_count, len(all_pngs),
            f"{len(all_pngs) - valid_count} archivos PNG corruptos"
        )
    
    @classmethod
    def tearDownClass(cls):
        """Resumen final"""
        print("\n" + "="*70)
        print("TESTS COMPLETADOS")
        if hasattr(cls, 'latest_output'):
            print(f"Resultados en: {cls.latest_output}")
        print("="*70 + "\n")


def run_test_suite():
    """Ejecutar suite de tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestUnifiedVisualizationOutput)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
