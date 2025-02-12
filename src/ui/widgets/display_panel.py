from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from .resource.display_panel import Ui_display_panel
from src.modbus.utils.dataframes.device_values import DeviceValues
from src.modbus.utils.dataframes import TemperatureProgram


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
            device_values.current_temperature / 10 ** device_values.current_point_position
        )
        # TODO: rewrite match case
        dd = {
            0: 'Cтоп',
            1: 'Работа',
            2: 'Критическая авария',
            3: 'Прогр. технолога завершена',
            4: 'Автонастройка ПИД',
            5: 'Ожид. запуска автонастройки',
            6: 'Автонастройка завершена',
            7: 'Настройка',
        }

        self.device_state_field.setText(dd.get(device_values.current_operating_mode, 'Стоп'))
