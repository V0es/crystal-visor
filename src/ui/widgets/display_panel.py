from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from .resource.display_panel import Ui_display_panel
from src.modbus.dataframes.device_values import DeviceValues
from src.modbus.dataframes.temperature_program import TemperatureProgram


class DisplayPanel(QWidget, Ui_display_panel):
    def __init__(self, parent=None):

        super(DisplayPanel, self).__init__(parent)

        self.setupUi(self)

    def _update_temperature_program(self, program: TemperatureProgram):
        self.target_temp_lcd.display(program.target_temperature)
        self.point_position_lcd.display(program.point_position)
        self.raising_time_lcd.display(program.raising_time)
        self.holding_temp_lcd.display(program.holding_time)

    @pyqtSlot(DeviceValues)
    def update_device_values(self, device_values: DeviceValues):
        self._update_temperature_program(device_values.current_program)
        self.current_temperature_lcd.display(
            device_values.current_temperature * 10 ** device_values.current_point_position
        )
        self.device_state_lcd.display(device_values.current_device_state)
