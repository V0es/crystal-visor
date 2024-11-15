from dataclasses import dataclass


@dataclass
class ModbusParams:
    serial_port: str
    slave_id: int
    baudrate: int
    bytesize: int
    pairity: str
    stopbits: int


@dataclass
class PollingSettings:
    modbus_polling_rate: int = 1000
    camera_polling_rate: int = 15000
