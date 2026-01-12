from typing import List, Tuple
from models.process import Process
from core.timeline import Timeline

class FCFS:
    """
    Algoritmo de planificación FCFS (First Come, First Serve).
    - Atiende los procesos en el orden en que llegan al sistema.
    - No es apropiativo: una vez que un proceso comienza, se ejecuta hasta terminar.
    """
    name = "FCFS"

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        """
        Ejecuta el algoritmo FCFS sobre una lista de procesos.
        - Devuelve:
            • Un objeto Timeline con el diagrama de Gantt.
            • La lista de procesos con métricas calculadas (inicio, finalización, etc.).
        """
        # Orden inicial de procesos por tiempo de llegada y luego por ID
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0  # Tiempo actual de la simulación
        timeline = Timeline()  # Acumula los segmentos de ejecución

        # Iterar sobre cada proceso en orden de llegada
        for p in procs:
            # Si el tiempo actual es menor al tiempo de llegada, la CPU queda idle
            if t < p.arrival_time:
                timeline.add_slot(None, t, p.arrival_time)  # CPU inactiva hasta que llegue el proceso
                t = p.arrival_time

            # Inicia ejecución del proceso
            p.state = "Ejecutando"
            if p.start_time is None:
                p.start_time = t  # Registrar primera ejecución

            start = t
            t += p.burst_time  # Ejecutar el proceso completo (no apropiativo)
            p.remaining_time = 0
            p.completion_time = t
            p.state = "Terminado"

            # Registrar ejecución en el diagrama de Gantt
            timeline.add_slot(p.id, start, t)

        # Devolver timeline y lista completa de procesos con métricas
        return timeline, procs
