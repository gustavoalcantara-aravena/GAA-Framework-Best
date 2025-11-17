# Datasets

Esta carpeta contiene las instancias del problema para experimentación.

## Estructura

```
06-Datasets/
├── training/          # Instancias para optimizar el AST
├── validation/        # Instancias para ajuste de hiperparámetros
├── test/              # Instancias para evaluación final
└── benchmark/         # Instancias estándar de la literatura
```

## Formato

El formato de los archivos se especifica en `Dataset-Specification.md`, el cual se sincroniza automáticamente desde `00-Core/Problem.md`.

## Agregar Nuevas Instancias

1. Coloca los archivos en la subcarpeta apropiada
2. Asegúrate de que cumplan el formato especificado
3. Ejecuta validación: `python 05-Automation/validate-datasets.py`
4. Actualiza el catálogo en `03-Experiments/Instances.md`

## Fuentes de Datos

[Lista de fuentes de donde se obtuvieron las instancias]

## Licencias

[Información sobre licencias de los datasets utilizados]
