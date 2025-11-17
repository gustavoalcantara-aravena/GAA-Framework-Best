# Instrucciones de Ejecución - KBP-SA

## 🚀 Inicio Rápido

### 1. Verificar Instalación

```powershell
# Instalar dependencias
pip install -r ../../requirements.txt

# Verificar framework
python ../../05-Automation/sync-engine.py --validate
```

### 2. Preparar Datasets

**Opción A: Generar datasets de ejemplo**
```powershell
python generate_example_datasets.py
```

**Opción B: Usar tus propios datasets**

Coloca archivos `.txt` en las carpetas correspondientes:
- `datasets/training/` - Instancias para entrenar el GAA
- `datasets/validation/` - Instancias para ajustar parámetros
- `datasets/test/` - Instancias para evaluar el algoritmo final

**Formato del archivo:**
```
n W
v_1 w_1
v_2 w_2
...
v_n w_n
```

Ejemplo (`kp_n5_W50.txt`):
```
5 50
10 5
20 10
30 15
15 8
25 12
```

### 3. Validar Datasets

```powershell
python validate_datasets.py
```

Deberías ver:
```
✅ Todos los datasets son válidos
```

### 4. Ejecutar Optimización

```powershell
python run.py
```

**Salida esperada:**
```
======================================================================
  GAA - Generación Automática de Algoritmos
  Proyecto: KBP-SA (Knapsack + Simulated Annealing)
======================================================================

📊 Cargando datasets...
✅ Cargadas 3 instancias de training

🎯 Configurando problema...
⚖️  Configurando evaluador de fitness...
🔥 Configurando Simulated Annealing...

======================================================================
  INICIANDO OPTIMIZACIÓN
======================================================================

🔥 Simulated Annealing iniciado (T0=100.0, α=0.95)
  Eval 1000/10000 | T=0.5987 | Best=245.3421
  Eval 2000/10000 | T=0.3584 | Best=267.8934
  ...
```

### 5. Ver Resultados

Los resultados se guardan en `generated/results/`:
- `best_algorithm_YYYYMMDD_HHMMSS.txt` - AST del mejor algoritmo
- `history_YYYYMMDD_HHMMSS.json` - Historial de fitness

---

## ⚙️ Configuración Avanzada

### Modificar Parámetros de SA

Edita `config.yaml`:

```yaml
metaheuristic:
  parameters:
    T0: 150.0              # ↑ Mayor exploración inicial
    alpha: 0.98            # ↑ Enfriamiento más lento
    iterations_per_temp: 150
    max_evaluations: 20000 # ↑ Más evaluaciones
```

### Cambiar Terminales Disponibles

Edita `problema_metaheuristica.md` sección `Domain-Operators`:

```markdown
## Domain-Operators

### Constructivos
- **GreedyByValue**: ...
- **MiNuevoOperador**: Descripción [Autor2024]
```

Luego sincroniza:
```powershell
python ../../05-Automation/sync-engine.py --sync
```

---

## 📊 Análisis de Resultados

### Leer el AST Generado

```python
# analyze_results.py
from pathlib import Path

# Leer AST
ast_file = Path("generated/results/best_algorithm_20251117_143052.txt")
with open(ast_file, 'r') as f:
    ast_content = f.read()

print(ast_content)
```

### Visualizar Convergencia

```python
import json
import matplotlib.pyplot as plt

# Cargar historial
with open("generated/results/history_20251117_143052.json", 'r') as f:
    history = json.load(f)

# Graficar
evals = [h['evaluation'] for h in history]
fitness = [h['best_fitness'] for h in history]

plt.plot(evals, fitness)
plt.xlabel('Evaluaciones')
plt.ylabel('Mejor Fitness')
plt.title('Convergencia del SA')
plt.grid(True)
plt.savefig('generated/convergence.png')
plt.show()
```

---

## 🐛 Troubleshooting

### Error: "No se encontraron instancias"

**Causa**: No hay archivos en `datasets/training/`

**Solución**:
```powershell
python generate_example_datasets.py
```

### Error: "Campo faltante: n"

**Causa**: Formato de dataset incorrecto

**Solución**: Verifica que la primera línea tenga `n W` y las siguientes `v w`

### Error: "No se ha podido resolver la importación numpy"

**Causa**: Dependencias no instaladas

**Solución**:
```powershell
pip install -r ../../requirements.txt
```

### Performance lento

**Causas posibles**:
- Demasiadas instancias de entrenamiento
- `max_evaluations` muy alto
- Instancias muy grandes

**Solución**: Reduce parámetros en `config.yaml`

---

## 📈 Próximos Pasos

1. **Ajustar parámetros**: Experimenta con diferentes valores de `T0`, `alpha`
2. **Más datasets**: Añade más instancias variadas
3. **Comparar metaheurísticas**: Prueba GP en lugar de SA
4. **Visualización**: Genera gráficas de convergencia
5. **Benchmarking**: Compara con algoritmos conocidos

---

**Última actualización**: 2025-11-17
