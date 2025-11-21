"""
Time Tracker - KBP-SA
Sistema de seguimiento de tiempo de ejecución en tiempo real
Genera archivo time_tracking.md con métricas de rendimiento

Fase 5 GAA: Experimentación controlada - Monitoreo de rendimiento
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import time
from dataclasses import dataclass, field
from contextlib import contextmanager


@dataclass
class ProcessInfo:
    """Información de un proceso individual"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    status: str = "En progreso"  # En progreso, Completado, Error
    details: Dict[str, Any] = field(default_factory=dict)
    sub_processes: List['ProcessInfo'] = field(default_factory=list)

    def finish(self, status: str = "Completado"):
        """Marca el proceso como finalizado"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = status

    def add_detail(self, key: str, value: Any):
        """Agrega un detalle al proceso"""
        self.details[key] = value


class TimeTracker:
    """
    Sistema de seguimiento de tiempo en tiempo real

    Registra todos los procesos y genera un archivo Markdown
    que se actualiza continuamente mientras el código se ejecuta.

    Features:
    - Seguimiento jerárquico de procesos
    - Actualización en tiempo real del archivo .md
    - Métricas acumuladas de tiempo
    - Registro de detalles por proceso
    """

    def __init__(self, output_file: str = "time_tracking.md", output_dir: str = "output", verbose: bool = True):
        """
        Args:
            output_file: Nombre del archivo de seguimiento
            output_dir: Directorio de salida
            verbose: Si True, imprime mensajes en consola con timestamps
        """
        self.output_path = Path(output_dir) / output_file
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.start_time = time.time()
        self.processes: List[ProcessInfo] = []
        self.current_process: Optional[ProcessInfo] = None
        self.process_stack: List[ProcessInfo] = []  # Para procesos anidados
        self.verbose = verbose

        self._initialize_file()

        if self.verbose:
            start_timestamp = datetime.fromtimestamp(self.start_time).strftime("%H:%M:%S")
            print(f"\n{'='*80}", flush=True)
            print(f"⏱️  TIME TRACKING INICIADO - {start_timestamp}", flush=True)
            print(f"{'='*80}\n", flush=True)

    def _initialize_file(self):
        """Inicializa el archivo de seguimiento"""
        content = self._generate_header()
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_header(self) -> str:
        """Genera el encabezado del archivo"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""# Time Tracking Report

**Fecha de inicio:** {now}
**Estado:** En ejecución

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Tiempo total | En progreso... |
| Procesos completados | 0 |
| Procesos activos | 0 |

---

## Procesos

