import os
from functools import lru_cache
from warnings import warn

from PyQt5 import Qt, QtCore
from PyQt5.QtGui import QBrush, QColor, QPalette, QIcon, QKeySequence
from PyQt5.QtMultimedia import QSound

from CherryTomato import about_window, APP_ICON, MEDIA_DIR, settings_window
from CherryTomato.main_ui import Ui_MainWindow
from CherryTomato.timer_proxy import AbstractTimerProxy


class CherryTomatoMainWindow(Qt.QMainWindow, Ui_MainWindow):
    def __init__(self, timerProxy: AbstractTimerProxy, settings, parent=None):
        super().__init__(parent=parent)
        self.settings = settings

        self.setupUi(self)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowSizeAndPosition()

        self.timerProxy = timerProxy

        self.button.clicked.connect(self.timerProxy.onAction)
        self.timerProxy.onChange.connect(self.display)
        self.timerProxy.finished.connect(self.setFocusOnWindowAndPlayNotification)

        self.display()

        self.aboutWindow = about_window.About()
        self.actionAbout.triggered.connect(self.showAboutWindow)
        self.settingsWindow = settings_window.Settings()
        self.actionSettings.triggered.connect(self.showSettingsWindow)
        self.settingsWindow.closing.connect(self.timerProxy.onSettingsChange)

        self.actionReset.setShortcut(QKeySequence('Ctrl+R'))
        self.actionReset.triggered.connect(self.timerProxy.reset)

    def setWindowSizeAndPosition(self):
        # Initial window size/pos last saved. Use default values for first time
        for _ in range(3):
            try:
                self.resize(self.settings.size)
                self.move(self.settings.position)
            except TypeError:
                del self.settings.size
                del self.settings.position
                continue
            else:
                break
        else:
            warn(UserWarning("Can't restore window settings"))

    def closeEvent(self, e):
        self.saveWindowSizeAndPosition()
        e.accept()

    def saveWindowSizeAndPosition(self):
        self.settings.size = self.size()
        self.settings.position = self.pos()

    def showAboutWindow(self):
        x, y = self.getWindowCenterPoint(self.aboutWindow)
        self.aboutWindow.move(x, y)
        self.aboutWindow.show()

    def showSettingsWindow(self):
        x, y = self.getWindowCenterPoint(self.settingsWindow)
        self.settingsWindow.move(x, y)
        self.settingsWindow.show()

    def getWindowCenterPoint(self, window):
        x = int(self.x() + self.width() / 2)
        y = int(self.y() + self.height() / 2)

        centerX = int(x - window.width() / 2)
        centerY = int(y - window.height() / 2)

        return centerX, centerY

    @Qt.pyqtSlot(name='display')
    def display(self):
        self.progress.setFormat(self.timerProxy.getUpperText())
        self.progress.setSecondFormat(self.timerProxy.getBottomText())
        self.progress.setValue(self.timerProxy.getProgress())
        self.changeButtonState()
        self.setColor(*self.timerProxy.getColorPalette())

    def changeButtonState(self):
        if not self.timerProxy.isRunning():
            self.button.setImage('play.png')
        else:
            self.button.setImage('stop.png')

    @lru_cache(maxsize=1)
    def setColor(self, base: tuple, highlight: tuple):
        base_brush = QBrush(QColor(*base))
        base_brush.setStyle(QtCore.Qt.SolidPattern)
        highlight_brush = QBrush(QColor(*highlight))
        highlight_brush.setStyle(QtCore.Qt.SolidPattern)

        palette = QPalette()
        palette.setBrush(QPalette.Active, QPalette.Base, base_brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, base_brush)
        palette.setBrush(QPalette.Active, QPalette.Highlight, highlight_brush)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, highlight_brush)
        palette.setBrush(QPalette.Text, highlight_brush)

        self.progress.setPalette(palette)
        self.button.setColor(highlight)

    @Qt.pyqtSlot(name='setFocusOnWindowAndPlayNotification')
    def setFocusOnWindowAndPlayNotification(self):
        if self.settings.interrupt:
            self.raise_()
            self.show()
            self.activateWindow()
            if self.windowState() == QtCore.Qt.WindowMinimized:
                # Window is minimised. Restore it.
                self.setWindowState(QtCore.Qt.WindowNoState)

        if self.settings.notification:
            QSound.play(os.path.join(MEDIA_DIR, 'sound.wav'))
