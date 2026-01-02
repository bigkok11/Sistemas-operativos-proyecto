from typing import List, Dict, Protocol, Tuple
from copy import deepcopy
from models.process import Process
from core.timeline import Timeline

class IScheduler(Protocol):
    """
    Interfaz (protocolo) para algoritmos de planificación de CPU.
    - Define la estructura mínima que debe cumplir cualquier scheduler:
        • Atributo `name`: nombre del algoritmo.
        • Método `run`: recibe una lista de procesos y devuelve:
            - Un objeto `Timeline` con la secuencia de ejecución.
            - Una lista de procesos finalizados con sus métricas calculadas.
    """
    name: str
    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        ...


def deep_reset(processes: List[Process]) -> List[Process]:
    """
    Crea una copia profunda de la lista de procesos y reinicia su estado.
    - Se utiliza para ejecutar múltiples algoritmos sobre la misma carga de trabajo
      sin que los resultados de uno afecten a los demás.
    - Llama al método `reset_runtime()` de cada proceso para restaurar tiempos y estado.
    """
    cloned = deepcopy(processes)  # Copia independiente de los procesos
    for p in cloned:
        p.reset_runtime()  # Reinicia métricas y estado
    return cloned


def generate_ready_list(processes: List[Process], t: int) -> List[Process]:
    """
    Genera la lista de procesos listos para ejecutar en un instante de tiempo `t`.
    - Incluye procesos cuya hora de llegada es menor o igual a `t`
      y que aún tienen tiempo restante de ejecución.
    - Se usa en algoritmos apropiativos como SRTF o Round Robin.
    """
    return [p for p in processes if p.arrival_time <= t and p.remaining_time > 0]


def pick_best_algorithm(results: Dict[str, Dict[str, float]]) -> str:
    """
    Selecciona automáticamente el 'mejor' algoritmo de planificación.
    - Criterio actual: menor tiempo promedio de espera (`avg_waiting`).
    - Recibe un diccionario con métricas por algoritmo.
    - Devuelve el nombre del algoritmo con mejor desempeño.
    - Nota: puede extenderse para incluir ponderaciones o múltiples métricas.
    """
    best = min(results.items(), key=lambda kv: kv[1]["avg_waiting"])
    return best[0]
