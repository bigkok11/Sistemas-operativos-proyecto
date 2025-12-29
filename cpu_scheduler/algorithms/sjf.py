# cpu_scheduler/algorithms/sjf.py
from typing import List, Tuple
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

class SJFNonPreemptive:
    name = "SJF (no apropiativo)"

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0
        timeline = Timeline()
        completed = 0
        n = len(procs)

        while completed < n:
            ready = [p for p in procs if p.arrival_time <= t and p.remaining_time > 0]
            if not ready:
                # avanzar al próximo arribo
                next_arrival = min([p.arrival_time for p in procs if p.remaining_time > 0], default=t)
                timeline.add_slot(None, t, next_arrival)
                t = next_arrival
                continue
            # elegir el de menor burst
            p = min(ready, key=lambda p: p.burst_time)
            p.state = "Ejecutando"
            if p.start_time is None:
                p.start_time = t
            start = t
            t += p.remaining_time
            p.remaining_time = 0
            p.completion_time = t
            p.state = "Terminado"
            completed += 1
            timeline.add_slot(p.id, start, t)

        return timeline, procs
