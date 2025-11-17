---
gaa_metadata:
  version: 1.0.0
  type: auto_generated
  depends_on:
    - 00-Core/Problem.md
    - 00-Core/Metaheuristic.md
  auto_sync: true
---

# Diseño Experimental

> **⚠️ AUTO-GENERADO**: Se sincroniza desde `Problem.md` y `Metaheuristic.md`.

## Protocolo Experimental

### Configuración

**Réplicas**: [Número de ejecuciones independientes]  
**Semilla base**: [Semilla para reproducibilidad]  
**Presupuesto computacional**: [Tiempo o evaluaciones]

### Instancias de Prueba

Ver: `03-Experiments/Instances.md` y `06-Datasets/`

### Factores Experimentales

<!-- AUTO-GENERATED -->
**Problema**: [Extraído de Problem.md]  
**Metaheurística**: [Extraído de Metaheuristic.md]  
**Parámetros**: [Configuraciones a probar]
<!-- END AUTO-GENERATED -->

## Métricas a Reportar

| Métrica | Descripción | Cálculo |
|---------|-------------|---------|
| **Calidad promedio** | Media de fitness obtenido | `mean(fitness)` |
| **Mejor solución** | Mejor fitness encontrado | `max(fitness)` |
| **Desviación estándar** | Variabilidad | `std(fitness)` |
| **Tiempo promedio** | Tiempo de ejecución | `mean(time)` |
| **Tasa de factibilidad** | % soluciones factibles | `sum(feasible)/n` |
| **Gap** | Distancia a óptimo conocido | `(opt - best)/opt` |

## Análisis Estadístico

### Pruebas a Realizar

- **Test de normalidad**: Shapiro-Wilk
- **Comparación de medias**: t-test o Wilcoxon
- **Comparación múltiple**: ANOVA o Kruskal-Wallis
- **Post-hoc**: Tukey HSD o Bonferroni

### Nivel de Significancia

α = 0.05

## Formato de Reporte

### Tabla de Resultados

```markdown
| Algoritmo | Promedio | Mejor | Peor | Desv.Std | Tiempo(s) | Gap(%) |
|-----------|----------|-------|------|----------|-----------|--------|
| Alg1      |          |       |      |          |           |        |
| Alg2      |          |       |      |          |           |        |
```

### Gráficos Requeridos

1. **Box plots**: Distribución de fitness por algoritmo
2. **Curvas de convergencia**: Fitness vs iteraciones
3. **Scatter plots**: Calidad vs tiempo
4. **Heatmaps**: Matriz de comparación pareada

## Reproducibilidad

### Información a Registrar

- Versión de Python
- Versiones de librerías (numpy, etc.)
- Hardware utilizado (CPU, RAM)
- Sistema operativo
- Semillas aleatorias
- Configuración completa de parámetros

---

## Estado

⏳ Pendiente de definición de experimentos
