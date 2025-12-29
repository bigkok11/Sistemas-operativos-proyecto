# cpu_scheduler/ui/interface.py
from typing import List, Dict
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.scheduler import IScheduler, deep_reset, pick_best_algorithm
from cpu_scheduler.metrics.metrics import compute_per_process_metrics, compute_system_metrics
from cpu_scheduler.ui.results_display import (
    print_gantt,
    print_process_metrics,
    print_system_metrics,
    print_comparison_table,
)

def run_simulation(processes: List[Process], schedulers: List[IScheduler]):
    """
    Ejecuta todos los algoritmos seleccionados sobre la misma carga de trabajo y muestra resultados.
    """
    comparison: Dict[str, Dict[str, float]] = {}
    for s in schedulers:
        print(f"\n=== Ejecutando {s.name} ===")
        timeline, finalized = s.run(deep_reset(processes))
        print_gantt(timeline)
        per = compute_per_process_metrics(finalized)
        print_process_metrics(per)
        metrics = compute_system_metrics(finalized, timeline)
        print_system_metrics(metrics)
        comparison[s.name] = metrics

    print_comparison_table(comparison)
    best = pick_best_algorithm(comparison)
    print(f"\nConclusión automática: mejor algoritmo para este caso (menor espera promedio) => {best}")
