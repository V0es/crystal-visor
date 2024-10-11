# --------------------------------------------------------------------------- #
import time

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)
from pymodbus.transaction import ModbusRtuFramer


def run_sync_simple_client(comm, port, framer=FramerType.RTU):
    """Run sync client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    if comm == "serial":
        client = ModbusClient.ModbusSerialClient(
            port,
            framer=framer,
            timeout=3,
            #retries=3,
            baudrate=19200,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )
    else:
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    client.connect()
    print(client.connected)
    print("get and verify data")

    try:
        valid = []
        for address in range(0, 331):
            resp = client.write_register(address, 2, slave=16)
            if not resp.isError():
                valid.append(address)
            time.sleep(0.1)
        print(valid)

        rr = client.read_input_registers(257, 1, slave=16)
        data = rr.registers[0]
        print('temp = ', data)

    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()

    print("close connection")
    client.close()


if __name__ == "__main__":
    run_sync_simple_client("serial", "COM3")
