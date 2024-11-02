import logging

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


if __name__ == '__main__':
    print('basic conf')
    logging.basicConfig(
        filename='journal.log',
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        encoding='utf-8')
    app = QApplication([])
    window = CrystalVisor()

    window.show()

    app.exec()
