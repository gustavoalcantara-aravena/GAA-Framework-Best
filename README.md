# GAA Framework - Generación Automática de Algoritmos

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research-orange.svg)]()

**Framework para Generación Automática de Algoritmos (GAA) aplicado a problemas de optimización combinatoria.**

---

## 📋 Descripción

Este framework implementa una metodología sistemática para la generación automática de algoritmos metaheurísticos usando una gramática formal (BNF) y técnicas de optimización. El sistema permite:

- ✅ **Generación automática** de algoritmos mediante gramática GAA
- ✅ **Experimentación rigurosa** con análisis estadístico
- ✅ **Evaluación en benchmarks** estándar
- ✅ **Visualización de resultados** con gráficas profesionales
- ✅ **Extensible** a múltiples problemas de optimización

---

## 🎯 Proyectos Implementados

### 1. **KBP-SA**: Knapsack Problem + Simulated Annealing
- **Datasets**: 31 instancias (10 low-dimensional, 21 large-scale)
- **Algoritmos**: Generación automática de metaheurísticas
- **Análisis**: Friedman, Wilcoxon, Cohen's d, Performance Profiles
- **Estado**: ✅ **Completamente funcional**

[📖 Ver documentación completa de KBP-SA](projects/KBP-SA/README.md)

### 2. **GCP-ILS**: Graph Coloring Problem + Iterated Local Search
- **Estado**: 🚧 En desarrollo

### 3. **VRPTW-GRASP**: Vehicle Routing Problem + GRASP
- **Estado**: 🚧 Planeado

---

## 🚀 Quick Start

### Prerrequisitos

```bash
# Python 3.8 o superior
python --version

# Clonar repositorio
git clone https://github.com/gustavoalcantara-aravena/GAA-Framework.git
```

### Ejecución Rápida (KBP-SA)

```bash
# Entrar al proyecto
cd projects/KBP-SA

# 1. Test rápido (10 segundos)
python test_quick.py

# 2. Demo completo (30 segundos)
python demo_complete.py

# 3. Experimentos con gráficas (1-2 minutos)
python demo_experimentation.py

# 4. Visualización SA (30 segundos)
python demo_acceptance_rate.py
```

**Las gráficas se guardan automáticamente en:**
- `output/plots_low_dimensional_TIMESTAMP/`
- `output/plots_acceptance_TIMESTAMP/`

---

## 📊 Estructura del Framework

```
GAA/
├── 00-Core/              # Documentación base (Problema, Metaheurística)
├── 01-System/            # Gramática GAA y nodos AST
├── 02-Components/        # Operadores y funciones de evaluación
├── 03-Experiments/       # Diseño experimental y métricas
├── 04-Generated/         # Código generado automáticamente
├── 05-Automation/        # Motor de sincronización
├── 06-Datasets/          # Benchmarks estándar
└── projects/             # Proyectos específicos
    ├── KBP-SA/           ✅ Knapsack + SA (FUNCIONAL)
    ├── GCP-ILS/          🚧 Graph Coloring + ILS
    └── VRPTW-GRASP/      🚧 VRP + GRASP
```

---

## 🧬 Gramática GAA

El sistema usa una gramática BNF para generar algoritmos:

```bnf
<Prog> ::= Seq(<Stmt>*)
<Stmt> ::= If(<Cond>, <Stmt>, <Stmt>)
         | While(<Bud>, <Stmt>)
         | For(<Int>, <Stmt>)
         | LocalSearch(<Neighborhood>, <Acceptance>)
         | GreedyConstruct(<Heuristic>)
         | ApplyUntilNoImprove(<Stmt>, <Stop>)
         | Call(<Terminal>)
```

**Ejemplo de algoritmo generado:**

```
SECUENCIA:
  1. CONSTRUIR_VORAZ usando GreedyByRatio
  2. MIENTRAS (presupuesto: 100 iteraciones):
       BUSQUEDA_LOCAL en TwoExchange (aceptación: Metropolis)
```

---

## 📈 Resultados (KBP-SA)

### Datasets Validados
- ✅ **10 instancias low-dimensional** (n=4-23 ítems)
- ✅ **21 instancias large-scale** (n=100-10,000 ítems)
- ✅ **100% datasets válidos** (31/31)

