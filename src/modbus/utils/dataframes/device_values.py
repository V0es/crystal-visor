import enum
from dataclasses import dataclass, field

from .temperature_program import TemperatureProgram
from ..enums import OperatingMode


@dataclass
class DeviceValues:
    current_operating_mode: int = OperatingMode.STOP
    current_program: TemperatureProgram = field(default_factory=lambda: TemperatureProgram())
    current_temperature: int = 0
    current_point_position: int = 0
