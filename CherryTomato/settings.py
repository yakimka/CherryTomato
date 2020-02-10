from collections import UserString

from PyQt5.QtCore import QSettings, QSize, QPoint


class State(UserString):
    def __init__(self, seq: object, time: int):
        self.time = time
        super().__init__(seq)


class CherryTomatoSettings:
    SIZE = 'size'
    SIZE_DEFAULT = QSize(400, 520)
    POSITION = 'position'
    POSITION_DEFAULT = QPoint(50, 50)

    STATE_TOMATO = 'state_tomato'
    TOMATO_DEFAULT = 25 * 60
    STATE_BREAK = 'state_break'
    BREAK_DEFAULT = 5 * 60
    STATE_LONG_BREAK = 'state_long_break'
    LONG_BREAK_DEFAULT = 15 * 60

    NOTIFICATION = 'notification'
    NOTIFICATION_DEFAULT = True
    INTERRUPT = 'interrupt'
    INTERRUPT_DEFAULT = True

    REPEAT = 'repeat'
    REPEAT_DEFAULT = 4
    AUTO_STOP_TOMATO = 'auto_stop_tomato'
    AUTO_STOP_TOMATO_DEFAULT = True
    AUTO_STOP_BREAK = 'auto_stop_break'
    AUTO_STOP_BREAK_DEFAULT = False
    SWITCH_TO_TOMATO_ON_ABORT = 'switch_to_tomato_on_abort'
    SWITCH_TO_TOMATO_ON_ABORT_DEFAULT = True

    def __init__(self):
        self.settings = QSettings()

    @property
    def size(self):
        return self.settings.value(self.SIZE, self.SIZE_DEFAULT)

    @size.setter
    def size(self, val):
        self.settings.setValue(self.SIZE, val)

    @size.deleter
    def size(self):
        self.settings.remove(self.SIZE)

    @property
    def position(self):
        return self.settings.value(self.POSITION, self.POSITION_DEFAULT)

    @position.setter
    def position(self, val):
        self.settings.setValue(self.POSITION, val)

    @position.deleter
    def position(self):
        self.settings.remove(self.POSITION)

    @property
    def notification(self):
        return self.settings.value(self.NOTIFICATION, self.NOTIFICATION_DEFAULT, type=bool)

    @notification.setter
    def notification(self, val):
        self.settings.setValue(self.NOTIFICATION, val)

    @property
    def interrupt(self):
        return self.settings.value(self.INTERRUPT, self.INTERRUPT_DEFAULT, type=bool)

    @interrupt.setter
    def interrupt(self, val):
        self.settings.setValue(self.INTERRUPT, val)

    @property
    def repeat(self):
        return self.settings.value(self.REPEAT, self.REPEAT_DEFAULT, type=int)

    @repeat.setter
    def repeat(self, val):
        self.settings.setValue(self.REPEAT, val)

    @property
    def autoStopTomato(self):
        return self.settings.value(self.AUTO_STOP_TOMATO, self.AUTO_STOP_TOMATO_DEFAULT, type=bool)

    @autoStopTomato.setter
    def autoStopTomato(self, val):
        self.settings.setValue(self.AUTO_STOP_TOMATO, val)

    @property
    def autoStopBreak(self):
        return self.settings.value(self.AUTO_STOP_BREAK, self.AUTO_STOP_BREAK_DEFAULT, type=bool)

    @autoStopBreak.setter
    def autoStopBreak(self, val):
        self.settings.setValue(self.AUTO_STOP_BREAK, val)

    @property
    def switchToTomatoOnAbort(self):
        return self.settings.value(
            self.SWITCH_TO_TOMATO_ON_ABORT, self.SWITCH_TO_TOMATO_ON_ABORT_DEFAULT, type=bool
        )

    @switchToTomatoOnAbort.setter
    def switchToTomatoOnAbort(self, val):
        self.settings.setValue(self.SWITCH_TO_TOMATO_ON_ABORT, val)

    @property
    def stateTomato(self):
        return self.settings.value(self.STATE_TOMATO, State('tomato', self.TOMATO_DEFAULT))

    @stateTomato.setter
    def stateTomato(self, min):
        state = self.stateTomato
        state.time = min
        self.settings.setValue(self.STATE_TOMATO, state)

    @property
    def stateBreak(self):
        return self.settings.value(self.STATE_BREAK, State('break', self.BREAK_DEFAULT))

    @stateBreak.setter
    def stateBreak(self, min):
        state = self.stateBreak
        state.time = min
        self.settings.setValue(self.STATE_BREAK, state)

    @property
    def stateLongBreak(self):
        return self.settings.value(
            self.STATE_LONG_BREAK, State('long_break', self.LONG_BREAK_DEFAULT)
        )

    @stateLongBreak.setter
    def stateLongBreak(self, min):
        state = self.stateLongBreak
        state.time = min
        self.settings.setValue(self.STATE_LONG_BREAK, state)
