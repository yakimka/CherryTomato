from PyQt5 import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from CherryTomato import APP_ICON, __version__ as VERSION
from CherryTomato.about_ui import Ui_About


class About(QtWidgets.QWidget, Ui_About):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        title = f'{self.labelTitle.text()} {VERSION}'
        self.labelTitle.setText(title)

        self.setWindowIcon(QIcon(APP_ICON))

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
