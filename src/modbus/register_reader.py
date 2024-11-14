import logging
import time
from typing import List

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from pymodbus.client import ModbusSerialClient

from src.modbus.exceptions import ReadRegistersError
from src.modbus.register_map import RegisterMap, Register
from src.modbus.utils.dataframes import DeviceValues, TemperatureProgram

logger = logging.getLogger(__name__)


class RegisterReaderThread(QThread):
    result = pyqtSignal(DeviceValues)

    modbus_connection_lost = pyqtSignal()
    read_registers_error = pyqtSignal()

    def __init__(self,
                 registers: RegisterMap,
                 modbus_client: ModbusSerialClient,
                 slave_id: int,
                 polling_rate_msec: int = 1000):

        super().__init__()
        self.is_running = False
        self._current_values_buffer = DeviceValues()

        self.registers = registers
        self.modbus = modbus_client
        self.slave_id = slave_id
        self.polling_rate_sec = polling_rate_msec / 1000

    def run(self):
        self.is_running = True
        while self.is_running:
            time.sleep(self.polling_rate_sec)

            logger.info('getting device values')

            current_operating_mode = self.get_current_operation_mode()
            print(f'operation mode: address 17 = {current_operating_mode}')
            time.sleep(0.2)

            current_temperature = self.get_current_temperature()
            print(f'current_temperature: address 2 = {current_temperature}')
            time.sleep(0.2)

            current_program = self.get_current_temperature_program()
            print(f'current program: address 256 = {current_program}')
            time.sleep(0.2)

            current_point_position = self.get_current_point_position()
            print(f'current point position: address 0 = {current_point_position}\n')

            device_values = DeviceValues(
                current_operating_mode,
                current_program,
                int(current_temperature),
                current_point_position
            )

            self.result.emit(device_values)

    @pyqtSlot()
    def stop(self):
        self.is_running = False

    def current_values(self) -> DeviceValues:
        return self._current_values_buffer

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
            mode = self._read_registers(self.registers.operating_mode)[0]

        except ReadRegistersError:
            logger.error('getting device state form buffer')
            mode = self._current_values_buffer.current_operating_mode
        return mode

    def _read_registers(self, register: Register) -> List[int] | None:
        """
        Read register(s) from device
        Raises ReadRegistersError if response is invalid
        :param register: Register dataclass with address and bits count
        :return: List of registers
        """
        logger.info('reading registers')
        if not self.modbus.connected:
            logger.error('no connection to modbus device')
            self.modbus.connect()
            # self.modbus_connection_lost.emit()

        response = self.modbus.read_input_registers(register.address, register.count, self.slave_id)
        if response.isError():
            logger.error('lost connection to modbus device')
            self.modbus_connection_lost.emit()
        try:
            registers = response.registers
        except AttributeError:
            logger.error(f'unable to read response registers, response: {response}')
            self.read_registers_error.emit()
            raise ReadRegistersError
        return registers

    def get_current_temperature(self) -> float | None:
        """
        Get thermocouple reading from TRM or get from buffer
        :return: Current temperature
        """
        logger.info('getting current temperature')
        try:
            current_temperature = self._read_registers(self.registers.current_temperature)[0]
            logger.info(f'current temperature: {current_temperature}')
        except ReadRegistersError:
            logger.error('getting current temperature from buffer')
            current_temperature = self._current_values_buffer.current_temperature
        return current_temperature

    def get_current_temperature_program(self) -> TemperatureProgram:
        """
        Get current temperature program parameters or read from buffer
        :return: TemperatureProgram object composed of fetched parameters
        """
        logger.info('getting current temperature program')
        try:
            registers = self._read_registers(self.registers.temperature_program)
            program = TemperatureProgram(*registers)

            # convert temperature to float
            program.target_temperature /= 10**program.point_position

        except ReadRegistersError:
            logger.error('getting temperature program from buffer')
            program = self._current_values_buffer.current_program

        return program

    def get_current_point_position(self):
        """
        Get current temperature's (not target!) value point position
        :return:
        """
        logger.info('getting current temperature point position')
        try:
            point_position = self._read_registers(self.registers.current_point_position)[0]
        except ReadRegistersError:
            logger.error('getting device state form buffer')
            point_position = self._current_values_buffer.current_point_position
        return point_position

