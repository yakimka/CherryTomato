import os
from functools import lru_cache

from PyQt6 import QtCore
from PyQt6.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt6.QtGui import QBrush, QColor, QPalette, QIcon, QKeySequence
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QMainWindow

from CherryTomato import about_window, APP_ICON, MEDIA_DIR, settings_window
from CherryTomato.main_ui import Ui_MainWindow
from CherryTomato.timer_proxy import AbstractTimerProxy
from CherryTomato.utils import classLogger

class CherryTomatoMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, timerProxy: AbstractTimerProxy, settings, parent=None):
        super().__init__(parent=parent)
        self.logger = classLogger(__name__, self.__class__.__name__)
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

        self.actionQuit.setShortcut(QKeySequence('Ctrl+Q'))
        self.actionQuit.triggered.connect(QCoreApplication.quit)

    def setWindowSizeAndPosition(self):
        # Initial window size/pos last saved. Use default values for first time
        for _ in range(2):
            try:
                self.resize(self.settings.size)
                self.move(self.settings.position)
            except TypeError:
                msg = "Can't read window size and position settings. Restore to defaults"
                self.logger.warning(msg)
                del self.settings.size
                del self.settings.position
                continue
            else:
                break
        else:
            msg = "Can't restore window settings"
            self.logger.error(msg)

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

    @pyqtSlot(name='display')
    def display(self):
        self.progress.useSystemFont = self.settings.useSystemFont
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
        base_brush.setStyle(Qt.BrushStyle.SolidPattern)
        highlight_brush = QBrush(QColor(*highlight))
        highlight_brush.setStyle(Qt.BrushStyle.SolidPattern)

        palette = QPalette()
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, base_brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, base_brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, highlight_brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, highlight_brush)
        palette.setBrush(QPalette.ColorRole.Text, highlight_brush)

        self.progress.setPalette(palette)
        self.button.setColor(highlight)

    @pyqtSlot(name='setFocusOnWindow')
    def setFocusOnWindow(self):
        self.show()
        self.activateWindow()
        self.raise_()

    @pyqtSlot(name='setFocusOnWindowAndPlayNotification')
    def setFocusOnWindowAndPlayNotification(self):
        if self.settings.interrupt:
            self.setFocusOnWindow()
            if self.windowState() == QtCore.Qt.WindowState.WindowMinimized:
                # Window is minimised. Restore it.
                self.setWindowState(QtCore.Qt.WindowState.WindowNoState)

        if self.settings.notification:
            sound_effect = QSoundEffect()
            sound_effect.setSource(QtCore.QUrl.fromLocalFile(os.path.join(MEDIA_DIR, 'sound.wav')))
            sound_effect.play()
