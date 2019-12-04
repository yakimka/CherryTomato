import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton

from CherryTomato import MEDIA_DIR
from qroundprogressbar import QRoundProgressBar as QRoundProgressBar_


class QRoundPushbutton(QPushButton):
    stylesheet = '''
        background-color: rgb{color};
        background-image: url("{image}");
        border: 1px solid rgb{color};
        border-radius: 20px;
        '''

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(40, 40)
        self.setFlat(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.color = (255, 37, 51)
        self.image = os.path.join(MEDIA_DIR, 'play.png')
        self.applyStyleSheet()

    def setColor(self, rgb: tuple):
        self.color = rgb
        self.applyStyleSheet()

    def setImage(self, image: str):
        self.image = os.path.join(MEDIA_DIR, image)
        self.applyStyleSheet()

    def applyStyleSheet(self):
        self.setStyleSheet(self.stylesheet.format(color=self.color, image=self.image))


class QRoundProgressBar(QRoundProgressBar_):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFormat('')
        self.setValue(0)
        self.setBarStyle(QRoundProgressBar.BarStyle.LINE)
        self.setOutlinePenWidth(6)
        self.setDataPenWidth(6)

    def resizeEvent(self, e):
        self.setMaximumWidth(self.height())
