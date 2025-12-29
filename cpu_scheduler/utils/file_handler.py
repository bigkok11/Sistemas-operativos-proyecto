# cpu_scheduler/utils/file_handler.py
import json
from typing import List
from cpu_scheduler.models.process import Process

def load_processes_from_json(path: str) -> List[Process]:
    """
    Espera JSON con formato:
    {
      "sets": {
        "set1": [
          {"id":"P1","arrival":0,"burst":8,"priority":3},
          ...
        ]
      }
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sets = data.get("sets", {})
    # Por defecto carga el primero si no especifican
    first_key = next(iter(sets), None)
    if not first_key:
        return []
    return [
        Process(
            id=item["id"],
            arrival_time=int(item["arrival"]),
            burst_time=int(item["burst"]),
            priority=int(item.get("priority", 0))
        )
        for item in sets[first_key]
    ]

def load_named_set(path: str, name: str) -> List[Process]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    arr = data.get("sets", {}).get(name, [])
    return [
        Process(
            id=item["id"],
            arrival_time=int(item["arrival"]),
            burst_time=int(item["burst"]),
            priority=int(item.get("priority", 0))
        )
        for item in arr
    ]
