from collections import UserString, namedtuple

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSignal

from CherryTomato.settings import STATE_TOMATO, STATE_LONG_BREAK, STATE_BREAK


class State(UserString):
    def __init__(self, seq: object, time: int):
        self.time = time
        super().__init__(seq)


TimerStatus = namedtuple('TimerStatus', 'tomatoes state')


class TomatoTimer(QObject):
    onStart = pyqtSignal(TimerStatus)
    onStop = pyqtSignal(TimerStatus)
    onStateChange = pyqtSignal(TimerStatus)
    onChange = pyqtSignal(TimerStatus)
    finished = pyqtSignal(TimerStatus)

    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.tickTime = 64  # ms

        self.reset()

    def getStatus(self):
        return TimerStatus(self.tomatoes, self.state)

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
        self.notifyOnStateChange()

    def notifyOnStateChange(self):
        self.onStateChange.emit(self.getStatus())

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
        self.onChange.emit(self.getStatus())

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
        self.notifyOnStop()

    def notifyOnStop(self):
        self.onStop.emit(self.getStatus())

    def notifyTimerIsOver(self):
        self.finished.emit(self.getStatus())

    def start(self):
        self.timer.start()
        self.notifyOnStart()

    def notifyOnStart(self):
        self.onStart.emit(self.getStatus())

    def abort(self):
        if not self.isTomato() and self.settings.switchToTomatoOnAbort:
            self.changeState()
        self.stop()
        self.resetTime()
        self.notifyAboutAnyChange()

    def onSettingsChange(self):
        if self.state.time != self.maxSeconds:
            self.resetTime()
            self.notifyAboutAnyChange()

    def resetTime(self):
        self.seconds = self.state.time
