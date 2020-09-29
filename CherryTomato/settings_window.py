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

        methods = {
            int: 'setValue',
            bool: 'setChecked',
            str: 'setText',
        }
        # Example:
        # self.stateTomato.setValue(self.settings.stateTomato)
        # self.useSystemFont.setChecked(self.settings.useSystemFont)
        # self.afterStartCommand.setText(self.settings.afterStartCommand)
        for opt in self.settings.options:
            if opt.ui:
                value = opt.toRepresentation(getattr(self.settings, opt.name))
                method = getattr(getattr(self, opt.name), methods[opt.type])
                method(value)

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
        methods = {
            int: 'value',
            bool: 'isChecked',
            str: 'text',
        }
        # Example:
        # self.settings.stateTomato = self.stateTomato.value()
        # self.settings.useSystemFont = self.useSystemFont.isChecked()
        # self.settings.afterStartCommand = self.afterStartCommand.text()
        for opt in self.settings.options:
            if opt.ui:
                value = getattr(getattr(self, opt.name), methods[opt.type])()
                setattr(self.settings, opt.name, opt.toInternalValue(value))
