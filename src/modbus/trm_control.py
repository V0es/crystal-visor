import logging
import time
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException
from minimalmodbus import Instrument
from src.modbus.register_map import RegisterMap
from src.modbus.register_reader import RegisterReaderThread
from src.modbus.utils.dataframes.device_values import DeviceValues
from src.modbus.utils.dataframes import TemperatureProgram
from src.modbus.utils.dataframes import ModbusParams
from src.modbus.exceptions import ReadRegistersError
from src.modbus.utils.dataframes.modbus_params import PollingSettings

logger = logging.getLogger(__name__)


class TRM(QObject):
    device_connected = pyqtSignal(bool)
    temperature_program_updated = pyqtSignal()

    modbus_connection_lost = pyqtSignal()
    read_registers_error = pyqtSignal()

    device_values_ready = pyqtSignal(DeviceValues)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.modbus_client: Instrument | None = None
        self.device_params: ModbusParams | None = None
        self.registers = RegisterMap()
        self.polling_settings = PollingSettings()

        self.current_values_buffer: DeviceValues = DeviceValues()
        self.current_temperature_program_buffer: TemperatureProgram = TemperatureProgram()

        self.register_read_thread: RegisterReaderThread | None = None

    def _init_device(self, modbus_params: ModbusParams):
        self.modbus_client = Instrument(
            port=modbus_params.serial_port,
            slaveaddress=modbus_params.slave_id,
        )
        self.device_params = modbus_params
        self.register_read_thread = RegisterReaderThread(
            self.registers,
            self.modbus_client,
            self.device_params.slave_id,
            self.polling_settings
        )

        self.connect_signals()

    def connect_signals(self):
        self.device_connected.connect(self.register_read_thread.start)
        self.register_read_thread.result.connect(self.device_values_ready)

    @pyqtSlot(ModbusParams)
    def connect_device(self, modbus_params: ModbusParams):
        self._init_device(modbus_params)
        logger.info('connecting to modbus')
        state = True
        logger.info(f'connection status {state}')
        self.device_connected.emit(state)

    @pyqtSlot(float)
    def adjust_temperature(self, delta_temp: float):
        program = self.register_read_thread.current_values().current_program

        new_target_temperature = round(program.target_temperature + delta_temp, 1)
        new_point_position = str(new_target_temperature)[::-1].find('.')
        new_target_temperature = int(new_target_temperature * 10**new_point_position)
        if new_target_temperature < 410 or new_target_temperature > 460:
            new_target_temperature = program.target_temperature
            new_point_position = program.point_position

        program.target_temperature = new_target_temperature
        program.point_position = new_point_position

        program.target_temperature += delta_temp
        logger.info(f'adjusting temperature for {delta_temp}')
        self.set_new_temperature_program(program)

    @pyqtSlot(TemperatureProgram)
    def set_new_temperature_program(self, temperature: TemperatureProgram):
        logger.info('setting new temperature program')
        if not self.modbus_client:
            self.modbus_connection_lost.emit()
            logger.warning('no modbus client or modbus client is not connected')
            return

        # TODO: come up with an idea of storing registers

        try:
            self.modbus_client.write_registers(
                self.registers.temperature_program.address,
                [
                    temperature.target_temperature,
                    temperature.point_position,
                    temperature.raising_time,
                    temperature.holding_time
                ]
            )
        except IOError:
            print('no response')
        self.set_running_state(False)
        time.sleep(0.5)
        self.set_running_state(True)
        self.temperature_program_updated.emit()

    @pyqtSlot(PollingSettings)
    def update_polling_settings(self, new_settings):
        self.polling_settings = new_settings
        if self.register_read_thread:
            self.register_read_thread.update_polling_settings(self.polling_settings)

    def set_running_state(self, running_state: bool):
        logger.info('setting running state')
        state = 1 if running_state else 0
        try:
            self.modbus_client.write_bit(self.registers.running_state.address, state, functioncode=5)
        except IOError as e:
            print('some error', e)
