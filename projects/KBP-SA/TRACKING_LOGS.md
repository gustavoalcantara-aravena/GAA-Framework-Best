# Sistema de Tracking Logs - KBP-SA

Este documento describe el sistema de logs de trackeo para variables calculadas por los algoritmos durante la experimentación.

---

## 📊 Variables Trackeadas

### 1. **Variables de Ejecución Principal**

| Variable | Descripción | Tipo | Rango/Unidad |
|----------|-------------|------|--------------|
| `iteration` | Número de iteración actual | int | [0, max_iterations] |
| `temperature` | Temperatura actual del SA | float | [T_min, T0] |
| `current_value` | Valor de la solución actual | int | [0, optimal] |
| `best_value` | Mejor valor encontrado | int | [0, optimal] |
| `current_weight` | Peso total de la solución actual | int | [0, capacity] |
| `best_weight` | Peso de la mejor solución | int | [0, capacity] |
| `is_feasible` | ¿Solución actual es factible? | bool | True/False |
| `delta_E` | Diferencia de energía (valor vecino - actual) | float | ℝ |
| `acceptance_probability` | Probabilidad de aceptación (Metropolis) | float | [0.0, 1.0] |
| `accepted` | ¿Vecino fue aceptado? | bool | True/False |
| `elapsed_time` | Tiempo transcurrido | float | segundos |

### 2. **Variables de Convergencia**

| Variable | Descripción | Tipo | Guardado |
|----------|-------------|------|----------|
| `gap_to_optimal` | Gap relativo al óptimo (%) | float | Por iteración |
| `improvement_count` | Número de mejoras acumuladas | int | Por iteración |
| `stagnation_counter` | Iteraciones sin mejora | int | Por iteración |
| `acceptance_rate_window` | Tasa de aceptación (ventana móvil) | float | Por temperatura |
| `diversity` | Diversidad de soluciones exploradas | float | Por nivel de T |

### 3. **Variables de Evaluación**

| Variable | Descripción | Tipo | Guardado |
|----------|-------------|------|----------|
| `evaluations` | Total de evaluaciones realizadas | int | Acumulativo |
| `feasible_evaluations` | Evaluaciones con soluciones factibles | int | Acumulativo |
| `infeasible_evaluations` | Evaluaciones con soluciones infactibles | int | Acumulativo |
| `best_value_history` | Historial del mejor valor | List[int] | Por iteración |

---

## 📁 Estructura de Archivos de Log

### Ubicación

Todos los logs se guardan en:

```
output/
└── {dataset_group}/                    # ej: low_dimensional, large_scale
    └── {instance_name}/                # ej: f1_l-d_kp_10_269
        ├── summary.json                # Resumen de la ejecución
        ├── tracking_full.csv           # Log completo por iteración
        ├── tracking_temperature.csv    # Log por nivel de temperatura
        ├── tracking_acceptance.csv     # Log de aceptaciones
        ├── convergence.json            # Datos de convergencia
        └── metadata.json               # Metadata del experimento
```

### Ejemplo de Ruta Completa

```
output/low_dimensional/f1_l-d_kp_10_269/tracking_full.csv
```

---

## 📝 Formato de Archivos

### 1. `tracking_full.csv`

Log detallado **por iteración** (puede ser muy grande):

```csv
iteration,temperature,current_value,best_value,current_weight,best_weight,is_feasible,delta_E,acceptance_prob,accepted,elapsed_time,gap_to_optimal
0,100.0,150,150,45,45,True,0.0,1.0,False,0.001,44.24
1,100.0,145,150,42,45,True,-5.0,0.0512,False,0.002,44.24
2,100.0,160,160,48,48,True,15.0,1.0,True,0.003,40.52
3,100.0,155,160,46,48,True,-5.0,0.0512,False,0.004,40.52
...
```

**Columnas:**
- `iteration`: Número de iteración
- `temperature`: Temperatura actual
- `current_value`: Valor de la solución actual
- `best_value`: Mejor valor encontrado hasta ahora
- `current_weight`: Peso de la solución actual
- `best_weight`: Peso de la mejor solución
- `is_feasible`: ¿Solución actual factible?
- `delta_E`: Diferencia de energía
- `acceptance_prob`: Probabilidad de aceptación calculada
- `accepted`: ¿Vecino aceptado?
- `elapsed_time`: Tiempo transcurrido (segundos)
- `gap_to_optimal`: Gap al óptimo conocido (%)

---

### 2. `tracking_temperature.csv`

Log agregado **por nivel de temperatura** (más compacto):

