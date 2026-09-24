import sys
import os
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

def cargar_estilos(app):
    qcss_path = "styles.qcss"
    if os.path.exists(qcss_path):
        with open(qcss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    cargar_estilos(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()