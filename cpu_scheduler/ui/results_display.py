# cpu_scheduler/ui/results_display.py
from typing import Dict, List
from cpu_scheduler.core.timeline import Timeline

def print_gantt(timeline: Timeline):
    print("\nDiagrama de Gantt (textual):")
    print(timeline.to_text())

def print_process_metrics(rows: List[Dict[str, float]]):
    print("\nMétricas por proceso:")
    header = ["ID", "Llegada", "Ráfaga", "Prioridad", "Inicio", "Fin", "Turnaround", "Espera", "Respuesta"]
    print(" | ".join(header))
    for r in rows:
        print(f"{r['id']} | {r['arrival']} | {r['burst']} | {r['priority']} | {r['start']} | {r['completion']} | {r['turnaround']:.2f} | {r['waiting']:.2f} | {r['response']:.2f}")

def print_system_metrics(metrics: Dict[str, float]):
    print("\nMétricas del sistema:")
    print(f"- Promedio Turnaround: {metrics['avg_turnaround']:.2f}")
    print(f"- Promedio Espera:     {metrics['avg_waiting']:.2f}")
    print(f"- Promedio Respuesta:  {metrics['avg_response']:.2f}")
    print(f"- Utilización CPU:     {metrics['cpu_utilization']:.2f}%")

def print_comparison_table(results: Dict[str, Dict[str, float]]):
    print("\nComparación entre algoritmos (promedios):")
    header = ["Algoritmo", "Avg Turnaround", "Avg Espera", "Avg Respuesta", "CPU Util (%)"]
    print(" | ".join(header))
    for algo, m in results.items():
        print(f"{algo} | {m['avg_turnaround']:.2f} | {m['avg_waiting']:.2f} | {m['avg_response']:.2f} | {m['cpu_utilization']:.2f}")
