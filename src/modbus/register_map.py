from dataclasses import dataclass, field


@dataclass
class Register:
    address: int
    count: int
    function: int


@dataclass
class Coil:
    address: int


@dataclass
class RegisterMap:
    temperature_program: Register = field(default_factory=lambda: Register(257, 4, 4))
    current_temperature: Register = field(default_factory=lambda: Register(2, 1, 4))
    current_point_position: Register = field(default_factory=lambda: Register(0, 1, 4))
    operating_mode: Register = field(default_factory=lambda: Register(17, 1, 4))

    running_state: Coil = field(default_factory=lambda: Coil(80))
