import logging
import os.path
from dataclasses import dataclass
from os import PathLike
from bisect import bisect_left

from PyQt6.QtCore import QTime

from src.core.math.interpolation import InterpolationType

logger = logging.getLogger(__name__)


@dataclass
class TimeFrame:
    time: QTime
    height: float

    def __lt__(self, other):
        if isinstance(other, QTime):
            return self.time < other
        return self.time < other.time

    def __gt__(self, other):
        if isinstance(other, QTime):
            return self.time > other
        return self.time > other.time

    def __eq__(self, other):
        if isinstance(other, QTime):
            return self.time == other
        return self.time == other.time

    def __le__(self, other):
        if isinstance(other, QTime):
            return self.time < other or self.time == other
        return self.time < other.time or self.time == other.time

    def __ge__(self, other):
        if isinstance(other, QTime):
            return self.time > other or self.time == other
        return self.time > other.time or self.time == other.time


class TimeTable:
    def __init__(self,
                 filepath: str | PathLike = None,
                 interpolation_type: int = InterpolationType.LINEAR):
        self._filepath = filepath
        self._timeframes = []
        self.interpolation_type = interpolation_type

    def awaited_height(self, time: QTime) -> float:
        left_frame, right_frame = self._find_neighbours(time)
        awaited_height = self._interpolate_frames(left_frame, right_frame, time)
        logger.info(f'awaited height at {time} : {awaited_height}')
        return awaited_height

    @staticmethod
    def _interpolate_frames(left: TimeFrame, right: TimeFrame, current_time: QTime) -> float:
        """
        Find value of interpolating function at current_time
        :param left: left point
        :param right: right point
        :param current_time: time to count value at
        :return: interpolated function value
        """
        # TODO: make better timedelta counting
        ctime = current_time.msecsSinceStartOfDay()
        left_time = left.time.msecsSinceStartOfDay()
        right_time = right.time.msecsSinceStartOfDay()

        value = left.height + ((right.height - left.height) / (right_time - left_time)) * (ctime - left_time)
        return value

    def set_file(self, path: str | PathLike) -> None:
        """
        Open file
        :param path: path to timetable file
        :return: None
        """
        if not path or not os.path.exists(path):
            return
        self._filepath = path
        with open(path, 'r', encoding='utf-8') as time_file:
            lines = time_file.readlines()
            for line in lines:
                timeframe = self._line_to_timeframe(line)
                self._timeframes.append(timeframe)
        self._timeframes.sort()

    @staticmethod
    def _line_to_timeframe(line: str) -> TimeFrame:
        """
        Parse line to timeframe
        :param line: string from timetable file
        :return: TimeFrame object
        """
        raw_time, height = line.strip().replace(' ', '').split('-')
        hours, minutes, seconds = map(int, raw_time.split(':'))

        time = QTime(hours, minutes, seconds)
        time_frame = TimeFrame(time, float(height))
        return time_frame

    @property
    def filepath(self):
        return self._filepath

    def _find_neighbours(self, time: QTime) -> (TimeFrame, TimeFrame):
        if not self._timeframes[0] <= time <= self._timeframes[-1]:
            # TODO: make exception
            raise Exception
        left_index = bisect_left(self._timeframes, time) - 1
        left_neighbor, right_neighbor = self._timeframes[left_index], self._timeframes[left_index + 1]
        print(left_neighbor, right_neighbor)

        return left_neighbor, right_neighbor
