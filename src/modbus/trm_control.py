import logging
from dataclasses import dataclass
from enum import Enum
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from pymodbus.client import ModbusSerialClient

from src.modbus.dataframes.device_values import DeviceValues
from src.modbus.dataframes.temperature_program import TemperatureProgram
from src.modbus.dataframes.modbus_params import ModbusParams
from src.modbus.exceptions import ModbusConnectionLost, ReadRegistersError, ModbusBaseException

logger = logging.getLogger(__name__)


@dataclass
class DeviceAddress:
    register_address: int
    count: int = None


class TRM(QObject):
    device_connected = pyqtSignal(bool)
    temperature_program_updated = pyqtSignal()

    modbus_connection_lost = pyqtSignal()

    device_values_ready = pyqtSignal(DeviceValues)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.modbus_client: ModbusSerialClient | None = None
        self.device_params: ModbusParams | None = None

        self.current_values_buffer: DeviceValues | None = None
        self.current_temperature_program_buffer: TemperatureProgram | None = None

    def _init_device(self, modbus_params: ModbusParams):
        self.modbus_client = ModbusSerialClient(
            port=modbus_params.serial_port,
            baudrate=modbus_params.baudrate,
            bytesize=modbus_params.bytesize,
            parity=modbus_params.pairity,
            stopbits=modbus_params.stopbits
        )
        self.device_params = modbus_params

    @pyqtSlot(ModbusParams)
    def connect_device(self, modbus_params: ModbusParams):
        self._init_device(modbus_params)
        logger.info('connecting to modbus')
        state = self.modbus_client.connect()
        logger.info(f'connection status {state}')
        self.device_connected.emit(state)

    @pyqtSlot(float)
    def adjust_temperature(self, delta_temp: float):
        program = self._get_current_temperature_program()
        program.target_temperature += delta_temp
        logger.info(f'adjusting temperature for {delta_temp}')
        self.set_new_temperature_program(program)

    @pyqtSlot(TemperatureProgram)
    def set_new_temperature_program(self, temperature: TemperatureProgram):
        logger.info('setting new temperature program')
        if not self.modbus_client or not self.modbus_client.connected:
            logger.warning('no modbus client or modbus client is not connected')
            return

        # TODO: come up with a idea of storing registers
        self.modbus_client.write_registers(
            257,
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

    def _get_current_temperature_program(self) -> TemperatureProgram:
        logger.info('getting current temperature program')
        try:
            registers = self.modbus_client.read_input_registers(
                257,
                4,
                self.device_params.slave_id
            ).registers
        except AttributeError:
            logger.error('unable to get current temperature program')
            if self.current_temperature_program_buffer:
                return self.current_temperature_program_buffer
            else:
                registers = [0, 0, 0, 0]

        program = TemperatureProgram(
            target_temperature=registers[0],
            point_position=registers[1],
            raising_time=registers[2],
            holding_time=registers[3]
        )
        return program

    def _get_device_state(self) -> int | None:
        device_state = None

        try:
            device_state = self.read_registers(
                17,
                1,
                self.device_params.slave_id)[0]
        except ModbusBaseException as exception:
            logger.error('failed to get device state')
            if isinstance(exception, ModbusConnectionLost):
                logger.error('no connection to modbus device')
                self.modbus_connection_lost.emit()
            elif isinstance(exception, ReadRegistersError):
                logger.error('unable to read response registers')
        return device_state

    def _get_current_temperature(self) -> float | None:
        current_temperature = None
        try:
            current_temperature = self.read_registers(
                2,
                1,
                self.device_params.slave_id)[0]
        except ModbusBaseException as exception:
            logger.error('failed to get current temperature')
            if isinstance(exception, ModbusConnectionLost):
                logger.error('no connection to modbus device')
                self.modbus_connection_lost.emit()
            elif isinstance(exception, ReadRegistersError):
                logger.error('unable to read response registers')
        return current_temperature

    @pyqtSlot()
    def get_current_values(self):
        logger.info('getting device values')
        device_state = self.read_registers(
            17,
            1,
            self.device_params.slave_id
        )[0]

        current_temperature = self.read_registers(
            2,
            1,
            self.device_params.slave_id
        )[0]

        except ModbusBaseException as exception:
            if isinstance(exception, ModbusConnectionLost):
                logger.error('no connection to modbus device')
                self.modbus_connection_lost.emit()
            if isinstance(exception, ReadRegistersError):
                logger.error('unable to read response registers')

            if self.current_values_buffer:
                logger.warning('getting device values from buffer')
                device_state = self.current_values_buffer.current_device_state
                current_temperature = self.current_values_buffer.current_temperature

        current_program = self._get_current_temperature_program()
        device_values = DeviceValues(device_state, current_program, current_temperature)

        self.device_values_ready.emit(device_values)

    def read_registers(self, address: int, count: int, slave_id: int) -> List[int] | None:
        logger.info('reading registers')
        if not self.modbus_client:
            return
        if not self.modbus_client.connected:
            logger.error('no connection to modbus device')
            self.modbus_connection_lost.emit()
        response = self.modbus_client.read_input_registers(address, count, slave_id)
        try:
            registers = response.registers
        except AttributeError:
            logger.error('unable to read response registers')
            raise ReadRegistersError
        return registers

    def write_registers(self, ):
        self.modbus_client.write_registers()


    def set_running_state(self, running_state: bool):
        logger.info('setting running state')
        self.modbus_client.write_coil(80, running_state, self.device_params.slave_id)