```csv
temperature_level,temperature,avg_value,best_value,avg_weight,acceptance_rate,improvements,iterations,elapsed_time
0,100.0,155.3,160,46.2,0.65,3,100,0.15
1,95.0,158.7,165,47.8,0.58,2,100,0.30
2,90.25,162.1,168,48.3,0.51,1,100,0.45
...
```

**Columnas:**
- `temperature_level`: Nivel de temperatura (0, 1, 2, ...)
- `temperature`: Valor de temperatura
- `avg_value`: Valor promedio de soluciones en este nivel
- `best_value`: Mejor valor encontrado en este nivel
- `avg_weight`: Peso promedio
- `acceptance_rate`: Tasa de aceptación en este nivel
- `improvements`: Número de mejoras en este nivel
- `iterations`: Iteraciones en este nivel
- `elapsed_time`: Tiempo acumulado

---

### 3. `tracking_acceptance.csv`

Log específico de **decisiones de aceptación**:

```csv
iteration,temperature,delta_E,acceptance_prob,accepted,move_type,improvement
0,100.0,15.0,1.0,True,improving,True
1,100.0,-5.0,0.0512,False,worsening,False
2,100.0,-3.0,0.0740,True,worsening,False
3,100.0,20.0,1.0,True,improving,True
...
```

**Columnas:**
- `iteration`: Número de iteración
- `temperature`: Temperatura actual
- `delta_E`: Diferencia de energía
- `acceptance_prob`: Probabilidad calculada
- `accepted`: ¿Fue aceptado?
- `move_type`: Tipo de movimiento (`improving`, `worsening`, `neutral`)
- `improvement`: ¿Resultó en mejora al best?

---

### 4. `summary.json`

Resumen ejecutivo de la ejecución:

```json
{
  "instance": {
    "name": "f1_l-d_kp_10_269",
    "n": 10,
    "capacity": 269,
    "optimal": 295
  },
  "algorithm": {
    "name": "SA_Geometric_Metropolis",
    "T0": 100.0,
    "alpha": 0.95,
    "iterations_per_temp": 100,
    "T_min": 0.01
  },
  "execution": {
    "seed": 42,
    "start_time": "2024-12-20T10:30:00",
    "end_time": "2024-12-20T10:30:15",
    "elapsed_time": 15.234
  },
  "results": {
    "initial_value": 150,
    "best_value": 285,
    "best_weight": 268,
    "is_feasible": true,
    "gap_to_optimal": 3.39,
    "total_iterations": 3500,
    "evaluations": 3500,
    "accepted_moves": 1250,
    "acceptance_rate": 35.71,
    "improvement_iterations": 45,
    "final_temperature": 0.0095
  },
  "convergence": {
    "first_improvement_iter": 2,
    "last_improvement_iter": 3280,
    "stagnation_period": 220,
    "avg_improvement_per_iter": 0.0386
  }
}
```

---

### 5. `convergence.json`

Datos específicos para gráficas de convergencia:

```json
{
  "iterations": [0, 1, 2, ..., 3500],
  "best_values": [150, 150, 160, ..., 285],
  "temperatures": [100.0, 100.0, 100.0, ..., 0.0095],
  "gaps": [49.15, 49.15, 45.76, ..., 3.39],
  "acceptance_windows": {
    "window_50": [0.68, 0.64, 0.60, ..., 0.12],
    "window_100": [0.65, 0.62, 0.58, ..., 0.15],
    "window_200": [0.63, 0.60, 0.56, ..., 0.18]
  },
  "improvement_markers": [2, 15, 28, ..., 3280]
}
```

---

### 6. `metadata.json`

Información del experimento:

```json
{
  "experiment": {
    "name": "KBP-SA_Experiment_LowDimensional",
    "date": "2024-12-20",
    "repetition": 1,
    "total_repetitions": 30
  },
  "environment": {
    "python_version": "3.9.7",
    "numpy_version": "1.21.0",
    "platform": "Windows-10",
    "cpu_count": 8
  },
  "dataset": {
    "group": "low_dimensional",
    "instance": "f1_l-d_kp_10_269",
    "source": "Pisinger (2005)"
  },
  "tracking": {
    "full_log": true,
    "temperature_log": true,
    "acceptance_log": true,
    "frequency": "every_iteration"
  }
}
```

---

## ⚙️ Configuración de Tracking

### Niveles de Detalle

El sistema soporta 3 niveles de tracking:

#### **Nivel 1: Mínimo** (solo resumen)
```python
tracking_config = {
    "level": "minimal",
    "save_summary": True,
    "save_full_log": False,
    "save_temperature_log": False,
    "save_acceptance_log": False
}
```

#### **Nivel 2: Moderado** (recomendado)
```python
tracking_config = {
    "level": "moderate",
    "save_summary": True,
    "save_full_log": False,
    "save_temperature_log": True,
    "save_acceptance_log": True,
    "sampling_rate": 10  # Guardar cada 10 iteraciones
}
```

