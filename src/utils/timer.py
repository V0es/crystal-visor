from PyQt6.QtCore import QTimer, pyqtSlot, QTime, QObject, pyqtSignal


class TimerControl(QObject):
    timer_updated = pyqtSignal(QTime)
    timer_stopped = pyqtSignal()

    def __init__(self, time_interval: int = 1000, parent=None):

        super().__init__(parent)

        self.timer = QTimer(self)
        self.time_interval = time_interval
        self.current_time = QTime(0, 0, 0)
        self.timer.setInterval(time_interval)

        self.connect_signals()

    def connect_signals(self):
        self.timer.timeout.connect(self.update_time)

    @pyqtSlot()
    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(self.time_interval)
        print('started')

    @pyqtSlot()
    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        print('paused')

    @pyqtSlot()
    def update_time(self):
        self.current_time = self.current_time.addSecs(self.time_interval // 1000)
        self.timer_updated.emit(self.current_time)

    @pyqtSlot()
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.current_time.setHMS(0, 0, 0)

        self.timer_updated.emit(self.current_time)
        self.timer_stopped.emit()

        print('stopped')
