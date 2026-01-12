from typing import List, Tuple
from models.process import Process
from core.timeline import Timeline

class SJFNonPreemptive:
    """
    Algoritmo de planificación SJF (Shortest Job First) en su versión no apropiativa.
    - Selecciona siempre el proceso con menor tiempo de ráfaga (burst).
    - Una vez que un proceso comienza a ejecutarse, no se interrumpe hasta finalizar.
    """
    name = "SJF (no apropiativo)"

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        """
        Ejecuta el algoritmo SJF no apropiativo sobre una lista de procesos.
        - Devuelve:
            • Un objeto Timeline con el diagrama de Gantt.
            • La lista de procesos con métricas calculadas (inicio, finalización, etc.).
        """
        # Orden inicial de procesos por tiempo de llegada y luego por ID
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0  # Tiempo actual de la simulación
        timeline = Timeline()  # Acumula los segmentos de ejecución
        completed = 0  # Contador de procesos completados
        n = len(procs)  # Número total de procesos

        # Bucle principal: se ejecuta hasta que todos los procesos terminen
        while completed < n:
            # Lista de procesos listos en el tiempo actual
            ready = [p for p in procs if p.arrival_time <= t and p.remaining_time > 0]

            if not ready:
                # Si no hay procesos listos, avanzar al próximo arribo
                next_arrival = min([p.arrival_time for p in procs if p.remaining_time > 0], default=t)
                timeline.add_slot(None, t, next_arrival)  # CPU idle hasta el próximo arribo
                t = next_arrival
                continue

            # Seleccionar el proceso con menor tiempo de ráfaga (criterio SJF)
            p = min(ready, key=lambda p: p.burst_time)
            p.state = "Ejecutando"

            # Registrar el tiempo de inicio si es la primera vez que ejecuta
            if p.start_time is None:
                p.start_time = t

            start = t
            # Ejecutar el proceso completo (no apropiativo: no se interrumpe)
            t += p.remaining_time
            p.remaining_time = 0
            p.completion_time = t
            p.state = "Terminado"
            completed += 1

            # Agregar el segmento al diagrama de Gantt
            timeline.add_slot(p.id, start, t)

        # Devolver timeline y lista completa de procesos con métricas
        return timeline, procs
