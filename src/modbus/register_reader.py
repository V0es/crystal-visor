import logging
import time
from typing import List

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from pymodbus.client import ModbusSerialClient

from src.modbus.exceptions import ReadRegistersError
from src.modbus.utils.dataframes import DeviceValues, TemperatureProgram

logger = logging.getLogger(__name__)


class RegisterReaderThread(QThread):
    result = pyqtSignal(DeviceValues)

    modbus_connection_lost = pyqtSignal()
    read_registers_error = pyqtSignal()

    def __init__(self, modbus_client: ModbusSerialClient, slave_id: int):
        super().__init__()
        self._is_running = False
        self.modbus = modbus_client
        self.slave_id = slave_id
        self._current_values_buffer = DeviceValues()

    def run(self):
        self._is_running = True
        while self._is_running:

            logger.info('getting device values')

            current_operating_mode = self.get_current_operation_mode()
            print(f'operation mode: address 17 = {current_operating_mode}')
            time.sleep(0.01)

            current_temperature = self.get_current_temperature()
            print(f'current_temperature: address 2 = {current_temperature}')
            time.sleep(0.01)

            current_program = self.get_current_temperature_program()
            print(f'current program: address 256 = {current_program}')
            time.sleep(0.01)

            current_point_position = self.get_current_point_position()
            print(f'current point position: address 0 = {current_point_position}\n')

            device_values = DeviceValues(
                current_operating_mode,
                current_program,
                int(current_temperature),
                current_point_position
            )

            self.result.emit(device_values)
            time.sleep(1)

    @pyqtSlot()
    def stop(self):
        self._is_running = False

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
            mode = self._read_registers(17, 1)[0]

        except ReadRegistersError:
            logger.error('getting device state form buffer')
            mode = self._current_values_buffer.current_operating_mode
        return mode

    def _read_registers(self, address: int, count: int) -> List[int] | None:
        """
        Read 'count' registers starting from 'address' from device with 'slave_id' id
        Raises ReadRegistersError if response is invalid
        :param address: Starting register address
        :param count: Amount of registers to read
        :return: List of registers
        """
        logger.info('reading registers')
        if not self.modbus.connected:
            logger.error('no connection to modbus device')
            self.modbus.connect()
            # self.modbus_connection_lost.emit()

        response = self.modbus.read_input_registers(address, count, self.slave_id)
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
            current_temperature = self._read_registers(2, 1)[0]
            logger.info(f'current temperature: {current_temperature}')
        except ReadRegistersError:
            logger.error('getting current temperature from buffer')
            current_temperature = self._current_values_buffer.current_temperature
        return current_temperature

    def get_current_temperature_program(self):
        """
                Get current temperature program parameters or read from buffer
                :return: TemperatureProgram object composed of fetched parameters
                """
        logger.info('getting current temperature program')
        try:
            registers = self._read_registers(257, 4)
            program = TemperatureProgram(*registers)

            program.target_temperature /= 10**program.point_position

        except ReadRegistersError:
            logger.error('getting temperature program from buffer')
            program = self._current_values_buffer.current_program

        return program

    def get_current_point_position(self):
        logger.info('getting current temperature point position')
        try:
            point_position = self._read_registers(0, 1)[0]
        except ReadRegistersError:
            logger.error('getting device state form buffer')
            point_position = self._current_values_buffer.current_point_position
        return point_position

