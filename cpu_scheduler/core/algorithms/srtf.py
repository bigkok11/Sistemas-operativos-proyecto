import copy
from typing import List, Tuple
from models.process import Process
from core.timeline import Timeline

class SRTF:
    """
    Algoritmo de planificación SRTF (Shortest Remaining Time First).
    - Es una versión apropiativa del algoritmo SJF.
    - Siempre selecciona el proceso con menor tiempo restante de ejecución.
    - Si llega un nuevo proceso con menor tiempo restante, interrumpe al actual.
    """
    def __init__(self):
        self.name = "SRTF (Shortest Remaining Time First)"

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        """
        Ejecuta el algoritmo SRTF sobre una lista de procesos.
        - Devuelve:
            • Un objeto Timeline con el diagrama de Gantt.
            • La lista de procesos con métricas calculadas (inicio, finalización, etc.).
        """
        # Copiamos los procesos para no modificar la lista original
        procs = [copy.deepcopy(p) for p in processes]
        timeline = Timeline()  # Acumula los segmentos de ejecución
        time = 0               # Tiempo actual de la simulación
        ready_queue = []       # Cola de procesos listos para ejecutar
        waiting = sorted(procs, key=lambda p: p.arrival_time)  # Procesos ordenados por llegada
        completed = 0          # Contador de procesos completados
        n = len(procs)         # Número total de procesos

        # Bucle principal: se ejecuta hasta que todos los procesos terminen
        while completed < n:
            # Agregar procesos que llegan en este tiempo a la cola de listos
            while waiting and waiting[0].arrival_time <= time:
                ready_queue.append(waiting.pop(0))

            if ready_queue:
                # Elegir el proceso con menor tiempo restante (criterio SRTF)
                ready_queue.sort(key=lambda p: p.remaining_time)
                current = ready_queue[0]

                # Si es la primera vez que ejecuta, registrar start_time
                if current.start_time is None:
                    current.start_time = time
                current.state = "Ejecutando"

                # Ejecutar 1 unidad de tiempo
                timeline.add_slot(current.id, time, time + 1)
                current.remaining_time -= 1
                time += 1

                # Si el proceso termina, registrar completion_time y sacarlo de la cola
                if current.remaining_time == 0:
                    current.completion_time = time
                    current.state = "Terminado"
                    ready_queue.pop(0)
                    completed += 1
            else:
                # Si no hay procesos listos, la CPU está inactiva (idle)
                timeline.add_slot(None, time, time + 1)
                time += 1

        # Devolver timeline y lista completa de procesos con métricas
        return timeline, procs
