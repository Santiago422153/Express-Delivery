import math
import time

class Pedido:
    def __init__(self, id_pedido, cliente, producto, destino, peso_kg, precio_usd, distancia_km, imagen_url=""):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.producto = producto
        self.destino = destino
        self.peso_kg = float(peso_kg)
        self.precio_usd = float(precio_usd)
        self.distancia_km = float(distancia_km)
        self.imagen_url = imagen_url
        self.timestamp = time.time()
        self.prioridad = self.calcular_prioridad()

    def calcular_prioridad(self):
        score_peso = math.log1p(self.peso_kg) * 40
        score_precio = math.log1p(self.precio_usd) * 40
        score_distancia = math.sqrt(self.distancia_km) * 20
        return round(score_peso + score_precio + score_distancia, 2)

    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "cliente": self.cliente,
            "producto": self.producto,
            "destino": self.destino,
            "peso_kg": self.peso_kg,
            "precio_usd": self.precio_usd,
            "distancia_km": self.distancia_km,
            "imagen_url": self.imagen_url,
            "prioridad": self.prioridad,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        pedido = cls(
            id_pedido=data["id_pedido"],
            cliente=data["cliente"],
            producto=data.get("producto", "Producto General"),
            destino=data["destino"],
            peso_kg=data["peso_kg"],
            precio_usd=data["precio_usd"],
            distancia_km=data["distancia_km"],
            imagen_url=data.get("imagen_url", "")
        )
        pedido.prioridad = data.get("prioridad", pedido.calcular_prioridad())
        pedido.timestamp = data.get("timestamp", time.time())
        return pedido