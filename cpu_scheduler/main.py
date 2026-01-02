import sys
import os
from typing import List
from models.process import Process
from algorithms.fcfs import FCFS
from algorithms.sjf import SJFNonPreemptive
from algorithms.round_robin import RoundRobin
from algorithms.priority import PriorityScheduler
from utils.file_handler import load_named_set
from utils.process_generator import manual_create_processes
from ui.interface import run_simulation
from algorithms.srtf import SRTF

# Ruta absoluta al directorio raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_PATH = os.path.join(PROJECT_ROOT, "tests", "cases.json")


def ask_until_valid(prompt: str, valid_options: List[str], default: str) -> str:
    """
    Pregunta al usuario hasta que ingrese una opción válida.
    - valid_options: lista de opciones aceptadas (strings).
    - default: valor por defecto si el usuario no escribe nada.
    """
    while True:
        value = input(prompt).strip().lower()
        if not value:
            return default
        if value in valid_options:
            return value
        print(f"Entrada inválida. Opciones válidas: {', '.join(valid_options)}")


def safe_int_input(prompt: str, default: int, min_val: int = 1, max_val: int = 100) -> int:
    """
    Función auxiliar para pedir un número entero al usuario.
    - Si la entrada no es válida, repregunta hasta obtener un número válido.
    - Aplica límites (min_val, max_val).
    """
    while True:
        value = input(prompt).strip()
        if not value:
            return default
        try:
            num = int(value)
            if num < min_val or num > max_val:
                print(f"El número debe estar entre {min_val} y {max_val}.")
                continue
            return num
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entero.")


def select_process_source() -> List[Process]:
    """
    Selección de fuente de procesos con validación robusta.
    """
    print("Fuente de procesos:")
    print("1) Cargar desde archivo JSON (tests/cases.json)")
    print("2) Crear manualmente")

    choice = ask_until_valid("Selecciona opción [1/2] (default 1): ", ["1", "2"], "1")

    if choice == "1":
        path = TESTS_PATH
        print("\nConjuntos disponibles: set1, set2, set_personal (edítalo).")
        name = input("Nombre del conjunto (default: set1): ").strip() or "set1"
        try:
            processes = load_named_set(path, name)
        except FileNotFoundError:
            print(f"Error: no se encontró el archivo {path}.")
            processes = []
        except Exception as e:
            print(f"Error cargando archivo: {e}")
            processes = []

        if not processes:
            print("No se encontraron procesos válidos. Volviendo a entrada manual.")
            processes = manual_create_processes()
        return processes

    elif choice == "2":
        return manual_create_processes()


def select_algorithms() -> List:
    """
    Selección de algoritmos con validación robusta.
    """
    print("\nAlgoritmos disponibles:")
    print("1) FCFS")
    print("2) SJF (no apropiativo)")
    print("3) Round Robin (configurable)")
    print("4) Prioridades (elige preemptivo/no preemptivo)")
    print("5) SRTF")
    print("6) Ejecutar TODOS")

    sel = ask_until_valid("Elige [1-6] (default 5): ", ["1", "2", "3", "4", "5", "6"], "5")

    if sel == "1":
        return [FCFS()]
    elif sel == "2":
        return [SJFNonPreemptive()]
    elif sel == "3":
        q = safe_int_input("Quantum (típicos: 2,4,6; default 4): ", 4, 1, 20)
        return [RoundRobin(quantum=q)]
    elif sel == "4":
        pre_flag = ask_until_valid("¿Preemptivo? [s/n] (default s): ", ["s", "n"], "s")
        preemptive = pre_flag == "s"
        return [PriorityScheduler(preemptive=preemptive)]
    elif sel == "5":
        return [SRTF()]
    elif sel == "6":
        q = safe_int_input("Quantum para Round Robin (default 4): ", 4, 1, 20)
        pre_flag = ask_until_valid("Prioridades preemptivo? [s/n] (default s): ", ["s", "n"], "s")
        preemptive = pre_flag == "s"
        return [FCFS(), SJFNonPreemptive(), RoundRobin(quantum=q), PriorityScheduler(preemptive=preemptive), SRTF()]


def main():
    """
    Función principal del programa con manejo robusto de errores.
    """
    print("Simulador de planificación de CPU (UCAB - Proyecto)")
    processes = select_process_source()
    if not processes:
        print("No hay procesos. Saliendo.")
        sys.exit(1)

    print("\nProcesos cargados/creados:")
    for p in processes:
        print(f"- {p.id}: llegada={p.arrival_time}, ráfaga={p.burst_time}, prioridad={p.priority}")

    schedulers = select_algorithms()
    try:
        run_simulation(processes, schedulers)
    except Exception as e:
        print(f"Error durante la simulación: {e}")
        print("Reintentando selección de algoritmos...")
        schedulers = select_algorithms()
        try:
            run_simulation(processes, schedulers)
        except Exception as e2:
            print(f"Error crítico: {e2}")
            sys.exit(1)


if __name__ == "__main__":
    main()
