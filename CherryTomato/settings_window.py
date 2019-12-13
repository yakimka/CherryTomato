from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from CherryTomato import APP_ICON
from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.settings_ui import Ui_Settings


settings = CherryTomatoSettings()

class Settings(QtWidgets.QWidget, Ui_Settings):
    closing = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setWindowIcon(QIcon(APP_ICON))

        state_tomato = settings.stateTomato
        self.stateTomato.setValue(int(state_tomato.time / 60))
        state_break = settings.stateBreak
        self.stateBreak.setValue(int(state_break.time / 60))
        state_long_break = settings.stateLongBreak
        self.stateLongBreak.setValue(int(state_long_break.time / 60))
        self.repeat.setValue(settings.repeat)

        self.notification.setChecked(settings.notification)
        self.interrupt.setChecked(settings.interrupt)
        self.autoStopTomato.setChecked(settings.autoStopTomato)
        self.autoStopBreak.setChecked(settings.autoStopBreak)
        self.switchToTomatoOnAbort.setChecked(settings.switchToTomatoOnAbort)

    def closeEvent(self, e):
        e.accept()
        self.updateSettings()
        self.closing.emit()

    def updateSettings(self):
        settings.stateTomato = self.stateTomato.value() * 60
        settings.stateBreak = self.stateBreak.value() * 60
        settings.stateLongBreak = self.stateLongBreak.value() * 60
        settings.repeat = self.repeat.value()

        settings.notification = self.notification.isChecked()
        settings.interrupt = self.interrupt.isChecked()
        settings.autoStopTomato = self.autoStopTomato.isChecked()
        settings.autoStopBreak = self.autoStopBreak.isChecked()
        settings.switchToTomatoOnAbort = self.switchToTomatoOnAbort.isChecked()
