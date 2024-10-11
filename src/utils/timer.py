from PyQt6.QtCore import QTimer, pyqtSlot, QTime, QObject, pyqtSignal


class TimerControl(QObject):
    timer_updated = pyqtSignal(QTime)
    timer_stopped = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.timer = QTimer(self)
        self.current_time = QTime(0, 0, 0)
        self.timer.setInterval(1000)

        self.connect_signals()

    def connect_signals(self):
        self.timer.timeout.connect(self.update_time)

    @pyqtSlot()
    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
        print('started')

    @pyqtSlot()
    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        print('paused')

    @pyqtSlot()
    def update_time(self):
        self.current_time = self.current_time.addSecs(1)
        self.timer_updated.emit(self.current_time)

    @pyqtSlot()
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.current_time.setHMS(0, 0, 0)

        self.timer_updated.emit(self.current_time)
        self.timer_stopped.emit()

        print('stopped')
