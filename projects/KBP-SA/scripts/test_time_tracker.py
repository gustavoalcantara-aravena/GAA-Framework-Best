#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del TimeTracker
Prueba simple para verificar que el sistema de tracking funciona
"""

import sys
import os
import time
from pathlib import Path

# Configurar encoding UTF-8 para salida en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from experimentation.time_tracker import TimeTracker


def main():
    print("=" * 60)
    print("  TEST: TimeTracker")
    print("=" * 60)
    print()

    # Crear tracker
    tracker = TimeTracker(output_file="test_tracking.md", output_dir="output/test")

    with tracker.track("Proceso completo de prueba"):

        # Paso 1
        with tracker.track("Paso 1: Inicialización", items=10):
            print("Ejecutando paso 1...")
            time.sleep(1)
            tracker.update_current(items_loaded=10)
            print("✓ Paso 1 completado")

        # Paso 2 con subprocesos
        with tracker.track("Paso 2: Procesamiento de datos"):
            print("\nEjecutando paso 2...")

            for i in range(3):
                with tracker.track(f"Subproceso 2.{i+1}", item_id=i+1):
                    print(f"  - Procesando item {i+1}")
                    time.sleep(0.5)
                    tracker.update_current(progress=f"{i+1}/3")

            print("✓ Paso 2 completado")

        # Paso 3
        with tracker.track("Paso 3: Generación de resultados"):
            print("\nEjecutando paso 3...")
            time.sleep(0.8)
            tracker.update_current(files_generated=5)
            print("✓ Paso 3 completado")

    # Finalizar
    tracker.finalize()

    print("\n" + "=" * 60)
    print(f"✅ Test completado!")
    print(f"📊 Archivo de tracking generado: {tracker.output_path}")
    print(f"   Abre el archivo para ver el reporte detallado.")
    print("=" * 60)


if __name__ == '__main__':
    main()
