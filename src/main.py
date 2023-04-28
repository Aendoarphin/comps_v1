from gui.main_window import *
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_mainWindow()
    ui.mainWindow.show()
    sys.exit(app.exec())

