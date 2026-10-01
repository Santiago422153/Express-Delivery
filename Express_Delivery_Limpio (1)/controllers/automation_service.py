import random
import urllib.request
from models.pedido import Pedido
from models.producto import CATALOGO_PRODUCTOS

NOMBRES_REALES = [
    "Jesús Pérez", "Mariana González", "Carlos Rodríguez", "Ana Sofía Martínez", 
    "José Gregorio Hernández", "Valeria Riera", "Alejandro Torrealba", "Daniela Blanco",
    "Luis Fernando Silva", "Carmen Teresa Colmenárez", "Gabriel E. Zambrano", "Oriana Lucena"
]

UBICACIONES_REALES = [
    "Carrera 19 con Calle 24, Centro, Barquisimeto",
    "Urbanización del Este, Av. Lara, Torre Metrópolis, Barquisimeto",
    "Este de Barquisimeto, Trinitarias, Res. El Parral",
    "Avenida Los Leones, Centro Comercial Sambil, Barquisimeto",
    "Barrio El Cercado, Vía Duaca, Barquisimeto",
    "Calle 8 con Carrera 3, Pata e' Palo, Barquisimeto",
    "Urb. Fundalara, Calle 4, Casa #12, Barquisimeto",
    "Av. Venezuela con Av. Bracamonte, Barquisimeto"
]

OPERADORAS = ["0414", "0424", "0412", "0416", "0426"]

DESCRIPCIONES_REALES = [
    "Por favor tocar el timbre dos veces al llegar.",
    "Dejar el paquete con el vigilante de la torre.",
    "Llamar al cliente 10 minutos antes de entregar.",
    "Pago exacto en divisas al momento de recibir.",
    "Cuidado con la caja, productos frágiles de tecnología.",
    "Entregar directamente en la oficina principal."
]

class AutomationService:
    @staticmethod
    def generar_pedido_aleatorio():
        cliente = random.choice(NOMBRES_REALES)
        destino = random.choice(UBICACIONES_REALES)
        
        operadora = random.choice(OPERADORAS)
        numero = random.randint(1000000, 9999999)
        telefono = f"{operadora}-{numero}"
        
        descripcion = random.choice(DESCRIPCIONES_REALES)
        distancia = round(random.uniform(2.5, 25.0), 1)
        id_ped = f"PED-{random.randint(10000, 99999)}"

        # Seleccionar entre 1 y 3 productos aleatorios del catálogo con cantidades aleatorias
        num_productos = random.randint(1, 3)
        prods_seleccionados = random.sample(CATALOGO_PRODUCTOS, num_productos)
        
        items = []
        nombres_resumen = []
        peso_total = 0.0
        precio_total = 0.0

        for prod in prods_seleccionados:
            cantidad = random.randint(1, 3)
            items.append({
                "nombre": prod.nombre,
                "cantidad": cantidad,
                "precio_unit": prod.precio_usd,
                "peso_unit": prod.peso_kg
            })
            nombres_resumen.append(f"{cantidad}x {prod.nombre}")
            peso_total += prod.peso_kg * cantidad
            precio_total += prod.precio_usd * cantidad

        resumen_producto = ", ".join(nombres_resumen)

        return Pedido(
            id_pedido=id_ped,
            cliente=cliente,
            producto=resumen_producto,
            destino=destino,
            peso_kg=peso_total,
            precio_usd=precio_total,
            distancia_km=distancia,
            imagen_url=CATALOGO_PRODUCTOS[0].imagen_url,
            telefono=telefono,
            descripcion=descripcion,
            items=items
        )

    @staticmethod
    def obtener_pixmap_desde_url(url):
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
