from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Process:
    """
    Clase que representa un proceso en el sistema de planificación de CPU.
    - Se utiliza en los algoritmos de scheduling para simular la ejecución de procesos.
    - Incluye atributos básicos (id, llegada, ráfaga, prioridad) y métricas calculadas durante la simulación.
    - El decorador @dataclass con `order=True` permite comparar procesos por sus atributos
      (útil en algoritmos como SJF o SRTF).
    """
    id: str                          # Identificador único del proceso (ejemplo: "P1")
    arrival_time: int                # Tiempo en que el proceso llega al sistema
    burst_time: int                  # Tiempo total de ejecución requerido (ráfaga)
    priority: int = 0                # Nivel de prioridad (menor valor = mayor prioridad)
    state: str = field(default="Nuevo", compare=False)  
    # Estado del proceso (ejemplo: "Nuevo", "Ejecutando", "Finalizado").
    # No se usa para comparación entre procesos.

    # Campos de métricas (se calculan durante la simulación)
    start_time: Optional[int] = field(default=None, compare=False)   
    # Momento en que el proceso comienza a ejecutarse por primera vez
    completion_time: Optional[int] = field(default=None, compare=False)  
    # Momento en que el proceso finaliza su ejecución
    remaining_time: Optional[int] = field(default=None, compare=False)  
    # Tiempo restante de ejecución (usado en algoritmos apropiativos como SRTF)

    def __post_init__(self):
        """
        Método especial de dataclass que se ejecuta después de la inicialización.
        - Si `remaining_time` no se especifica, se inicializa con `burst_time`.
        - Esto asegura que algoritmos como SRTF puedan calcular correctamente el tiempo restante.
        """
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

    def reset_runtime(self):
        """
        Reinicia el estado del proceso para permitir nuevas simulaciones.
        - Restablece el estado a "Nuevo".
        - Borra tiempos de inicio y finalización.
        - Reinicia el tiempo restante con el valor original de ráfaga.
        """
        self.state = "Nuevo"
        self.start_time = None
        self.completion_time = None
        self.remaining_time = self.burst_time
