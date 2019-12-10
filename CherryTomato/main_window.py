import os

from PyQt5 import Qt, QtCore
from PyQt5.QtCore import QSettings, QSize, QPoint
from PyQt5.QtGui import QBrush, QColor, QPalette, QIcon
from PyQt5.QtMultimedia import QSound

from CherryTomato import about, APP_ICON, MEDIA_DIR
from CherryTomato.main_ui import Ui_MainWindow
from CherryTomato.tomato_timer import TomatoTimer


class TomatoTimerWindow(Qt.QMainWindow, Ui_MainWindow):
    APP_TITLE = 'CherryTomato'
    NOTIFICATION_ON = True

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.setWindowIcon(QIcon(APP_ICON))

        self.settings = QSettings('yakimka', self.APP_TITLE)
        # Initial window size/pos last saved. Use default values for first time
        self.resize(self.settings.value('size', QSize(400, 520)))
        self.move(self.settings.value('pos', QPoint(50, 50)))

        self.tomatoTimer = TomatoTimer()

        self.button.clicked.connect(self.do_start)
        self.tomatoTimer.stateChanged.connect(self.display)
        self.tomatoTimer.finished.connect(self.setFocusOnWindowAndPlayNotification)

        self.display()

        self.aboutWindow = about.About()
        self.actionAbout.triggered.connect(self.showAboutWindow)

    def showAboutWindow(self):
        centerX, centerY = self.getCenterPoint()
        x = int(centerX - self.aboutWindow.width() / 2)
        y = int(centerY - self.aboutWindow.height() / 2)
        self.aboutWindow.move(x, y)
        self.aboutWindow.show()

    def getCenterPoint(self):
        x = int(self.x() + self.width() / 2)
        y = int(self.y() + self.height() / 2)

        return x, y

    def closeEvent(self, e):
        # Write window size and position to config file
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())

        e.accept()

    @Qt.pyqtSlot()
    def display(self):
        TOMATO_SIGN = '˙'
        minutes, seconds = int(self.tomatoTimer.seconds // 60), int(self.tomatoTimer.seconds % 60)
        display = f'\n{minutes:02d}:{seconds:02d}\n{TOMATO_SIGN * self.tomatoTimer.tomatoes}'
        self.progress.setFormat(display)
        self.progress.setValue(self.tomatoTimer.progress)
        self.changeButtonState()

        if self.tomatoTimer.isTomato():
            self.setRed()
        else:
            self.setGreen()

    @Qt.pyqtSlot()
    def do_start(self):
        # trigger through proxy
        self.tomatoTimer.start()

    @Qt.pyqtSlot()
    def do_stop(self):
        # trigger through proxy
        self.tomatoTimer.abort()

    def changeButtonState(self):
        if not self.tomatoTimer.running:
            self.button.setImage('play.png')
            self.button.clicked.disconnect()
            self.button.clicked.connect(self.do_start)
        else:
            self.button.setImage('stop.png')
            self.button.clicked.disconnect()
            self.button.clicked.connect(self.do_stop)

    def setRed(self):
        # https://coolors.co/eff0f1-d11f2a-8da1b9-95adb6-fad0cf
        lightRed = (249, 192, 191)
        red = (255, 37, 51)
        self.setColor(lightRed, red)

    def setColor(self, base: tuple, highlight: tuple):
        base_brush = QBrush(QColor(*base))
        base_brush.setStyle(QtCore.Qt.SolidPattern)
        highlight_brush = QBrush(QColor(*highlight))
        highlight_brush.setStyle(QtCore.Qt.SolidPattern)

        palette = QPalette()
        palette.setBrush(QPalette.Active, QPalette.Base, base_brush)
        palette.setBrush(QPalette.Active, QPalette.Highlight, highlight_brush)

        palette.setBrush(QPalette.Inactive, QPalette.Base, base_brush)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, highlight_brush)

        palette.setBrush(QPalette.Text, highlight_brush)

        self.progress.setPalette(palette)

        self.button.setColor(highlight)

    def setGreen(self):
        # https://coolors.co/b5ffe1-3cbb6f-b0ecc1-4e878c-00241b
        lightGreen = (176, 236, 193)
        green = (60, 187, 111)
        self.setColor(lightGreen, green)

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    @Qt.pyqtSlot()
    def setFocusOnWindowAndPlayNotification(self):
        self.raise_()
        self.show()
        self.activateWindow()
        if self.windowState() == QtCore.Qt.WindowMinimized:
            # Window is minimised. Restore it.
            self.setWindowState(QtCore.Qt.WindowNoState)

        if self.NOTIFICATION_ON:
            QSound.play(os.path.join(MEDIA_DIR, 'sound.wav'))
