import logging
from typing import List

from PyQt6.QtCore import pyqtSlot, QRegularExpression, pyqtSignal, QThreadPool
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import QWidget

from .resource.settings_panel import Ui_settings_panel
from src.utils.serial import SerialPortWorker
from src.modbus.utils.dataframes import ModbusParams
from src.camera.camera_connection_settings import CameraConnection

logger = logging.getLogger(__name__)


class SettingsPanel(QWidget, Ui_settings_panel):
    modbus_connect = pyqtSignal(ModbusParams)
    camera_connect = pyqtSignal(CameraConnection)

    def __init__(self, parent=None):

        super(SettingsPanel, self).__init__(parent)

        self.threadpool = QThreadPool()

        self.setupUi(self)
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.baudrate_combo.addItems(
            [
                '19200'
            ]
        )

        self.pairity_combo.addItems(
            [
                'N',
                '1',
                '2'
            ]
        )

        self.stopbits_spinbox.setValue(1)
        self.bytesize_spinbox.setValue(8)
        self.slave_id_spinbox.setValue(16)
        self.get_available_serial_ports()

        self.camera_ip_field.setValidator(
            QRegularExpressionValidator(
                QRegularExpression(
                    '^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$'
                )
            )
        )

        self.camera_port_field.setValidator(QIntValidator())

        self.camera_stream_combo.addItems(
            [
                'main'
            ]
        )

    def connect_signals(self):
        self.refresh_serial_ports_btn.clicked.connect(self.get_available_serial_ports)
        self.modbus_connect_btn.clicked.connect(self.connect_to_modbus_device)
        self.connect_camera_btn.clicked.connect(self.connect_to_camera_device)

    @pyqtSlot()
    def get_available_serial_ports(self):
        serial_worker = SerialPortWorker()
        serial_worker.signals.available_ports_ready.connect(self.update_available_serial_ports)
        self.threadpool.start(serial_worker)

    @pyqtSlot(list)
    def update_available_serial_ports(self, serial_ports: List[str]):

        logger.info(f'got available serial ports: {serial_ports}')
        # TODO: optimize loop
        for i in range(self.serial_port_combo.count()):
            self.serial_port_combo.removeItem(i)

        self.serial_port_combo.addItems(serial_ports)
        logger.info('updated com ports')

    @pyqtSlot()
    def connect_to_modbus_device(self):
        modbus_params = ModbusParams(
            serial_port=self.serial_port_combo.currentText(),
            slave_id=self.slave_id_spinbox.value(),
            baudrate=int(self.baudrate_combo.currentText()),
            bytesize=self.bytesize_spinbox.value(),
            pairity=self.pairity_combo.currentText(),
            stopbits=self.stopbits_spinbox.value()
        )
        self.modbus_connect.emit(modbus_params)

    @pyqtSlot()
    def connect_to_camera_device(self):
        camera_connection = CameraConnection(
            ip_address=self.camera_ip_field.text(),
            port=self.camera_port_field.text(),
            username=self.username_field.text(),
            password=self.password_field.text(),
            stream=self.camera_stream_combo.currentText()
        )
        self.camera_connect.emit(camera_connection)

    @pyqtSlot(bool)
    def update_modbus_connection_state(self, is_connected: bool):
        if is_connected:
            state = 'Подключён'
        else:
            state = 'Не подключён'
        self.modbus_state_label.setText(state)

    @pyqtSlot()
    def update_camera_connection_state(self):
        current_state = self.camera_state_label.text()

        if current_state == 'Не подключено':
            self.camera_state_label.setText('Подключено')
        else:
            self.camera_state_label.setText('Не подключено')
