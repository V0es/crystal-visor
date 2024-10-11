from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout
from ui.widgets import ProjectWidget


class CrystalVisor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_widget = ProjectWidget(self)

        self.connect_signals()
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 600)

        self.setCentralWidget(self.project_widget)


    def connect_signals(self):
        ...


app = QApplication([])
window = CrystalVisor()

window.show()

app.exec()
