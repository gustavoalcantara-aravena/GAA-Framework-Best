# Guía de Uso del Framework GAA

## ✅ Estructura Creada Exitosamente

El framework GAA ha sido generado con **automatización completa** entre archivos .md y generación de scripts.

## 📁 Estructura del Proyecto

```
GAA/
├── 🎯 GAA-Agent-System-Prompt.md       # Prompt base (COORDINA TODO)
├── 📖 README.md                         # Documentación principal
│
├── .gaa-config/                         # Sistema de sincronización
│   ├── dependency-graph.json            # Grafo de dependencias
│   ├── sync-rules.json                  # Reglas de extracción
│   └── project-state.json               # Estado actual
│
├── 00-Core/                             # ✏️ ARCHIVOS EDITABLES
│   ├── Problem.md                       # 🎯 EDITA AQUÍ tu problema
│   ├── Metaheuristic.md                 # 🎯 EDITA AQUÍ tu metaheurística
│   ├── Project-Config.md                # [Auto] Estado del proyecto
│   └── Sync-Log.md                      # [Auto] Historial de cambios
│
├── 01-System/                           # Sistema GAA base
│   ├── Grammar.md                       # [Auto] BNF con terminales
│   ├── AST-Nodes.md                     # [Auto] Clases de nodos
│   └── Code-Templates.md                # Plantillas de código
│
├── 02-Components/                       # Componentes del sistema
│   ├── Fitness-Function.md              # [Auto] Función de evaluación
│   ├── Search-Operators.md              # [Auto] Operadores búsqueda
│   └── Evaluator.md                     # [Auto] Evaluador
│
├── 03-Experiments/                      # Experimentación
│   ├── Experimental-Design.md           # [Auto] Protocolo
│   ├── Instances.md                     # [Auto] Catálogo
│   └── Metrics.md                       # [Auto] Métricas
│
├── 04-Generated/                        # 🔨 Código Python generado
│   ├── Generation-Plan.md               # Plan de generación
│   ├── _metadata.yaml                   # Metadata de scripts
│   └── scripts/                         # Aquí van los .py
│
├── 05-Automation/                       # ⚙️ Motor de automatización
│   ├── sync-engine.py                   # Script principal
│   └── README.md                        # Documentación
│
└── 06-Datasets/                         # 📊 Instancias del problema
    ├── training/                        # Para optimizar AST
    ├── validation/                      # Para validar
    ├── test/                            # Para evaluación final
    ├── benchmark/                       # Instancias estándar
    ├── Dataset-Specification.md         # [Auto] Formato de datos
    └── README.md                        # Instrucciones
```

## 🚀 Workflow Automatizado

### 1️⃣ Definir el Problema

Edita `00-Core/Problem.md`:

```markdown
## Problema Seleccionado
**Nombre**: Knapsack Problem
**Tipo**: Maximización

## Domain-Operators
- **GreedyByValue**: Inserta ítems por valor decreciente [Dantzig1957]
- **FlipWorstItem**: Remueve ítem con peor ratio [Martello1990]
- **SwapItems**: Intercambia ítems [Pisinger2005]

## Mathematical-Model
Maximizar: sum(v_i * x_i)
Sujeto a: sum(w_i * x_i) <= W
```

### 2️⃣ Sincronizar Automáticamente

```bash
cd GAA
python 05-Automation/sync-engine.py --sync
```

**Resultado**: El motor extrae automáticamente:
- ✅ Terminales de `Domain-Operators` → `01-System/Grammar.md`
- ✅ Función objetivo de `Mathematical-Model` → `02-Components/Fitness-Function.md`
- ✅ Formato de datos de `Solution-Representation` → `06-Datasets/Dataset-Specification.md`

### 3️⃣ Verificar Sincronización

```bash
python 05-Automation/sync-engine.py --validate
```

### 4️⃣ Definir Metaheurística

Edita `00-Core/Metaheuristic.md`:

```markdown
## Selected-Metaheuristic
**Algoritmo**: Simulated Annealing

## Configuration
- **Temperatura inicial**: T₀ = 100
- **Factor de enfriamiento**: α = 0.95
- **Iteraciones por temp**: L = 100

## Search-Strategy
- Mutación de nodo
- Mutación de terminal
- Criterio Metropolis
```

### 5️⃣ Sincronizar Nuevamente

```bash
python 05-Automation/sync-engine.py --sync
```

