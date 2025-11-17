"""
AST Nodes - KBP-SA
Definición de nodos del Árbol Sintáctico Abstracto
Fase 3 GAA: Estructura de algoritmos

Basado en gramática BNF del GAA-Agent-System-Prompt
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json


class ASTNode(ABC):
    """Clase base para todos los nodos del AST"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el nodo a diccionario"""
        pass
    
    @abstractmethod
    def to_pseudocode(self, indent: int = 0) -> str:
        """Genera pseudocódigo legible"""
        pass
    
    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class Seq(ASTNode):
    """
    Secuencia de operaciones
    
    Sintaxis BNF: Seq(<Stmt>*)
    
    Ejemplo:
    ```
    Seq([
        GreedyConstruct("GreedyByRatio"),
        LocalSearch("FlipBestItem", "Improving")
    ])
    ```
    """
    body: List[ASTNode] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Seq",
            "body": [stmt.to_dict() for stmt in self.body]
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}SECUENCIA:"]
        for i, stmt in enumerate(self.body, 1):
            lines.append(f"{ind}  {i}. {stmt.to_pseudocode(indent + 1)}")
        return "\n".join(lines)


@dataclass
class If(ASTNode):
    """
    Condicional
    
    Sintaxis BNF: If(<Cond>, <Stmt>, <Stmt>)
    
    Condiciones disponibles:
    - IsFeasible(): verifica factibilidad
    - Improves(): verifica mejora
    - Prob(p): probabilidad p
    - Stagnation(): detecta estancamiento
    """
    condition: str
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None
    params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": "If",
            "cond": {"type": self.condition, **self.params},
            "then": self.then_branch.to_dict()
        }
        if self.else_branch:
            result["else"] = self.else_branch.to_dict()
        return result
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}SI {self.condition}:"]
        lines.append(self.then_branch.to_pseudocode(indent + 1))
        if self.else_branch:
            lines.append(f"{ind}SINO:")
            lines.append(self.else_branch.to_pseudocode(indent + 1))
        return "\n".join(lines)


@dataclass
class While(ASTNode):
    """
    Bucle con presupuesto
    
    Sintaxis BNF: While(<Bud>, <Stmt>)
    
    Presupuestos:
    - IterBudget(n): n iteraciones
    - TimeBudget(t): t segundos
    """
    budget_type: str  # "IterBudget" o "TimeBudget"
    budget_value: Union[int, float]
    body: ASTNode
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "While",
            "budget": {
                "kind": self.budget_type,
                "value": self.budget_value
            },
            "body": self.body.to_dict()
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        budget_str = f"{self.budget_value} iteraciones" if self.budget_type == "IterBudget" else f"{self.budget_value}s"
        lines = [f"{ind}MIENTRAS (presupuesto: {budget_str}):"]
        lines.append(self.body.to_pseudocode(indent + 1))
        return "\n".join(lines)


@dataclass
class For(ASTNode):
    """
    Bucle For con número fijo de iteraciones
    
    Sintaxis BNF: For(<Int>, <Stmt>)
    """
    iterations: int
    body: ASTNode
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "For",
            "iterations": self.iterations,
            "body": self.body.to_dict()
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}PARA i=1 HASTA {self.iterations}:"]
        lines.append(self.body.to_pseudocode(indent + 1))
        return "\n".join(lines)


@dataclass
class Call(ASTNode):
    """
    Llamada a terminal (operador del dominio)
    
    Sintaxis BNF: Call(<Terminal>)
    
    Terminales disponibles:
    - Constructivos: GreedyByValue, GreedyByRatio, etc.
    - Mejora: FlipBestItem, OneExchange, etc.
    - Perturbación: RandomFlip, ShakeByRemoval, etc.
    - Reparación: RepairByRemoval, RepairByGreedy
    """
    name: str
    args: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"type": "Call", "name": self.name}
        if self.args:
            result["args"] = self.args
        return result
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        args_str = f"({self.args})" if self.args else ""
        return f"{ind}LLAMAR {self.name}{args_str}"


@dataclass
class GreedyConstruct(ASTNode):
    """
    Construcción voraz
    
    Sintaxis BNF: GreedyConstruct(<Heuristic>)
    
    Heurísticas:
    - GreedyByValue
    - GreedyByWeight
    - GreedyByRatio
    - RandomConstruct
    """
    heuristic: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "GreedyConstruct",
            "heuristic": self.heuristic
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}CONSTRUIR_VORAZ usando {self.heuristic}"


