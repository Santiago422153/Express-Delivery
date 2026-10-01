import json
import os
from models.pedido import Pedido

class DataManager:
    def __init__(self, filepath="data/pedidos.json"):
        self.filepath = filepath
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self.guardar_pedidos([])

    def cargar_pedidos(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Pedido.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar_pedidos(self, lista_pedidos):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in lista_pedidos], f, indent=4, ensure_ascii=False)