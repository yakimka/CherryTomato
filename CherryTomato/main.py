#!/usr/bin/env python3

import sys

from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication

from CherryTomato import ORGANIZATION_NAME, APPLICATION_NAME
from CherryTomato.main_window import CherryTomatoMainWindow
from CherryTomato.settings import CherryTomatoSettings


def main():
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = Qt.QApplication(sys.argv)

    settings = CherryTomatoSettings.createQT()
    watch = CherryTomatoMainWindow(settings)
    watch.show()

    app.exec_()


if __name__ == '__main__':
    main()
