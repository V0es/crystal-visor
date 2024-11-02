from dataclasses import dataclass


@dataclass
class TemperatureProgram:
    target_temperature: int = 0
    point_position: int = 0
    raising_time: int = 0
    holding_time: int = 0
