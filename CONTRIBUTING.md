# Guía de Contribución

¡Gracias por tu interés en contribuir al Framework GAA! Este documento proporciona directrices para contribuir al proyecto.

---

## 📋 Código de Conducta

- **Respeto**: Trata a todos los participantes con respeto y consideración
- **Colaboración**: Trabaja en conjunto para mejorar el proyecto
- **Profesionalismo**: Mantén un ambiente profesional y constructivo

---

## 🚀 Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/GAA-Framework.git
cd GAA-Framework

# Agrega el repositorio original como upstream
git remote add upstream https://github.com/gustavoalcantara-aravena/GAA-Framework.git
```

### 2. Crea una Rama

```bash
# Actualiza tu main
git checkout main
git pull upstream main

# Crea una rama para tu feature/fix
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-bug
```

### 3. Realiza tus Cambios

- Sigue las convenciones de código del proyecto
- Escribe código claro y bien documentado
- Añade tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 4. Tests

```bash
# Ejecuta todos los tests antes de hacer commit
cd projects/KBP-SA
pytest tests/ -v

# Verifica que todos los tests pasen
# Resultado esperado: X passed
```

### 5. Commit

```bash
# Sigue Conventional Commits
git add .
git commit -m "feat: agrega nueva funcionalidad X"
# o
git commit -m "fix: corrige error en Y"
# o
git commit -m "docs: actualiza documentación de Z"
```

**Tipos de commit:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `test:` Añade o modifica tests
- `refactor:` Refactorización de código
- `style:` Cambios de formato (no afectan funcionalidad)
- `chore:` Tareas de mantenimiento

### 6. Push y Pull Request

```bash
# Push a tu fork
git push origin feature/nombre-descriptivo

# Luego crea un Pull Request en GitHub
```

---

## 📝 Directrices de Código

### Estilo Python

- Sigue **PEP 8**
- Usa **type hints** cuando sea posible
- Docstrings en formato **Google Style**:

```python
def ejemplo(param1: int, param2: str) -> bool:
    """Breve descripción de la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ValueError: Cuándo se lanza esta excepción
    """
    pass
```

### Nombres

- **Clases**: `PascalCase` (ej: `KnapsackProblem`)
- **Funciones/métodos**: `snake_case` (ej: `evaluate_solution`)
- **Constantes**: `UPPER_SNAKE_CASE` (ej: `MAX_ITERATIONS`)
- **Variables**: `snake_case` descriptivo

### Estructura de Archivos

```python
# Orden de imports
import standard_library
import third_party
import local_modules

# Orden en archivo
1. Docstring del módulo
2. Imports
3. Constantes
4. Clases
5. Funciones
```

---

## 🧪 Tests

### Escribir Tests

- Un test por funcionalidad
- Nombres descriptivos: `test_deberia_hacer_X_cuando_Y`
- Usa `pytest` fixtures cuando sea apropiado
- Cubre casos normales y edge cases

```python
def test_knapsack_problem_deberia_rechazar_pesos_negativos():
    """Verifica que se lance ValueError con pesos negativos."""
    with pytest.raises(ValueError, match="pesos deben ser positivos"):
        KnapsackProblem(
            n=3,
            capacity=10,
            values=np.array([1, 2, 3]),
            weights=np.array([1, -2, 3])  # Peso negativo
        )
```

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Un archivo específico
pytest tests/test_core.py -v

# Un test específico
pytest tests/test_core.py::test_nombre -v

# Con coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 📚 Documentación

### Actualizar Documentación

Si tu cambio afecta:

1. **Funcionalidad existente**: Actualiza el README correspondiente
2. **Nueva funcionalidad**: Añade sección en documentación
3. **API**: Actualiza docstrings
4. **Configuración**: Actualiza archivos .md en `00-Core/`

### Formato de Documentación

- Usa Markdown para archivos .md
- Incluye ejemplos de código cuando sea relevante
- Añade capturas de pantalla para UI/gráficas
- Mantén un tono claro y conciso

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que no sea un problema conocido en [Issues](https://github.com/gustavoalcantara-aravena/GAA-Framework/issues)
2. Intenta reproducir el bug en la última versión
3. Recopila información del sistema

### Crear Issue

Incluye:

```markdown
**Descripción del Bug**
Descripción clara y concisa del problema

**Pasos para Reproducir**
1. Ir a '...'
2. Ejecutar '...'
3. Ver error

**Comportamiento Esperado**
Qué debería suceder

**Comportamiento Actual**
Qué sucede en realidad

**Screenshots/Logs**
Si aplica, añade capturas o logs

**Entorno**
- OS: [ej: Windows 10]
- Python: [ej: 3.9.5]
- Versión GAA: [ej: 1.0.0]

**Contexto Adicional**
Cualquier información relevante
```

---

## 💡 Sugerir Features

### Formato de Propuesta

```markdown
**Descripción del Feature**
Descripción clara de la funcionalidad propuesta

**Motivación**
Por qué es útil este feature

**Propuesta de Implementación**
Cómo se podría implementar (opcional)

**Alternativas Consideradas**
Otras formas de lograr el objetivo

**Contexto Adicional**
Cualquier información relevante
```

---

## 🔍 Proceso de Revisión

### Para Revisores

- Verifica que los tests pasen
- Revisa la calidad del código
- Comprueba que la documentación esté actualizada
- Prueba la funcionalidad localmente
- Proporciona feedback constructivo

### Para Contribuidores

- Responde a comentarios de revisión
- Actualiza el PR según feedback
- Mantén la rama actualizada con main
- Sé paciente y respetuoso

---

## 📦 Estructura del Proyecto

```
GAA/
├── projects/KBP-SA/     # Proyecto principal activo
│   ├── core/            # Clases base (Problem, Solution, Evaluator)
│   ├── operators/       # Operadores de búsqueda
│   ├── gaa/             # Sistema GAA (Grammar, Generator, Interpreter)
│   ├── metaheuristic/   # Componentes SA (core, cooling, acceptance)
│   ├── experimentation/ # Framework experimental
│   ├── data/            # Carga de datos
│   ├── utils/           # Utilidades
│   └── tests/           # Tests unitarios
└── 00-Core/             # Documentación framework GAA
```

---

## 🎯 Áreas de Contribución

### Alta Prioridad

- ✅ Más tests (coverage > 80%)
- ✅ Documentación de ejemplos
- ✅ Optimización de performance
- ✅ Validación de datasets

### Media Prioridad

- 🔄 Nuevos operadores para KBP
- 🔄 Visualizaciones adicionales
- 🔄 Exportación de resultados (CSV, Excel)
- 🔄 Logging mejorado

### Exploratoria

- 💡 Nuevos problemas (GCP, VRP)
- 💡 Nuevas metaheurísticas (GRASP, ILS)
- 💡 Paralelización de experimentos
- 💡 Dashboard interactivo

---

## ❓ Preguntas

Si tienes preguntas sobre cómo contribuir:

1. Revisa la [documentación](README.md)
2. Busca en [Issues cerrados](https://github.com/gustavoalcantara-aravena/GAA-Framework/issues?q=is%3Aissue+is%3Aclosed)
3. Abre un [nuevo Issue](https://github.com/gustavoalcantara-aravena/GAA-Framework/issues/new) con la etiqueta "question"

---

## 🙏 Agradecimientos

Todas las contribuciones son valoradas, desde corrección de typos hasta nuevas funcionalidades. ¡Gracias por ayudar a mejorar GAA Framework!

---

**Última actualización**: Diciembre 2024
