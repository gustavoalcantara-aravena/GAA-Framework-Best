#!/usr/bin/env python3
"""
Test: Visualización de AST
Prueba el módulo de visualización de árboles sintácticos
"""

import sys
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.ast_visualization import ASTVisualizer


def test_ast_visualization():
    print("=" * 80)
    print("  TEST: VISUALIZACIÓN DE ÁRBOLES SINTÁCTICOS (AST)")
    print("=" * 80)
    print()
    
    # 1. Generar algunos algoritmos
    print("🌳 Paso 1: Generando algoritmos GAA...\n")
    
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    algorithms = []
    for i in range(3):
        ast = generator.generate_with_validation()
        if ast:
            algorithms.append({
                'name': f'Algoritmo_{i+1}',
                'ast': ast
            })
            print(f"✅ {algorithms[-1]['name']} generado")
    
    print()
    
    # 2. Crear visualizador
    print("🎨 Paso 2: Inicializando visualizador...\n")
    
    output_dir = project_root / "output" / "ast_visualizations"
    visualizer = ASTVisualizer(output_dir=output_dir)
    
    if visualizer.has_graphviz:
        print("✅ Graphviz disponible")
    else:
        print("⚠️  Graphviz NO disponible. Instalar con:")
        print("   pip install graphviz")
        print("   Además necesitas el ejecutable: https://graphviz.org/download/")
    
    print()
    
    # 3. Visualización ASCII (siempre disponible)
    print("📊 Paso 3: Visualización ASCII en terminal...\n")
    
    for alg in algorithms[:1]:  # Solo el primero
        print(f"🌳 {alg['name']}:")
        print()
        visualizer.print_ast_ascii(alg['ast'])
        print()
    
    # 4. Estadísticas del AST
    print("📈 Paso 4: Estadísticas de los algoritmos...\n")
    
    for alg in algorithms:
        stats = visualizer.get_ast_statistics(alg['ast'])
        print(f"📊 {alg['name']}:")
        print(f"   • Nodos totales: {stats['total_nodes']}")
        print(f"   • Profundidad: {stats['depth']}")
        print(f"   • Tipos de nodos: {dict(stats['node_types'])}")
        print(f"   • Operadores terminales: {stats['terminal_operators']}")
        print()
    
    # 5. Gráficos Graphviz (si está disponible)
    if visualizer.has_graphviz:
        print("🎨 Paso 5: Generando gráficos Graphviz...\n")
        
        # 5.1 Gráfico individual del primer algoritmo
        print("📊 Gráfico 1: AST individual")
        path1 = visualizer.plot_ast_graphviz(
            ast_node=algorithms[0]['ast'],
            filename="algorithm_1_ast",
            title=f"Estructura AST - {algorithms[0]['name']}",
            format='png'
        )
        if path1:
            print(f"   ✅ Generado: {path1}\n")
        
        # 5.2 Gráfico del segundo algoritmo
        if len(algorithms) > 1:
            print("📊 Gráfico 2: AST del segundo algoritmo")
            path2 = visualizer.plot_ast_graphviz(
                ast_node=algorithms[1]['ast'],
                filename="algorithm_2_ast",
                title=f"Estructura AST - {algorithms[1]['name']}",
                format='png'
            )
            if path2:
                print(f"   ✅ Generado: {path2}\n")
        
        # 5.3 Comparación de algoritmos
        if len(algorithms) >= 2:
            print("📊 Gráfico 3: Comparación de ASTs")
            comparison_data = [
                (alg['ast'], alg['name']) for alg in algorithms[:2]
            ]
            path3 = visualizer.plot_ast_comparison(
                asts=comparison_data,
                filename="ast_comparison",
                title="Comparación de Algoritmos GAA",
                format='png'
            )
            if path3:
                print(f"   ✅ Generado: {path3}\n")
        
        print("\n" + "=" * 80)
        print("📂 ARCHIVOS GENERADOS")
        print("=" * 80)
        print(f"\nDirectorio: {output_dir}/\n")
        
        import os
        if output_dir.exists():
            for file in sorted(output_dir.glob("*.png")):
                print(f"  ✅ {file.name}")
        
        print("\n💡 Abriendo carpeta de resultados...")
        import subprocess
        subprocess.run(['explorer', str(output_dir)], check=False)
    
    else:
        print("\n⚠️  Graphviz no disponible. Solo se generaron visualizaciones ASCII.")
        print("   Para gráficos profesionales, instala graphviz:")
        print("   1. pip install graphviz")
        print("   2. Descarga el ejecutable: https://graphviz.org/download/")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    test_ast_visualization()
