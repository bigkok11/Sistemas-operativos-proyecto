# cpu_scheduler/metrics/metrics.py
from typing import Dict, List
from cpu_scheduler.models.process import Process
from cpu_scheduler.core.timeline import Timeline

def compute_per_process_metrics(processes: List[Process]) -> List[Dict[str, float]]:
    rows = []
    for p in processes:
        if p.completion_time is None or p.start_time is None:
            raise ValueError(f"Proceso {p.id} sin tiempos completos.")
        turnaround = p.completion_time - p.arrival_time
        waiting = turnaround - p.burst_time
        response = p.start_time - p.arrival_time
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
    per = compute_per_process_metrics(processes)
    avg_turnaround = sum(r["turnaround"] for r in per) / len(per)
    avg_waiting = sum(r["waiting"] for r in per) / len(per)
    avg_response = sum(r["response"] for r in per) / len(per)
    cpu_utilization = (timeline.busy_time / timeline.makespan * 100) if timeline.makespan > 0 else 0.0
    return {
        "avg_turnaround": avg_turnaround,
        "avg_waiting": avg_waiting,
        "avg_response": avg_response,
        "cpu_utilization": cpu_utilization,
    }
