# cpu_scheduler/core/scheduler.py
from typing import List, Dict, Protocol, Tuple
from copy import deepcopy
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

class IScheduler(Protocol):
    name: str
    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        ...

def deep_reset(processes: List[Process]) -> List[Process]:
    cloned = deepcopy(processes)
    for p in cloned:
        p.reset_runtime()
    return cloned

def generate_ready_list(processes: List[Process], t: int) -> List[Process]:
    return [p for p in processes if p.arrival_time <= t and p.remaining_time > 0]

def pick_best_algorithm(results: Dict[str, Dict[str, float]]) -> str:
    """
    Escoge 'mejor' algoritmo según menor promedio de espera.
    Se puede extender a ponderaciones.
    """
    best = min(results.items(), key=lambda kv: kv[1]["avg_waiting"])
    return best[0]
