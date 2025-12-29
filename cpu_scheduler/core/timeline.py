# cpu_scheduler/core/timeline.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GanttSlot:
    """
    Un segmento de ejecución en el diagrama de Gantt.
    """
    process_id: Optional[str]  # None para idle
    start: int
    end: int

class Timeline:
    """
    Acumula los segmentos del diagrama de Gantt y calcula makespan.
    """
    def __init__(self):
        self.slots: List[GanttSlot] = []

    def add_slot(self, process_id: Optional[str], start: int, end: int):
        if start == end:
            return
        # Merge simple si el mismo proceso continúa contiguo
        if self.slots and self.slots[-1].process_id == process_id and self.slots[-1].end == start:
            self.slots[-1].end = end
        else:
            self.slots.append(GanttSlot(process_id, start, end))

    @property
    def makespan(self) -> int:
        return self.slots[-1].end if self.slots else 0

    @property
    def busy_time(self) -> int:
        return sum(slot.end - slot.start for slot in self.slots if slot.process_id is not None)

    def to_text(self) -> str:
        """
        Gantt textual simple.
        """
        if not self.slots:
            return "Sin ejecución."
        parts = []
        for s in self.slots:
            pid = s.process_id or "IDLE"
            parts.append(f"[{pid} | {s.start}→{s.end}]")
        return " ".join(parts)
