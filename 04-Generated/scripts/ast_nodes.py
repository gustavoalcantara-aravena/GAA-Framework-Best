"""
Nodos del AST - Template Base GAA

Este archivo se genera automáticamente desde 01-System/AST-Nodes.md
Define la jerarquía de nodos para representar algoritmos como AST.

AUTO-GENERATED - DO NOT EDIT MANUALLY
Edita: 01-System/AST-Nodes.md o 01-System/Grammar.md
"""

from typing import List, Any, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random


# ============================================================================
# NODOS BASE
# ============================================================================

class ASTNode(ABC):
    """Clase base abstracta para todos los nodos del AST"""
    
    def __init__(self):
        self.parent: Optional['ASTNode'] = None
        self.depth: int = 0
    
    @abstractmethod
    def execute(self, context: dict) -> Any:
        """Ejecuta el nodo en un contexto dado"""
        pass
    
    @abstractmethod
    def copy(self) -> 'ASTNode':
        """Crea una copia profunda del nodo"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Retorna el número total de nodos en el subárbol"""
        pass
    
    @abstractmethod
    def to_string(self, indent: int = 0) -> str:
        """Representación en string del AST"""
        pass
    
    def get_all_nodes(self) -> List['ASTNode']:
        """Retorna lista de todos los nodos del subárbol"""
        return [self]


# ============================================================================
# NODOS DE CONTROL
# ============================================================================

