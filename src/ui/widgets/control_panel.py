from PyQt6.QtCore import pyqtSlot, QTime, pyqtSignal
from PyQt6.QtWidgets import QWidget

from .resource.control_panel import Ui_control_panel
from src.modbus.dataframes.temperature_program import TemperatureProgram


class ControlPanel(QWidget, Ui_control_panel):
    temperature_program_ready = pyqtSignal(TemperatureProgram)
    adjustment_delta_ready = pyqtSignal(float)

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)

        self.setupUi(self)

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.update_temperature_adjustment_availability()

    def connect_signals(self):
        self.auto_temp_adjustment_checkbox.stateChanged.connect(self.update_temperature_adjustment_availability)
        self.set_new_values_btn.clicked.connect(self.manual_update_temperature_program)

    @pyqtSlot(QTime)
    def update_timer_label(self, time: QTime):
        self.time_label.setText(time.toString('hh:mm:ss'))

    @pyqtSlot()
    def update_temperature_adjustment_availability(self):
        current_state = self.auto_temp_adjustment_checkbox.isChecked()
        self.delta_adjustment_label.setEnabled(current_state)
        self.delta_temperature_dspinbox.setEnabled(current_state)
        self.delta_temperature_label.setEnabled(current_state)

    @pyqtSlot()
    def manual_update_temperature_program(self):
        if self.auto_temp_adjustment_checkbox.isChecked():
            return
        new_program = TemperatureProgram(
            target_temperature=self.new_temperature_spinbox.value(),
            point_position=self.new_point_position_spinbox.value(),
            raising_time=self.new_raising_time_spinbox.value(),
            holding_time=self.new_holding_time_spinbox.value()
        )
        self.temperature_program_ready.emit(new_program)

    @pyqtSlot(float)
    def auto_update_temperature_program(self, current_height: float):
        if not self.auto_temp_adjustment_checkbox.isChecked():
            return

        adjusted_delta_temp = current_height * self.delta_temperature_dspinbox.value()

        self.adjustment_delta_ready.emit(adjusted_delta_temp)
