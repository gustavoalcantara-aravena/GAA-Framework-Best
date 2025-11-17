---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Metaheuristic.md
    - 01-System/Grammar.md
  auto_sync: true
---

# Operadores de Búsqueda sobre AST

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Metaheuristic.md` y `Grammar.md`.

## Operadores de Mutación

### Mutación de Nodo Función

```python
def mutate_function_node(ast, grammar):
    """
    Selecciona un nodo función aleatorio y lo reemplaza
    por otro compatible según la gramática.
    """
    # Seleccionar nodo aleatorio que sea función
    node = select_random_function_node(ast)
    
    # Obtener funciones compatibles (misma aridad)
    compatible_functions = grammar.get_compatible_functions(node.arity)
    
    # Reemplazar por función aleatoria compatible
    new_function = random.choice(compatible_functions)
    replace_node(ast, node, new_function)
    
    return ast
```

### Mutación de Terminal

```python
def mutate_terminal_node(ast, grammar):
    """
    Selecciona un nodo terminal aleatorio y lo reemplaza
    por otro terminal del dominio.
    """
    # Seleccionar nodo terminal aleatorio
    terminal_node = select_random_terminal_node(ast)
    
    # Obtener terminales disponibles
    available_terminals = grammar.get_terminals()
    
    # Reemplazar por terminal aleatorio
    new_terminal = random.choice(available_terminals)
    replace_node(ast, terminal_node, new_terminal)
    
    return ast
```

### Mutación de Parámetro

```python
def mutate_parameter(ast, delta_percent=0.1):
    """
    Selecciona un parámetro numérico y lo modifica ±δ%
    """
    # Seleccionar nodo con parámetros numéricos
    node = select_node_with_parameters(ast)
    
    # Seleccionar parámetro aleatorio
    param_name = random.choice(list(node.parameters.keys()))
    old_value = node.parameters[param_name]
    
    # Perturbar valor
    delta = old_value * delta_percent * random.choice([-1, 1])
    new_value = old_value + delta
    
    node.parameters[param_name] = new_value
    
    return ast
```

## Operadores de Crossover

### Subtree Crossover

```python
def subtree_crossover(ast1, ast2):
    """
    Intercambia subárboles aleatorios entre dos AST.
    """
    # Seleccionar puntos de corte aleatorios
    node1 = select_random_node(ast1)
    node2 = select_random_node(ast2)
    
    # Intercambiar subárboles
    offspring1 = clone_ast(ast1)
    offspring2 = clone_ast(ast2)
    
    swap_subtrees(offspring1, node1, offspring2, node2)
    
    return offspring1, offspring2
```

## Operadores de Perturbación

### Destroy-Repair

```python
def destroy_repair(ast, destroy_ratio=0.3):
    """
    Destruye una porción del AST y la reconstruye aleatoriamente.
    """
    # Seleccionar nodos a destruir
    num_nodes = count_nodes(ast)
    num_destroy = int(num_nodes * destroy_ratio)
    
    nodes_to_destroy = random.sample(get_all_nodes(ast), num_destroy)
    
    # Destruir (convertir a placeholders)
    for node in nodes_to_destroy:
        replace_with_placeholder(ast, node)
    
    # Reparar (generar nodos aleatorios válidos)
    for placeholder in get_placeholders(ast):
        new_node = generate_random_valid_node(grammar, placeholder.context)
        replace_node(ast, placeholder, new_node)
    
    return ast
```

## Validación Post-Operador

```python
def validate_and_repair(ast, grammar):
    """
    Valida que el AST cumpla la gramática y repara si es necesario.
    """
    if not is_valid_ast(ast, grammar):
        # Estrategias de reparación
        ast = repair_invalid_nodes(ast, grammar)
        ast = ensure_valid_structure(ast, grammar)
    
    return ast
```

## Configuración de Operadores

<!-- AUTO-GENERATED from 00-Core/Metaheuristic.md::Search-Strategy -->
```python
# [Pendiente de extracción]
# Probabilidades de aplicación de cada operador
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
PERTURBATION_RATE = 0.05
```
<!-- END AUTO-GENERATED -->

---

## Estado de Sincronización

⏳ Pendiente de sincronización con `Metaheuristic.md`
