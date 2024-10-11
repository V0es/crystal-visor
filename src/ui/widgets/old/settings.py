from typing import List

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal, pyqtSlot

from src.ui.widgets.old.settings import Ui_settings

from src.utils.serial import available_serial_ports


import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
)


class Settings(QWidget, Ui_settings):
    data_received = pyqtSignal(float)

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self.setupUi(self)
        self.init_ui()

        self.modbus_client = None
        # uic.loadUi('ui/widgets/settings.ui', self)

    def init_ui(self):
        self.baudrate_combo.addItems([
            '9600',
            '19200'
        ])

        self.baudrate_combo.setCurrentIndex(1)

        self.bytesize_spinbox.setValue(8)
        self.stopbits_spinbox.setValue(1)
        self.slave_id_spinbox.setValue(16)

        self.serial_port_combo.addItems(serial_ports())

        self.pairity_combo.addItems([
            'N',
            '1',
            '2'
        ])
        self.pairity_combo.setCurrentIndex(0)

        self.ip_field.setValidator(
            QRegularExpressionValidator(
                QRegularExpression(
                    '^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$'
                )
            )
        )

        self.port_field.setValidator(QIntValidator())

        self.stream_type_combo.addItem('main')

    @pyqtSlot(int)
    def get_value(self, address: int):
        print('get value')
        if not self.modbus_client:
            self._init_modbus_client()
        try:
            data = self.modbus_client.read_input_registers(address, 1, slave=self.slave_id_spinbox.value())
            self.data_received.emit(data.registers[0])
        except Exception as e:
            print('unlucky', e)

    @pyqtSlot(int, int, list)
    def send_value(self, address: int, function_type: int, values: List[int]):
        print(f'write values {values} to {address}')
        print(type(address))
        if not self.modbus_client:
            self._init_modbus_client()
        resp = None
        try:
            match function_type:
                case 5:
                    resp = self.modbus_client.write_coil(address, bool(values[0]), self.slave_id_spinbox.value())
                case 6:
                    resp = self.modbus_client.write_register(address, values[0], self.slave_id_spinbox.value())
                case 10:
                    resp = self.modbus_client.write_registers(address, values, self.slave_id_spinbox.value())

            print(f'response: {resp}')
        except Exception as e:
            print('unlucky', e)
        #self.data_received.emit(data.registers[0])

    def _init_modbus_client(self):
        self.modbus_client = ModbusClient.ModbusSerialClient(
            self.serial_port_combo.currentText(),
            framer=FramerType.RTU,
            # timeout=10,
            # retries=3,
            baudrate=int(self.baudrate_combo.currentText()),
            bytesize=self.bytesize_spinbox.value(),
            parity=self.pairity_combo.currentText(),
            stopbits=self.stopbits_spinbox.value(),
            # handle_local_echo=False,
        )

        self.modbus_client.connect()
