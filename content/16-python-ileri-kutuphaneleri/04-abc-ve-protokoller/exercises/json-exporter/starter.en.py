import json
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str:
        ...


class JsonExporter(Exporter):
    def dump(self, rows):
        return json.dumps(rows)

rows = [{"name": "pen", "price": 1.5}]
print(JsonExporter().export(rows))