### Métricas Implementadas
- 📊 Gap to optimal
- ⏱️ Tiempo de ejecución
- 🔄 Tasa de convergencia
- 📉 Análisis estadístico (Friedman, Wilcoxon, Cohen's d)

### Visualizaciones
- 📦 Boxplots de calidad por algoritmo
- 📊 Barras comparativas con error bars
- 🎯 Scatter tiempo vs calidad
- 📈 Tasa de aceptación vs iteración (SA)

---

## 🧪 Testing

```bash
# Tests unitarios
cd projects/KBP-SA
pytest tests/test_core.py -v

# Resultado esperado: 18 passed ✅
```

**Cobertura de tests:**
- ✅ Validación de KnapsackProblem
- ✅ Operaciones en KnapsackSolution
- ✅ Cálculo de métricas (gap, evaluación)
- ✅ Carga de datasets
- ✅ Manejo de errores

---

## 📚 Documentación

### Por Proyecto
- [KBP-SA - Quick Start](projects/KBP-SA/QUICKSTART_EJECUTABLE.md)
- [KBP-SA - Sistema Completo](projects/KBP-SA/README_SISTEMA.md)
- [KBP-SA - Experimentos](projects/KBP-SA/COMO_EJECUTAR_EXPERIMENTOS.md)

### Framework GAA
- [Arquitectura General](ARCHITECTURE.md)
- [Estado del Framework](FRAMEWORK_STATUS.md)
- [Resumen Ejecutivo](EXECUTIVE_SUMMARY.md)
- [Guía de Desarrollo](DEVELOPMENT.md)

---

## 🔧 Requisitos

### Obligatorios
```
numpy >= 1.21.0
scipy >= 1.7.0
```

### Opcionales (para gráficas y análisis)
```
matplotlib >= 3.4.0
pandas >= 1.3.0
pytest >= 7.0.0 (para tests)
```

---

## 🤝 Contribuciones

Este es un proyecto de investigación académica. Si deseas contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📖 Publicaciones

Este trabajo es parte de una investigación doctoral sobre Generación Automática de Algoritmos aplicada a optimización combinatoria.

**Referencias clave:**
- Kirkpatrick et al. (1983): Optimization by Simulated Annealing
- Pisinger (2005): Where are the hard knapsack problems?
- Barr et al. (1995): Designing and reporting on computational experiments

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

---

## 👤 Autor

**Gustavo Alcántara-Aravena**
- GitHub: [@gustavoalcantara-aravena](https://github.com/gustavoalcantara-aravena)
- Repositorio: [Tesis_doctoral](https://github.com/gustavoalcantara-aravena/Tesis_doctoral)

---

## 🙏 Agradecimientos

- Comunidad de investigación en metaheurísticas
- Autores de los benchmarks utilizados
- Colaboradores del proyecto

---

## 📊 Estado del Proyecto

| Componente | Estado | Cobertura |
|------------|--------|-----------|
| Framework GAA | ✅ Funcional | Core completo |
| KBP-SA | ✅ Producción | 31 instancias |
| Tests Unitarios | ✅ Implementado | 18 tests |
| Documentación | ✅ Completa | 100% |
| GCP-ILS | 🚧 Desarrollo | - |
| VRPTW-GRASP | 📋 Planeado | - |

---

## 🔗 Links Útiles

- [Documentación Completa](docs/)
- [Issues](https://github.com/gustavoalcantara-aravena/GAA-Framework/issues)
- [Changelog](CHANGELOG.md)

---

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!**
4. ⏳ Problema Maestro → `00-Core/Metaheuristic.md`
5. ⏳ Experimentación → `03-Experiments/`
6. ⏳ Algoritmos Finales → Construcción de 3 algoritmos específicos
7. ⏳ Documentación → Generación de paper académico

## 🛠️ Comandos Útiles

```bash
# Validar consistencia
python 05-Automation/sync-engine.py --validate

# Sincronizar archivos
python 05-Automation/sync-engine.py --sync

## 📖 Documentación

### 🚀 Para Empezar
- **Resumen Ejecutivo**: [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Estado completo del framework
- **Inicio Rápido**: [QUICKSTART.md](QUICKSTART.md) - Tutorial paso a paso
- **Estado del Framework**: [FRAMEWORK_STATUS.md](FRAMEWORK_STATUS.md) - Verificación detallada

### 🏗️ Arquitectura y Desarrollo
- **Arquitectura Técnica**: [ARCHITECTURE.md](ARCHITECTURE.md) - Diseño del sistema
- **Guía de Desarrollo**: [DEVELOPMENT.md](DEVELOPMENT.md) - Para desarrolladores
- **Base Metodológica**: [GAA-Agent-System-Prompt.md](GAA-Agent-System-Prompt.md) - Metodología GAA

### 🎯 Proyectos
- **Índice de Proyectos**: [projects/README.md](projects/README.md)
- **KBP-SA**: [projects/KBP-SA/INSTRUCTIONS.md](projects/KBP-SA/INSTRUCTIONS.md)
- **GCP-ILS**: [projects/GCP-ILS/README.md](projects/GCP-ILS/README.md)
- **VRPTW-GRASP**: [projects/VRPTW-GRASP/README.md](projects/VRPTW-GRASP/README.md)

---

## 📚 Referencias

- Base metodológica: Ver `GAA-Agent-System-Prompt.md`
- Gramática BNF: `01-System/Grammar.md`
- Ejemplos de terminales: Papers en `00-Core/Problem.md`

## 🎯 Proyectos Incluidos

El framework incluye **3 proyectos completos** listos para usar:

### 1. **KBP-SA**: Knapsack Problem con Simulated Annealing
- 13 terminales identificados
- Metaheurística: SA con enfriamiento geométrico
- Datasets: Usuario debe proporcionar
- [Ver proyecto →](projects/KBP-SA/)

### 2. **GCP-ILS**: Graph Coloring Problem con ILS
- 15 terminales identificados
- Metaheurística: Iterated Local Search
- Datasets: DIMACS Challenge benchmarks
- [Ver proyecto →](projects/GCP-ILS/)

### 3. **VRPTW-GRASP**: Vehicle Routing con GRASP
- 22 terminales identificados
- Metaheurística: GRASP con VND
- Datasets: Solomon Instances
- [Ver proyecto →](projects/VRPTW-GRASP/)

**Índice de proyectos**: [projects/README.md](projects/README.md)

---

## 🤝 Contribución

Este es un framework en desarrollo. Próximas funcionalidades:
- [ ] Generación completa de código Python
- [ ] Visualizador de AST
- [ ] Ejecución automática de experimentos
- [ ] Generación de reportes académicos
- [ ] Más proyectos de ejemplo

## 📄 Licencia

[Especificar licencia]

---

**Desarrollado con el framework de Generación Automática de Algoritmos (GAA)**