#### **Nivel 3: Completo** (para análisis detallado)
```python
tracking_config = {
    "level": "full",
    "save_summary": True,
    "save_full_log": True,
    "save_temperature_log": True,
    "save_acceptance_log": True,
    "save_convergence": True,
    "sampling_rate": 1  # Guardar todas las iteraciones
}
```

---

## 🔧 Implementación

### Variables Calculadas Automáticamente

El sistema `SimulatedAnnealing` y `ExperimentRunner` calculan automáticamente:

1. **Durante la ejecución**:
   - `iteration`: Contador interno del SA
   - `temperature`: Actualizada por `CoolingSchedule`
   - `current_value`: Evaluación de la solución actual
   - `best_value`: Máximo valor encontrado
   - `delta_E`: Calculado como `-(neighbor.value - current.value)`
   - `acceptance_prob`: Calculado por `AcceptanceCriterion`
   - `accepted`: Decisión booleana
   - `elapsed_time`: Usando `time.time()`

2. **Post-procesamiento**:
   - `gap_to_optimal`: `((optimal - best_value) / optimal) * 100`
   - `acceptance_rate`: `(accepted_moves / total_iterations) * 100`
   - `improvement_count`: Contador de mejoras al best
   - `stagnation_period`: Iteraciones desde última mejora

### Guardado Automático

Los logs se guardan automáticamente en:

```python
# Al finalizar cada ejecución
output_dir = Path(f"output/{dataset_group}/{instance_name}")
output_dir.mkdir(parents=True, exist_ok=True)

# Guardar logs
save_tracking_logs(
    output_dir=output_dir,
    tracking_data=sa.get_convergence_data(),
    summary=sa.get_statistics(),
    config=tracking_config
)
```

---

## 📈 Uso de los Logs

### Análisis de Convergencia

```python
import pandas as pd
import matplotlib.pyplot as plt

# Cargar log completo
df = pd.read_csv("output/low_dimensional/f1_l-d_kp_10_269/tracking_full.csv")

# Graficar convergencia
plt.plot(df['iteration'], df['best_value'])
plt.xlabel('Iteration')
plt.ylabel('Best Value')
plt.title('Convergence Plot')
plt.show()
```

### Análisis de Temperatura vs Aceptación

```python
# Cargar log de temperatura
df_temp = pd.read_csv("output/low_dimensional/f1_l-d_kp_10_269/tracking_temperature.csv")

# Graficar relación
plt.plot(df_temp['temperature'], df_temp['acceptance_rate'], 'o-')
plt.xlabel('Temperature')
plt.ylabel('Acceptance Rate (%)')
plt.xscale('log')
plt.show()
```

### Estadísticas de Aceptación

```python
# Cargar log de aceptación
df_acc = pd.read_csv("output/low_dimensional/f1_l-d_kp_10_269/tracking_acceptance.csv")

# Analizar por tipo de movimiento
print(df_acc.groupby('move_type')['accepted'].mean())
# improving    1.00
# worsening    0.35
# neutral      0.50
```

---

## 🚀 Activación del Tracking

### En `demo_experimentation.py`

```python
# Activar tracking completo
runner = ExperimentRunner(config)
runner.enable_tracking(level="full")
runner.run()
```

### En `experiment_large_scale.py`

```python
# Tracking moderado (ahorra espacio)
runner.enable_tracking(
    level="moderate",
    sampling_rate=10
)
```

---

## 💾 Gestión de Espacio

### Tamaños Estimados

| Nivel | Instancia pequeña (n=10) | Instancia grande (n=10,000) |
|-------|--------------------------|------------------------------|
| Mínimo | ~5 KB | ~10 KB |
| Moderado | ~50 KB | ~200 KB |
| Completo | ~500 KB | ~20 MB |

### Recomendaciones

- **Low-dimensional**: Usar nivel **completo** (instancias pequeñas)
- **Large-scale**: Usar nivel **moderado** con sampling (instancias grandes)
- **Producción**: Usar nivel **mínimo** (solo resumen)

---

## 🔍 Variables Adicionales Personalizadas

Puedes agregar variables personalizadas al tracking:

```python
# En sa_core.py, durante optimize()
self.custom_tracking['diversity'] = calculate_diversity(current, best)
self.custom_tracking['exploration_ratio'] = exploration / exploitation
```

---

## 📊 Ejemplos de Salida

Ver carpeta `output/` después de ejecutar:
```bash
python demo_experimentation.py
```

Los archivos generados incluirán todos los logs descritos en este documento.

---

**Última actualización**: Diciembre 2024
