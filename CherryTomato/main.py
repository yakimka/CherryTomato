#!/usr/bin/env python3

import logging
import sys

from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from CherryTomato import ORGANIZATION_NAME, APPLICATION_NAME, APP_ICON
from CherryTomato.main_window import CherryTomatoMainWindow
from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.timer_proxy import TomatoTimerProxy
from CherryTomato.tomato_timer import TomatoTimer
from CherryTomato.utils import CommandExecutor, CompactFormatter, makeLogger, addCustomFont

logFmt = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CompactFormatter(logFmt, "%Y-%m-%d %H:%M:%S"))
logger = makeLogger(None, handler=handler, level='INFO')


def setTrayIcon(app, mainWindow):
    app.setQuitOnLastWindowClosed(False)
    icon = QIcon(APP_ICON)
    trayIcon = QSystemTrayIcon(parent=mainWindow, icon=icon)

    menu = QMenu(parent=mainWindow)

    settingsAction = QAction(text='Settings', parent=mainWindow)
    settingsAction.triggered.connect(mainWindow.showSettingsWindow)
    menu.addAction(settingsAction)

    aboutAction = QAction(text='About', parent=mainWindow)
    aboutAction.triggered.connect(mainWindow.showAboutWindow)
    menu.addAction(aboutAction)

    quitAction = QAction(text='Quit', parent=mainWindow)
    quitAction.triggered.connect(app.quit)
    menu.addAction(quitAction)

    trayIcon.activated.connect(mainWindow.setFocusOnWindow)

    trayIcon.setContextMenu(menu)
    trayIcon.setVisible(True)


def main():
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = Qt.QApplication(sys.argv)

    # https://bugs.documentfoundation.org/show_bug.cgi?id=125934
    app.setDesktopFileName('cherrytomato.desktop')

    settings = CherryTomatoSettings.createQT()

    if not settings.useSystemFont:
        addCustomFont()

    tomatoTimer = TomatoTimer(settings)
    timerProxy = TomatoTimerProxy(tomatoTimer)

    cmdExec = CommandExecutor(settings)
    timerProxy.onStart.connect(cmdExec.onStart)
    timerProxy.onStop.connect(cmdExec.onStop)
    timerProxy.onStateChange.connect(cmdExec.onStateChange)

    watch = CherryTomatoMainWindow(timerProxy, settings)

    if settings.showTrayIcon:
        setTrayIcon(app, watch)

    watch.show()

    app.exec_()


if __name__ == '__main__':
    main()
