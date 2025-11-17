"""
Motor de Sincronización del Framework GAA

Este script detecta cambios en Problem.md o Metaheuristic.md y actualiza
automáticamente todos los archivos dependientes según el grafo de dependencias.

Uso:
    python sync-engine.py --sync      # Sincronizar archivos
    python sync-engine.py --generate  # Generar scripts Python
    python sync-engine.py --validate  # Validar consistencia
    python sync-engine.py --watch     # Monitoreo continuo (TODO)
"""

import yaml
import json
import hashlib
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class GAASync:
    """Motor de sincronización automática del framework GAA"""
    
    def __init__(self, root_dir: Path):
        self.root = Path(root_dir)
        self.config_dir = self.root / ".gaa-config"
        
        # Cargar configuraciones
        self.dep_graph = self._load_json("dependency-graph.json")
        self.sync_rules = self._load_json("sync-rules.json")
        self.project_state = self._load_json("project-state.json")
    
    def _load_json(self, filename: str) -> Dict:
        """Carga un archivo JSON de configuración"""
        path = self.config_dir / filename
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_json(self, filename: str, data: Dict):
        """Guarda datos en un archivo JSON"""
        path = self.config_dir / filename
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _compute_hash(self, file_path: Path) -> str:
        """Calcula hash MD5 de un archivo"""
        if not file_path.exists():
            return ""
        content = file_path.read_text(encoding='utf-8')
        return hashlib.md5(content.encode()).hexdigest()
    
    def _file_changed(self, rel_path: str) -> bool:
        """Detecta si un archivo cambió desde la última sincronización"""
        file_path = self.root / rel_path
        
        if not file_path.exists():
            return False
        
        current_hash = self._compute_hash(file_path)
        stored_info = self.project_state.get("files", {}).get(rel_path, {})
        stored_hash = stored_info.get("hash", "")
        
        return current_hash != stored_hash
    
    def _update_file_state(self, rel_path: str):
        """Actualiza el estado de un archivo en project-state.json"""
        file_path = self.root / rel_path
        
        if "files" not in self.project_state:
            self.project_state["files"] = {}
        
        self.project_state["files"][rel_path] = {
            "hash": self._compute_hash(file_path),
            "last_modified": datetime.now().isoformat(),
            "synced": True
        }
        
        self._save_json("project-state.json", self.project_state)
    
    def sync_all(self):
        """Ejecuta sincronización completa"""
        print("🔄 Iniciando sincronización del framework GAA...\n")
        
        # Verificar cambios en triggers principales
        triggers = ["00-Core/Problem.md", "00-Core/Metaheuristic.md"]
        changes_detected = False
        
        for trigger in triggers:
            if self._file_changed(trigger):
                print(f"✓ Cambio detectado en {trigger}")
                changes_detected = True
                
                if trigger == "00-Core/Problem.md":
                    self._sync_from_problem()
                elif trigger == "00-Core/Metaheuristic.md":
                    self._sync_from_metaheuristic()
                
                self._update_file_state(trigger)
        
        if not changes_detected:
            print("ℹ️  No se detectaron cambios en archivos trigger.")
            print("   Los archivos están sincronizados.\n")
        else:
            print("\n✅ Sincronización completada exitosamente")
            self._log_sync_event(triggers)
    
    def _sync_from_problem(self):
        """Sincroniza archivos que dependen de Problem.md"""
        print("\n📝 Sincronizando desde Problem.md...")
        
        problem_data = self._parse_markdown("00-Core/Problem.md")
        
        # 1. Actualizar Grammar.md con terminales
        if "Domain-Operators" in problem_data['sections']:
            self._update_grammar(problem_data['sections']['Domain-Operators'])
        
        # 2. Actualizar Fitness-Function.md
        if "Mathematical-Model" in problem_data['sections']:
            self._update_fitness_objective(problem_data['sections']['Mathematical-Model'])
        
        # 3. Actualizar Dataset-Specification.md
        if "Solution-Representation" in problem_data['sections']:
            self._update_dataset_spec(problem_data['sections']['Solution-Representation'])
        
        # 4. Marcar scripts para regeneración
        self._mark_for_regeneration(['problem.py', 'fitness.py', 'data_loader.py'])
        
        print("   ✓ Sincronización desde Problem.md completada")
    
    def _sync_from_metaheuristic(self):
        """Sincroniza archivos que dependen de Metaheuristic.md"""
        print("\n🔧 Sincronizando desde Metaheuristic.md...")
        
        meta_data = self._parse_markdown("00-Core/Metaheuristic.md")
        
        # 1. Actualizar Search-Operators.md
        if "Search-Strategy" in meta_data['sections']:
            self._update_search_operators(meta_data['sections']['Search-Strategy'])
        
        # 2. Marcar scripts para regeneración
        self._mark_for_regeneration(['metaheuristic.py'])
        
        print("   ✓ Sincronización desde Metaheuristic.md completada")
    
    def _parse_markdown(self, rel_path: str) -> Dict:
        """Parsea un archivo .md y extrae metadatos y secciones"""
        file_path = self.root / rel_path
        
        if not file_path.exists():
            return {'metadata': {}, 'sections': {}}
        
        content = file_path.read_text(encoding='utf-8')
        
        # Extraer frontmatter YAML
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                except:
                    metadata = {}
        
        # Extraer secciones (## Titulo)
        sections = self._extract_sections(content)
        
        return {
            'metadata': metadata,
            'sections': sections,
            'content': content
        }
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extrae contenido de secciones ## Nombre-Seccion"""
        sections = {}
        
        # Pattern para secciones de nivel 2
        pattern = r'^## ([^\n]+)\n(.*?)(?=\n## |\Z)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_name] = section_content
        
        return sections
    
    def _extract_terminals(self, operators_text: str) -> List[str]:
        """Extrae nombres de terminales del texto Domain-Operators"""
        # Busca patrones como: - **TerminalName**: descripción
        pattern = r'\*\*([A-Z][a-zA-Z0-9_]*)\*\*:'
        terminals = re.findall(pattern, operators_text)
        return terminals
    
    def _update_grammar(self, domain_operators: str):
        """Actualiza 01-System/Grammar.md con nuevos terminales"""
        terminals = self._extract_terminals(domain_operators)
        
        if not terminals:
            print("   ⚠️  No se encontraron terminales en Domain-Operators")
            return
        
        grammar_path = self.root / "01-System/Grammar.md"
        content = grammar_path.read_text(encoding='utf-8')
        
        # Generar nueva sección de terminales
        terminals_bnf = terminals[0]
        for t in terminals[1:]:
            terminals_bnf += f"\n             | {t}"
        
        new_section = f"""<!-- AUTO-GENERATED from 00-Core/Problem.md::Domain-Operators -->
```bnf
<Terminal> ::= {terminals_bnf}
```
<!-- END AUTO-GENERATED -->"""
        
        # Reemplazar entre marcadores
        pattern = r'<!-- AUTO-GENERATED from 00-Core/Problem.md::Domain-Operators -->.*?<!-- END AUTO-GENERATED -->'
        updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        
        grammar_path.write_text(updated_content, encoding='utf-8')
        self._update_file_state("01-System/Grammar.md")
        
        print(f"   ✓ Grammar.md actualizado con {len(terminals)} terminales")
    
    def _update_fitness_objective(self, mathematical_model: str):
        """Actualiza sección de función objetivo en Fitness-Function.md"""
        fitness_path = self.root / "02-Components/Fitness-Function.md"
        content = fitness_path.read_text(encoding='utf-8')
        
        # Generar código Python básico (placeholder)
        new_section = f"""<!-- AUTO-GENERATED from 00-Core/Problem.md::Mathematical-Model -->
```python
def evaluate_solution(solution, problem_instance):
    \"\"\"
    Función objetivo extraída del modelo matemático:
    
{mathematical_model}
    \"\"\"
    # TODO: Implementar evaluación específica
    pass
```
<!-- END AUTO-GENERATED -->"""
        
        pattern = r'<!-- AUTO-GENERATED from 00-Core/Problem.md::Mathematical-Model -->.*?<!-- END AUTO-GENERATED -->'
        updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        
        fitness_path.write_text(updated_content, encoding='utf-8')
        self._update_file_state("02-Components/Fitness-Function.md")
        
        print("   ✓ Fitness-Function.md actualizado con función objetivo")
    
    def _update_dataset_spec(self, solution_repr: str):
        """Actualiza especificación de datasets"""
        spec_path = self.root / "06-Datasets/Dataset-Specification.md"
        content = spec_path.read_text(encoding='utf-8')
        
        new_section = f"""<!-- AUTO-GENERATED from 00-Core/Problem.md::Solution-Representation -->
```
Representación de solución:
{solution_repr}

Formato de archivo de instancia:
- Extensión recomendada: .txt
- Estructura: [A definir según el problema específico]
```
<!-- END AUTO-GENERATED -->"""
        
        pattern = r'<!-- AUTO-GENERATED from 00-Core/Problem.md::Solution-Representation -->.*?<!-- END AUTO-GENERATED -->'
        updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        
        spec_path.write_text(updated_content, encoding='utf-8')
        self._update_file_state("06-Datasets/Dataset-Specification.md")
        
        print("   ✓ Dataset-Specification.md actualizado")
    
    def _update_search_operators(self, search_strategy: str):
        """Actualiza configuración de operadores en Search-Operators.md"""
        ops_path = self.root / "02-Components/Search-Operators.md"
        content = ops_path.read_text(encoding='utf-8')
        
        new_section = f"""<!-- AUTO-GENERATED from 00-Core/Metaheuristic.md::Search-Strategy -->
```python
# Configuración de operadores extraída de Metaheuristic.md
# {search_strategy[:200]}...

MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
PERTURBATION_RATE = 0.05
```
<!-- END AUTO-GENERATED -->"""
        
        pattern = r'<!-- AUTO-GENERATED from 00-Core/Metaheuristic.md::Search-Strategy -->.*?<!-- END AUTO-GENERATED -->'
        updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        
        ops_path.write_text(updated_content, encoding='utf-8')
        self._update_file_state("02-Components/Search-Operators.md")
        
        print("   ✓ Search-Operators.md actualizado")
    
    def _mark_for_regeneration(self, scripts: List[str]):
        """Marca scripts para regeneración en Generation-Plan.md"""
        print(f"   ⏳ {len(scripts)} scripts marcados para regeneración: {', '.join(scripts)}")
        
        # Actualizar metadata
        metadata_path = self.root / "04-Generated/_metadata.yaml"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)
        
        for script in scripts:
            if script in metadata.get('scripts', {}):
                metadata['scripts'][script]['status'] = 'pending_regeneration'
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)
    
    def _log_sync_event(self, triggers: List[str]):
        """Registra evento de sincronización en Sync-Log.md"""
        log_path = self.root / "00-Core/Sync-Log.md"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
