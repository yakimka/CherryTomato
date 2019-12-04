from collections import UserString

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSignal


class State(UserString):
    def __init__(self, seq: object, time: int):
        self.time = time
        super().__init__(seq)


class TomatoTimer(QObject):
    TOMATOS_BEFORE_LONG_BREAK = 4
    AUTO_STOP_TOMATO = True
    AUTO_STOP_BREAK = False
    SWITCH_TO_TOMATO_ON_ABORT = True

    TICK_TIME = 64  # ms
    STATE_TOMATO = State('tomato', 25 * 60)
    STATE_BREAK = State('break', 5 * 60)
    STATE_LONG_BREAK = State('long_break', 20 * 60)

    stateChanged = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.tomatoes = 0
        self.state = None

        self.createTimer()
        self.changeState()

    @property
    def running(self):
        return self.timer.isActive()

    @property
    def seconds(self):
        return max(0, getattr(self, '_seconds', 0))

    @seconds.setter
    def seconds(self, val):
        self._seconds = val

    @property
    def progress(self):
        return int(100 - (self.seconds / self.state.time * 100))

    def start(self):
        self.timer.start()

    def abort(self):
        self.stop()
        if not self.isTomato() and self.SWITCH_TO_TOMATO_ON_ABORT:
            self.changeState()
        else:
            self.reset()
        self.notifyAboutAnyChange()

    def createTimer(self):
        self.timer = Qt.QTimer()
        self.timer.setInterval(self.TICK_TIME)
        self.timer.timeout.connect(self.tick)

    @Qt.pyqtSlot()
    def tick(self):
        self.seconds -= self.TICK_TIME / 1000

        if self.seconds <= 0:
            if self.isTomato():
                self.tomatoes += 1
            self.changeState()
            if self._isNeedAutoStop():
                self.stop()
            self.notifyTimerIsOver()

        self.notifyAboutAnyChange()

    def isTomato(self):
        return self.state == self.STATE_TOMATO

    def _isNeedAutoStop(self):
        if self.isTomato() and self.AUTO_STOP_TOMATO:
            return True
        elif not self.isTomato() and self.AUTO_STOP_BREAK:
            return True
        return False

    def stop(self):
        self.timer.stop()

    def changeState(self):
        if not hasattr(self, '_states'):
            self._states = self._statesGen()

        self.state = next(self._states)
        self.seconds = self.state.time

    def _statesGen(self):
        while True:
            yield self.STATE_TOMATO
            yield self.STATE_LONG_BREAK if self._isTimeForLongBreak() else self.STATE_BREAK

    def _isTimeForLongBreak(self):
        if self.tomatoes == 0:
            return False
        return self.isTomato() and self.tomatoes % self.TOMATOS_BEFORE_LONG_BREAK == 0

    def reset(self):
        self.seconds = self.state.time

    def notifyAboutAnyChange(self):
        self.stateChanged.emit()

    def notifyTimerIsOver(self):
        self.finished.emit()
