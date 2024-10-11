import enum
from dataclasses import dataclass

from .temperature_program import TemperatureProgram


@dataclass
class DeviceValues:
    current_device_state: int
    current_program: TemperatureProgram = None
    current_temperature: int = 0
    current_point_position: int = 0
