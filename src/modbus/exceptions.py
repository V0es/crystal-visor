class ModbusBaseException(Exception):
    pass


class ModbusConnectionLost(ModbusBaseException):
    pass


class ReadRegistersError(ModbusBaseException):
    pass