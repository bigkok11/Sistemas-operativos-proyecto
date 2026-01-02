from typing import Dict, List
from core.timeline import Timeline

def print_gantt(timeline: Timeline):
    """
    Muestra el diagrama de Gantt en formato textual.
    - Recibe un objeto `Timeline` que contiene la secuencia de ejecución de procesos.
    - Utiliza el método `to_text()` para representar gráficamente la planificación.
    """
    print("\nDiagrama de Gantt (textual):")
    print(timeline.to_text())


def print_process_metrics(rows: List[Dict[str, float]]):
    """
    Imprime métricas individuales por proceso en formato tabular.
    - Cada fila del parámetro `rows` corresponde a un proceso con sus métricas calculadas:
        • ID: identificador del proceso
        • Llegada: tiempo de llegada
        • Ráfaga: duración de ejecución
        • Prioridad: nivel de prioridad
        • Inicio: instante en que comienza a ejecutarse
        • Fin: instante en que termina
        • Turnaround: tiempo total desde llegada hasta finalización
        • Espera: tiempo en cola antes de ejecución
        • Respuesta: tiempo hasta la primera ejecución
    """
    print("\nMétricas por proceso:")
    header = ["ID", "Llegada", "Ráfaga", "Prioridad", "Inicio", "Fin", "Turnaround", "Espera", "Respuesta"]
    print(" | ".join(header))
    for r in rows:
        # Se imprimen las métricas con formato numérico (dos decimales en métricas de tiempo)
        print(f"{r['id']} | {r['arrival']} | {r['burst']} | {r['priority']} | {r['start']} | {r['completion']} | {r['turnaround']:.2f} | {r['waiting']:.2f} | {r['response']:.2f}")


def print_system_metrics(metrics: Dict[str, float]):
    """
    Imprime métricas globales del sistema.
    - Recibe un diccionario con valores promedio y de utilización:
        • avg_turnaround: tiempo promedio de turnaround
        • avg_waiting: tiempo promedio de espera
        • avg_response: tiempo promedio de respuesta
        • cpu_utilization: porcentaje de utilización de CPU
    """
    print("\nMétricas del sistema:")
    print(f"- Promedio Turnaround: {metrics['avg_turnaround']:.2f}")
    print(f"- Promedio Espera:     {metrics['avg_waiting']:.2f}")
    print(f"- Promedio Respuesta:  {metrics['avg_response']:.2f}")
    print(f"- Utilización CPU:     {metrics['cpu_utilization']:.2f}%")


def print_comparison_table(results: Dict[str, Dict[str, float]]):
    """
    Imprime una tabla comparativa entre algoritmos de planificación.
    - Recibe un diccionario donde cada clave es el nombre de un algoritmo
      y el valor es otro diccionario con sus métricas promedio.
    - Muestra los resultados en formato tabular para facilitar la comparación.
    """
    print("\nComparación entre algoritmos (promedios):")
    header = ["Algoritmo", "Avg Turnaround", "Avg Espera", "Avg Respuesta", "CPU Util (%)"]
    print(" | ".join(header))
    for algo, m in results.items():
        # Se imprimen métricas promedio con dos decimales
        print(f"{algo} | {m['avg_turnaround']:.2f} | {m['avg_waiting']:.2f} | {m['avg_response']:.2f} | {m['cpu_utilization']:.2f}")
