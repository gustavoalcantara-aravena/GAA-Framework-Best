# Automation Scripts

Scripts de Python para automatizar la sincronización y generación de código del framework GAA.

## Scripts Disponibles

### `sync-engine.py`

Motor principal de sincronización automática.

**Comandos**:

```bash
# Sincronizar archivos después de editar Problem.md o Metaheuristic.md
python sync-engine.py --sync

# Validar consistencia de archivos
python sync-engine.py --validate

# Generar scripts Python (en desarrollo)
python sync-engine.py --generate
```

**Funcionalidad**:
- Detecta cambios en `00-Core/Problem.md` y `00-Core/Metaheuristic.md`
- Extrae información relevante (terminales, función objetivo, etc.)
- Actualiza automáticamente archivos dependientes
- Mantiene log de sincronizaciones
- Marca scripts para regeneración

## Flujo de Trabajo

1. **Editar archivos base**:
   ```bash
   # Editar 00-Core/Problem.md
   # Completar secciones requeridas
   ```

2. **Sincronizar**:
   ```bash
   python 05-Automation/sync-engine.py --sync
   ```

3. **Validar**:
   ```bash
   python 05-Automation/sync-engine.py --validate
   ```

4. **Generar código** (cuando esté implementado):
   ```bash
   python 05-Automation/sync-engine.py --generate
   ```

## Dependencias

```bash
pip install pyyaml
```

## Estructura de Sincronización

```
Problem.md → sync-engine.py → Grammar.md
                             → Fitness-Function.md
                             → Dataset-Specification.md
                             → [marca] problem.py

Metaheuristic.md → sync-engine.py → Search-Operators.md
                                  → [marca] metaheuristic.py
```

## Desarrollo Futuro

- [ ] Generación completa de scripts Python
- [ ] Modo watch para sincronización continua
- [ ] Validación de sintaxis generada
- [ ] Tests automáticos de código generado
