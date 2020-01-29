from PyQt5 import QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from CherryTomato import APP_ICON
from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.settings_ui import Ui_Settings


class Settings(QtWidgets.QWidget, Ui_Settings):
    closing = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setWindowIcon(QIcon(APP_ICON))
        self.settings = CherryTomatoSettings()

        state_tomato = self.settings.stateTomato
        self.stateTomato.setValue(int(state_tomato.time / 60))
        state_break = self.settings.stateBreak
        self.stateBreak.setValue(int(state_break.time / 60))
        state_long_break = self.settings.stateLongBreak
        self.stateLongBreak.setValue(int(state_long_break.time / 60))
        self.repeat.setValue(self.settings.repeat)

        self.notification.setChecked(self.settings.notification)
        self.interrupt.setChecked(self.settings.interrupt)
        self.autoStopTomato.setChecked(self.settings.autoStopTomato)
        self.autoStopBreak.setChecked(self.settings.autoStopBreak)
        self.switchToTomatoOnAbort.setChecked(self.settings.switchToTomatoOnAbort)

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, e):
        e.accept()
        self.updateSettings()
        self.closing.emit()

    def updateSettings(self):
        self.settings.stateTomato = self.stateTomato.value() * 60
        self.settings.stateBreak = self.stateBreak.value() * 60
        self.settings.stateLongBreak = self.stateLongBreak.value() * 60
        self.settings.repeat = self.repeat.value()

        self.settings.notification = self.notification.isChecked()
        self.settings.interrupt = self.interrupt.isChecked()
        self.settings.autoStopTomato = self.autoStopTomato.isChecked()
        self.settings.autoStopBreak = self.autoStopBreak.isChecked()
        self.settings.switchToTomatoOnAbort = self.switchToTomatoOnAbort.isChecked()