@dataclass
class LocalSearch(ASTNode):
    """
    Búsqueda local
    
    Sintaxis BNF: LocalSearch(<Neighborhood>, <Acceptance>)
    
    Vecindarios:
    - FlipBestItem, FlipWorstItem
    - OneExchange, TwoExchange
    
    Criterios de aceptación:
    - Improving: solo acepta mejoras
    - Metropolis: criterio de Metropolis (SA)
    - FirstImproving: primera mejora encontrada
    """
    neighborhood: str
    acceptance: str = "Improving"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "LocalSearch",
            "neighborhood": self.neighborhood,
            "acceptance": self.acceptance
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}BUSQUEDA_LOCAL en {self.neighborhood} (aceptación: {self.acceptance})"


@dataclass
class ChooseBestOf(ASTNode):
    """
    Elige mejor solución de n intentos
    
    Sintaxis BNF: ChooseBestOf(<Int>, <Stmt>)
    """
    n_tries: int
    body: ASTNode
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ChooseBestOf",
            "n": self.n_tries,
            "body": self.body.to_dict()
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}ELEGIR_MEJOR_DE {self.n_tries} intentos:"]
        lines.append(self.body.to_pseudocode(indent + 1))
        return "\n".join(lines)


@dataclass
class ApplyUntilNoImprove(ASTNode):
    """
    Aplica operación hasta no mejorar
    
    Sintaxis BNF: ApplyUntilNoImprove(<Stmt>, <Stop>)
    
    Condiciones de parada:
    - MaxIter: máximo de iteraciones
    - Stagnation: número de iteraciones sin mejora
    """
    body: ASTNode
    stop_condition: str = "Stagnation"
    stop_value: int = 10
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ApplyUntilNoImprove",
            "body": self.body.to_dict(),
            "stop": {
                "type": self.stop_condition,
                "value": self.stop_value
            }
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        lines = [f"{ind}APLICAR_HASTA_NO_MEJORAR (parada: {self.stop_condition}={self.stop_value}):"]
        lines.append(self.body.to_pseudocode(indent + 1))
        return "\n".join(lines)


@dataclass
class DestroyRepair(ASTNode):
    """
    Destrucción y reparación
    
    Sintaxis BNF: DestroyRepair(<Destroy>, <Repair>)
    """
    destroy_op: str
    repair_op: str
    destruction_rate: float = 0.3
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "DestroyRepair",
            "destroy": self.destroy_op,
            "repair": self.repair_op,
            "rate": self.destruction_rate
        }
    
    def to_pseudocode(self, indent: int = 0) -> str:
        ind = "  " * indent
        return f"{ind}DESTRUIR_REPARAR: {self.destroy_op} → {self.repair_op} (rate={self.destruction_rate})"


# Funciones auxiliares para construcción de AST

def parse_json_ast(json_data: Union[str, Dict]) -> ASTNode:
    """
    Parsea AST desde JSON
    
    Args:
        json_data: String JSON o diccionario
    
    Returns:
        Nodo raíz del AST
    """
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    node_type = data["type"]
    
    if node_type == "Seq":
        return Seq(body=[parse_json_ast(stmt) for stmt in data["body"]])
    elif node_type == "If":
        return If(
            condition=data["cond"]["type"],
            then_branch=parse_json_ast(data["then"]),
            else_branch=parse_json_ast(data["else"]) if "else" in data else None,
            params={k: v for k, v in data["cond"].items() if k != "type"}
        )
    elif node_type == "While":
        return While(
            budget_type=data["budget"]["kind"],
            budget_value=data["budget"]["value"],
            body=parse_json_ast(data["body"])
        )
    elif node_type == "For":
        return For(
            iterations=data["iterations"],
            body=parse_json_ast(data["body"])
        )
    elif node_type == "Call":
        return Call(
            name=data["name"],
            args=data.get("args", {})
        )
    elif node_type == "GreedyConstruct":
        return GreedyConstruct(heuristic=data["heuristic"])
    elif node_type == "LocalSearch":
        return LocalSearch(
            neighborhood=data["neighborhood"],
            acceptance=data.get("acceptance", "Improving")
        )
    elif node_type == "ChooseBestOf":
        return ChooseBestOf(
            n_tries=data["n"],
            body=parse_json_ast(data["body"])
        )
    elif node_type == "ApplyUntilNoImprove":
        return ApplyUntilNoImprove(
            body=parse_json_ast(data["body"]),
            stop_condition=data["stop"]["type"],
            stop_value=data["stop"]["value"]
        )
    elif node_type == "DestroyRepair":
        return DestroyRepair(
            destroy_op=data["destroy"],
            repair_op=data["repair"],
            destruction_rate=data.get("rate", 0.3)
        )
    else:
        raise ValueError(f"Tipo de nodo desconocido: {node_type}")