**Resultado**:
- ✅ Operadores extraídos → `02-Components/Search-Operators.md`
- ✅ Scripts marcados para regeneración

### 6️⃣ Agregar Datasets

Coloca tus instancias en:
```
06-Datasets/
├── training/instance1.txt
├── training/instance2.txt
├── test/testA.txt
└── test/testB.txt
```

### 7️⃣ Generar Scripts Python (Próximamente)

```bash
python 05-Automation/sync-engine.py --generate
```

Generará en `04-Generated/scripts/`:
- `problem.py` - Clase del problema
- `ast_nodes.py` - Nodos del AST
- `metaheuristic.py` - Algoritmo de búsqueda
- `fitness.py` - Evaluador de AST
- `data_loader.py` - Cargador de instancias
- `main.py` - Script principal

## 🔄 Diagrama de Flujo de Sincronización

```
┌─────────────────┐
│   Problem.md    │ ◄── Usuario edita
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ sync-engine.py  │ ◄── Detecta cambios
└────────┬────────┘
         │
         ├──► Grammar.md (extrae terminales)
         ├──► Fitness-Function.md (extrae objetivo)
         ├──► Dataset-Specification.md (extrae formato)
         └──► Marca: problem.py, fitness.py

┌─────────────────────┐
│ Metaheuristic.md    │ ◄── Usuario edita
└──────────┬──────────┘
           │
           ▼
    ┌─────────────────┐
    │ sync-engine.py  │
    └──────────┬──────┘
               │
               ├──► Search-Operators.md
               └──► Marca: metaheuristic.py
```

## 📊 Archivos con Metadatos YAML

Cada `.md` auto-generado tiene frontmatter:

```yaml
---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
  sync_rules:
    - source: "00-Core/Problem.md::Domain-Operators"
      action: "extract_terminals"
      target: "section:Terminals"
  auto_sync: true
---
```

## 🎯 Secciones AUTO-GENERATED

Los archivos sincronizados tienen marcadores:

```markdown
<!-- AUTO-GENERATED from 00-Core/Problem.md::Domain-Operators -->
<Terminal> ::= GreedyByValue 
             | FlipWorstItem 
             | SwapItems
<!-- END AUTO-GENERATED -->
```

**No edites entre estos marcadores** - se sobrescribirán en la próxima sincronización.

## 🛠️ Comandos Disponibles

```bash
# Sincronizar después de editar Problem.md o Metaheuristic.md
python 05-Automation/sync-engine.py --sync

# Validar consistencia
python 05-Automation/sync-engine.py --validate

# Generar scripts Python (en desarrollo)
python 05-Automation/sync-engine.py --generate

# Ver estado del proyecto
cat 00-Core/Project-Config.md

# Ver log de sincronizaciones
cat 00-Core/Sync-Log.md
```

## ✅ Checklist de Uso

- [ ] Completar `00-Core/Problem.md` (todas las secciones)
- [ ] Ejecutar `sync-engine.py --sync`
- [ ] Verificar que `01-System/Grammar.md` tiene tus terminales
- [ ] Completar `00-Core/Metaheuristic.md`
- [ ] Ejecutar `sync-engine.py --sync` nuevamente
- [ ] Agregar datasets en `06-Datasets/training/`
- [ ] Validar con `sync-engine.py --validate`
- [ ] Generar scripts con `sync-engine.py --generate`

## 🎓 Próximos Pasos

1. **Lee el README.md** para entender el framework completo
2. **Revisa GAA-Agent-System-Prompt.md** para la metodología completa
3. **Edita Problem.md** con tu problema específico
4. **Ejecuta sincronización** y observa la magia ✨

## 💡 Características Clave

✅ **Sincronización automática** entre .md  
✅ **Extracción inteligente** de terminales, funciones, parámetros  
✅ **Trazabilidad completa** con logs y metadatos  
✅ **Validación de consistencia**  
✅ **Estructura modular** y escalable  
✅ **Datasets organizados** por propósito  
✅ **Generación de código** desde especificaciones  

## 📝 Notas Importantes

1. **Solo edita archivos en `00-Core/`** - El resto se sincroniza automáticamente
2. **Los marcadores `<!-- AUTO-GENERATED -->` indican contenido sincronizado**
3. **Ejecuta `--sync` después de cada edición** importante
4. **Usa `--validate` antes de generar** scripts
5. **Los datasets deben cumplir el formato** en Dataset-Specification.md

---

**¡Framework GAA listo para usar!** 🎉
