from dataclasses import dataclass


@dataclass
class ModbusParams:
    serial_port: str
    slave_id: int
    baudrate: int
    bytesize: int
    pairity: str
    stopbits: int
