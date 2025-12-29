# cpu_scheduler/algorithms/round_robin.py
from typing import List, Tuple, Optional
from collections import deque
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

class RoundRobin:
    name = "Round Robin"

    def __init__(self, quantum: int = 4):
        if quantum <= 0:
            raise ValueError("El quantum debe ser mayor a 0.")
        self.quantum = quantum

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0
        timeline = Timeline()
        queue = deque()
        idx = 0
        finished = 0
        n = len(procs)

        while finished < n:
            # Ingresar procesos que llegan en t
            while idx < n and procs[idx].arrival_time <= t:
                queue.append(procs[idx])
                procs[idx].state = "Listo"
                idx += 1

            if not queue:
                # Si no hay listos, saltar al próximo arrival
                if idx < n:
                    next_arrival = procs[idx].arrival_time
                    timeline.add_slot(None, t, next_arrival)
                    t = next_arrival
                    continue
                else:
                    break

            p = queue.popleft()
            run_time = min(self.quantum, p.remaining_time)
            if p.start_time is None:
                p.start_time = t
            p.state = "Ejecutando"
            start = t
            t += run_time
            p.remaining_time -= run_time
            timeline.add_slot(p.id, start, t)

            # Agregar nuevos arribos durante el quantum
            while idx < n and procs[idx].arrival_time <= t:
                queue.append(procs[idx])
                procs[idx].state = "Listo"
                idx += 1

            if p.remaining_time > 0:
                p.state = "Listo"
                queue.append(p)  # vuelve al final
            else:
                p.state = "Terminado"
                p.completion_time = t
                finished += 1

        return timeline, procs
