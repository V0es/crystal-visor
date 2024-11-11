import random
import logging
from typing import List

from src.modbus import TRM
from src.modbus.exceptions import ReadRegistersError
from src.modbus.utils.dataframes import ModbusParams, TemperatureProgram, DeviceValues

logger = logging.getLogger(__name__)


class TrmMock(TRM):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.registers = {
            2: 0.0,
            17: 0,
            257: 0,
            258: 0,
            259: 0,
            260: 0
        }
        self.current_values_buffer: DeviceValues = DeviceValues()
        self.current_temperature_program_buffer: TemperatureProgram = TemperatureProgram()

    def _init_device(self, modbus_params: ModbusParams):
        logger.info('CREATED MODBUS_CLIENT INSTANCE')
        self.device_params = modbus_params

    def connect_device(self, modbus_params: ModbusParams):
        self._init_device(modbus_params)
        logger.info('TRYING TO CONNECT MODBUS')
        self.device_connected.emit(True)

    def adjust_temperature(self, delta_temp: float):
        program = self.get_current_temperature_program()
        logger.info('ADJUSTING TEMPERATURE PROGRAM')
        program.target_temperature += delta_temp
        self.set_new_temperature_program(program)

    def set_new_temperature_program(self, temperature: TemperatureProgram):
        logger.info('SETTING NEW PROGRAM')
        self.registers[257] = temperature.target_temperature
        self.registers[258] = temperature.point_position
        self.registers[259] = temperature.raising_time
        self.registers[260] = temperature.holding_time

        self.set_running_state(True)
        self.temperature_program_updated.emit()

    def get_current_temperature_program(self) -> TemperatureProgram:
        logger.info('GETTING CURRENT TEMPERATURE PROGRAM')
        try:
            registers = self._read_registers(257, 4, self.device_params.slave_id)
            program = TemperatureProgram(*registers)

        except TypeError:
            logger.error('GETTING TEMPERATURE PROGRAM FROM BUFFER')
            program = self.current_values_buffer.current_program

        return program

    def get_current_values(self):
        logger.info('GETTING DEVICE VALUES')
        self.registers[2] = random.randint(1500, 5000) / 100
        current_operating_mode = self.get_current_operation_mode()
        current_temperature = self.get_current_temperature()
        current_program = self.get_current_temperature_program()

        device_values = DeviceValues(current_operating_mode, current_program, int(current_temperature))
        self.current_values_buffer = device_values  # update buffer

        self.device_values_ready.emit(device_values)

    def set_running_state(self, running_state: bool):
        logger.info(f'SETTING RUNNING STATE: {running_state}')
        if running_state:
            self.registers[17] = 1
        else:
            self.registers[17] = 0

    def _read_registers(self, address: int, count: int, slave_id: int) -> List[int] | None:
        regs = [self.registers[address + i] for i in range(count)]

        return regs if random.random() > 0.1 else self.read_registers_error.emit()

    def get_current_temperature(self) -> float | None:
        logger.info('GETTING CURRENT TEMPERATURE')
        try:
            current_temperature = self._read_registers(2, 1, self.device_params.slave_id)[0]
        except TypeError:
            logger.error('GETTING CURRENT TEMPERATURE FROM BUFFER')
            current_temperature = self.current_values_buffer.current_temperature
        return current_temperature

    def get_current_operation_mode(self) -> int:
        logger.info('GETTING DEVICE STATE')
        try:
            mode = self._read_registers(17, 1, self.device_params.slave_id)[0]
        except TypeError:
            logger.error('GETTING DEVICE STATE FORM BUFFER')
            mode = self.current_values_buffer.current_operating_mode
        return mode
