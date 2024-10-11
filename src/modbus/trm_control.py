from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from pymodbus.client import ModbusSerialClient

from src.modbus.dataframes.device_values import DeviceValues
from src.modbus.dataframes.temperature_program import TemperatureProgram
from src.modbus.dataframes.modbus_params import ModbusParams


class TRM(QObject):
    device_connected = pyqtSignal(bool)
    temperature_program_updated = pyqtSignal()

    device_values_ready = pyqtSignal(DeviceValues)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.modbus_client: ModbusSerialClient | None = None
        self.device_params: ModbusParams | None = None

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
        print('trying to connect modbus')
        state = self.modbus_client.connect()
        self.device_connected.emit(state)

    @pyqtSlot(float)
    def adjust_temperature(self, delta_temp: float):
        print('auto adjusting')
        program = self._get_current_temperature_program()
        program.target_temperature += delta_temp
        self.set_new_temperature_program(program)

    @pyqtSlot(TemperatureProgram)
    def set_new_temperature_program(self, temperature: TemperatureProgram):
        print('set new program')
        if not self.modbus_client or not self.modbus_client.connected:
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
        registers = self.modbus_client.read_input_registers(
            257,
            4,
            self.device_params.slave_id
        ).registers

        program = TemperatureProgram(
            target_temperature=registers[0],
            point_position=registers[1],
            raising_time=registers[2],
            holding_time=registers[3]
        )
        return program

    @pyqtSlot()
    def get_current_values(self):
        print('getting device values')
        if not self.modbus_client or not self.modbus_client.connected:
            return
        device_state = self.modbus_client.read_input_registers(
            17,
            1,
            self.device_params.slave_id).registers[0]

        current_temperature = self.modbus_client.read_input_registers(
            2,
            1,
            self.device_params.slave_id).registers[0]
        current_program = self._get_current_temperature_program()

        device_values = DeviceValues(device_state, current_program, current_temperature)

        self.device_values_ready.emit(device_values)

    def set_running_state(self, running_state: bool):
        print('setting running state')
        self.modbus_client.write_coil(80, running_state, self.device_params.slave_id)
