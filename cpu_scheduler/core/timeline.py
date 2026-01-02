from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GanttSlot:
    """
    Representa un segmento de ejecución en el diagrama de Gantt.
    - Cada slot indica qué proceso se ejecuta en un intervalo de tiempo.
    - Si `process_id` es None, significa que la CPU estuvo en estado idle (inactiva).
    """
    process_id: Optional[str]  # Identificador del proceso, None si la CPU está inactiva
    start: int                 # Tiempo de inicio del segmento
    end: int                   # Tiempo de finalización del segmento


class Timeline:
    """
    Clase que acumula los segmentos del diagrama de Gantt y calcula métricas globales.
    - Contiene una lista de `GanttSlot` que representan la ejecución de procesos.
    - Permite calcular:
        • makespan: tiempo total de la simulación (desde el inicio hasta el último slot).
        • busy_time: tiempo total en que la CPU estuvo ocupada ejecutando procesos.
    - También ofrece una representación textual del diagrama de Gantt.
    """
    def __init__(self):
        self.slots: List[GanttSlot] = []  # Lista de segmentos de ejecución

    def add_slot(self, process_id: Optional[str], start: int, end: int):
        """
        Agrega un nuevo segmento al diagrama de Gantt.
        - Si el intervalo es vacío (start == end), no se agrega nada.
        - Si el proceso es el mismo que el último y los intervalos son contiguos,
          se fusionan en un único segmento (optimización simple).
        """
        if start == end:
            return
        # Merge simple si el mismo proceso continúa inmediatamente después
        if self.slots and self.slots[-1].process_id == process_id and self.slots[-1].end == start:
            self.slots[-1].end = end
        else:
            self.slots.append(GanttSlot(process_id, start, end))

    @property
    def makespan(self) -> int:
        """
        Devuelve el tiempo total de la simulación.
        - Corresponde al tiempo de finalización del último segmento.
        - Si no hay slots, devuelve 0.
        """
        return self.slots[-1].end if self.slots else 0

    @property
    def busy_time(self) -> int:
        """
        Devuelve el tiempo total en que la CPU estuvo ocupada.
        - Se calcula sumando la duración de todos los slots con procesos activos.
        - Los slots con `process_id = None` (idle) no se cuentan.
        """
        return sum(slot.end - slot.start for slot in self.slots if slot.process_id is not None)

    def to_text(self) -> str:
        """
        Genera una representación textual simple del diagrama de Gantt.
        - Cada segmento se muestra como: [Proceso | inicio→fin]
        - Si el proceso es None, se muestra como "IDLE".
        """
        if not self.slots:
            return "Sin ejecución."
        parts = []
        for s in self.slots:
            pid = s.process_id or "IDLE"
            parts.append(f"[{pid} | {s.start}→{s.end}]")
        return " ".join(parts)
