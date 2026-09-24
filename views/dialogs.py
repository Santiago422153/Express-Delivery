import random
from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox, 
                             QDoubleSpinBox, QDialogButtonBox, QVBoxLayout, 
                             QLabel, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from models.producto import CATALOGO_PRODUCTOS
from controllers.automation_service import AutomationService

class PedidoDialog(QDialog):
    def __init__(self, parent=None, pedido=None):
        super().__init__(parent)
        self.pedido = pedido
        self.setWindowTitle("Editar Pedido" if pedido else "Crear Nuevo Pedido")
        self.resize(420, 380)
        self.init_ui()
        if pedido:
            self.cargar_datos_pedido()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_cliente = QLineEdit()
        self.combo_producto = QComboBox()
        
        for prod in CATALOGO_PRODUCTOS:
            self.combo_producto.addItem(f"{prod.nombre} (${prod.precio_usd:.2f})", prod)

        self.combo_producto.currentIndexChanged.connect(self.al_cambiar_producto)

        self.lbl_preview_img = QLabel("Cargando imagen...")
        self.lbl_preview_img.setFixedSize(120, 120)
        self.lbl_preview_img.setStyleSheet("border: 1px solid #3d4d5c; border-radius: 6px;")
        self.lbl_preview_img.setAlignment(Qt.AlignCenter)

        self.input_destino = QLineEdit()
        
        self.spin_peso = QDoubleSpinBox()
        self.spin_peso.setRange(0.1, 1000.0)
        self.spin_peso.setSuffix(" kg")

        self.spin_precio = QDoubleSpinBox()
        self.spin_precio.setRange(0.1, 50000.0)
        self.spin_precio.setPrefix("$ ")

        self.spin_distancia = QDoubleSpinBox()
        self.spin_distancia.setRange(1.0, 3000.0)
        self.spin_distancia.setSuffix(" km")

        form.addRow("Cliente:", self.input_cliente)
        form.addRow("Catálogo de Producto:", self.combo_producto)
        
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.lbl_preview_img)
        img_layout.addStretch()
        form.addRow("Vista previa:", img_layout)

        form.addRow("Destino / Ciudad:", self.input_destino)
        form.addRow("Peso Total:", self.spin_peso)
        form.addRow("Valor ($):", self.spin_precio)
        form.addRow("Distancia (km):", self.spin_distancia)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validar_y_aceptar)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        # Cargar valores del primer producto
        self.al_cambiar_producto(0)

    def al_cambiar_producto(self, index):
        prod = self.combo_producto.itemData(index)
        if prod:
            self.spin_peso.setValue(prod.peso_kg)
            self.spin_precio.setValue(prod.precio_usd)
            
            pixmap = AutomationService.obtener_pixmap_desde_url(prod.imagen_url)
            if pixmap and not pixmap.isNull():
                self.lbl_preview_img.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.lbl_preview_img.setText("Sin Imagen")

    def cargar_datos_pedido(self):
        self.input_cliente.setText(self.pedido.cliente)
        self.input_destino.setText(self.pedido.destino)
        self.spin_peso.setValue(self.pedido.peso_kg)
        self.spin_precio.setValue(self.pedido.precio_usd)
        self.spin_distancia.setValue(self.pedido.distancia_km)

    def validar_y_aceptar(self):
        if not self.input_cliente.text().strip() or not self.input_destino.text().strip():
            QMessageBox.warning(self, "Atención", "Escribe el cliente y destino.")
            return
        self.accept()

    def get_data(self):
        id_ped = self.pedido.id_pedido if self.pedido else f"ENV-{random.randint(1000, 9999)}"
        prod_seleccionado = self.combo_producto.currentData()
        
        return {
            "id_pedido": id_ped,
            "cliente": self.input_cliente.text().strip(),
            "producto": prod_seleccionado.nombre if prod_seleccionado else "Personalizado",
            "destino": self.input_destino.text().strip(),
            "peso_kg": self.spin_peso.value(),
            "precio_usd": self.spin_precio.value(),
            "distancia_km": self.spin_distancia.value(),
            "imagen_url": prod_seleccionado.imagen_url if prod_seleccionado else ""
        }