import datetime
import logging
import time

from PyQt6.QtCore import QTimer, pyqtSlot, QTime, QObject, pyqtSignal

logger = logging.getLogger(__name__)


class Time:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def add_hrs(self, hrs):
        self.hours += hrs

    def add_mins(self, mins: int):
        self.minutes += mins
        if self.minutes >= 60:
            self.add_hrs(self.minutes // 60)
            self.minutes %= 60

    def add_secs(self, secs: int):
        self.seconds += secs
        if self.seconds >= 60:
            self.add_mins(self.seconds // 60)
            self.seconds %= 60
        return self

    def set_time(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __repr__(self):
        hours_str = str(self.hours)
        minutes_str = str(self.minutes)
        seconds_str = str(self.seconds)

        if len(hours_str) == 1:
            hours_str = '0' + hours_str

        if len(minutes_str) == 1:
            minutes_str = '0' + minutes_str

        if len(seconds_str) == 1:
            seconds_str = '0' + seconds_str

        return f'{hours_str}:{minutes_str}:{seconds_str}'


class TimerControl(QObject):
    timer_updated = pyqtSignal(Time)
    timer_stopped = pyqtSignal()

    def __init__(self, time_interval: int = 1000, parent=None):

        super().__init__(parent)
        self.start_time = None

        self.timer = QTimer(self)
        self.time_interval = time_interval
        self.current_time = Time()
        self.timer.setInterval(int(time_interval / 1000))

        self.connect_signals()

    def connect_signals(self):
        self.timer.timeout.connect(self.update_time)

    @pyqtSlot()
    def start_timer(self):
        self.start_time = time.time()
        if not self.timer.isActive():
            self.timer.start(self.time_interval)

        logger.info('timer started')

    @pyqtSlot()
    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        logger.info('paused')

    @pyqtSlot()
    def update_time(self):
        self.current_time.add_secs(int(self.time_interval / 1000))
        self.timer_updated.emit(self.current_time)

    @pyqtSlot()
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.current_time.set_time(0, 0, 0)

        self.timer_updated.emit(self.current_time)
        self.timer_stopped.emit()

        logger.info('timer stopped')

    def set_interval(self, new_interval_msec):
        self.pause_timer()
        self.time_interval = new_interval_msec
        self.start_timer()