from typing import List, Tuple, Optional
from collections import deque
from models.process import Process
from core.timeline import Timeline

class RoundRobin:
    """
    Algoritmo de planificación Round Robin.
    - Asigna un quantum fijo de tiempo a cada proceso.
    - Los procesos se ejecutan en orden de llegada y se intercalan de forma cíclica.
    - Si un proceso no termina en su quantum, vuelve al final de la cola.
    """
    name = "Round Robin"

    def __init__(self, quantum: int = 4):
        """
        Inicializa el algoritmo con un quantum específico.
        - El quantum debe ser mayor que 0.
        """
        if quantum <= 0:
            raise ValueError("El quantum debe ser mayor a 0.")
        self.quantum = quantum

    def run(self, processes: List[Process]) -> Tuple[Timeline, List[Process]]:
        """
        Ejecuta el algoritmo Round Robin sobre una lista de procesos.
        - Devuelve:
            • Un objeto Timeline con el diagrama de Gantt.
            • La lista de procesos con métricas calculadas (inicio, finalización, etc.).
        """
        # Orden inicial de procesos por tiempo de llegada y luego por ID
        procs = sorted(processes, key=lambda p: (p.arrival_time, p.id))
        t = 0  # Tiempo actual de la simulación
        timeline = Timeline()  # Acumula los segmentos de ejecución
        queue = deque()  # Cola circular de procesos listos
        idx = 0  # Índice para recorrer procesos ordenados por llegada
        finished = 0  # Contador de procesos completados
        n = len(procs)  # Número total de procesos

        # Bucle principal: se ejecuta hasta que todos los procesos terminen
        while finished < n:
            # Ingresar procesos que llegan en el tiempo actual
            while idx < n and procs[idx].arrival_time <= t:
                queue.append(procs[idx])
                procs[idx].state = "Listo"
                idx += 1

            if not queue:
                # Si no hay procesos listos, avanzar al próximo arribo
                if idx < n:
                    next_arrival = procs[idx].arrival_time
                    timeline.add_slot(None, t, next_arrival)  # CPU idle hasta próximo arribo
                    t = next_arrival
                    continue
                else:
                    break  # No quedan procesos pendientes

            # Seleccionar el primer proceso de la cola
            p = queue.popleft()
            run_time = min(self.quantum, p.remaining_time)  # Ejecutar hasta quantum o hasta terminar
            if p.start_time is None:
                p.start_time = t  # Registrar primera ejecución
            p.state = "Ejecutando"
            start = t
            t += run_time
            p.remaining_time -= run_time
            timeline.add_slot(p.id, start, t)  # Registrar ejecución en el diagrama de Gantt

            # Ingresar nuevos procesos que hayan llegado durante este quantum
            while idx < n and procs[idx].arrival_time <= t:
                queue.append(procs[idx])
                procs[idx].state = "Listo"
                idx += 1

            if p.remaining_time > 0:
                # Si el proceso no terminó, vuelve al final de la cola
                p.state = "Listo"
                queue.append(p)
            else:
                # Si terminó, registrar tiempo de finalización
                p.state = "Terminado"
                p.completion_time = t
                finished += 1

        # Devolver timeline y lista completa de procesos con métricas
        return timeline, procs
