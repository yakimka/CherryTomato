#!/usr/bin/env python3

import sys

from PyQt5 import Qt

from CherryTomato.main_window import TomatoTimerWindow

app = Qt.QApplication(sys.argv)

watch = TomatoTimerWindow()
watch.show()

app.exec_()
