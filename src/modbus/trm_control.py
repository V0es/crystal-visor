import logging
import time
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException

from src.modbus.register_map import RegisterMap
from src.modbus.register_reader import RegisterReaderThread
from src.modbus.utils.dataframes.device_values import DeviceValues
from src.modbus.utils.dataframes import TemperatureProgram
from src.modbus.utils.dataframes import ModbusParams
from src.modbus.exceptions import ReadRegistersError


logger = logging.getLogger(__name__)


class TRM(QObject):
    device_connected = pyqtSignal(bool)
    temperature_program_updated = pyqtSignal()

    modbus_connection_lost = pyqtSignal()
    read_registers_error = pyqtSignal()

    device_values_ready = pyqtSignal(DeviceValues)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.modbus_client: ModbusSerialClient | None = None
        self.device_params: ModbusParams | None = None
        self.registers = RegisterMap()

        self.current_values_buffer: DeviceValues = DeviceValues()
        self.current_temperature_program_buffer: TemperatureProgram = TemperatureProgram()

        self.register_read_thread: RegisterReaderThread | None = None

    def _init_device(self, modbus_params: ModbusParams):
        self.modbus_client = ModbusSerialClient(
            port=modbus_params.serial_port,
            baudrate=modbus_params.baudrate,
            bytesize=modbus_params.bytesize,
            parity=modbus_params.pairity,
            stopbits=modbus_params.stopbits
        )
        self.device_params = modbus_params
        self.register_read_thread = RegisterReaderThread(
            self.registers,
            self.modbus_client,
            self.device_params.slave_id
        )

        self.connect_signals()

    def connect_signals(self):
        self.device_connected.connect(self.register_read_thread.start)
        self.register_read_thread.result.connect(self.device_values_ready)

    @pyqtSlot(ModbusParams)
    def connect_device(self, modbus_params: ModbusParams):
        self._init_device(modbus_params)
        logger.info('connecting to modbus')
        state = self.modbus_client.connect()
        logger.info(f'connection status {state}')
        self.device_connected.emit(state)

    @pyqtSlot(float)
    def adjust_temperature(self, delta_temp: float):
        program = self.register_read_thread.current_values().current_program
        program.target_temperature += delta_temp
        logger.info(f'adjusting temperature for {delta_temp}')
        self.set_new_temperature_program(program)

    @pyqtSlot(TemperatureProgram)
    def set_new_temperature_program(self, temperature: TemperatureProgram):
        logger.info('setting new temperature program')
        if not self.modbus_client or not self.modbus_client.connected:
            self.modbus_connection_lost.emit()
            logger.warning('no modbus client or modbus client is not connected')
            return

        # TODO: come up with an idea of storing registers
        self.modbus_client.write_registers(
            self.registers.temperature_program.address,
            [
                temperature.target_temperature,
                temperature.point_position,
                temperature.raising_time,
                temperature.holding_time
            ],
            self.device_params.slave_id
        )
        self.set_running_state(True)
        self.temperature_program_updated.emit()

    def set_running_state(self, running_state: bool):
        logger.info('setting running state')
        self.modbus_client.write_coil(self.registers.running_state.address, running_state, self.device_params.slave_id)
