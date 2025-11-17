---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
  sync_rules:
    - source: "00-Core/Problem.md::Solution-Representation"
      action: "extract_format"
      target: "section:Format-Specification"
  auto_sync: true
---

# Especificación de Datasets

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md`.

## Estructura de Directorios

```
06-Datasets/
├── training/          # Instancias para entrenar (optimizar AST)
├── validation/        # Instancias para validación
├── test/              # Instancias para evaluación final
└── benchmark/         # Instancias estándar de la literatura
```

## Format-Specification

<!-- AUTO-GENERATED from 00-Core/Problem.md::Solution-Representation -->
```
[Pendiente de extracción desde Problem.md]

Formato esperado:
- Extensión: .txt | .dat | .json
- Estructura: [A definir según el problema]
```
<!-- END AUTO-GENERATED -->

## Ejemplo de Archivo de Instancia

```
# [Ejemplo basado en el problema]
```

## Loader Script

```python
def load_instance(file_path):
    """
    Carga una instancia del problema desde archivo.
    
    Args:
        file_path: Ruta al archivo de instancia
    
    Returns:
        instance: Diccionario con datos de la instancia
    """
    # [AUTO-GENERADO según Format-Specification]
    pass
```

## Validación de Formato

```python
def validate_instance_format(instance):
    """
    Valida que una instancia cumpla con el formato esperado.
    """
    # [AUTO-GENERADO]
    pass
```

## Catálogo de Datasets Disponibles

| Dataset | # Instancias | Tamaño | Fuente | Óptimos Conocidos |
|---------|--------------|--------|--------|-------------------|
|         |              |        |        |                   |

---

## Instrucciones de Uso

1. Coloca tus archivos de instancias en las subcarpetas apropiadas:
   - `training/`: Para optimizar el AST
   - `validation/`: Para ajustar hiperparámetros
   - `test/`: Para evaluación final

2. Asegúrate de que cumplan el formato especificado

3. Ejecuta validación:
   ```bash
   python 05-Automation/validate-datasets.py
   ```

---

## Estado

⏳ Pendiente de sincronización con `Problem.md`
