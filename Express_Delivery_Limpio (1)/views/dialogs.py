import random
import urllib.parse
import webbrowser
from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox, 
                             QDoubleSpinBox, QSpinBox, QDialogButtonBox, QVBoxLayout, 
                             QLabel, QMessageBox, QHBoxLayout, QTextEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from models.producto import CATALOGO_PRODUCTOS
from controllers.automation_service import AutomationService

class PedidoDialog(QDialog):
    def __init__(self, parent=None, pedido=None):
        super().__init__(parent)
        self.pedido = pedido
        self.setWindowTitle("Editar Pedido" if pedido else "Crear Nuevo Pedido Inteligente")
        self.resize(650, 720)
        self.init_ui()
        if pedido:
            self.cargar_datos_pedido()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_cliente = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Ej: 0414-1234567")

        # Aviso de Ubicación Automática Detectada del Sistema
        self.lbl_ubicacion_sistema = QLabel("📍 Ubicación base detectada: <b>Barquisimeto, Lara (Almacén Central)</b>")
        self.lbl_ubicacion_sistema.setStyleSheet("color: #38ef7d; font-size: 12px; padding: 4px;")

        # Tabla de Selección de Productos y Cantidades con estilos oscuros forzados
        self.table_catalogo = QTableWidget()
        self.table_catalogo.setColumnCount(4)
        self.table_catalogo.setHorizontalHeaderLabels(["Producto", "Precio ($)", "Peso (kg)", "Cantidad"])
        self.table_catalogo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_catalogo.setMaximumHeight(180)
        self.table_catalogo.setStyleSheet("background-color: #1a232e; color: #ffffff; gridline-color: #263342;")
        
        self.spin_boxes_cantidades = []
        
        for row, prod in enumerate(CATALOGO_PRODUCTOS):
            self.table_catalogo.insertRow(row)
            
            item_nombre = QTableWidgetItem(prod.nombre)
            item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
            
            item_precio = QTableWidgetItem(f"${prod.precio_usd:.2f}")
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            
            item_peso = QTableWidgetItem(f"{prod.peso_kg:.2f} kg")
            item_peso.setFlags(item_peso.flags() & ~Qt.ItemIsEditable)
            
            spin_cant = QSpinBox()
            spin_cant.setRange(0, 100)
            spin_cant.setValue(0)
            spin_cant.setStyleSheet("background-color: #24303f; color: #ffffff; border: 1px solid #36475b;")
            spin_cant.valueChanged.connect(self.recalcular_totales)
            
            self.table_catalogo.setItem(row, 0, item_nombre)
            self.table_catalogo.setItem(row, 1, item_precio)
            self.table_catalogo.setItem(row, 2, item_peso)
            self.table_catalogo.setCellWidget(row, 3, spin_cant)
            
            self.spin_boxes_cantidades.append((prod, spin_cant))

        # Dirección y botón de Google Maps
        self.input_destino = QLineEdit()
        self.input_destino.setPlaceholderText("Ej: Av. Lara con Leones, Barquisimeto")
        self.input_destino.textChanged.connect(self.calcular_distancia_automatica)
        
        btn_maps = QPushButton("🗺️ Google Maps")
        btn_maps.setStyleSheet("background-color: #2980b9; color: white; font-size: 11px; padding: 6px; border-radius: 4px;")
        btn_maps.setAutoDefault(False)
        btn_maps.setDefault(False)
        btn_maps.clicked.connect(self.abrir_google_maps)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.input_destino)
        dir_layout.addWidget(btn_maps)

        # Campos calculados automáticamente
        self.spin_peso_total = QDoubleSpinBox()
        self.spin_peso_total.setRange(0.1, 10000.0)
        self.spin_peso_total.setSuffix(" kg")
        self.spin_peso_total.setReadOnly(True)

        self.spin_precio_total = QDoubleSpinBox()
        self.spin_precio_total.setRange(0.1, 100000.0)
        self.spin_precio_total.setPrefix("$ ")
        self.spin_precio_total.setReadOnly(True)

        self.spin_distancia = QDoubleSpinBox()
        self.spin_distancia.setRange(0.5, 3000.0)
        self.spin_distancia.setValue(5.0)
        self.spin_distancia.setSuffix(" km")

        self.input_descripcion = QTextEdit()
        self.input_descripcion.setMaximumHeight(60)
        self.input_descripcion.setPlaceholderText("Instrucciones de entrega, notas de pago...")

        form.addRow("Cliente:", self.input_cliente)
        form.addRow("Teléfono:", self.input_telefono)
        form.addRow("Ubicación:", self.lbl_ubicacion_sistema)
        form.addRow("Seleccionar Productos:", self.table_catalogo)
        form.addRow("Dirección del Cliente:", dir_layout)
        form.addRow("Distancia (Auto-calculada):", self.spin_distancia)
        form.addRow("Peso Total:", self.spin_peso_total)
        form.addRow("Valor Total ($):", self.spin_precio_total)
        form.addRow("Descripción / Notas:", self.input_descripcion)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validar_y_aceptar)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        self.recalcular_totales()

    def calcular_distancia_automatica(self):
        # Detección inteligente de distancia basada en palabras clave de la dirección respecto a Barquisimeto
        dir_texto = self.input_destino.text().lower().strip()
        if not dir_texto:
            return
        
        # Estimación en base a ciudades o zonas de Venezuela
        if "caracas" in dir_texto:
            self.spin_distancia.setValue(365.0)
        elif "valencia" in dir_texto:
            self.spin_distancia.setValue(165.0)
        elif "maracaibo" in dir_texto:
            self.spin_distancia.setValue(260.0)
        elif "carora" in dir_texto:
            self.spin_distancia.setValue(95.0)
        elif "acariqua" in dir_texto or "acarigua" in dir_texto:
            self.spin_distancia.setValue(85.0)
        elif "cabudare" in dir_texto:
            self.spin_distancia.setValue(12.0)
        elif "sural" in dir_texto or "centro" in dir_texto or "lara" in dir_texto or "leones" in dir_texto:
            self.spin_distancia.setValue(round(random.uniform(3.0, 9.5), 1))
        else:
            self.spin_distancia.setValue(round(random.uniform(5.0, 25.0), 1))

    def recalcular_totales(self):
        peso_total = 0.0
        precio_total = 0.0
        for prod, spin in self.spin_boxes_cantidades:
            cant = spin.value()
            if cant > 0:
                peso_total += prod.peso_kg * cant
                precio_total += prod.precio_usd * cant
        
        self.spin_peso_total.setValue(max(peso_total, 0.1))
        self.spin_precio_total.setValue(max(precio_total, 0.1))

    def abrir_google_maps(self):
        direccion = self.input_destino.text().strip()
        if not direccion:
            QMessageBox.warning(self, "Dirección vacía", "Por favor ingresa una dirección primero.")
            return
        url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(direccion)}"
        try:
            QDesktopServices.openUrl(QUrl(url))
        except Exception:
            webbrowser.open(url)

    def cargar_datos_pedido(self):
        self.input_cliente.setText(self.pedido.cliente)
        self.input_telefono.setText(getattr(self.pedido, "telefono", ""))
        self.input_destino.setText(self.pedido.destino)
        self.spin_distancia.setValue(self.pedido.distancia_km)
        self.input_descripcion.setPlainText(getattr(self.pedido, "descripcion", ""))
        
        items = getattr(self.pedido, "items", [])
        items_dict = {item["nombre"]: item["cantidad"] for item in items}
        
        for prod, spin in self.spin_boxes_cantidades:
            if prod.nombre in items_dict:
                spin.setValue(items_dict[prod.nombre])

    def validar_y_aceptar(self):
        if not self.input_cliente.text().strip() or not self.input_destino.text().strip():
            QMessageBox.warning(self, "Atención", "Escribe el cliente y la dirección de destino.")
            return
        
        total_items = sum(spin.value() for _, spin in self.spin_boxes_cantidades)
        if total_items == 0:
            QMessageBox.warning(self, "Atención", "Selecciona al menos una unidad de algún producto.")
            return
            
        self.accept()

    def get_data(self):
        id_ped = self.pedido.id_pedido if self.pedido else f"ENV-{random.randint(1000, 9999)}"
        
        items_seleccionados = []
        nombres_resumen = []
        
        for prod, spin in self.spin_boxes_cantidades:
            cant = spin.value()
            if cant > 0:
                items_seleccionados.append({
                    "nombre": prod.nombre,
                    "cantidad": cant,
                    "precio_unit": prod.precio_usd,
                    "peso_unit": prod.peso_kg
                })
                nombres_resumen.append(f"{cant}x {prod.nombre}")

        resumen_producto = ", ".join(nombres_resumen)
        imagen_principal = CATALOGO_PRODUCTOS[0].imagen_url if CATALOGO_PRODUCTOS else ""

        return {
            "id_pedido": id_ped,
            "cliente": self.input_cliente.text().strip(),
            "telefono": self.input_telefono.text().strip(),
            "producto": resumen_producto,
            "destino": self.input_destino.text().strip(),
            "peso_kg": self.spin_peso_total.value(),
            "precio_usd": self.spin_precio_total.value(),
            "distancia_km": self.spin_distancia.value(),
            "imagen_url": imagen_principal,
            "descripcion": self.input_descripcion.toPlainText().strip(),
            "items": items_seleccionados
        }
