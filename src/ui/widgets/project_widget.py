from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .display_panel import DisplayPanel
from .settings_panel import SettingsPanel
from .control_panel import ControlPanel

from src.modbus import TRM
from src.camera import CameraDevice
from src.utils.timer import TimerControl


class ProjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.control_panel = ControlPanel()
        self.settings_panel = SettingsPanel()
        self.display_panel = DisplayPanel()

        self.trm = TRM()
        self.camera = CameraDevice()
        self.timer = TimerControl()

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        side_layout = QVBoxLayout()
        side_widget = QWidget(self)
        side_layout.addWidget(self.display_panel)
        side_layout.addWidget(self.settings_panel)
        side_widget.setLayout(side_layout)

        layout = QHBoxLayout()
        layout.addWidget(side_widget)
        layout.addWidget(self.control_panel)
        self.setLayout(layout)

    def connect_signals(self):
        self.settings_panel.modbus_connect.connect(self.trm.connect_device)
        self.settings_panel.camera_connect.connect(self.camera.connect_camera)

        self.trm.device_connected.connect(self.settings_panel.update_modbus_connection_state)
        self.trm.device_values_ready.connect(self.display_panel.update_device_values)

        self.camera.opened.connect(self.settings_panel.update_camera_connection_state)

        self.control_panel.start_process_btn.clicked.connect(self.timer.start_timer)
        self.control_panel.pause_process_btn.clicked.connect(self.timer.pause_timer)
        self.control_panel.stop_process_btn.clicked.connect(self.timer.stop_timer)
        self.control_panel.temperature_program_ready.connect(self.trm.set_new_temperature_program)
        self.control_panel.adjustment_delta_ready.connect(self.trm.adjust_temperature)

        self.timer.timer_updated.connect(self.control_panel.update_timer_label)
        self.timer.timer_updated.connect(self.trm.get_current_values)
