# cpu_scheduler/algorithms/priority.py
from typing import List, Tuple
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

class PriorityScheduler:
    name = "Prioridades"

    def __init__(self, preemptive: bool = True):
        self.preemptive = preemptive

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0
        timeline = Timeline()
        n = len(procs)
        finished = 0
        current = None  # proceso actual

        while finished < n:
            ready = [p for p in procs if p.arrival_time <= t and p.remaining_time > 0]
            if not ready:
                next_arrival = min([p.arrival_time for p in procs if p.remaining_time > 0], default=t)
                timeline.add_slot(None, t, next_arrival)
                t = next_arrival
                current = None
                continue

            # Selección por prioridad (menor número => mayor prioridad)
            highest = min(ready, key=lambda p: (p.priority, p.arrival_time, p.id))

            if not self.preemptive and current is not None and current.remaining_time > 0:
                # No apropiativo: continuar con current hasta terminar
                chosen = current
            else:
                chosen = highest

            if chosen.start_time is None:
                chosen.start_time = t
            chosen.state = "Ejecutando"

            if self.preemptive:
                # Ejecuta 1 unidad y reevalúa
                start = t
                t += 1
                chosen.remaining_time -= 1
                timeline.add_slot(chosen.id, start, t)
            else:
                # Ejecuta hasta terminar
                start = t
                t += chosen.remaining_time
                chosen.remaining_time = 0
                timeline.add_slot(chosen.id, start, t)

            if chosen.remaining_time == 0:
                chosen.state = "Terminado"
                chosen.completion_time = t
                finished += 1
                current = None
            else:
                chosen.state = "Listo"
                current = chosen if not self.preemptive else None

        return timeline, procs
