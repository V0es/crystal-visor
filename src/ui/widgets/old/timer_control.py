from PyQt6.QtCore import QTimer, pyqtSlot, QTime
from PyQt6.QtWidgets import QWidget

from src.ui.widgets.old.timer_control import Ui_TimerControl


class TimerControl(QWidget, Ui_TimerControl):
    def __init__(self, parent=None):
        super(TimerControl, self).__init__(parent)

        # uic.loadUi('ui/widgets/timer_control.ui', self)
        self.setupUi(self)

        self.timer = QTimer(self)
        self.current_time = QTime(0, 0, 0)
        self.timer.setInterval(1000)

        self.connect_signals()

    def connect_signals(self):
        self.timer.timeout.connect(self.update_time)
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.stop_btn.clicked.connect(self.stop_timer)

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
        self.time_label.setText(self.current_time.toString('hh:mm:ss'))

    @pyqtSlot()
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.current_time.setHMS(0, 0, 0)
        self.time_label.setText(self.current_time.toString('hh:mm:ss'))

        print('stopped')
