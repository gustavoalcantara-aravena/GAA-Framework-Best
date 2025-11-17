"""
Script de Verificación Completa del Framework GAA

Verifica que todo el sistema esté correctamente configurado y listo para usar.
"""

from pathlib import Path
import sys
import json
import yaml


class FrameworkValidator:
    """Validador completo del framework GAA"""
    
    def __init__(self, root_dir: Path):
        self.root = Path(root_dir)
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def check_directory_structure(self):
        """Verifica que todos los directorios necesarios existan"""
        print("\n📁 Verificando estructura de directorios...")
        
        required_dirs = [
            ".gaa-config",
            "00-Core",
            "01-System",
            "02-Components",
            "03-Experiments",
            "04-Generated/scripts",
            "05-Automation",
            "06-Datasets",
            "projects"
        ]
        
        for dir_path in required_dirs:
            full_path = self.root / dir_path
            if full_path.exists():
                self.passed.append(f"✅ {dir_path}/")
            else:
                self.errors.append(f"❌ Falta directorio: {dir_path}/")
    
    def check_config_files(self):
        """Verifica archivos de configuración JSON"""
        print("\n⚙️  Verificando archivos de configuración...")
        
        config_files = [
            ".gaa-config/dependency-graph.json",
            ".gaa-config/sync-rules.json",
            ".gaa-config/project-state.json"
        ]
        
        for config_file in config_files:
            full_path = self.root / config_file
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        json.load(f)
                    self.passed.append(f"✅ {config_file}")
                except json.JSONDecodeError as e:
                    self.errors.append(f"❌ JSON inválido en {config_file}: {e}")
            else:
                self.errors.append(f"❌ Falta archivo: {config_file}")
    
    def check_python_scripts(self):
        """Verifica que los scripts Python existan"""
        print("\n🐍 Verificando scripts Python...")
        
        scripts = [
            "05-Automation/sync-engine.py",
            "04-Generated/scripts/problem.py",
            "04-Generated/scripts/ast_nodes.py",
            "04-Generated/scripts/fitness.py",
            "04-Generated/scripts/metaheuristic.py",
            "04-Generated/scripts/data_loader.py"
        ]
        
        for script in scripts:
            full_path = self.root / script
            if full_path.exists():
                # Intentar compilar
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), str(full_path), 'exec')
                    self.passed.append(f"✅ {script}")
                except SyntaxError as e:
                    self.errors.append(f"❌ Error de sintaxis en {script}: {e}")
            else:
                self.errors.append(f"❌ Falta script: {script}")
    
    def check_markdown_files(self):
        """Verifica archivos markdown principales"""
        print("\n📝 Verificando archivos markdown...")
        
        md_files = [
            "README.md",
            "QUICKSTART.md",
            "ARCHITECTURE.md",
            "DEVELOPMENT.md",
            "GAA-Agent-System-Prompt.md",
            "00-Core/Problem.md",
            "00-Core/Metaheuristic.md",
            "01-System/Grammar.md",
            "01-System/AST-Nodes.md"
        ]
        
        for md_file in md_files:
            full_path = self.root / md_file
            if full_path.exists():
                # Verificar YAML frontmatter si es necesario
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        try:
                            # Extraer YAML
                            parts = content.split('---', 2)
                            if len(parts) >= 3:
                                yaml.safe_load(parts[1])
                            self.passed.append(f"✅ {md_file}")
                        except yaml.YAMLError as e:
                            self.warnings.append(f"⚠️  YAML inválido en {md_file}: {e}")
                    else:
                        self.passed.append(f"✅ {md_file}")
            else:
                self.warnings.append(f"⚠️  Falta archivo: {md_file}")
    
    def check_projects(self):
        """Verifica que los proyectos estén correctamente configurados"""
        print("\n🎯 Verificando proyectos...")
        
        projects = ['KBP-SA', 'GCP-ILS', 'VRPTW-GRASP']
        
        for project in projects:
            project_dir = self.root / 'projects' / project
            
            if not project_dir.exists():
                self.errors.append(f"❌ Proyecto no encontrado: {project}")
                continue
            
            # Verificar archivos del proyecto
            required_files = [
                'problema_metaheuristica.md',
                'config.yaml',
                'README.md'
            ]
            
            project_ok = True
            for file in required_files:
                if not (project_dir / file).exists():
                    self.warnings.append(f"⚠️  {project}: falta {file}")
                    project_ok = False
            
            # Verificar directorios de datasets (al menos uno debe existir)
            dataset_options = [
                ['datasets/low_dimensional', 'datasets/large_scale'],  # Nuevas carpetas
                ['datasets/training', 'datasets/validation', 'datasets/test']  # Clásicas
            ]
            
            has_datasets = False
            for option_group in dataset_options:
                if any((project_dir / ds_dir).exists() for ds_dir in option_group):
                    has_datasets = True
                    break
            
            if not has_datasets:
                self.warnings.append(f"⚠️  {project}: no tiene datasets (ni low_dimensional/large_scale ni training/validation/test)")
                project_ok = False
            
            if project_ok:
                self.passed.append(f"✅ Proyecto {project}")
    
    def check_dependencies(self):
        """Verifica que las dependencias de Python estén instaladas"""
        print("\n📦 Verificando dependencias Python...")
        
        required = ['numpy', 'yaml', 'matplotlib', 'scipy']
        
        for package in required:
            try:
                __import__(package)
                self.passed.append(f"✅ {package} instalado")
            except ImportError:
                self.warnings.append(f"⚠️  {package} no instalado (opcional)")
    
    def run_all_checks(self):
        """Ejecuta todas las verificaciones"""
        print("=" * 70)
        print("  VERIFICACIÓN COMPLETA DEL FRAMEWORK GAA")
        print("=" * 70)
        
        self.check_directory_structure()
        self.check_config_files()
        self.check_python_scripts()
        self.check_markdown_files()
        self.check_projects()
        self.check_dependencies()
        
        # Mostrar resumen
        print("\n" + "=" * 70)
        print("  RESUMEN")
        print("=" * 70)
        
        print(f"\n✅ Verificaciones exitosas: {len(self.passed)}")
        print(f"⚠️  Advertencias: {len(self.warnings)}")
        print(f"❌ Errores: {len(self.errors)}")
        
        if self.errors:
            print("\n🔴 ERRORES ENCONTRADOS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n🟡 ADVERTENCIAS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        # Conclusión
        print("\n" + "=" * 70)
        if not self.errors:
            print("✅ FRAMEWORK LISTO PARA USAR")
            print("\nPróximos pasos para KBP-SA:")
            print("  1. Validar datasets: python projects/KBP-SA/validate_datasets.py")
            print("  2. Prueba rápida: python projects/KBP-SA/test_quick.py")
            print("  3. Ejecutar proyecto: python projects/KBP-SA/run.py")
        else:
            print("❌ FRAMEWORK INCOMPLETO")
            print("Por favor, corrige los errores antes de continuar")
        print("=" * 70)
        
        return len(self.errors) == 0


def main():
    # Obtener directorio raíz del framework
    root = Path(__file__).parent
    
    validator = FrameworkValidator(root)
    success = validator.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
