"""
Generador de Datasets de Ejemplo - KBP

Genera instancias aleatorias del Knapsack Problem para testing.
"""

import random
from pathlib import Path


def generate_knapsack_instance(n: int, capacity: int, seed: int = None) -> dict:
    """
    Genera una instancia aleatoria del Knapsack Problem
    
    Args:
        n: Número de ítems
        capacity: Capacidad de la mochila
        seed: Semilla para reproducibilidad
        
    Returns:
        Diccionario con valores y pesos
    """
    if seed is not None:
        random.seed(seed)
    
    # Generar valores entre 1 y 100
    values = [random.randint(1, 100) for _ in range(n)]
    
    # Generar pesos entre 1 y capacity/2 (para que sean instancias interesantes)
    max_weight = max(1, capacity // 2)
    weights = [random.randint(1, max_weight) for _ in range(n)]
    
    return {
        'n': n,
        'capacity': capacity,
        'values': values,
        'weights': weights
    }


def save_instance(instance: dict, filepath: Path):
    """Guarda una instancia en formato texto"""
    with open(filepath, 'w') as f:
        f.write(f"{instance['n']} {instance['capacity']}\n")
        for v, w in zip(instance['values'], instance['weights']):
            f.write(f"{v} {w}\n")


def main():
    """Genera datasets de ejemplo"""
    print("=" * 70)
    print("  Generador de Datasets - KBP")
    print("=" * 70)
    print()
    
    project_dir = Path(__file__).parent
    
    # Configuración de instancias
    configs = {
        'training': [
            (10, 50, 'kp_n10_W50'),
            (20, 100, 'kp_n20_W100'),
            (50, 250, 'kp_n50_W250'),
        ],
        'validation': [
            (30, 150, 'kp_n30_W150'),
            (50, 300, 'kp_n50_W300'),
        ],
        'test': [
            (100, 500, 'kp_n100_W500'),
            (200, 1000, 'kp_n200_W1000'),
        ]
    }
    
    for subset, instances_config in configs.items():
        print(f"\n📂 Generando {subset.upper()}...")
        
        subset_dir = project_dir / 'datasets' / subset
        subset_dir.mkdir(parents=True, exist_ok=True)
        
        for n, capacity, name in instances_config:
            # Generar instancia
            instance = generate_knapsack_instance(n, capacity, seed=42)
            
            # Guardar
            filepath = subset_dir / f"{name}.txt"
            save_instance(instance, filepath)
            
            print(f"  ✅ {filepath.name} (n={n}, W={capacity})")
    
    print("\n✅ Datasets generados exitosamente")
    print("\nPara validar, ejecuta:")
    print("  python validate_datasets.py")


if __name__ == "__main__":
    main()
