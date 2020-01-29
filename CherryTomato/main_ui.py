# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 60)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progress = QRoundProgressBar(self.centralwidget)
        self.progress.setMinimumSize(QtCore.QSize(200, 200))
        self.progress.setObjectName("progress")
        self.horizontalLayout.addWidget(self.progress)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.button = QRoundPushbutton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy)
        self.button.setMinimumSize(QtCore.QSize(40, 40))
        self.button.setMaximumSize(QtCore.QSize(40, 40))
        self.button.setBaseSize(QtCore.QSize(0, 0))
        self.button.setStyleSheet("background-color: rgb(255, 37, 51);\n"
"background-image: url(\"./play.png\");\n"
"border: 1px solid rgb(255, 37, 51);\n"
"border-radius: 20px;")
        self.button.setText("")
        self.button.setFlat(True)
        self.button.setObjectName("button")
        self.verticalLayout.addWidget(self.button, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CherryTomato"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
from CherryTomato.widget import QRoundProgressBar, QRoundPushbutton