@dataclass
class Seq(ASTNode):
    """Secuencia de statements"""
    statements: List[ASTNode] = field(default_factory=list)
    
    def execute(self, context: dict) -> Any:
        result = None
        for stmt in self.statements:
            result = stmt.execute(context)
        return result
    
    def copy(self) -> 'Seq':
        return Seq([s.copy() for s in self.statements])
    
    def size(self) -> int:
        return 1 + sum(s.size() for s in self.statements)
    
    def to_string(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}Seq("]
        for stmt in self.statements:
            lines.append(stmt.to_string(indent + 1))
        lines.append(f"{prefix})")
        return "\n".join(lines)
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        for stmt in self.statements:
            nodes.extend(stmt.get_all_nodes())
        return nodes


@dataclass
class If(ASTNode):
    """Condicional if-then-else"""
    condition: ASTNode
    then_branch: ASTNode
    else_branch: ASTNode
    
    def execute(self, context: dict) -> Any:
        if self.condition.execute(context):
            return self.then_branch.execute(context)
        else:
            return self.else_branch.execute(context)
    
    def copy(self) -> 'If':
        return If(
            self.condition.copy(),
            self.then_branch.copy(),
            self.else_branch.copy()
        )
    
    def size(self) -> int:
        return 1 + self.condition.size() + self.then_branch.size() + self.else_branch.size()
    
    def to_string(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}If(\n{self.condition.to_string(indent+1)},\n{self.then_branch.to_string(indent+1)},\n{self.else_branch.to_string(indent+1)}\n{prefix})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        nodes.extend(self.condition.get_all_nodes())
        nodes.extend(self.then_branch.get_all_nodes())
        nodes.extend(self.else_branch.get_all_nodes())
        return nodes


@dataclass
class While(ASTNode):
    """Bucle while con presupuesto"""
    budget: ASTNode
    body: ASTNode
    
    def execute(self, context: dict) -> Any:
        max_iter = self.budget.execute(context)
        result = None
        for _ in range(max_iter):
            result = self.body.execute(context)
        return result
    
    def copy(self) -> 'While':
        return While(self.budget.copy(), self.body.copy())
    
    def size(self) -> int:
        return 1 + self.budget.size() + self.body.size()
    
    def to_string(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}While(\n{self.budget.to_string(indent+1)},\n{self.body.to_string(indent+1)}\n{prefix})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        nodes.extend(self.budget.get_all_nodes())
        nodes.extend(self.body.get_all_nodes())
        return nodes


@dataclass
class For(ASTNode):
    """Bucle for con número fijo de iteraciones"""
    iterations: ASTNode
    body: ASTNode
    
    def execute(self, context: dict) -> Any:
        n = self.iterations.execute(context)
        result = None
        for _ in range(n):
            result = self.body.execute(context)
        return result
    
    def copy(self) -> 'For':
        return For(self.iterations.copy(), self.body.copy())
    
    def size(self) -> int:
        return 1 + self.iterations.size() + self.body.size()
    
    def to_string(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}For(\n{self.iterations.to_string(indent+1)},\n{self.body.to_string(indent+1)}\n{prefix})"
    
    def get_all_nodes(self) -> List[ASTNode]:
        nodes = [self]
        nodes.extend(self.iterations.get_all_nodes())
        nodes.extend(self.body.get_all_nodes())
        return nodes


# ============================================================================
# NODOS DE CONDICIONES
# ============================================================================

@dataclass
class IsFeasible(ASTNode):
    """Verifica si la solución actual es factible"""
    
    def execute(self, context: dict) -> bool:
        problem = context['problem']
        current_sol = context['current_solution']
        return problem.is_feasible(current_sol)
    
    def copy(self) -> 'IsFeasible':
        return IsFeasible()
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return "  " * indent + "IsFeasible()"


@dataclass
class Improves(ASTNode):
    """Verifica si la nueva solución mejora la actual"""
    
    def execute(self, context: dict) -> bool:
        problem = context['problem']
        current = context['current_solution']
        candidate = context['candidate_solution']
        
        f_current = problem.evaluate(current)
        f_candidate = problem.evaluate(candidate)
        
        if problem.optimization_type == "maximize":
            return f_candidate > f_current
        else:
            return f_candidate < f_current
    
    def copy(self) -> 'Improves':
        return Improves()
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return "  " * indent + "Improves()"


@dataclass
class Prob(ASTNode):
    """Condición probabilística"""
    probability: float
    
    def execute(self, context: dict) -> bool:
        return random.random() < self.probability
    
    def copy(self) -> 'Prob':
        return Prob(self.probability)
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return f"{'  ' * indent}Prob({self.probability:.2f})"


# ============================================================================
# NODOS DE PRESUPUESTO
# ============================================================================

@dataclass
class IterBudget(ASTNode):
    """Presupuesto de iteraciones"""
    iterations: int
    
    def execute(self, context: dict) -> int:
        return self.iterations
    
    def copy(self) -> 'IterBudget':
        return IterBudget(self.iterations)
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return f"{'  ' * indent}IterBudget({self.iterations})"


@dataclass
class IntLiteral(ASTNode):
    """Literal entero"""
    value: int
    
    def execute(self, context: dict) -> int:
        return self.value
    
    def copy(self) -> 'IntLiteral':
        return IntLiteral(self.value)
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return f"{'  ' * indent}{self.value}"


# ============================================================================
# NODOS DE LLAMADA A TERMINALES
# ============================================================================

@dataclass
class Call(ASTNode):
    """Llamada a un terminal (operador del dominio)"""
    terminal_name: str
    terminal_func: Optional[Callable] = None
    
    def execute(self, context: dict) -> Any:
        if self.terminal_func:
            return self.terminal_func(context)
        
        # Buscar en contexto
        terminals = context.get('terminals', {})
        if self.terminal_name in terminals:
            return terminals[self.terminal_name](context)
        
        raise ValueError(f"Terminal no encontrado: {self.terminal_name}")
    
    def copy(self) -> 'Call':
        return Call(self.terminal_name, self.terminal_func)
    
    def size(self) -> int:
        return 1
    
    def to_string(self, indent: int = 0) -> str:
        return f"{'  ' * indent}Call({self.terminal_name})"


# ============================================================================
# UTILIDADES
# ============================================================================

def random_ast(max_depth: int = 3, terminals: List[str] = None) -> ASTNode:
    """Genera un AST aleatorio"""
    if terminals is None:
        terminals = ['Terminal1', 'Terminal2', 'Terminal3']
    
    if max_depth == 0:
        return Call(random.choice(terminals))
    
    node_types = [Seq, If, For, Call]
    node_type = random.choice(node_types)
    
    if node_type == Seq:
        n_stmts = random.randint(1, 3)
        return Seq([random_ast(max_depth - 1, terminals) for _ in range(n_stmts)])
    elif node_type == If:
        return If(
            Prob(random.random()),
            random_ast(max_depth - 1, terminals),
            random_ast(max_depth - 1, terminals)
        )
    elif node_type == For:
        return For(
            IntLiteral(random.randint(5, 20)),
            random_ast(max_depth - 1, terminals)
        )
    else:
        return Call(random.choice(terminals))


if __name__ == "__main__":
    # Ejemplo de uso
    ast = random_ast(max_depth=2)
    print(ast.to_string())
    print(f"\nTamaño del AST: {ast.size()} nodos")
    print(f"Total de nodos: {len(ast.get_all_nodes())}")
