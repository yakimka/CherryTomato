# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(402, 222)
        self.verticalLayout = QtWidgets.QVBoxLayout(About)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setText("CherryTomato")
        self.labelTitle.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelText = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.labelText.sizePolicy().hasHeightForWidth())
        self.labelText.setSizePolicy(sizePolicy)
        self.labelText.setTextFormat(QtCore.Qt.RichText)
        self.labelText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelText.setWordWrap(True)
        self.labelText.setOpenExternalLinks(True)
        self.labelText.setObjectName("labelText")
        self.verticalLayout.addWidget(self.labelText)
        self.labelCopyright = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCopyright.sizePolicy().hasHeightForWidth())
        self.labelCopyright.setSizePolicy(sizePolicy)
        self.labelCopyright.setText("Copyright © 2019 yakimka")
        self.labelCopyright.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.labelCopyright.setObjectName("labelCopyright")
        self.verticalLayout.addWidget(self.labelCopyright)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About CherryTomato"))
        self.labelText.setText(_translate("About", "<html><head/><body><p>CherryTomato is a simple tomato timer app.</p><p>It\'s written in Python 3 using PyQt5.</p><p>Project page: <a href=\"https://github.com/yakimka/CherryTomato\"><span style=\" text-decoration: underline; color:#4877b1;\">https://github.com/yakimka/CherryTomato</span></a></p></body></html>"))
