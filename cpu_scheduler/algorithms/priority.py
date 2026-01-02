from typing import List, Tuple
from models.process import Process
from core.timeline import Timeline

class PriorityScheduler:
    """
    Algoritmo de planificación por prioridades.
    - Cada proceso tiene un valor de prioridad (menor número = mayor prioridad).
    - Puede funcionar en dos modos:
        • Preemptivo: interrumpe el proceso actual si llega otro con mayor prioridad.
        • No preemptivo: una vez que un proceso comienza, se ejecuta hasta terminar.
    """
    name = "Prioridades"

    def __init__(self, preemptive: bool = True):
        """
        Inicializa el planificador con el modo deseado.
        - preemptive=True: versión apropiativa.
        - preemptive=False: versión no apropiativa.
        """
        self.preemptive = preemptive

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        """
        Ejecuta el algoritmo de planificación por prioridades.
        - Recibe una lista de procesos.
        - Devuelve:
            • Un objeto Timeline con el diagrama de Gantt.
            • La lista de procesos con métricas calculadas (inicio, finalización, etc.).
        """
        # Orden inicial de procesos por tiempo de llegada y luego por ID
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0  # Tiempo actual de la simulación
        timeline = Timeline()  # Acumula los segmentos de ejecución
        n = len(procs)  # Número total de procesos
        finished = 0  # Contador de procesos completados
        current = None  # Proceso en ejecución (solo relevante en modo no preemptivo)

        # Bucle principal: se ejecuta hasta que todos los procesos terminen
        while finished < n:
            # Lista de procesos listos en el tiempo actual
            ready = [p for p in procs if p.arrival_time <= t and p.remaining_time > 0]

            if not ready:
                # Si no hay procesos listos, avanzar al próximo arribo
                next_arrival = min([p.arrival_time for p in procs if p.remaining_time > 0], default=t)
                timeline.add_slot(None, t, next_arrival)  # CPU idle hasta próximo arribo
                t = next_arrival
                current = None
                continue

            # Selección por prioridad (menor número => mayor prioridad).
            # En caso de empate, se usa tiempo de llegada e ID como criterios secundarios.
            highest = min(ready, key=lambda p: (p.priority, p.arrival_time, p.id))

            if not self.preemptive and current is not None and current.remaining_time > 0:
                # No apropiativo: continuar con el proceso actual hasta terminar
                chosen = current
            else:
                # Preemptivo o inicio de nuevo proceso
                chosen = highest

            # Registrar tiempo de inicio si es la primera vez que ejecuta
            if chosen.start_time is None:
                chosen.start_time = t
            chosen.state = "Ejecutando"

            if self.preemptive:
                # Modo preemptivo: ejecutar solo 1 unidad de tiempo y luego reevaluar
                start = t
                t += 1
                chosen.remaining_time -= 1
                timeline.add_slot(chosen.id, start, t)
            else:
                # Modo no preemptivo: ejecutar hasta terminar
                start = t
                t += chosen.remaining_time
                chosen.remaining_time = 0
                timeline.add_slot(chosen.id, start, t)

            # Verificar si el proceso terminó
            if chosen.remaining_time == 0:
                chosen.state = "Terminado"
                chosen.completion_time = t
                finished += 1
                current = None
            else:
                # Si aún queda tiempo, vuelve a estado "Listo"
                chosen.state = "Listo"
                current = chosen if not self.preemptive else None

        # Devolver timeline y lista completa de procesos con métricas
        return timeline, procs
