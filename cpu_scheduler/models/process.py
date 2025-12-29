# cpu_scheduler/models/process.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Process:
    """
    Representa un proceso en el sistema.
    """
    id: str
    arrival_time: int
    burst_time: int
    priority: int = 0  # Menor valor = mayor prioridad por defecto
    state: str = field(default="Nuevo", compare=False)

    # Campos de métricas (se calculan durante la simulación)
    start_time: Optional[int] = field(default=None, compare=False)  # Primera vez que ejecuta
    completion_time: Optional[int] = field(default=None, compare=False)
    remaining_time: Optional[int] = field(default=None, compare=False)

    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

    def reset_runtime(self):
        self.state = "Nuevo"
        self.start_time = None
        self.completion_time = None
        self.remaining_time = self.burst_time
