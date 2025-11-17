"""
Grammar - KBP-SA
Gramática BNF y validación de AST
Fase 3 GAA: Reglas de producción

Gramática BNF:
--------------
<Prog> ::= Seq(<Stmt>*)
<Stmt> ::= If(<Cond>, <Stmt>, <Stmt>)
         | While(<Bud>, <Stmt>)
         | For(<Int>, <Stmt>)
         | Seq(<Stmt>*)
         | ChooseBestOf(<Int>, <Stmt>)
         | ApplyUntilNoImprove(<Stmt>, <Stop>)
         | LocalSearch(<Neighborhood>, <Acceptance>)
         | GreedyConstruct(<Heuristic>)
         | DestroyRepair(<Destroy>, <Repair>)
         | Call(<Terminal>)
<Cond> ::= IsFeasible | Improves | Prob | Stagnation
<Bud>  ::= IterBudget | TimeBudget
"""

from typing import Set, Dict, List, Any
from .ast_nodes import ASTNode


class Grammar:
    """
    Gramática GAA para validación de AST
    
    Define:
    - Terminales disponibles del dominio
    - Funciones (nodos internos)
    - Restricciones de profundidad
    - Validación de tipos
    """
    
    # Terminales constructivos
    CONSTRUCTIVE_TERMINALS = {
        'GreedyByValue',
        'GreedyByWeight',
        'GreedyByRatio',
        'RandomConstruct'
    }
    
    # Terminales de mejora
    IMPROVEMENT_TERMINALS = {
        'FlipBestItem',
        'FlipWorstItem',
        'OneExchange',
        'TwoExchange'
    }
    
    # Terminales de perturbación
    PERTURBATION_TERMINALS = {
        'RandomFlip',
        'ShakeByRemoval',
        'DestroyRepair'
    }
    
    # Terminales de reparación
    REPAIR_TERMINALS = {
        'RepairByRemoval',
        'RepairByGreedy'
    }
    
    # Todos los terminales
    ALL_TERMINALS = (
        CONSTRUCTIVE_TERMINALS | 
        IMPROVEMENT_TERMINALS | 
        PERTURBATION_TERMINALS | 
        REPAIR_TERMINALS
    )
    
    # Funciones (nodos internos)
    FUNCTIONS = {
        'Seq', 'If', 'While', 'For',
        'ChooseBestOf', 'ApplyUntilNoImprove',
        'LocalSearch', 'GreedyConstruct',
        'DestroyRepair', 'Call'
    }
    
    # Condiciones
    CONDITIONS = {
        'IsFeasible',
        'Improves',
        'Prob',
        'Stagnation'
    }
    
    # Presupuestos
    BUDGETS = {
        'IterBudget',
        'TimeBudget'
    }
    
    # Vecindarios (para LocalSearch)
    NEIGHBORHOODS = IMPROVEMENT_TERMINALS
    
    # Criterios de aceptación
    ACCEPTANCE_CRITERIA = {
        'Improving',
        'Metropolis',
        'FirstImproving',
        'AlwaysAccept'
    }
    
    def __init__(self, min_depth: int = 2, max_depth: int = 5):
        """
        Inicializa gramática con restricciones
        
        Args:
            min_depth: Profundidad mínima del AST
            max_depth: Profundidad máxima del AST
        """
        self.min_depth = min_depth
        self.max_depth = max_depth
    
    def is_valid_terminal(self, name: str) -> bool:
        """Verifica si es un terminal válido"""
        return name in self.ALL_TERMINALS
    
    def is_valid_function(self, name: str) -> bool:
        """Verifica si es una función válida"""
        return name in self.FUNCTIONS
    
    def is_valid_condition(self, name: str) -> bool:
        """Verifica si es una condición válida"""
        return name in self.CONDITIONS
    
    def is_valid_budget(self, name: str) -> bool:
        """Verifica si es un presupuesto válido"""
        return name in self.BUDGETS
    
    def is_valid_neighborhood(self, name: str) -> bool:
        """Verifica si es un vecindario válido"""
        return name in self.NEIGHBORHOODS
    
    def is_valid_acceptance(self, name: str) -> bool:
        """Verifica si es un criterio de aceptación válido"""
        return name in self.ACCEPTANCE_CRITERIA
    
    def get_terminals_by_category(self, category: str) -> Set[str]:
        """
        Obtiene terminales por categoría
        
        Args:
            category: 'constructive', 'improvement', 'perturbation', 'repair'
        
        Returns:
            Set de nombres de terminales
        """
        categories = {
            'constructive': self.CONSTRUCTIVE_TERMINALS,
            'improvement': self.IMPROVEMENT_TERMINALS,
            'perturbation': self.PERTURBATION_TERMINALS,
            'repair': self.REPAIR_TERMINALS,
            'all': self.ALL_TERMINALS
        }
        return categories.get(category, set())
    
    def validate_ast(self, node: ASTNode, depth: int = 0) -> List[str]:
        """
        Valida AST recursivamente
        
        Args:
            node: Nodo raíz del AST
            depth: Profundidad actual
        
        Returns:
            Lista de errores (vacía si es válido)
        """
        errors = []
        
        # Verificar profundidad máxima
        if depth > self.max_depth:
            errors.append(f"Profundidad excede máximo: {depth} > {self.max_depth}")
            return errors
        
        node_type = node.__class__.__name__
        
        # Validar según tipo de nodo
        if node_type == 'Seq':
            if not node.body:
                errors.append("Seq vacío no permitido")
            for stmt in node.body:
                errors.extend(self.validate_ast(stmt, depth + 1))
        
        elif node_type == 'If':
            if not self.is_valid_condition(node.condition):
                errors.append(f"Condición inválida: {node.condition}")
            errors.extend(self.validate_ast(node.then_branch, depth + 1))
            if node.else_branch:
                errors.extend(self.validate_ast(node.else_branch, depth + 1))
        
        elif node_type == 'While':
            if not self.is_valid_budget(node.budget_type):
                errors.append(f"Presupuesto inválido: {node.budget_type}")
            if node.budget_value <= 0:
                errors.append(f"Valor de presupuesto debe ser positivo: {node.budget_value}")
            errors.extend(self.validate_ast(node.body, depth + 1))
        
        elif node_type == 'For':
            if node.iterations <= 0:
                errors.append(f"Iteraciones deben ser positivas: {node.iterations}")
            errors.extend(self.validate_ast(node.body, depth + 1))
        
        elif node_type == 'Call':
            if not self.is_valid_terminal(node.name):
                errors.append(f"Terminal inválido: {node.name}")
        
        elif node_type == 'GreedyConstruct':
            if node.heuristic not in self.CONSTRUCTIVE_TERMINALS:
                errors.append(f"Heurística constructiva inválida: {node.heuristic}")
        
        elif node_type == 'LocalSearch':
            if not self.is_valid_neighborhood(node.neighborhood):
                errors.append(f"Vecindario inválido: {node.neighborhood}")
            if not self.is_valid_acceptance(node.acceptance):
                errors.append(f"Criterio de aceptación inválido: {node.acceptance}")
        
        elif node_type == 'ChooseBestOf':
            if node.n_tries <= 0:
                errors.append(f"Número de intentos debe ser positivo: {node.n_tries}")
            errors.extend(self.validate_ast(node.body, depth + 1))
        
        elif node_type == 'ApplyUntilNoImprove':
            errors.extend(self.validate_ast(node.body, depth + 1))
        
        elif node_type == 'DestroyRepair':
            if node.destroy_op not in self.PERTURBATION_TERMINALS:
                errors.append(f"Operador de destrucción inválido: {node.destroy_op}")
            if node.repair_op not in self.REPAIR_TERMINALS:
                errors.append(f"Operador de reparación inválido: {node.repair_op}")
        
        else:
            errors.append(f"Tipo de nodo desconocido: {node_type}")
        
        return errors
    
    def get_depth(self, node: ASTNode) -> int:
        """
        Calcula profundidad del AST
        
        Args:
            node: Nodo raíz
        
        Returns:
            Profundidad máxima
        """
        node_type = node.__class__.__name__
        
        if node_type in ['Call', 'GreedyConstruct', 'DestroyRepair']:
            return 1
        
        elif node_type == 'Seq':
            if not node.body:
                return 1
            return 1 + max(self.get_depth(stmt) for stmt in node.body)
        
        elif node_type in ['If', 'While', 'For', 'ChooseBestOf', 'ApplyUntilNoImprove']:
            depths = []
            if hasattr(node, 'body') and node.body:
                depths.append(self.get_depth(node.body))
            if hasattr(node, 'then_branch') and node.then_branch:
                depths.append(self.get_depth(node.then_branch))
            if hasattr(node, 'else_branch') and node.else_branch:
                depths.append(self.get_depth(node.else_branch))
            
            return 1 + max(depths) if depths else 1
        
        elif node_type == 'LocalSearch':
            return 1
        
        else:
            return 1
    
    def count_nodes(self, node: ASTNode) -> Dict[str, int]:
        """
        Cuenta nodos por tipo
        
        Args:
            node: Nodo raíz
        
        Returns:
            Diccionario con conteo por tipo
        """
        counts = {}
        
        def _count(n: ASTNode):
            node_type = n.__class__.__name__
            counts[node_type] = counts.get(node_type, 0) + 1
            
            if node_type == 'Seq':
                for stmt in n.body:
                    _count(stmt)
            elif node_type == 'If':
                _count(n.then_branch)
                if n.else_branch:
                    _count(n.else_branch)
            elif node_type in ['While', 'For', 'ChooseBestOf', 'ApplyUntilNoImprove']:
                _count(n.body)
        
        _count(node)
        return counts
    
    def get_statistics(self, node: ASTNode) -> Dict[str, Any]:
        """
        Obtiene estadísticas del AST
        
        Args:
            node: Nodo raíz
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'depth': self.get_depth(node),
            'node_counts': self.count_nodes(node),
            'total_nodes': sum(self.count_nodes(node).values()),
            'is_valid': len(self.validate_ast(node)) == 0,
            'errors': self.validate_ast(node)
        }
