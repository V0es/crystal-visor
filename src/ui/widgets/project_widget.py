import logging

import numpy as np
from PyQt6.QtCore import pyqtSlot, QThreadPool
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox

from .display_panel import DisplayPanel
from .settings_panel import SettingsPanel
from .control_panel import ControlPanel

from src.utils.timer import TimerControl

DEBUG = True

if DEBUG:
    from test.mock.trm_mock import TrmMock as TRM
    from test.mock.camera_mock import CameraMock as CameraDevice
    from test.mock.image_analysis_mock import ImageAnalysisMock as ImageAnalysisWorker
else:
    from src.modbus import TRM
    from src.camera import CameraDevice
    from src.core import ImageAnalysisWorker

logger = logging.getLogger(__name__)


class ProjectWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        logger.warning(f'DEBUG option is set to {DEBUG}')

        self.control_panel = ControlPanel()
        self.settings_panel = SettingsPanel()
        self.display_panel = DisplayPanel()

        self.trm = TRM(self)
        self.camera = CameraDevice()
        self.analysis_threadpool = QThreadPool()

        self.camera_timer = TimerControl(10000, self)
        self.trm_timer = TimerControl(1000, self)
        self.label_timer = TimerControl(1000, self)

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

    @pyqtSlot(np.ndarray)
    def send_image_to_analysis(self, image: np.ndarray):
        worker = ImageAnalysisWorker(image)
        worker.signals.delta_height_ready.connect(self.control_panel.auto_update_temperature_program)
        self.analysis_threadpool.start(worker)

    def read_registers_error(self):
        # TODO: decide if registers error is needed
        message = QMessageBox.warning(
            self,
            'Ошибка при чтении регистров',
            'Не получилось прочитать регистры, взято значение из буффера',
            QMessageBox.StandardButton.Ok
        )

        if message == QMessageBox.StandardButton.Ok:
            return
        pass

    def modbus_connection_lost(self):
        message = QMessageBox.critical(
            self,
            'Потеряна связь с ТРМ',
            'Не получилось подключиться к ТРМ',
            QMessageBox.StandardButton.Ok
        )
        if message == QMessageBox.StandardButton.Ok:
            return

    def camera_connection_lost(self):
        message = QMessageBox(
            self,
            'Потеряна связь с камерой',
            'Не получилось подключиться к камере',
            QMessageBox.StandardButton.Ok
        )
        if message == QMessageBox.StandardButton.Ok:
            return

    def connect_signals(self):
        self.settings_panel.modbus_connect.connect(self.trm.connect_device)
        self.settings_panel.camera_connect.connect(self.camera.connect_camera)

        # Error message boxes
        self.trm.modbus_connection_lost.connect(self.modbus_connection_lost)
        self.trm.read_registers_error.connect(self.read_registers_error)
        self.camera.connection_lost.connect(self.camera_connection_lost)

        self.trm.device_connected.connect(self.settings_panel.update_modbus_connection_state)
        self.trm.device_connected.connect(self.trm_timer.start_timer)
        self.trm.device_values_ready.connect(self.display_panel.update_device_values)

        self.trm_timer.timer_updated.connect(self.trm.get_current_values)

        self.camera.opened.connect(self.settings_panel.update_camera_connection_state)
        # START ANALYSIS
        # TODO: make better
        self.camera.image_ready.connect(self.send_image_to_analysis)

        # self.image_analysis.delta_height_ready.connect(self.control_panel.auto_update_temperature_program)

        self.control_panel.start_process_btn.clicked.connect(self.camera_timer.start_timer)
        self.control_panel.start_process_btn.clicked.connect(self.label_timer.start_timer)

        self.control_panel.pause_process_btn.clicked.connect(self.camera_timer.pause_timer)
        self.control_panel.pause_process_btn.clicked.connect(self.label_timer.pause_timer)

        self.control_panel.stop_process_btn.clicked.connect(self.camera_timer.stop_timer)
        self.control_panel.stop_process_btn.clicked.connect(self.label_timer.stop_timer)
        self.control_panel.stop_process_btn.clicked.connect(lambda: self.trm.set_running_state(False))

        self.control_panel.temperature_program_ready.connect(self.trm.set_new_temperature_program)
        self.control_panel.adjustment_delta_ready.connect(self.trm.adjust_temperature)

        self.label_timer.timer_updated.connect(self.control_panel.update_timer_label)
        self.camera_timer.timer_updated.connect(self.camera.capture_image)
