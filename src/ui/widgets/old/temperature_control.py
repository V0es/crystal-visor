from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget

from src.ui.widgets.old.temperature_control import Ui_temperature_control


class TemperatureControl(QWidget, Ui_temperature_control):
    read_data = pyqtSignal(int)
    send_data = pyqtSignal(int, int, list)

    def __init__(self, parent=None):
        super(TemperatureControl, self).__init__(parent)

        self.setupUi(self)
        self.init_ui()

        self.modbus_client = None

        self.connect_signals()
        # uic.loadUi('ui/widgets/temperature_control.ui', self)

    def connect_signals(self):
        self.read_btn.clicked.connect(self.read_button_clicked)
        self.send_btn.clicked.connect(self.send_button_clicked)

    def init_ui(self):
        self.recieve_value_lcd.display(0)
        self.function_type_combo.addItems(
            [
                '5',
                '6',
                '10'
            ]
        )

    def read_button_clicked(self):
        address = self.recieve_address_spinbox.value()
        print(f'read from {address}')
        self.read_data.emit(address)

    def send_button_clicked(self):
        address = self.send_address_spinbox.value()
        function_type = int(self.function_type_combo.currentText())
        values = [int(value) for value in self.values_field.text().split(';')]
        print(f'write to {address}')
        self.send_data.emit(address, function_type, values)

    @pyqtSlot(float)
    def display_value(self, value: float):
        self.recieve_value_lcd.display(value)
