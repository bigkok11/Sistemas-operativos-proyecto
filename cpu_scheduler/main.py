import sys
import os
from colorama import *
from typing import List
from models.process import Process
from core.algorithms.fcfs import FCFS
from core.algorithms.sjf import SJFNonPreemptive
from core.algorithms.round_robin import RoundRobin
from core.algorithms.priority import PriorityScheduler
from utils.file_handler import load_named_set
from utils.process_generator import manual_create_processes
from ui.interface import run_simulation
from core.algorithms.srtf import SRTF

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
        print( Fore.RED + f"Entrada inválida. Opciones válidas: {', '.join(valid_options)}" + Style.RESET_ALL)


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
                print(Fore.RED + f"El número debe estar entre {min_val} y {max_val}." + Style.RESET_ALL)
                continue
            return num
        except ValueError:
            print(Fore.RED + "Entrada inválida. Debes ingresar un número entero." + Style.RESET_ALL)


def select_process_source() -> List[Process]:
    """
    Selección de fuente de procesos con validación robusta.
    """
    print(Fore.MAGENTA + "Fuente de procesos:" + Style.RESET_ALL)
    print("1) Cargar desde archivo JSON (tests/cases.json)")
    print("2) Crear manualmente")

    choice = ask_until_valid("Selecciona opción [1/2] (default 1): ", ["1", "2"], "1")

    if choice == "1":
        path = TESTS_PATH
        print(Fore.MAGENTA + "\nConjuntos disponibles: set1, set2, set_personal (edítalo)." + Style.RESET_ALL)
        name = input("Nombre del conjunto (default: set1): ").strip() or "set1"
        try:
            processes = load_named_set(path, name)
        except FileNotFoundError:
            print(Fore.RED + f"Error: no se encontró el archivo {path}." + Style.RESET_ALL)
            processes = []
        except Exception as e:
            print(Fore.RED + f"Error cargando archivo: {e}" + Style.RESET_ALL)
            processes = []

        if not processes:
            print(Fore.RED + "No se encontraron procesos válidos. Volviendo a entrada manual." + Style.RESET_ALL)
            processes = manual_create_processes()
        return processes

    elif choice == "2":
        return manual_create_processes()


def select_algorithms() -> List:
    """
    Selección de algoritmos con validación robusta.
    """
    print(Fore.MAGENTA + "\nAlgoritmos disponibles:" + Style.RESET_ALL)
    print("1) FCFS")
    print("2) SJF (no apropiativo)")
    print("3) Round Robin (configurable)")
    print("4) Prioridades (elige preemptivo/no preemptivo)")
    print("5) SRTF")
    print("6) Ejecutar TODOS")

    sel = ask_until_valid(Fore.BLUE + "Elige [1-6] (default 5): "+ Style.RESET_ALL, ["1", "2", "3", "4", "5", "6"], "5")

    if sel == "1":
        return [FCFS()]
    elif sel == "2":
        return [SJFNonPreemptive()]
    elif sel == "3":
        q = safe_int_input(Fore.BLUE + "Quantum (típicos: 2,4,6; default 4): " + Style.RESET_ALL, 4, 1, 20)
        return [RoundRobin(quantum=q)]
    elif sel == "4":
        pre_flag = ask_until_valid(Fore.BLUE + "¿Preemptivo? [s/n] (default s): " + Style.RESET_ALL, ["s", "n"], "s" )
        preemptive = pre_flag == "s"
        return [PriorityScheduler(preemptive=preemptive)]
    elif sel == "5":
        return [SRTF()]
    elif sel == "6":
        q = safe_int_input(Fore.BLUE + "Quantum para Round Robin (default 4): " + Style.RESET_ALL, 4, 1, 20 )
        pre_flag = ask_until_valid(Fore.BLUE + "Prioridades preemptivo? [s/n] (default s): " + Style.RESET_ALL, ["s", "n"], "s")
        preemptive = pre_flag == "s"
        return [FCFS(), SJFNonPreemptive(), RoundRobin(quantum=q), PriorityScheduler(preemptive=preemptive), SRTF()]


def main():
    """
    Función principal del programa con manejo robusto de errores.
    """
    print(Fore.GREEN+ "Simulador de planificación de CPU (UCAB - Proyecto)" + Style.RESET_ALL)
    processes = select_process_source()
    if not processes:
        print(Fore.RED + "No hay procesos. Saliendo." + Style.RESET_ALL)
        sys.exit(1)

    print( Fore.GREEN + "\nProcesos cargados/creados:" + Style.RESET_ALL)
    for p in processes:
        print(f"- {p.id}: llegada={p.arrival_time}, ráfaga={p.burst_time}, prioridad={p.priority}")

    schedulers = select_algorithms()
    try:
        run_simulation(processes, schedulers)
    except Exception as e:
        print(Fore.RED + f"Error durante la simulación: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Reintentando selección de algoritmos..." + Style.RESET_ALL)
        schedulers = select_algorithms()
        try:
            run_simulation(processes, schedulers)
        except Exception as e2:
            print(Fore.RED + f"Error crítico: {e2}" + Style.RESET_ALL)
            sys.exit(1)


if __name__ == "__main__":
    main()
