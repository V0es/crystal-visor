import sys
import glob
from typing import List
import logging
import serial
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal

logger = logging.getLogger(__name__)


class WorkerSignals(QObject):
    available_ports_ready = pyqtSignal(list)


class SerialPortWorker(QRunnable):
    def __init__(self):
        self.signals = WorkerSignals()
        super().__init__()

    def run(self):
        """ Lists serial port names

                :raises EnvironmentError:
                    On unsupported or unknown platforms
                :returns:
                    A list of the serial ports available on the system
            """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        available_ports = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                available_ports.append(port)
            except (OSError, serial.SerialException):
                pass
        self.signals.available_ports_ready.emit(available_ports)
