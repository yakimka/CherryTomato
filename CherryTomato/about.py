from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from CherryTomato import APP_ICON
from .about_ui import Ui_About


class About(QtWidgets.QWidget, Ui_About):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setWindowIcon(QIcon(APP_ICON))
