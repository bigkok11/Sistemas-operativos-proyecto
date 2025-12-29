# cpu_scheduler/utils/process_generator.py
from typing import List
from cpu_scheduler.models.process import Process

def manual_create_processes() -> List[Process]:
    """
    Entrada por consola para crear procesos.
    """
    processes: List[Process] = []
    print("Creación manual de procesos (deja ID vacío para terminar).")
    while True:
        pid = input("ID del proceso (ej: P1): ").strip()
        if pid == "":
            break
        arrival = int(input("Tiempo de llegada (entero): ").strip())
        burst = int(input("Tiempo de ráfaga (entero): ").strip())
        priority = int(input("Prioridad (entero, menor = mayor prioridad, default 0): ").strip() or "0")
        processes.append(Process(id=pid, arrival_time=arrival, burst_time=burst, priority=priority))
        print("Proceso agregado.\n")
    if not processes:
        print("No se crearon procesos.")
    return processes
