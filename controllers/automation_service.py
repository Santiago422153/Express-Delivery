import random
import urllib.request
from models.pedido import Pedido
from models.producto import CATALOGO_PRODUCTOS

NOMBRES_CLIENTES = ["Carlos Mendoza", "María Rodríguez", "Alejandro Silva", "Elena Torres", "Gabriel Ruiz", "Sofia Vargas"]
CIUDADES_VEN = ["Caracas", "Valencia", "Maracaibo", "Barquisimeto", "Puerto Ordaz", "Mérida", "San Cristóbal"]

class AutomationService:
    @staticmethod
    def generar_pedido_aleatorio():
        prod = random.choice(CATALOGO_PRODUCTOS)
        cliente = random.choice(NOMBRES_CLIENTES)
        destino = random.choice(CIUDADES_VEN)
        distancia = random.randint(20, 850)
        id_ped = f"AUT-{random.randint(10000, 99999)}"

        return Pedido(
            id_pedido=id_ped,
            cliente=cliente,
            producto=prod.nombre,
            destino=destino,
            peso_kg=prod.peso_kg,
            precio_usd=prod.precio_usd,
            distancia_km=distancia,
            imagen_url=prod.imagen_url
        )

    @staticmethod
    def obtener_pixmap_desde_url(url):
        """Descarga la imagen para renderizarla en PyQt5 usando urllib estándar."""
        from PyQt5.QtGui import QPixmap
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                return pixmap
        except Exception:
            return None