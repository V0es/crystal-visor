from abc import ABC, abstractmethod

from pymodbus.client import ModbusSerialClient
from pymodbus import (
    ExceptionResponse,
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

class BaseModbusDevice(ABC):

    def __init__(self):
        self.modbus_client = None

    def _read_value(self, address: int, count: int, slave_id: int):
        """
        0x03
        :param address:
        :param count:
        :param slave_id:
        :return:
        """
        ...

    def _write_bool(self, address: int, value: bool, slave_id: int):
        """
        0x05
        :return:
        """
        ...

    def _write_value(self, address: int, value: bytes, slave_id: int):
        """
        0x06
        :return:
        """
        ...

    def _write_values(self, address: int, values: List[bytes], slave_id: int):
        """
        0x10
        :return:
        """
        ...
