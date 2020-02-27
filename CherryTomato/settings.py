from PyQt5.QtCore import QSettings, QSize, QPoint

STATE_TOMATO = 'stateTomato'
STATE_BREAK = 'stateBreak'
STATE_LONG_BREAK = 'stateLongBreak'


class Option:
    def __init__(self, name, default, type=None, deleter=False):
        self.name = name
        self.default = default
        self.type = type
        self.deleter = deleter

    def getTypeKwarg(self):
        kwargs = {}
        if self.type is not None:
            kwargs['type'] = self.type

        return kwargs


class CherryTomatoSettings:
    options = [
        Option(STATE_TOMATO, 25 * 60, int),
        Option(STATE_BREAK, 5 * 60, int),
        Option(STATE_LONG_BREAK, 15 * 60, int),

        Option('size', QSize(400, 520), deleter=True),
        Option('position', QPoint(50, 50), deleter=True),
        Option('notification', True, bool),
        Option('interrupt', True, bool),
        Option('repeat', 4, int),
        Option('autoStopTomato', True, bool),
        Option('autoStopBreak', False, bool),
        Option('switchToTomatoOnAbort', True, bool),

        Option('afterStartCommand', '', str),
        Option('afterStopCommand', '', str),
    ]

    def __init__(self, settingsBackend):
        self.settingsBackend = settingsBackend

    @classmethod
    def createQT(cls):
        settingsBackend = QSettings()
        return cls(settingsBackend)

    def __getattr__(self, item):
        opt = self._findOption(item)
        if opt:
            return self.settingsBackend.value(opt.name, opt.default, **opt.getTypeKwarg())
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}")

    def _findOption(self, name):
        return next((opt for opt in self.options if opt.name == name), None)

    def __setattr__(self, key, value):
        opt = self._findOption(key)
        if opt:
            self.settingsBackend.setValue(opt.name, value)
        else:
            super().__setattr__(key, value)

    def __delattr__(self, item):
        opt = self._findOption(item)
        if opt and opt.deleter:
            self.settingsBackend.remove(opt.name)
        else:
            super().__delattr__(item)
