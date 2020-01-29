#!/usr/bin/env python3

import sys

from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication

from CherryTomato import ORGANIZATION_NAME, APPLICATION_NAME
from CherryTomato.main_window import CherryTomatoMainWindow

QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
QCoreApplication.setApplicationName(APPLICATION_NAME)

app = Qt.QApplication(sys.argv)

watch = CherryTomatoMainWindow()
watch.show()

app.exec_()
