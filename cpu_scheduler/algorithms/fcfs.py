# cpu_scheduler/algorithms/fcfs.py
from typing import List, Tuple
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

class FCFS:
    name = "FCFS"

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0
        timeline = Timeline()

        for p in procs:
            if t < p.arrival_time:
                timeline.add_slot(None, t, p.arrival_time)
                t = p.arrival_time
            p.state = "Ejecutando"
            if p.start_time is None:
                p.start_time = t
            start = t
            t += p.burst_time
            p.remaining_time = 0
            p.completion_time = t
            p.state = "Terminado"
            timeline.add_slot(p.id, start, t)

        return timeline, procs
