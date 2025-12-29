# cpu_scheduler/main.py
import sys
from typing import List
from cpu_scheduler.models.process import Process
from cpu_scheduler.algorithms.fcfs import FCFS
from cpu_scheduler.algorithms.sjf import SJFNonPreemptive
from cpu_scheduler.algorithms.round_robin import RoundRobin
from cpu_scheduler.algorithms.priority import PriorityScheduler
from cpu_scheduler.utils.file_handler import load_named_set
from cpu_scheduler.utils.process_generator import manual_create_processes
from cpu_scheduler.ui.interface import run_simulation
def select_process_source() -> List[Process]:
    print("Fuente de procesos:")
    print("1) Cargar desde archivo JSON (tests/cases.json)")
    print("2) Crear manualmente")
    choice = input("Selecciona opción [1/2]: ").strip() or "1"
    if choice == "1":
        path = "tests/cases.json"
        print("\nConjuntos disponibles: set1, set2, set_personal (edítalo).")
        name = input("Nombre del conjunto (default: set1): ").strip() or "set1"
        try:
            processes = load_named_set(path, name)
        except Exception as e:
            print(f"Error cargando archivo: {e}")
            processes = []
        if not processes:
            print("No se encontraron procesos. Volviendo a entrada manual.")
            processes = manual_create_processes()
        return processes
    else:
        return manual_create_processes()

def select_algorithms() -> List:
    print("\nAlgoritmos disponibles:")
    print("1) FCFS")
    print("2) SJF (no apropiativo)")
    print("3) Round Robin (configurable)")
    print("4) Prioridades (elige preemptivo/no preemptivo)")
    print("5) Ejecutar TODOS")
    sel = input("Elige [1-5] (default 5): ").strip() or "5"

    algos = []
    if sel == "1":
        algos = [FCFS()]
    elif sel == "2":
        algos = [SJFNonPreemptive()]
    elif sel == "3":
        q = int(input("Quantum (típicos: 2,4,6; default 4): ").strip() or "4")
        algos = [RoundRobin(quantum=q)]
    elif sel == "4":
        pre_flag = input("¿Preemptivo? [s/n] (default s): ").strip().lower() or "s"
        preemptive = pre_flag.startswith("s")
        algos = [PriorityScheduler(preemptive=preemptive)]
    else:
        q = int(input("Quantum para Round Robin (default 4): ").strip() or "4")
        pre_flag = input("Prioridades preemptivo? [s/n] (default s): ").strip().lower() or "s"
        preemptive = pre_flag.startswith("s")
        algos = [FCFS(), SJFNonPreemptive(), RoundRobin(quantum=q), PriorityScheduler(preemptive=preemptive)]
    return algos

def main():
    print("Simulador de planificación de CPU (UCAB - Proyecto)")
    processes = select_process_source()
    if not processes:
        print("No hay procesos. Saliendo.")
        sys.exit(1)
    print("\nProcesos cargados/creados:")
    for p in processes:
        print(f"- {p.id}: llegada={p.arrival_time}, ráfaga={p.burst_time}, prioridad={p.priority}")

    schedulers = select_algorithms()
    run_simulation(processes, schedulers)

if __name__ == "__main__":
    main()
