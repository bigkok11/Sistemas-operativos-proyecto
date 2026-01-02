from typing import List, Dict
from models.process import Process
from core.scheduler import IScheduler, deep_reset, pick_best_algorithm
from metrics.metrics import compute_per_process_metrics, compute_system_metrics
from ui.results_display import (
    print_gantt,
    print_process_metrics,
    print_system_metrics,
    print_comparison_table,
)

def run_simulation(processes: List[Process], schedulers: List[IScheduler]):
    """
    Función principal para ejecutar la simulación de planificación de CPU.
    - Recibe una lista de procesos y una lista de algoritmos de planificación (schedulers).
    - Ejecuta cada algoritmo sobre la misma carga de trabajo.
    - Muestra resultados individuales (Gantt, métricas por proceso, métricas del sistema).
    - Compara los algoritmos y selecciona automáticamente el mejor según el tiempo de espera promedio.
    """
    # Diccionario para almacenar métricas comparativas de cada algoritmo
    comparison: Dict[str, Dict[str, float]] = {}

    # Itera sobre cada algoritmo seleccionado
    for s in schedulers:
        print(f"\n=== Ejecutando {s.name} ===")
        # Se reinicia el estado de los procesos antes de ejecutar cada algoritmo
        timeline, finalized = s.run(deep_reset(processes))

        # Muestra el diagrama de Gantt (orden de ejecución de procesos en el tiempo)
        print_gantt(timeline)

        # Calcula métricas por proceso (tiempo de espera, tiempo de retorno, etc.)
        per = compute_per_process_metrics(finalized)
        print_process_metrics(per)

        # Calcula métricas globales del sistema (promedios, utilización, etc.)
        metrics = compute_system_metrics(finalized, timeline)
        print_system_metrics(metrics)

        # Almacena las métricas en el diccionario de comparación
        comparison[s.name] = metrics

    # Muestra tabla comparativa de resultados entre algoritmos
    print_comparison_table(comparison)

    # Selecciona automáticamente el mejor algoritmo según menor tiempo de espera promedio
    best = pick_best_algorithm(comparison)
    print(f"\nConclusión automática: mejor algoritmo para este caso (menor espera promedio) => {best}")
