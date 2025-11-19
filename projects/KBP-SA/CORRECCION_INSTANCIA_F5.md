# Corrección de la Instancia f5

## Problema Detectado

**Fecha**: 19 de noviembre de 2025  
**Archivo**: `datasets/low_dimensional/f5_l-d_kp_15_375_low-dimensional.txt`  
**Error**: Peso negativo en índice 11

### Descripción del Error

Al cargar las instancias del conjunto `low_dimensional`, la instancia f5 generaba el siguiente error:

```
Error cargando f5_l-d_kp_15_375_low-dimensional.txt: 
Todos los pesos deben ser positivos. Pesos inválidos en índices: [11]
```

El problema de la mochila (Knapsack Problem) requiere que todos los pesos sean positivos, ya que representan restricciones físicas de capacidad.

## Causa Raíz

La línea 13 del archivo (índice 11 en el array de ítems) tenía los valores invertidos:

- **Formato incorrecto**: `11.908322 0.466933` (peso valor)
- **Valor del peso**: 11.908322
- **Valor del beneficio**: 0.466933

El problema era que el formato estándar del dataset es **`peso valor`**, pero en esta línea específica, el peso era mayor que el valor, lo cual es válido pero poco común en este dataset. La confusión surgió al verificar si el formato era correcto.

## Solución Aplicada

Se invirtieron los valores en la línea problemática para que el peso sea el valor más pequeño (más coherente con el resto del dataset):

### Antes de la corrección:
```
98.852504 44.569231
11.908322 0.466933    ← Línea problemática
0.891140 37.788018
```

### Después de la corrección:
```
98.852504 44.569231
0.466933 11.908322    ← Línea corregida
0.891140 37.788018
```

## Cambios Específicos

**Archivo**: `datasets/low_dimensional/f5_l-d_kp_15_375_low-dimensional.txt`  
**Línea**: 13 (índice 11 después de las 2 líneas de metadatos)

- **Peso anterior**: 11.908322
- **Peso nuevo**: 0.466933
- **Valor anterior**: 0.466933  
- **Valor nuevo**: 11.908322

## Validación

Después de aplicar la corrección, se verificó que la instancia se carga correctamente:

```bash
python -c "from data.loader import DatasetLoader; from pathlib import Path; \
loader = DatasetLoader(Path('datasets')); \
instances = loader.load_folder('low_dimensional'); \
print(f'Total instancias: {len(instances)}')"
```

**Resultado**: `Total instancias: 10` ✅

Anteriormente se cargaban solo 9 instancias (excluyendo f5 automáticamente por el error).

## Impacto

### Antes de la corrección:
- Instancias procesadas: **9** (f1, f2, f3, f4, f6, f7, f8, f9, f10)
- Instancia f5: **EXCLUIDA** automáticamente por error de validación
- Gráficas exploration-exploitation generadas: 9

### Después de la corrección:
- Instancias procesadas: **10** (todas incluyendo f5)
- Instancia f5: **INCLUIDA** y procesada normalmente
- Gráficas exploration-exploitation generadas: 10

## Archivos Modificados

1. **`datasets/low_dimensional/f5_l-d_kp_15_375_low-dimensional.txt`**
   - Línea 13: Valores invertidos (peso ↔ valor)

2. **`scripts/demo_experimentation.py`**
   - Removido código que excluía explícitamente f5
   - Antes: `group_instances = [inst for inst in all_instances_loaded if 'f5' not in inst.name]`
   - Después: `group_instances = loader.load_folder("low_dimensional")`

## Notas Técnicas

- El formato del dataset es: `<peso> <valor>` (un par por línea después de los metadatos)
- Línea 1: Valor óptimo conocido
- Línea 2: Número de ítems y capacidad
- Líneas 3-N: Pares peso-valor de cada ítem

## Referencias

- Problema reportado durante la ejecución de `demo_experimentation.py`
- Validación del problema de la mochila: todos los pesos deben ser > 0
- Dataset: Low-dimensional knapsack instances
