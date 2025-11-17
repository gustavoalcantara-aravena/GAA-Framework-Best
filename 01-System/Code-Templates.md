# Plantillas de Generación de Código

> Plantillas reutilizables para generar código Python desde los .md

## Template: Terminal Class

```python
class {{TERMINAL_NAME}}(Terminal):
    """
    {{DESCRIPTION}}
    Referencia: {{CITATION}}
    """
    
    def __init__(self, {{PARAMETERS}}):
        super().__init__(name="{{TERMINAL_NAME}}")
        {{PARAMETER_ASSIGNMENTS}}
    
    def execute(self, context):
        """
        {{EXECUTION_DESCRIPTION}}
        """
        solution = context.current_solution
        problem = context.problem
        
        # TODO: Implementar lógica específica
        {{IMPLEMENTATION_PLACEHOLDER}}
        
        context.current_solution = solution
        return solution
    
    def to_json(self):
        return {
            "type": "Call",
            "name": "{{TERMINAL_NAME}}",
            "args": {{PARAMETERS_DICT}}
        }
```

## Template: Problem Class

```python
class {{PROBLEM_NAME}}(Problem):
    """
    {{PROBLEM_DESCRIPTION}}
    
    Tipo: {{OPTIMIZATION_TYPE}}
    """
    
    def __init__(self, instance_path: str):
        super().__init__(name="{{PROBLEM_NAME}}")
        self.load_instance(instance_path)
    
    def load_instance(self, path: str):
        """Carga instancia desde archivo"""
        # {{LOADING_LOGIC}}
        pass
    
    def evaluate(self, solution) -> float:
        """
        {{OBJECTIVE_FUNCTION}}
        """
        # {{EVALUATION_LOGIC}}
        pass
    
    def is_feasible(self, solution) -> bool:
        """
        {{CONSTRAINTS}}
        """
        # {{FEASIBILITY_LOGIC}}
        pass
```

## Template: Metaheuristic Class

```python
class {{METAHEURISTIC_NAME}}:
    """
    {{METAHEURISTIC_DESCRIPTION}}
    """
    
    def __init__(self, {{PARAMETERS}}):
        {{PARAMETER_ASSIGNMENTS}}
    
    def optimize(self, initial_ast, problem, instances, budget):
        """
        Optimiza el AST usando {{METAHEURISTIC_NAME}}
        """
        current_ast = initial_ast
        best_ast = current_ast
        best_fitness = self.evaluate_ast(current_ast, problem, instances)
        
        {{OPTIMIZATION_LOOP}}
        
        return best_ast, best_fitness
    
    def evaluate_ast(self, ast, problem, instances):
        """Evalúa un AST en el conjunto de instancias"""
        results = []
        for instance in instances:
            result = ast.execute(ExecutionContext(problem, instance))
            results.append(result)
        return self.aggregate_results(results)
```
