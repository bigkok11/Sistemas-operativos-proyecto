from typing import Dict, List
from models.process import Process
from core.timeline import Timeline

def compute_per_process_metrics(processes: List[Process]) -> List[Dict[str, float]]:
    """
    Calcula métricas individuales para cada proceso.
    - Recorre la lista de procesos finalizados y obtiene:
        • Turnaround: tiempo total desde llegada hasta finalización.
        • Waiting: tiempo en cola (turnaround - ráfaga).
        • Response: tiempo desde llegada hasta primera ejecución.
    - Devuelve una lista de diccionarios con métricas por proceso.
    """
    rows = []
    for p in processes:
        # Validación: el proceso debe tener tiempos de inicio y finalización definidos
        if p.completion_time is None or p.start_time is None:
            raise ValueError(f"Proceso {p.id} sin tiempos completos.")
        
        # Cálculo de métricas básicas
        turnaround = p.completion_time - p.arrival_time
        waiting = turnaround - p.burst_time
        response = p.start_time - p.arrival_time

        # Se agregan las métricas en un diccionario por proceso
        rows.append({
            "id": p.id,
            "arrival": p.arrival_time,
            "burst": p.burst_time,
            "priority": p.priority,
            "start": p.start_time,
            "completion": p.completion_time,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response,
        })
    return rows


def compute_system_metrics(processes: List[Process], timeline: Timeline) -> Dict[str, float]:
    """
    Calcula métricas globales del sistema a partir de los procesos y la línea de tiempo.
    - Promedio Turnaround: tiempo medio total de ejecución por proceso.
    - Promedio Espera: tiempo medio en cola.
    - Promedio Respuesta: tiempo medio hasta la primera ejecución.
    - Utilización CPU: porcentaje de tiempo ocupado respecto al makespan.
    """
    # Obtiene métricas individuales primero
    per = compute_per_process_metrics(processes)

    # Promedios de métricas por proceso
    avg_turnaround = sum(r["turnaround"] for r in per) / len(per)
    avg_waiting = sum(r["waiting"] for r in per) / len(per)
    avg_response = sum(r["response"] for r in per) / len(per)

    # Utilización de CPU: tiempo ocupado / tiempo total de simulación
    cpu_utilization = (timeline.busy_time / timeline.makespan * 100) if timeline.makespan > 0 else 0.0

    # Diccionario con métricas globales
    return {
        "avg_turnaround": avg_turnaround,
        "avg_waiting": avg_waiting,
        "avg_response": avg_response,
        "cpu_utilization": cpu_utilization,
    }
