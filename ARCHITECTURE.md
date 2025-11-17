# Arquitectura del Framework GAA
# Generación Automática de Algoritmos

## 📐 Visión General

El framework GAA (Generación Automática de Algoritmos) es un sistema para evolucionar automáticamente algoritmos de optimización representados como **Abstract Syntax Trees (AST)**.

### Conceptos Clave

1. **Algoritmos como AST**: Los algoritmos son representados como árboles sintácticos que pueden ser manipulados mediante operadores genéticos.

2. **Gramática BNF**: Define el espacio de búsqueda de algoritmos válidos, incluyendo estructuras de control y terminales específicos del dominio.

3. **Terminales del Dominio**: Operadores específicos del problema (e.g., construcción voraz, búsqueda local) extraídos de la literatura.

4. **Metaheurística**: Algoritmo evolutivo (SA, GP, etc.) que explora el espacio de ASTs buscando el mejor algoritmo.

5. **Evaluación Multi-instancia**: Los algoritmos se evalúan en múltiples instancias del problema para medir su generalización.

---

## 🏗️ Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE USUARIO                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Problem.md   │  │Metaheur.md   │  │  Projects/   │      │
│  │ (Trigger)    │  │ (Trigger)    │  │  KBP-SA/     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘      │
└─────────┼──────────────────┼──────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│              MOTOR DE SINCRONIZACIÓN                         │
│  ┌───────────────────────────────────────────────────┐      │
│  │  sync-engine.py                                    │      │
│  │  - Detecta cambios (MD5 hashing)                  │      │
│  │  - Extrae secciones (YAML + regex)                │      │
│  │  - Actualiza dependientes                         │      │
│  │  - Genera código Python                           │      │
│  └───────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              ARCHIVOS AUTO-GENERADOS                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Grammar.md  │  │ Fitness.md  │  │ Scripts/    │         │
│  │ (BNF)       │  │ (Evaluador) │  │ .py         │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              NÚCLEO DE EJECUCIÓN                             │
│  ┌──────────────────────────────────────────────────┐       │
│  │  AST Nodes        Problem         Fitness        │       │
│  │  (Nodos)          (Problema)      (Evaluador)    │       │
│  │     │                │                │          │       │
│  │     └────────────────┴────────────────┘          │       │
│  │                      │                           │       │
│  │                      ▼                           │       │
│  │              Metaheuristic                       │       │
│  │              (SA, GP, ILS, GRASP)                │       │
│  │                      │                           │       │
│  │                      ▼                           │       │
│  │              Best Algorithm (AST)                │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Trabajo

### 1. Definición del Problema (Usuario)

```mermaid
Problem.md (editado)
    │
    ├─► Modelo matemático
    ├─► Restricciones
    ├─► Operadores del dominio (terminales)
    └─► Representación de soluciones
```

### 2. Sincronización Automática

```python
sync-engine.py --sync
    │
    ├─► Detecta cambio en Problem.md (MD5)
    ├─► Extrae sección "Domain-Operators"
    ├─► Actualiza Grammar.md (terminales BNF)
    ├─► Actualiza Fitness-Function.md
    ├─► Genera problem.py
    └─► Registra en Sync-Log.md
```

### 3. Generación de Código

```
04-Generated/scripts/
    ├─► problem.py         (Clases Problem, Solution)
    ├─► ast_nodes.py       (Nodos del AST: If, While, Call, etc.)
    ├─► fitness.py         (FitnessEvaluator)
    ├─► metaheuristic.py   (SA, GP, ILS, GRASP)
    └─► data_loader.py     (Carga de datasets)
```

### 4. Ejecución

```python
# projects/KBP-SA/run.py

1. Cargar config.yaml
2. Cargar datasets (training, validation, test)
3. Crear problema (KnapsackProblem)
4. Crear evaluador (FitnessEvaluator)
5. Ejecutar metaheurística (SimulatedAnnealing)
6. Obtener mejor algoritmo (AST)
7. Guardar resultados
```

---

## 📊 Estructura de Datos

### AST Node (Ejemplo)

```python
Seq(
  Call(GreedyByRatio),        # Terminal: construcción voraz
  For(
    IntLiteral(100),
    If(
      Improves(),
      Call(TwoExchange),      # Terminal: mejora local
      Call(RandomFlip)        # Terminal: perturbación
    )
  )
)
```

### Contexto de Ejecución

