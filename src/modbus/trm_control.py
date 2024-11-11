import logging
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException

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

        self.current_values_buffer: DeviceValues = DeviceValues()
        self.current_temperature_program_buffer: TemperatureProgram = TemperatureProgram()

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
        program = self.get_current_temperature_program()
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

    def get_current_temperature_program(self) -> TemperatureProgram:
        """
        Get current temperature program parameters or read from buffer
        :return: TemperatureProgram object composed of fetched parameters
        """
        logger.info('getting current temperature program')
        try:
            registers = self._read_registers(257, 4, self.device_params.slave_id)
            program = TemperatureProgram(*registers)

        except ReadRegistersError:
            logger.error('getting temperature program from buffer')
            program = self.current_values_buffer.current_program

        return program

    def get_current_temperature(self) -> float | None:
        """
        Get thermocouple reading from TRM or get from buffer
        :return: Current temperature
        """
        logger.info('getting current temperature')
        try:
            current_temperature = self._read_registers(2, 1, self.device_params.slave_id)[0]
            logger.info(f'current temperature: {current_temperature}')
        except ReadRegistersError:
            logger.error('getting current temperature from buffer')
            current_temperature = self.current_values_buffer.current_temperature
        return current_temperature

    def get_current_operation_mode(self) -> int:
        """
        Get current operating mode
        0 - idle
        1 - running
        2 - critical error
        3 - program ended
        4 - PID autotuning
        5 - waiting for PID autotuning
        6 - PID autotuning ended
        7 - setting

        :return:
        """
        logger.info('getting device state')
        try:
            mode = self._read_registers(17, 1, self.device_params.slave_id)[0]
        except ReadRegistersError:
            logger.error('getting device state form buffer')
            mode = self.current_values_buffer.current_operating_mode
        return mode

    @pyqtSlot()
    def get_current_values(self) -> None:
        """
        Collect values, compose to data object, update buffer and emit signal
        :return: None
        """
        logger.info('getting device values')

        current_operating_mode = self.get_current_operation_mode()
        current_temperature = self.get_current_temperature()
        current_program = self.get_current_temperature_program()
        current_point_position = self.get_current_point_position()

        device_values = DeviceValues(
            current_operating_mode,
            current_program,
            int(current_temperature),
            current_point_position
        )
        self.current_values_buffer = device_values  # update buffer

        self.device_values_ready.emit(device_values)

    def _read_registers(self, address: int, count: int, slave_id: int) -> List[int] | None:
        """
        Read 'count' registers starting from 'address' from device with 'slave_id' id
        Raises ReadRegistersError if response is invalid
        :param address: Starting register address
        :param count: Amount of registers to read
        :param slave_id: Modbus device id
        :return: List of registers
        """
        logger.info('reading registers')
        if not self.modbus_client:
            return
        if not self.modbus_client.connected:
            logger.error('no connection to modbus device')
            self.modbus_connection_lost.emit()
        try:
            response = self.modbus_client.read_input_registers(address, count, slave_id)
        except ConnectionException:
            logger.error('lost connection to modbus device')
            self.modbus_connection_lost.emit()
        try:
            registers = response.registers
        except AttributeError:
            logger.error(f'unable to read response registers, response: {response}')
            self.read_registers_error.emit()
            raise ReadRegistersError
        return registers

    def set_running_state(self, running_state: bool):
        logger.info('setting running state')
        self.modbus_client.write_coil(80, running_state, self.device_params.slave_id)

    def get_current_point_position(self):
        logger.info('getting current temperature point position')
        try:
            point_position = self._read_registers(0, 1, self.device_params.slave_id)[0]
        except ReadRegistersError:
            logger.error('getting device state form buffer')
            point_position = self.current_values_buffer.current_point_position
        return point_position
