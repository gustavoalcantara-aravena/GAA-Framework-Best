#!/usr/bin/env python3
"""
Prueba rápida: Visualización de AST del mejor algoritmo
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gaa.generator import AlgorithmGenerator
from gaa.grammar import Grammar
from experimentation.ast_visualization import ASTVisualizer

def main():
    print("=" * 80)
    print("  PRUEBA: AST CON GRAPHVIZ")
    print("=" * 80)
    print()
    
    # Generar un algoritmo
    grammar = Grammar(min_depth=2, max_depth=3)
    generator = AlgorithmGenerator(grammar=grammar, seed=42)
    
    print("🌳 Generando algoritmo...")
    ast = generator.generate_with_validation()
    
    print("\n📊 Estructura ASCII:")
    print()
    
    # Crear visualizador
    visualizer = ASTVisualizer(output_dir="output/quick_ast_test")
    visualizer.print_ast_ascii(ast)
    
    print()
    
    # Estadísticas
    stats = visualizer.get_ast_statistics(ast)
    print(f"📈 Estadísticas:")
    print(f"   • Nodos: {stats['total_nodes']}")
    print(f"   • Profundidad: {stats['depth']}")
    print(f"   • Operadores: {stats['terminal_operators']}")
    print()
    
    # Verificar Graphviz
    print(f"🔍 Graphviz disponible: {'✅ SÍ' if visualizer.has_graphviz else '❌ NO'}")
    print()
    
    if visualizer.has_graphviz:
        print("🎨 Generando gráfico PNG...")
        path = visualizer.plot_ast_graphviz(
            ast_node=ast,
            filename="algorithm_ast",
            title="Algoritmo Seleccionado - Estructura AST",
            format='png'
        )
        
        if path:
            print(f"\n✅ Gráfico generado exitosamente!")
            print(f"📂 Abriendo: {path}")
            
            import subprocess
            subprocess.run(['explorer', str(Path(path).parent)], check=False)
    else:
        print("⚠️  Instala Graphviz para ver gráficos:")
        print("   PATH debe incluir: C:\\Program Files\\Graphviz\\bin")
    
    print("\n" + "=" * 80)
    print("✅ COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()
