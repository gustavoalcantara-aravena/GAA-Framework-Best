#!/usr/bin/env python3
"""
Test Rápido - KBP-SA
Prueba el sistema con una instancia low-dimensional
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.loader import DatasetLoader
import yaml


def load_config():
    """Carga configuración del proyecto"""
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def test_single_instance():
    """Prueba con una instancia simple"""
    print("=" * 70)
    print("  Test Rápido - KBP-SA")
    print("=" * 70)
    print()
    
    # Cargar configuración
    config = load_config()
    project_dir = Path(__file__).parent
    
    # Cargar instancia f1 (la más simple con óptimo conocido)
    print("📂 Cargando instancia f1_l-d_kp_10_269...")
    
    instance_path = project_dir / "datasets/low_dimensional/f1_l-d_kp_10_269_low-dimensional.txt"
    
    loader = DatasetLoader(project_dir / "datasets")
    
    instance = loader.load_instance(instance_path)
    
    print(f"✅ Instancia cargada:")
    print(f"   • n = {instance.n} ítems")
    print(f"   • Capacidad = {instance.capacity}")
    print(f"   • Óptimo conocido = {instance.optimal_value if instance.optimal_value else 'N/A'}")
    print()
    
    # Mostrar estadísticas
    print("📊 Estadísticas de ítems:")
    print(f"   • Valores: min={min(instance.values)}, max={max(instance.values)}, "
          f"suma={sum(instance.values)}")
    print(f"   • Pesos: min={min(instance.weights)}, max={max(instance.weights)}, "
          f"suma={sum(instance.weights)}")
    print()
    
    # Solución trivial (tomar todos los ítems)
    total_value_all = sum(instance.values)
    total_weight_all = sum(instance.weights)
    print(f"💡 Solución trivial (todos los ítems):")
    print(f"   • Valor total = {total_value_all}")
    print(f"   • Peso total = {total_weight_all}")
    print(f"   • ¿Factible? {'NO' if total_weight_all > instance.capacity else 'SÍ'}")
    print()
    
    # Solución greedy simple (ordenar por ratio valor/peso)
    items = list(zip(instance.values, instance.weights, range(instance.n)))
    items_sorted = sorted(items, key=lambda x: x[0]/x[1] if x[1] > 0 else 0, reverse=True)
    
    greedy_value = 0
    greedy_weight = 0
    greedy_items = []
    
    for value, weight, idx in items_sorted:
        if greedy_weight + weight <= instance.capacity:
            greedy_value += value
            greedy_weight += weight
            greedy_items.append(idx)
    
    print(f"🎯 Solución Greedy (ratio valor/peso):")
    print(f"   • Ítems seleccionados: {len(greedy_items)} de {instance.n}")
    print(f"   • Valor total = {greedy_value}")
    print(f"   • Peso total = {greedy_weight}/{instance.capacity}")
    print(f"   • Utilización = {greedy_weight/instance.capacity*100:.1f}%")
    
    if instance.optimal_value:
        gap = (instance.optimal_value - greedy_value) / instance.optimal_value * 100
        print(f"   • Gap vs óptimo = {gap:.2f}%")
    
    print()
    print("=" * 70)
    print("✅ Test completado exitosamente")
    print("=" * 70)
    print()
    print("Siguiente paso: ejecutar run.py para optimización completa")
    print()


if __name__ == '__main__':
    test_single_instance()
