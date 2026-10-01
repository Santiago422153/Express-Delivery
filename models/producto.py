class Producto:
    def __init__(self, nombre, precio_usd, peso_kg, imagen_url):
        self.nombre = nombre
        self.precio_usd = float(precio_usd)
        self.peso_kg = float(peso_kg)
        self.imagen_url = imagen_url

# Catálogo predeterminado ampliado
CATALOGO_PRODUCTOS = [
    # Tecnología y Computación
    Producto("Laptop Gaming", 1200.0, 2.5, "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcQVuqWjv3gLBH6D9CeuWsA06W91bsRu5YXqom2xZpZiGPfVWoottSgNk3-KLTUdo6cLlwaT_yvEkIBJyUw"),
    Producto("Smartphone 5G", 800.0, 0.4, "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTmJMvlG0B1HXBtM0WeqHBv8QEBPS7AtovieB_ZSINN4es6VVYHvrhZ1oZlz4VZBkBzjzqNJloCG7R4rBc"),
    Producto("Auriculares Bluetooth", 150.0, 0.3, "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQrAz2P8jdX9vFxdd4YZD-Bmx7kzefqN1zJc6CfbC4b7orDr_9U1MEwPpKWeDRmzu_gGPLdfYIKjuG73Uk"),
    Producto("Smartwatch Deportivo", 220.0, 0.2, "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRTpQBm0Gl8EwO1HLWvFq_M4uppDs1qhUj8Ro6pAE3rBZLBbrWsbFGIvlP3CJFM1_WA-U8ya7h7FB4i9oI"),
    Producto("Monitor Gamer 4K", 450.0, 6.5, "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSeKy5LRMvLKsVSn3lranazPUyBsUZr6U0LoMtgvFlYPm9res4nOI2lUgQw94yMx9th8MV6zm6DXXkJWiw"),
    Producto("Teclado Mecánico RGB", 110.0, 1.1, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQv5LW-_YE5fdW0AC7yoxGhou-tevpKnPjv92Ps7ey5WmuvNbxwYCynDle-aS_41HCOI7G2IkjwKpey_bs"),
    
    # Nuevos productos añadidos
    Producto("Tablet Pro 11'", 650.0, 0.8, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z..."),
    Producto("Consola de Videojuegos", 500.0, 3.2, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z..."),
    Producto("Cámara Mirrorless", 950.0, 1.2, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z..."),
    Producto("Micrófono Condensador USB", 90.0, 0.6, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z..."),
    Producto("Silla Gamer Ergonómica", 300.0, 18.0, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z..."),
    Producto("Disco Duro Externo 2TB", 85.0, 0.2, "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRz-8Z...")
]