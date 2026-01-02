import json
from typing import List
from models.process import Process

def load_processes_from_json(path: str) -> List[Process]:
    """
    Función principal para cargar procesos desde un archivo JSON.
    - El archivo debe tener el formato:
      {
        "sets": {
          "set1": [
            {"id":"P1","arrival":0,"burst":8,"priority":3},
            ...
          ]
        }
      }
    - Devuelve una lista de objetos `Process` correspondientes al primer conjunto encontrado.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Carga el contenido del archivo JSON en un diccionario
    sets = data.get("sets", {})  # Obtiene el diccionario de conjuntos de procesos
    # Por defecto carga el primer conjunto si no se especifica uno
    first_key = next(iter(sets), None)
    if not first_key:
        return []  # Si no hay conjuntos, devuelve lista vacía
    return [
        # Se crea un objeto Process por cada entrada en el conjunto
        Process(
            id=item["id"],  # Identificador del proceso
            arrival_time=int(item["arrival"]),  # Tiempo de llegada
            burst_time=int(item["burst"]),  # Tiempo de ráfaga (ejecución)
            priority=int(item.get("priority", 0))  # Prioridad (por defecto 0 si no está en JSON)
        )
        for item in sets[first_key]
    ]


def load_named_set(path: str, name: str) -> List[Process]:
    """
    Función para cargar un conjunto específico de procesos desde un archivo JSON.
    - Recibe la ruta del archivo y el nombre del conjunto.
    - Devuelve una lista de objetos `Process` correspondientes al conjunto indicado.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Carga el archivo JSON
    arr = data.get("sets", {}).get(name, [])  # Obtiene el conjunto por nombre
    return [
        # Se construye la lista de procesos a partir del conjunto solicitado
        Process(
            id=item["id"],  # Identificador único del proceso
            arrival_time=int(item["arrival"]),  # Tiempo de llegada
            burst_time=int(item["burst"]),  # Duración de ejecución
            priority=int(item.get("priority", 0))  # Nivel de prioridad (default 0)
        )
        for item in arr
    ]
