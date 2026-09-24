import math
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, 
                             QHeaderView, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QTimer
from controllers.data_manager import DataManager
from controllers.bcv_service import BCVService
from controllers.automation_service import AutomationService
from models.pedido import Pedido
from views.dialogs import PedidoDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Envíos Express (Modo Oscuro) - Tienda Online")
        self.resize(1050, 650)
        
        self.data_manager = DataManager()
        self.tasa_bcv = BCVService.obtener_tasa_dolar()
        self.pedidos = self.data_manager.cargar_pedidos()

        # Temporizador para automatización de pedidos
        self.timer_auto = QTimer(self)
        self.timer_auto.timeout.connect(self.generar_pedido_automatico)

        self.init_ui()
        self.actualizar_tabla()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Panel Superior - BCV y Automatización
        top_card = QFrame()
        top_card.setObjectName("topCard")
        top_layout = QHBoxLayout(top_card)

        self.label_tasa = QLabel(f"<b>Tasa Oficial BCV:</b> {self.tasa_bcv:.2f} VES/USD")
        self.label_tasa.setObjectName("labelTasa")
        
        btn_refrescar_bcv = QPushButton("🔄 Actualizar BCV")
        btn_refrescar_bcv.clicked.connect(self.actualizar_tasa_bcv)

        self.btn_auto = QPushButton("⚡ Activar Automatización")
        self.btn_auto.setCheckable(True)
        self.btn_auto.setObjectName("btnAuto")
        self.btn_auto.toggled.connect(self.toggle_automatizacion)

        top_layout.addWidget(self.label_tasa)
        top_layout.addWidget(btn_refrescar_bcv)
        top_layout.addSpacing(20)
        top_layout.addWidget(self.btn_auto)
        top_layout.addStretch()

        main_layout.addWidget(top_card)

        # Tabla Principal
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Producto", "Destino", "Peso", "Precio ($)", "Precio (VES)", "Prioridad"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        main_layout.addWidget(self.table)

        # Botones de Control
        btn_layout = QHBoxLayout()
        
        btn_crear = QPushButton("➕ Crear Manual")
        btn_crear.setObjectName("btnCrear")
        btn_crear.clicked.connect(self.crear_pedido)

        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_pedido)

        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setObjectName("btnEliminar")
        btn_eliminar.clicked.connect(self.borrar_pedido)

        btn_layout.addWidget(btn_crear)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_eliminar)

        main_layout.addLayout(btn_layout)

    def toggle_automatizacion(self, checked):
        if checked:
            self.btn_auto.setText("⏸️ Detener Automatización")
            self.btn_auto.setStyleSheet("background-color: #e67e22; color: white;")
            # Genera un pedido cada 5 segundos
            self.timer_auto.start(5000)
        else:
            self.btn_auto.setText("⚡ Activar Automatización")
            self.btn_auto.setStyleSheet("")
            self.timer_auto.stop()

    def generar_pedido_automatico(self):
        nuevo = AutomationService.generar_pedido_aleatorio()
        self.pedidos.append(nuevo)
        self.data_manager.guardar_pedidos(self.pedidos)
        self.actualizar_tabla()

    def actualizar_tasa_bcv(self):
        self.tasa_bcv = BCVService.obtener_tasa_dolar()
        self.label_tasa.setText(f"<b>Tasa Oficial BCV:</b> {self.tasa_bcv:.2f} VES/USD")
        self.actualizar_tabla()

    def ordenar_pedidos_por_prioridad(self):
        self.pedidos.sort(key=lambda p: p.prioridad, reverse=True)

    def actualizar_tabla(self):
        self.ordenar_pedidos_por_prioridad()
        self.table.setRowCount(0)

        for row, p in enumerate(self.pedidos):
            self.table.insertRow(row)
            precio_ves = math.ceil(p.precio_usd * self.tasa_bcv * 100) / 100.0

            self.table.setItem(row, 0, QTableWidgetItem(p.id_pedido))
            self.table.setItem(row, 1, QTableWidgetItem(p.cliente))
            self.table.setItem(row, 2, QTableWidgetItem(p.producto))
            self.table.setItem(row, 3, QTableWidgetItem(p.destino))
            self.table.setItem(row, 4, QTableWidgetItem(f"{p.peso_kg:.2f} kg"))
            self.table.setItem(row, 5, QTableWidgetItem(f"$ {p.precio_usd:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"Bs. {precio_ves:,.2f}"))
            
            item_prioridad = QTableWidgetItem(f"{p.prioridad:.2f}")
            item_prioridad.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 7, item_prioridad)

    def crear_pedido(self):
        dialog = PedidoDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            nuevo = Pedido.from_dict(data)
            self.pedidos.append(nuevo)
            self.data_manager.guardar_pedidos(self.pedidos)
            self.actualizar_tabla()

    def editar_pedido(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Atención", "Selecciona un envío para editar.")
            return

        pedido_actual = self.pedidos[selected]
        dialog = PedidoDialog(self, pedido=pedido_actual)
        if dialog.exec_():
            data = dialog.get_data()
            pedido_actual.cliente = data["cliente"]
            pedido_actual.producto = data["producto"]
            pedido_actual.destino = data["destino"]
            pedido_actual.peso_kg = data["peso_kg"]
            pedido_actual.precio_usd = data["precio_usd"]
            pedido_actual.distancia_km = data["distancia_km"]
            pedido_actual.imagen_url = data["imagen_url"]
            pedido_actual.prioridad = pedido_actual.calcular_prioridad()

            self.data_manager.guardar_pedidos(self.pedidos)
            self.actualizar_tabla()

    def borrar_pedido(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Atención", "Selecciona un envío para borrar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar", "¿Eliminar este pedido?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.pedidos.pop(selected)
            self.data_manager.guardar_pedidos(self.pedidos)
            self.actualizar_tabla()