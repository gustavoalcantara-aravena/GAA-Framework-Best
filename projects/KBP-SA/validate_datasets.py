"""
Script de Validación de Datasets - KBP-SA

Valida que todos los datasets estén en el formato correcto.
"""

import sys
from pathlib import Path
import yaml

# Añadir ruta de scripts del framework
framework_scripts = Path(__file__).parent.parent.parent / "04-Generated" / "scripts"
sys.path.insert(0, str(framework_scripts))

from data_loader import DataLoader


def load_config() -> dict:
    """Carga la configuración del proyecto"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def validate_datasets():
    """Valida todos los datasets del proyecto"""
    print("=" * 70)
    print("  Validación de Datasets - KBP-SA")
    print("=" * 70)
    print()
    
    project_dir = Path(__file__).parent
    
    # Validar subsets incluidos
    subsets = {
        'low_dimensional': 'datasets/low_dimensional',
        'large_scale': 'datasets/large_scale',
        'training': 'datasets/training',
        'validation': 'datasets/validation',
        'test': 'datasets/test'
    }
    
    all_valid = True
    total_instances = 0
    results = {}
    
    for subset_name, subset_path in subsets.items():
        full_path = project_dir / subset_path
        
        if not full_path.exists():
            print(f"\n📂 {subset_name.upper()}: No existe")
            continue
        
        print(f"\n📂 Validando {subset_name.upper()}...")
        print("-" * 70)
        
        loader = DataLoader(
            dataset_dir=full_path,
            problem_type='knapsack'
        )
        
        # Cargar instancias del directorio
        txt_files = list(full_path.glob('*.txt'))
        
        if not txt_files:
            print(f"  ⚠️  No se encontraron archivos .txt en {subset_path}/")
            results[subset_name] = {'valid': 0, 'invalid': 0, 'total': 0}
            continue
        
        valid_count = 0
        invalid_count = 0
        
        for txt_file in txt_files:
            try:
                instance = loader._parse_file(txt_file)
                instance['filename'] = txt_file.name
                is_valid = loader.validate_instance(instance)
                
                if is_valid:
                    valid_count += 1
                    print(f"  ✅ {txt_file.name}: VÁLIDO (n={instance['n']}, W={instance['capacity']})")
                else:
                    invalid_count += 1
                    print(f"  ❌ {txt_file.name}: INVÁLIDO")
                    all_valid = False
            except Exception as e:
                invalid_count += 1
                print(f"  ❌ {txt_file.name}: ERROR - {e}")
                all_valid = False
        
        subset_total = valid_count + invalid_count
        total_instances += subset_total
        results[subset_name] = {
            'valid': valid_count,
            'invalid': invalid_count,
            'total': subset_total
        }
        
        print(f"\n  Resumen {subset_name}: {valid_count} válidas, {invalid_count} inválidas")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("  RESUMEN FINAL")
    print("=" * 70)
    
    for subset_name, stats in results.items():
        if stats['total'] > 0:
            status = "✅" if stats['invalid'] == 0 else "⚠️"
            print(f"{status} {subset_name}: {stats['valid']}/{stats['total']} válidas")
    
    print(f"\n📊 Total de instancias: {total_instances}")
    
    if all_valid and total_instances > 0:
        print("✅ Todos los datasets son válidos")
        
        # Mostrar distribución
        low_dim = results.get('low_dimensional', {}).get('total', 0)
        large_sc = results.get('large_scale', {}).get('total', 0)
        
        if low_dim > 0 or large_sc > 0:
            print("\n📦 Datasets incluidos:")
            if low_dim > 0:
                print(f"  • Low-dimensional: {low_dim} instancias (n=4-23)")
            if large_sc > 0:
                print(f"  • Large-scale: {large_sc} instancias (n=100-10000)")
        
        return True
    elif total_instances == 0:
        print("⚠️  No se encontraron datasets")
        print("\nOpciones:")
        print("  1. Usar instancias incluidas en low_dimensional/ y large_scale/")
        print("  2. Generar ejemplos: python generate_example_datasets.py")
        print("  3. Añadir tus propios datasets en training/, validation/, test/")
        print("\nFormato esperado:")
        print("  optimal_value")
        print("  n W")
        print("  v_1 w_1")
        print("  v_2 w_2")
        print("  ...")
        return False
    else:
        print("❌ Hay datasets inválidos")
        return False


if __name__ == "__main__":
    success = validate_datasets()
    sys.exit(0 if success else 1)
