import random
import logging

from src.modbus import TRM
from src.modbus.dataframes import ModbusParams, TemperatureProgram, DeviceValues

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

    def _init_device(self, modbus_params: ModbusParams):
        logger.info('CREATED MODBUS_CLIENT INSTANCE')
        self.device_params = modbus_params

    def connect_device(self, modbus_params: ModbusParams):
        self._init_device(modbus_params)
        logger.info('TRYING TO CONNECT MODBUS')
        self.device_connected.emit(True)

    def adjust_temperature(self, delta_temp: float):
        program = self._get_current_temperature_program()
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

    def _get_current_temperature_program(self) -> TemperatureProgram:
        logger.info('GETTING CURRENT TEMP PROGRAM')
        program = TemperatureProgram(
            target_temperature=self.registers[257],
            point_position=self.registers[258],
            raising_time=self.registers[259],
            holding_time=self.registers[260]
        )
        return program

    def get_current_values(self):
        logger.info('GETTING DEVICE VALUES')
        self.registers[2] = random.randint(1500, 5000) / 100
        device_state = self.registers[17]
        current_temp = self.registers[2]
        current_program = self._get_current_temperature_program()

        device_values = DeviceValues(device_state, current_program, current_temp)

        self.device_values_ready.emit(device_values)

    def set_running_state(self, running_state: bool):
        logger.info(f'SETTING RUNNING STATE: {running_state}')
        if running_state:
            self.registers[17] = 1
        else:
            self.registers[17] = 0
