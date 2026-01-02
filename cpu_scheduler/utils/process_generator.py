from typing import List
from models.process import Process

def manual_create_processes() -> List[Process]:
    """
    Función principal para la creación manual de procesos.
    - Permite al usuario ingresar procesos por consola.
    - Cada proceso requiere:
        • ID (ejemplo: P1)
        • Tiempo de llegada (entero)
        • Tiempo de ráfaga (entero)
        • Prioridad (entero; menor número = mayor prioridad; por defecto 0)
    - El ingreso termina cuando el usuario deja el ID vacío.
    - Devuelve una lista de objetos `Process`.
    """
    processes: List[Process] = []  # Lista donde se almacenarán los procesos creados
    print("Creación manual de procesos (deja ID vacío para terminar).")
    while True:
        # Solicita al usuario el identificador del proceso
        pid = input("ID del proceso (ej: P1) deja ID vacío para terminar: ").strip()
        if pid == "":
            # Si el ID está vacío, se termina la entrada
            break
        # Solicita atributos básicos del proceso
        arrival = int(input("Tiempo de llegada (entero): ").strip())
        burst = int(input("Tiempo de ráfaga (entero): ").strip())
        # La prioridad es opcional, por defecto se asigna 0
        priority = int(input("Prioridad (entero, menor = mayor prioridad, default 0): ").strip() or "0")
        
        # Se crea un objeto Process y se agrega a la lista
        processes.append(Process(id=pid, arrival_time=arrival, burst_time=burst, priority=priority))
        print("Proceso agregado.\n")
    
    # Si no se creó ningún proceso, se notifica al usuario
    if not processes:
        print("No se crearon procesos.")
    return processes
