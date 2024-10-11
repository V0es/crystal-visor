import serial

with serial.Serial('COM3', 19200, timeout=1) as ser:
    print(ser.isOpen())
    x = ser.read()          # read one byte
    print(x)
    s = ser.write(b'10')        # read up to ten bytes (timeout)
    print(s)
    line = ser.readline()   # read a '\n' terminated line
