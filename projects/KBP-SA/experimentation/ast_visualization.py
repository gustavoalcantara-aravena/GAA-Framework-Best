"""
AST Visualization - KBP-SA
Visualización de Árboles Sintácticos Abstractos
Módulo de experimentación para graficar algoritmos GAA
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import json


class ASTVisualizer:
    """
    Visualizador de Árboles Sintácticos Abstractos
    
    Genera representaciones gráficas de algoritmos GAA:
    - Graphviz (profesional, para papers)
    - ASCII (terminal, debugging)
    - Comparación de múltiples ASTs
    """
    
    def __init__(self, output_dir: Path):
        """
        Inicializa el visualizador
        
        Args:
            output_dir: Directorio para guardar visualizaciones
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar graphviz
        self.has_graphviz = self._check_graphviz()
        
        # Configuración de colores por tipo de nodo
        self.node_colors = {
            'Seq': '#E8F4F8',           # Azul claro
            'If': '#FFF4E6',            # Naranja claro
            'While': '#F3E8FF',         # Púrpura claro
            'For': '#FCE4EC',           # Rosa claro
            'Call': '#E8F5E9',          # Verde claro
            'GreedyConstruct': '#FFE0B2',  # Naranja
            'LocalSearch': '#C8E6C9',   # Verde
            'ChooseBestOf': '#FFECB3',  # Amarillo
            'ApplyUntilNoImprove': '#D1C4E9',  # Púrpura
            'DestroyRepair': '#FFCCBC'  # Rojo claro
        }
    
    def _check_graphviz(self) -> bool:
        """Verifica si graphviz está disponible"""
        try:
            import graphviz
            return True
        except ImportError:
            return False
    
    def plot_ast_graphviz(
        self, 
        ast_node, 
        filename: str,
        title: Optional[str] = None,
        format: str = 'png'
    ) -> Optional[str]:
        """
        Genera visualización profesional del AST con Graphviz
        
        Args:
            ast_node: Nodo raíz del AST
            filename: Nombre del archivo (sin extensión)
            title: Título opcional del gráfico
            format: Formato de salida ('png', 'pdf', 'svg')
            
        Returns:
            str: Ruta del archivo generado, None si falla
        """
        if not self.has_graphviz:
            print("⚠️  graphviz no disponible. Instalar con: pip install graphviz")
            return None
        
        import graphviz
        
        # Crear grafo dirigido
        dot = graphviz.Digraph(comment='Algorithm AST')
        dot.attr(rankdir='TB')  # Top to Bottom
        dot.attr('node', shape='box', style='filled,rounded', 
                fontname='Arial', fontsize='10')
        dot.attr('edge', color='#666666', arrowsize='0.7')
        
        # Título
        if title:
            dot.attr(label=title, fontsize='14', fontname='Arial Bold')
            dot.attr(labelloc='t')  # Top
        
        # Construir árbol recursivamente
        counter = [0]  # Contador mutable para IDs únicos
        self._build_graphviz_tree(ast_node, dot, None, counter)
        
        # Guardar
        output_path = self.output_dir / filename
        try:
            dot.render(str(output_path), format=format, cleanup=True)
            final_path = f"{output_path}.{format}"
            print(f"📊 Gráfico AST guardado: {final_path}")
            return final_path
        except Exception as e:
            print(f"❌ Error generando gráfico AST: {e}")
            return None
    
    def _build_graphviz_tree(
        self, 
        node, 
        dot, 
        parent_id: Optional[str], 
        counter: List[int]
    ):
        """
        Construye árbol Graphviz recursivamente
        
        Args:
            node: Nodo AST actual
            dot: Objeto Graphviz
            parent_id: ID del nodo padre
            counter: Contador para IDs únicos
        """
        # Generar ID único
        node_id = f"node_{counter[0]}"
        counter[0] += 1
        
        # Determinar etiqueta
        node_type = node.__class__.__name__
        label = node_type
        
        # Agregar información adicional según el tipo
        if node_type == 'Call' and hasattr(node, 'name'):
            label = f"{node_type}\n«{node.name}»"
        elif node_type == 'If' and hasattr(node, 'condition'):
            label = f"{node_type}\n[{node.condition}]"
        elif node_type == 'While' and hasattr(node, 'condition'):
            label = f"{node_type}\n[{node.condition}]"
        elif node_type == 'For' and hasattr(node, 'iterations'):
            label = f"{node_type}\n(n={node.iterations})"
        elif node_type == 'ChooseBestOf' and hasattr(node, 'n_tries'):
            label = f"{node_type}\n(n={node.n_tries})"
        elif node_type == 'GreedyConstruct' and hasattr(node, 'strategy'):
            label = f"{node_type}\n«{node.strategy}»"
        elif node_type == 'LocalSearch':
            if hasattr(node, 'neighborhood') and hasattr(node, 'strategy'):
                label = f"{node_type}\n«{node.neighborhood}»\n({node.strategy})"
        elif node_type == 'DestroyRepair':
            if hasattr(node, 'destruction_rate'):
                label = f"{node_type}\n(rate={node.destruction_rate})"
        
        # Color según tipo
        color = self.node_colors.get(node_type, '#F5F5F5')
        
        # Agregar nodo
        dot.node(node_id, label, fillcolor=color)
        
        # Conectar con padre
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        
        # Procesar hijos
        children = self._get_node_children(node)
        for i, child in enumerate(children):
            self._build_graphviz_tree(child, dot, node_id, counter)
    
    def _get_node_children(self, node) -> List:
        """
        Extrae hijos de un nodo AST
        
        Args:
            node: Nodo AST
            
        Returns:
            Lista de nodos hijos
        """
        children = []
        node_type = node.__class__.__name__
        
        if node_type == 'Seq':
            # Secuencia tiene lista de statements
            if hasattr(node, 'body') and isinstance(node.body, list):
                children = node.body
        
        elif node_type in ['If', 'While', 'For', 'ChooseBestOf', 'ApplyUntilNoImprove']:
            # Estos tienen un body (que puede ser un nodo o lista)
            if hasattr(node, 'then_branch'):
                children.append(node.then_branch)
            if hasattr(node, 'else_branch') and node.else_branch is not None:
                children.append(node.else_branch)
            if hasattr(node, 'body'):
                if isinstance(node.body, list):
                    children.extend(node.body)
                elif node.body is not None:
                    children.append(node.body)
        
        elif node_type == 'DestroyRepair':
            # DestroyRepair puede tener destroy y repair
            if hasattr(node, 'destroy') and node.destroy is not None:
                children.append(node.destroy)
            if hasattr(node, 'repair') and node.repair is not None:
                children.append(node.repair)
        
        # Call, GreedyConstruct, LocalSearch son terminales (sin hijos)
        
        return children
    
    def print_ast_ascii(self, node, prefix: str = "", is_last: bool = True):
        """
        Imprime árbol en formato ASCII en terminal
        
        Args:
            node: Nodo raíz del AST
            prefix: Prefijo para indentación
            is_last: Si es el último hijo
        """
        # Conector
        connector = "└── " if is_last else "├── "
        
        # Etiqueta
        node_type = node.__class__.__name__
        label = node_type
        
        if hasattr(node, 'name'):
            label += f" ({node.name})"
        elif hasattr(node, 'condition'):
            label += f" [{node.condition}]"
        elif hasattr(node, 'iterations'):
            label += f" (n={node.iterations})"
        elif hasattr(node, 'n_tries'):
            label += f" (n={node.n_tries})"
        
        # Imprimir nodo
        print(prefix + connector + label)
        
        # Extensión del prefijo para hijos
        extension = "    " if is_last else "│   "
        
        # Procesar hijos
        children = self._get_node_children(node)
        for i, child in enumerate(children):
            self.print_ast_ascii(child, prefix + extension, i == len(children) - 1)
    
    def plot_ast_comparison(
        self,
        asts: List[tuple],  # [(ast, name), ...]
        filename: str,
        title: Optional[str] = None,
        format: str = 'png'
    ) -> Optional[str]:
        """
        Genera comparación lado a lado de múltiples ASTs
        
        Args:
            asts: Lista de tuplas (ast_node, nombre)
            filename: Nombre del archivo
            title: Título del gráfico
            format: Formato de salida
            
        Returns:
            str: Ruta del archivo generado
        """
        if not self.has_graphviz:
            print("⚠️  graphviz no disponible")
            return None
        
        import graphviz
        
        # Crear grafo con subgrafos
        dot = graphviz.Digraph(comment='AST Comparison')
        dot.attr(rankdir='TB', compound='true')
        
        if title:
            dot.attr(label=title, fontsize='16', fontname='Arial Bold')
            dot.attr(labelloc='t')
        
        # Crear subgrafo para cada AST
        for idx, (ast_node, name) in enumerate(asts):
            with dot.subgraph(name=f'cluster_{idx}') as sub:
                sub.attr(label=name, fontsize='12', fontname='Arial Bold')
                sub.attr(style='rounded,filled', fillcolor='#F8F8F8')
                
                counter = [idx * 1000]  # IDs únicos por subgrafo
                self._build_graphviz_tree(ast_node, sub, None, counter)
        
        # Guardar
        output_path = self.output_dir / filename
        try:
            dot.render(str(output_path), format=format, cleanup=True)
            final_path = f"{output_path}.{format}"
            print(f"📊 Gráfico de comparación AST guardado: {final_path}")
            return final_path
        except Exception as e:
            print(f"❌ Error generando comparación: {e}")
            return None
    
    def get_ast_statistics(self, node) -> Dict[str, Any]:
        """
        Calcula estadísticas del AST
        
        Args:
            node: Nodo raíz del AST
            
        Returns:
            Dict con estadísticas
        """
        stats = {
            'total_nodes': 0,
            'depth': 0,
            'node_types': {},
            'terminal_operators': []
        }
        
        def traverse(n, depth=0):
            stats['total_nodes'] += 1
            stats['depth'] = max(stats['depth'], depth)
            
            node_type = n.__class__.__name__
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            
            # Operadores terminales
            if node_type in ['Call', 'GreedyConstruct', 'LocalSearch']:
                if hasattr(n, 'name'):
                    stats['terminal_operators'].append(n.name)
                elif hasattr(n, 'strategy'):
                    stats['terminal_operators'].append(n.strategy)
            
            # Recursión
            for child in self._get_node_children(n):
                traverse(child, depth + 1)
        
        traverse(node)
        return stats