```python
context = {
    'problem': KnapsackProblem(instance),
    'current_solution': Solution([0,1,0,1,...]),
    'best_solution': Solution([...]),
    'best_fitness': 245.0,
    'evaluations': 1523,
    'max_evaluations': 10000,
    'terminals': {
        'GreedyByRatio': function,
        'TwoExchange': function,
        ...
    }
}
```

---

## 🔌 Puntos de Extensión

### 1. Nuevos Problemas

```python
# En problem.py
class NewProblem(Problem):
    def evaluate(self, solution):
        # Implementar función objetivo
        pass
    
    def is_feasible(self, solution):
        # Verificar restricciones
        pass
    
    def repair(self, solution):
        # Reparar soluciones infactibles
        pass
```

### 2. Nuevos Terminales

```python
# En problema_metaheuristica.md
## Domain-Operators

### Mi Nuevo Operador
- **NewOperator**: Descripción del operador [Autor2024]
```

Automáticamente se:
- Añade a Grammar.md
- Incluye en terminales disponibles
- Documenta en AST-Nodes.md

### 3. Nuevas Metaheurísticas

```python
# En metaheuristic.py
class NuevaMetaheuristica(Metaheuristic):
    def optimize(self):
        # Implementar lógica de búsqueda
        pass
```

---

## 🎯 Dependencias entre Archivos

```yaml
Problem.md (trigger):
  - Grammar.md ← terminales
  - Fitness-Function.md ← función objetivo
  - Dataset-Specification.md ← formato
  - problem.py ← clases Python

Metaheuristic.md (trigger):
  - Search-Operators.md ← mutación/crossover
  - Experimental-Design.md ← parámetros
  - metaheuristic.py ← implementación

Grammar.md (auto):
  - AST-Nodes.md ← definiciones de nodos
  - ast_nodes.py ← clases Python
```

---

## 📈 Pipeline de Evaluación

```
Algoritmo (AST)
    │
    ├─► Instancia 1 → ejecutar → fitness_1
    ├─► Instancia 2 → ejecutar → fitness_2
    ├─► Instancia 3 → ejecutar → fitness_3
    │
    └─► Fitness Final = mean(fitness_1, fitness_2, fitness_3)
```

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Propósito |
|------------|-----------|-----------|
| **Representación** | Python AST | Manipulación de árboles sintácticos |
| **Gramática** | BNF | Definir espacio de búsqueda válido |
| **Configuración** | YAML | Metadata y configuración |
| **Sincronización** | MD5 + Regex | Detección de cambios |
| **Optimización** | SA/GP/ILS/GRASP | Evolución de algoritmos |
| **Datos** | NumPy/Pandas | Procesamiento numérico |
| **Visualización** | Matplotlib | Gráficas de convergencia |

---

## 🔐 Garantías de Consistencia

1. **MD5 Hashing**: Detecta cambios reales en archivos
2. **YAML Frontmatter**: Metadata versionada en cada archivo
3. **Dependency Graph**: Grafo acíclico dirigido de dependencias
4. **Sync Log**: Trazabilidad completa de sincronizaciones
5. **Validation**: Verificación antes de generar código

---

## 📝 Convenciones

### Archivos Markdown

- **Triggers** (editables): `00-Core/Problem.md`, `00-Core/Metaheuristic.md`
- **Auto-generados**: Marcados con `<!-- AUTO-GENERATED -->` y `type: auto_generated`
- **YAML Frontmatter**: Obligatorio en todos los `.md`

### Archivos Python

- **Templates**: En `04-Generated/scripts/`
- **Implementaciones**: Usuario extiende classes base
- **Docstrings**: Formato Google style

### Datasets

- **Formato**: Específico por problema (ver `Dataset-Specification.md`)
- **Subsets**: `training/`, `validation/`, `test/`, `benchmark/`
- **Naming**: Descriptivo con tamaño (e.g., `kp_n100_W500.txt`)

---

## 🚀 Próximos Pasos

1. **Code Generation**: Completar generación automática de `.py` desde `.md`
2. **Watch Mode**: Sincronización en tiempo real
3. **GUI**: Interfaz gráfica para visualizar ASTs
4. **Multi-objetivo**: Soporte para optimización multi-objetivo
5. **Paralelización**: Evaluación paralela en múltiples núcleos
6. **Cloud**: Ejecución distribuida en cluster

---

**Fecha**: 2025-11-17  
**Versión**: 1.0.0  
**Autor**: GAA Framework Team
