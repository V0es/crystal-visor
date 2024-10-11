from dataclasses import dataclass


@dataclass
class TemperatureProgram:
    target_temperature: int
    point_position: int
    raising_time: int
    holding_time: int
