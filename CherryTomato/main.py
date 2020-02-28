#!/usr/bin/env python3
import logging
import sys

from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication

from CherryTomato import ORGANIZATION_NAME, APPLICATION_NAME
from CherryTomato.main_window import CherryTomatoMainWindow
from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.timer_proxy import TomatoTimerProxy
from CherryTomato.tomato_timer import TomatoTimer
from CherryTomato.utils import CommandExecutor, CompactFormatter, makeLogger

logFmt = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CompactFormatter(logFmt, "%Y-%m-%d %H:%M:%S"))
logger = makeLogger('CherryTomato', handler=handler, level='INFO')


def main():
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = Qt.QApplication(sys.argv)
    settings = CherryTomatoSettings.createQT()

    tomatoTimer = TomatoTimer(settings)
    timerProxy = TomatoTimerProxy(tomatoTimer)

    cmdExec = CommandExecutor(settings)
    timerProxy.onStart.connect(cmdExec.onStart)
    timerProxy.onStop.connect(cmdExec.onStop)
    timerProxy.onStateChange.connect(cmdExec.onStateChange)

    watch = CherryTomatoMainWindow(timerProxy, settings)
    watch.show()

    app.exec_()


if __name__ == '__main__':
    main()
