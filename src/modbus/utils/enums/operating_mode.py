from enum import Enum


class OperatingMode(Enum):
    STOP = 0
    RUNNING = 1
    CRITICAL_ERROR = 2
    PROGRAM_ENDED = 3
    PID_AUTOTUNING = 4
    WAITING_FOR_PID_AUTOTUNING = 5
    PID_AUTOTUNING_ENDED = 6
    SETTING = 7
