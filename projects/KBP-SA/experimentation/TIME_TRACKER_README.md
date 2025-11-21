# TimeTracker - Sistema de Seguimiento de Tiempo

## Descripción

El `TimeTracker` es un sistema que genera automáticamente un archivo `time_tracking.md` que se actualiza en tiempo real durante la ejecución del código, mostrando cuánto tiempo toma cada proceso y subproceso.

## Características

- ✅ **Actualización en tiempo real**: El archivo `.md` se actualiza mientras el código se ejecuta
- ✅ **Jerarquía de procesos**: Soporta procesos anidados (procesos y subprocesos)
- ✅ **Métricas detalladas**: Duración, estado, hora de inicio/fin
- ✅ **Detalles personalizados**: Puedes agregar cualquier información adicional
- ✅ **Formato Markdown**: Fácil de leer y compatible con visualizadores

## Uso Básico

### 1. Importar el TimeTracker

```python
from experimentation.time_tracker import TimeTracker
```

### 2. Crear una instancia

```python
tracker = TimeTracker(
    output_file="time_tracking.md",  # Nombre del archivo
    output_dir="output/experiments"   # Directorio de salida
)
```

### 3. Usar context managers para tracking automático

```python
# Proceso principal
with tracker.track("Proceso completo"):

    # Subproceso 1
    with tracker.track("Paso 1: Cargar datos", num_files=10):
        cargar_datos()
        tracker.update_current(files_loaded=10)

    # Subproceso 2
    with tracker.track("Paso 2: Procesar", algoritmo="SA"):
        procesar()
        tracker.update_current(iterations=1000)

    # Subproceso 3
    with tracker.track("Paso 3: Guardar resultados"):
        guardar()

# Finalizar
tracker.finalize()
```

### 4. Actualizar información durante la ejecución

```python
with tracker.track("Procesando datos"):
    for i in range(100):
        # ... procesamiento ...

        # Actualizar progreso cada 10 iteraciones
        if i % 10 == 0:
            tracker.update_current(progress=f"{i}/100")
```

## API del TimeTracker

### Constructor

```python
TimeTracker(output_file="time_tracking.md", output_dir="output")
```

**Parámetros:**
- `output_file` (str): Nombre del archivo de tracking
- `output_dir` (str): Directorio donde se guardará el archivo

### Métodos Principales

#### `track(name, **details)`

Context manager para tracking automático de un proceso.

```python
with tracker.track("Nombre del proceso", param1=valor1, param2=valor2):
    # código a ejecutar
    pass
```

**Parámetros:**
- `name` (str): Nombre descriptivo del proceso
- `**details`: Detalles adicionales (pueden ser cualquier clave-valor)

#### `update_current(**details)`

Actualiza detalles del proceso actual sin finalizarlo.

```python
tracker.update_current(progreso="50%", archivos=10)
```

#### `start_process(name, details=None)`

Inicia un nuevo proceso manualmente (alternativa a `track`).

```python
process = tracker.start_process("Mi proceso", details={"type": "test"})
```

#### `finish_process(status="Completado", **details)`

Finaliza el proceso actual manualmente.

```python
tracker.finish_process(status="Completado", total_items=100)
```

#### `finalize()`

Finaliza todo el tracking y genera el reporte final.

```python
tracker.finalize()
```

## Ejemplo Completo

Ver el archivo [test_time_tracker.py](../scripts/test_time_tracker.py) para un ejemplo completo y funcional.

## Formato del Archivo Generado

El archivo `time_tracking.md` contiene:

### 1. Encabezado

```markdown
# Time Tracking Report

**Fecha de inicio:** 2025-11-20 13:06:33
**Última actualización:** 2025-11-20 13:06:36
**Estado:** En ejecución / Completado
```

### 2. Resumen

```markdown
## Resumen

| Métrica | Valor |
|---------|-------|
| Tiempo total | 3.31s |
| Procesos totales | 7 |
| Procesos completados | 7 |
| Procesos activos | 0 |
```

### 3. Lista de Procesos

Para cada proceso muestra:
- ✅/⏳/❌ Estado (Completado/En progreso/Error)
- Nombre del proceso
- Duración
- Hora de inicio y fin
- Detalles personalizados
- Subprocesos (si existen)

```markdown
### ✅ Paso 1: Cargar datos

**Estado:** Completado
**Duración:** 1.00s
**Inicio:** 13:06:33
**Fin:** 13:06:34

**Detalles:**
- num_files: 10
- files_loaded: 10
```

## Integración con demo_experimentation_low.py

El `TimeTracker` ya está integrado en `demo_experimentation_low.py`. Cuando ejecutes ese script:

```bash
python scripts/demo_experimentation_low.py
```

Se generará automáticamente el archivo:
```
output/all_instances_experiments/time_tracking.md
```

Este archivo se irá actualizando en tiempo real mostrando:
- Paso 1: Generación de algoritmos GAA
- Paso 2: Configuración del experimento
- Paso 3: Ejecución de experimentos
- Paso 4: Guardado de resultados
- Paso 5: Análisis estadístico
- Paso 6: Comparación entre algoritmos
- Paso 7: Generación de visualizaciones

## Ventajas

1. **Transparencia**: Ves en tiempo real qué está haciendo el código
2. **Debugging**: Identifica fácilmente qué procesos toman más tiempo
3. **Documentación**: El archivo generado sirve como registro histórico
4. **Reproducibilidad**: Puedes comparar tiempos entre ejecuciones

## Notas

- El archivo se actualiza después de cada proceso, no en cada iteración (para evitar sobrecarga de I/O)
- Los tiempos se formatean automáticamente (ms, s, m, h)
- Soporta procesos anidados ilimitados
- Thread-safe para uso en contextos concurrentes (con precauciones)
