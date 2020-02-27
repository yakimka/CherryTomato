from collections import UserString

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSignal

from CherryTomato.settings import STATE_TOMATO, STATE_LONG_BREAK, STATE_BREAK


class State(UserString):
    def __init__(self, seq: object, time: int):
        self.time = time
        super().__init__(seq)


class TomatoTimer(QObject):
    stateChanged = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.tickTime = 64  # ms

        self.reset()

    def reset(self):
        self.tomatoes = 0
        self.stateName = None
        self.maxSeconds = None

        self.createTimer()
        self.changeState()
        self.notifyAboutAnyChange()

    def createTimer(self):
        if hasattr(self, 'timer'):
            self.timer.timeout.disconnect()
        self.timer = Qt.QTimer()
        self.timer.setInterval(self.tickTime)
        self.timer.timeout.connect(self.tick)

    def changeState(self):
        if self.state is None:
            self._states = self._statesGen()

        self.stateName = next(self._states)
        self.seconds = self.state.time

    @property
    def state(self):
        if self.stateName is None:
            return None

        time = getattr(self.settings, self.stateName)
        return State(self.stateName, time)

    def _statesGen(self):
        while True:
            yield STATE_TOMATO
            yield STATE_LONG_BREAK if self._isTimeForLongBreak() else STATE_BREAK

    def _isTimeForLongBreak(self):
        if self.tomatoes == 0:
            return False
        return self.isTomato() and (self.tomatoes % self.settings.repeat == 0)

    def isTomato(self):
        return self.state == STATE_TOMATO

    def notifyAboutAnyChange(self):
        self.stateChanged.emit()

    @property
    def running(self):
        return self.timer.isActive()

    @property
    def seconds(self):
        return max(0, getattr(self, '_seconds', 0))

    @seconds.setter
    def seconds(self, val):
        self._seconds = val
        self.maxSeconds = val

    @property
    def progress(self):
        return int(100 - (self.seconds / self.state.time * 100))

    @Qt.pyqtSlot(name='tick')
    def tick(self):
        self.applyTick()

        if self.seconds <= 0:
            if self.isTomato():
                self.tomatoes += 1
            self.changeState()
            if self._isNeedAutoStop():
                self.stop()
            self.notifyTimerIsOver()
        self.notifyAboutAnyChange()

    def applyTick(self):
        self._seconds -= self.tickTime / 1000

    def _isNeedAutoStop(self):
        if self.isTomato() and self.settings.autoStopTomato:
            return True
        elif not self.isTomato() and self.settings.autoStopBreak:
            return True
        return False

    def stop(self):
        self.timer.stop()

    def notifyTimerIsOver(self):
        self.finished.emit()

    def start(self):
        self.timer.start()

    def abort(self):
        self.stop()
        if not self.isTomato() and self.settings.switchToTomatoOnAbort:
            self.changeState()
        else:
            self.resetTime()
        self.notifyAboutAnyChange()

    def onSettingsChange(self):
        if self.state.time != self.maxSeconds:
            self.resetTime()
            self.notifyAboutAnyChange()

    def resetTime(self):
        self.seconds = self.state.time
