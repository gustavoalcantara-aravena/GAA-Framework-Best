# 🚀 QUICK START - KBP-SA Sistema GAA

Guía rápida para ejecutar el sistema de Generación Automática de Algoritmos para Knapsack Problem con Simulated Annealing.

---

## 📋 Prerrequisitos

### 1. Verificar Python
```powershell
python --version  # Requiere Python 3.8+
```

### 2. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

**Dependencias principales:**
- `numpy >= 1.21.0` (obligatorio)
- `scipy >= 1.7.0` (obligatorio para estadísticas)
- `matplotlib >= 3.4.0` (opcional, para gráficas)
- `pandas >= 1.3.0` (opcional, para análisis)

### 3. Verificar Estructura
```powershell
python validate_datasets.py  # Valida datasets
```

---

## 🎯 Orden de Ejecución Recomendado

### **Nivel 1: Validación Básica** (5 minutos)

#### 1️⃣ Test Rápido
```powershell
python test_quick.py
```
**Qué hace**: Carga una instancia simple (f1) y verifica funcionalidad básica.  
**Esperado**: Debe mostrar ✅ sin errores.

#### 2️⃣ Demo Completo del Sistema
```powershell
python demo_complete.py
```
**Qué hace**: Ejecuta 5 demos mostrando:
- ✅ Carga de problema
- ✅ Operadores constructivos
- ✅ Operadores de mejora
- ✅ Generación de algoritmos GAA
- ✅ Comparación de métodos

**Tiempo**: ~30 segundos  
**Esperado**: Todos los demos deben completarse con ✅

---

### **Nivel 2: Experimentación** (30 minutos)

#### 3️⃣ Experimentos Low-Dimensional
```powershell
python demo_experimentation.py
```
**Qué hace**: 
- Genera 3 algoritmos GAA aleatorios
- Ejecuta en **9 instancias low-dimensional**
- 1 repetición por instancia (cobertura completa)
- Genera análisis estadístico (Friedman, Wilcoxon)
- Crea 3 visualizaciones PNG

**Tiempo**: ~1-2 minutos  
**Salidas**:
- `output/all_instances_experiments/experiment_*.json`
- `output/plots_low_dimensional_TIMESTAMP/*.png`

#### 4️⃣ Visualización de Tasa de Aceptación SA
```powershell
python demo_acceptance_rate.py
```
**Qué hace**:
- Ejecuta SA directamente sobre instancia f8
- Trackea decisiones de aceptación/rechazo
- Genera 3 gráficas (ventanas de 50, 100, 200 iteraciones)

**Tiempo**: ~30 segundos  
**Salidas**: `output/plots_acceptance_TIMESTAMP/acceptance_rate_w*.png`

---

### **Nivel 3: Experimentos Large-Scale** (30-60 minutos)

#### 5️⃣ Experimentos Large-Scale (OPCIONAL)
```powershell
python experiment_large_scale.py
```
**Qué hace**:
- Genera 3 algoritmos GAA
- Ejecuta en **21 instancias large-scale** (100-10,000 ítems)
- 1 repetición por instancia
- Timeout: 600s por ejecución

**⚠️ ADVERTENCIA**: Esto toma **30-60 minutos**  
**Salidas**: `output/large_scale_experiments/`

---

## 📊 Resultados Esperados

### ✅ Ejecución Exitosa
```
✅ Experimentos completados: 27/27
📁 Instancias procesadas: 9
🏆 Mejor algoritmo: GAA_Algorithm_X
   Gap promedio: 4.07%
✅ Gráficas guardadas en: output/plots_low_dimensional_TIMESTAMP/
```

### ❌ Problemas Comunes

#### Error: "No module named 'matplotlib'"
```powershell
pip install matplotlib
```

#### Error: "Could not find platform independent libraries"
**Solución**: Este warning es normal en algunos entornos virtuales, no afecta ejecución.

#### Error: "Error cargando f5_l-d_kp_15_375_low-dimensional.txt"
**Causa**: La instancia f5 tiene pesos negativos (bug en dataset original).  
**Solución**: Se omite automáticamente, procesa las otras 9 instancias.

#### Error: "Timeout exceeded"
**Solución**: Reducir `max_time_seconds` en configuración o `max_evaluations` en SA.

---

## 🧪 Tests Unitarios

### Ejecutar Suite de Tests
```powershell
pytest tests/test_core.py -v
```

**Tests incluidos** (15 tests):
- ✅ Validación de KnapsackProblem
- ✅ Operaciones en KnapsackSolution
- ✅ Evaluación y cálculo de gap
- ✅ Carga de datasets

---

## 📁 Estructura de Outputs

```
output/
├── all_instances_experiments/
│   └── experiment_all_instances_TIMESTAMP.json
├── plots_low_dimensional_TIMESTAMP/
│   ├── demo_boxplot.png
│   ├── demo_bars.png
│   └── demo_scatter.png
├── plots_acceptance_TIMESTAMP/
│   ├── acceptance_rate_w50.png
│   ├── acceptance_rate_w100.png
│   └── acceptance_rate_w200.png
└── large_scale_experiments/  (si ejecutaste nivel 3)
```

---

## 🔧 Configuración Personalizada

### Modificar Parámetros SA
Edita `demo_acceptance_rate.py`:
```python
sa = SimulatedAnnealing(
    problem=problem,
    T0=100.0,           # Temperatura inicial
    alpha=0.95,         # Factor enfriamiento
    iterations_per_temp=100,  # Iteraciones por T
    T_min=0.01,         # Temperatura mínima
    max_evaluations=10000,    # Presupuesto
    seed=42
)
```

### Modificar Instancias de Experimento
Edita `demo_experimentation.py` línea ~70:
```python
config = ExperimentConfig(
    name="my_experiment",
    instances=instance_names,  # Lista de nombres
    algorithms=algorithms,      # Lista de AST
    repetitions=1,             # Cambiar a 30 para validación
    max_time_seconds=60.0,     # Timeout
    output_dir="output/my_experiments"
)
```

---

## 📚 Siguiente Paso

Una vez validado el sistema:
1. Lee `COMO_EJECUTAR_EXPERIMENTOS.md` para experimentación avanzada
2. Lee `README_SISTEMA.md` para arquitectura detallada
3. Genera población de 50+ algoritmos para selección
4. Ejecuta validación estadística con 30 repeticiones

---

## 🐛 Reportar Problemas

Si encuentras bugs:
1. Verifica que tienes la última versión
2. Ejecuta `python validate_datasets.py`
3. Revisa logs en consola
4. Abre issue con:
   - Comando ejecutado
   - Mensaje de error completo
   - Salida de `python --version`

---

## ✅ Checklist Pre-Experimentación

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`requirements.txt`)
- [ ] `test_quick.py` pasa sin errores
- [ ] `demo_complete.py` pasa sin errores
- [ ] Datasets validados (`validate_datasets.py`)
- [ ] Espacio en disco para outputs (~100MB)

**¡Listo para experimentar!** 🚀
