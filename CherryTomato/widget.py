import os

from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QFont, QFontMetricsF, QPaintEvent, QImage
from PyQt5.QtWidgets import QPushButton
from qroundprogressbar import QRoundProgressBar as QRoundProgressBar_

from CherryTomato import MEDIA_DIR


class QRoundPushbutton(QPushButton):
    stylesheet = '''
        background-color: rgb{color};
        background-image: url("{image}");
        border: 1px solid rgb{color};
        border-radius: 20px;
        '''

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(40, 40)
        self.setFlat(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.color = (255, 37, 51)
        self.image = os.path.join(MEDIA_DIR, 'play.png')
        self.applyStyleSheet()

    def setColor(self, rgb: tuple):
        self.color = rgb
        self.applyStyleSheet()

    def setImage(self, image: str):
        path = os.path.join(MEDIA_DIR, image)
        if path != self.image:
            self.image = path
            self.applyStyleSheet()

    def applyStyleSheet(self):
        self.setStyleSheet(self.stylesheet.format(color=self.color, image=self.image))


class QRoundProgressBar(QRoundProgressBar_):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.useSystemFont = True
        self.m_second_format = ''

        self.setFormat('')
        self.setValue(0)
        self.setBarStyle(QRoundProgressBar.BarStyle.LINE)
        self.setOutlinePenWidth(4)
        self.setDataPenWidth(4)

    def resizeEvent(self, e):
        self.setMaximumWidth(self.height())

    def setSecondFormat(self, val: str):
        if val != self.m_second_format:
            self.m_second_format = val
            self.valueFormatChanged()

    def paintEvent(self, event: QPaintEvent):
        outerRadius = min(self.width(), self.height())
        baseRect = QRectF(1, 1, outerRadius - 2, outerRadius - 2)
        buffer = QImage(outerRadius, outerRadius, QImage.Format_ARGB32_Premultiplied)
        p = QPainter(buffer)
        p.setRenderHint(QPainter.Antialiasing)
        self.rebuildDataBrushIfNeeded()
        self.drawBackground(p, buffer.rect())
        self.drawBase(p, baseRect)
        if self.m_value > 0:
            delta = (self.m_max - self.m_min) / (self.m_value - self.m_min)
        else:
            delta = 0
        self.drawValue(p, baseRect, self.m_value, delta)
        firstInnerRect, secondInnerRect, innerRadius = self.calculateInnerRect(outerRadius)
        self.drawInnerBackground(p, firstInnerRect)
        self.drawInnerBackground(p, secondInnerRect)
        self.drawTwoTexts(p, firstInnerRect, secondInnerRect, innerRadius, self.m_value)
        p.end()
        painter = QPainter(self)
        painter.fillRect(baseRect, self.palette().window())
        painter.drawImage(0, 0, buffer)

    def calculateInnerRect(self, outerRadius: float):
        innerRect, innerRadius = super().calculateInnerRect(outerRadius)

        left, top, width, height = innerRect.getRect()

        firstHeight = height * 0.7
        firstInnerRect = QRectF(left, top, width, firstHeight)
        secondInnerRect = QRectF(left, top + firstHeight, width, height - firstHeight)
        return firstInnerRect, secondInnerRect, innerRadius

    def drawTwoTexts(
            self,
            p: QPainter,
            firstRect: QRectF,
            secondRect: QRectF,
            innerRadius: float,
            value: float,
    ):
        if not self.m_format:
            return

        if self.useSystemFont:
            font = QFont(self.font())
        else:
            font = QFont('Noto Sans')

        font.setPixelSize(10)
        fm = QFontMetricsF(font)
        maxWidth = fm.width(self.valueToText(self.m_max))
        delta = innerRadius / maxWidth
        timeFontSize = font.pixelSize() * delta * 0.75
        font.setPixelSize(int(timeFontSize))
        p.setFont(font)
        timeTextRect = QRectF(firstRect)
        tomatoesTextRect = QRectF(secondRect)
        p.setPen(self.palette().text().color())
        p.drawText(timeTextRect, Qt.AlignCenter | Qt.AlignBottom, self.valueToText(value))
        tomatoesFontSize = timeFontSize * 0.3
        font.setPixelSize(int(tomatoesFontSize))
        p.setFont(font)
        p.drawText(tomatoesTextRect, Qt.AlignHCenter, self.m_second_format)