"""

    def start_process(self, name: str, details: Optional[Dict[str, Any]] = None) -> ProcessInfo:
        """
        Inicia un nuevo proceso

        Args:
            name: Nombre del proceso
            details: Detalles opcionales del proceso

        Returns:
            Información del proceso iniciado
        """
        process = ProcessInfo(
            name=name,
            start_time=time.time(),
            details=details or {}
        )

        # Si hay un proceso activo, este es un subproceso
        if self.current_process:
            self.current_process.sub_processes.append(process)
            self.process_stack.append(self.current_process)
        else:
            self.processes.append(process)

        self.current_process = process

        # Imprimir mensaje de inicio si verbose está activado
        if self.verbose:
            timestamp = datetime.fromtimestamp(process.start_time).strftime("%H:%M:%S")
            indent = "  " * len(self.process_stack)
            print(f"{indent}⏱️  [{timestamp}] INICIANDO: {name}", flush=True)
            if details:
                for key, value in details.items():
                    print(f"{indent}   └─ {key}: {value}", flush=True)

        self._update_file()

        return process

    def finish_process(self, status: str = "Completado", **details):
        """
        Finaliza el proceso actual

        Args:
            status: Estado final del proceso
            **details: Detalles adicionales a agregar
        """
        if self.current_process:
            self.current_process.finish(status)

            # Agregar detalles adicionales
            for key, value in details.items():
                self.current_process.add_detail(key, value)

            # Imprimir mensaje de finalización si verbose está activado
            if self.verbose:
                end_timestamp = datetime.fromtimestamp(self.current_process.end_time).strftime("%H:%M:%S")
                duration_str = self._format_duration(self.current_process.duration)
                indent = "  " * len(self.process_stack)

                status_icon = "✅" if status == "Completado" else "❌" if status == "Error" else "⚪"
                print(f"{indent}{status_icon} [{end_timestamp}] FINALIZADO: {self.current_process.name}", flush=True)
                print(f"{indent}   └─ Duración: {duration_str}", flush=True)

                if details:
                    for key, value in details.items():
                        print(f"{indent}   └─ {key}: {value}", flush=True)
                print(flush=True)  # Línea en blanco para separar

            # Volver al proceso padre si existe
            if self.process_stack:
                self.current_process = self.process_stack.pop()
            else:
                self.current_process = None

            self._update_file()

    def update_current(self, **details):
        """
        Actualiza detalles del proceso actual sin finalizarlo

        Args:
            **details: Detalles a actualizar
        """
        if self.current_process:
            for key, value in details.items():
                self.current_process.add_detail(key, value)
            self._update_file()

    @contextmanager
    def track(self, name: str, **details):
        """
        Context manager para tracking automático

        Usage:
            with tracker.track("Cargar datos", dataset="low_dim"):
                # código a ejecutar
                pass

        Args:
            name: Nombre del proceso
            **details: Detalles del proceso
        """
        process = self.start_process(name, details)
        try:
            yield process
            self.finish_process("Completado")
        except Exception as e:
            self.finish_process("Error", error=str(e))
            raise

    def _update_file(self):
        """Actualiza el archivo con el estado actual"""
        content = self._generate_content()
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_content(self) -> str:
        """Genera el contenido completo del archivo"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed = time.time() - self.start_time

        # Contar procesos
        total_processes = self._count_processes(self.processes)
        completed = self._count_completed(self.processes)
        active = 1 if self.current_process else 0

        content = f"""# Time Tracking Report

**Fecha de inicio:** {datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S")}
**Última actualización:** {now}
**Estado:** {"En ejecución" if self.current_process or active > 0 else "Completado"}

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Tiempo total | {self._format_duration(elapsed)} |
| Procesos totales | {total_processes} |
| Procesos completados | {completed} |
| Procesos activos | {active} |

---

## Procesos

"""
        # Agregar procesos
        for process in self.processes:
            content += self._format_process(process, level=0)

        # Agregar proceso actual si existe
        if self.current_process and self.current_process not in self.processes:
            # Es un subproceso, ya está incluido
            pass

        return content

    def _format_process(self, process: ProcessInfo, level: int = 0) -> str:
        """
        Formatea un proceso para el archivo Markdown

        Args:
            process: Información del proceso
            level: Nivel de indentación (para subprocesos)

        Returns:
            String formateado en Markdown
        """
        indent = "  " * level
        icon = self._get_status_icon(process.status)

        # Calcular duración
        if process.duration:
            duration_str = self._format_duration(process.duration)
        elif process.status == "En progreso":
            current_duration = time.time() - process.start_time
            duration_str = f"{self._format_duration(current_duration)} (en progreso)"
        else:
            duration_str = "N/A"

        # Título del proceso
        content = f"{indent}### {icon} {process.name}\n\n"

        # Detalles
        content += f"{indent}**Estado:** {process.status}  \n"
        content += f"{indent}**Duración:** {duration_str}  \n"
        content += f"{indent}**Inicio:** {datetime.fromtimestamp(process.start_time).strftime('%H:%M:%S')}  \n"

        if process.end_time:
            content += f"{indent}**Fin:** {datetime.fromtimestamp(process.end_time).strftime('%H:%M:%S')}  \n"

        # Detalles adicionales
        if process.details:
            content += f"\n{indent}**Detalles:**\n"
            for key, value in process.details.items():
                content += f"{indent}- {key}: {value}\n"

        content += "\n"

        # Subprocesos
        if process.sub_processes:
            content += f"{indent}**Subprocesos:**\n\n"
            for sub in process.sub_processes:
                content += self._format_process(sub, level + 1)

        return content

    def _get_status_icon(self, status: str) -> str:
        """Obtiene el icono según el estado"""
        icons = {
            "En progreso": "⏳",
            "Completado": "✅",
            "Error": "❌"
        }
        return icons.get(status, "⚪")

    def _format_duration(self, seconds: float) -> str:
        """Formatea duración en formato legible"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.1f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def _count_processes(self, processes: List[ProcessInfo]) -> int:
        """Cuenta total de procesos incluyendo subprocesos"""
        count = len(processes)
        for p in processes:
            count += self._count_processes(p.sub_processes)
        return count

    def _count_completed(self, processes: List[ProcessInfo]) -> int:
        """Cuenta procesos completados"""
        count = sum(1 for p in processes if p.status == "Completado")
        for p in processes:
            count += self._count_completed(p.sub_processes)
        return count

    def finalize(self):
        """Finaliza el tracking y genera reporte final"""
        if self.current_process:
            self.finish_process("Completado")

        self._update_file()

        total_time = time.time() - self.start_time
        end_timestamp = datetime.now().strftime("%H:%M:%S")

        if self.verbose:
            print(f"\n{'='*80}", flush=True)
            print(f"⏱️  TIME TRACKING FINALIZADO - {end_timestamp}", flush=True)
            print(f"{'='*80}", flush=True)
            print(f"📊 Resumen:", flush=True)
            print(f"   • Archivo: {self.output_path}", flush=True)
            print(f"   • Tiempo total: {self._format_duration(total_time)}", flush=True)
            print(f"   • Procesos totales: {self._count_processes(self.processes)}", flush=True)
            print(f"   • Procesos completados: {self._count_completed(self.processes)}", flush=True)
            print(f"{'='*80}\n", flush=True)
        else:
            print(f"\n📊 Time tracking finalizado:", flush=True)
            print(f"   • Archivo: {self.output_path}", flush=True)
            print(f"   • Tiempo total: {self._format_duration(total_time)}", flush=True)
            print(f"   • Procesos: {self._count_processes(self.processes)}", flush=True)