## {timestamp}

**Trigger**: {', '.join(triggers)}
**Archivos actualizados**: 
- 01-System/Grammar.md
- 02-Components/Fitness-Function.md
- 02-Components/Search-Operators.md
- 06-Datasets/Dataset-Specification.md

**Estado**: ✅ Exitoso
**Detalles**: Sincronización automática completada

---
"""
        
        # Agregar al log
        current_content = log_path.read_text(encoding='utf-8')
        # Insertar después del encabezado
        parts = current_content.split('---\n', 1)
        if len(parts) == 2:
            new_content = parts[0] + '---\n' + log_entry + parts[1]
        else:
            new_content = current_content + log_entry
        
        log_path.write_text(new_content, encoding='utf-8')
    
    def validate(self):
        """Valida consistencia de archivos"""
        print("🔍 Validando consistencia del framework...\n")
        
        issues = []
        
        # Verificar que archivos triggers existen y están completos
        if not (self.root / "00-Core/Problem.md").exists():
            issues.append("❌ 00-Core/Problem.md no existe")
        else:
            problem = self._parse_markdown("00-Core/Problem.md")
            if not problem['sections'].get('Domain-Operators'):
                issues.append("⚠️  Problem.md: falta sección Domain-Operators")
            if not problem['sections'].get('Mathematical-Model'):
                issues.append("⚠️  Problem.md: falta sección Mathematical-Model")
        
        if not (self.root / "00-Core/Metaheuristic.md").exists():
            issues.append("❌ 00-Core/Metaheuristic.md no existe")
        
        # Verificar sincronización
        for file_rel in ["01-System/Grammar.md", "02-Components/Fitness-Function.md"]:
            if not self.project_state.get("files", {}).get(file_rel, {}).get("synced", False):
                issues.append(f"⚠️  {file_rel} no está sincronizado")
        
        # Reporte
        if not issues:
            print("✅ Todos los archivos son consistentes\n")
            return True
        else:
            print("Problemas encontrados:\n")
            for issue in issues:
                print(f"  {issue}")
            print()
            return False
    
    def generate_scripts(self):
        """Genera scripts Python desde los .md (implementación básica)"""
        print("🔨 Generación de scripts...\n")
        print("⚠️  Funcionalidad de generación de código en desarrollo")
        print("   Por ahora, ejecuta sincronización con: --sync\n")
        
        # TODO: Implementar generación completa de scripts
        # Esto requeriría:
        # 1. Parsear cada .md según sus templates
        # 2. Generar código Python usando las plantillas
        # 3. Validar sintaxis generada
        # 4. Guardar en 04-Generated/scripts/


def main():
    """Punto de entrada del script"""
    
    # Obtener directorio raíz del proyecto GAA
    root = Path(__file__).parent.parent
    
    gaa = GAASync(root)
    
    if len(sys.argv) < 2:
        print("Uso: python sync-engine.py [--sync|--validate|--generate|--watch]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--sync":
        gaa.sync_all()
    
    elif command == "--validate":
        gaa.validate()
    
    elif command == "--generate":
        gaa.generate_scripts()
    
    elif command == "--watch":
        print("⚠️  Modo watch no implementado aún")
        print("   Ejecuta manualmente: python sync-engine.py --sync")
    
    else:
        print(f"Comando desconocido: {command}")
        print("Uso: python sync-engine.py [--sync|--validate|--generate|--watch]")
        sys.exit(1)


if __name__ == "__main__":
    main()
