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
        self.settings = CherryTomatoSettings.createQT()

        self.stateTomato.setValue(int(self.settings.stateTomato / 60))
        self.stateBreak.setValue(int(self.settings.stateBreak / 60))
        self.stateLongBreak.setValue(int(self.settings.stateLongBreak / 60))
        self.repeat.setValue(self.settings.repeat)

        self.notification.setChecked(self.settings.notification)
        self.interrupt.setChecked(self.settings.interrupt)
        self.autoStopTomato.setChecked(self.settings.autoStopTomato)
        self.autoStopBreak.setChecked(self.settings.autoStopBreak)
        self.switchToTomatoOnAbort.setChecked(self.settings.switchToTomatoOnAbort)

        self.afterStartCommand.setText(self.settings.afterStartCommand)
        self.afterStopCommand.setText(self.settings.afterStopCommand)
        self.onTomatoCommand.setText(self.settings.onTomatoCommand)
        self.onBreakCommand.setText(self.settings.onBreakCommand)

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

        self.settings.afterStartCommand = self.afterStartCommand.text()
        self.settings.afterStopCommand = self.afterStopCommand.text()
        self.settings.onTomatoCommand = self.onTomatoCommand.text()
        self.settings.onBreakCommand = self.onBreakCommand.text()
