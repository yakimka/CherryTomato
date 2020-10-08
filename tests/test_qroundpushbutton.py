from unittest.mock import Mock

import pytest
from PyQt5 import QtCore

from CherryTomato.widget import QRoundPushbutton, QPushButton


@pytest.fixture
def mock_qpushbutton(mocker):
    mocker.patch('CherryTomato.widget.QPushButton.__init__')
    mocker.patch('CherryTomato.widget.QPushButton.setFixedSize')
    mocker.patch('CherryTomato.widget.QPushButton.setFlat')
    mocker.patch('CherryTomato.widget.QPushButton.setAttribute')
    mocker.patch('CherryTomato.widget.QPushButton.setStyleSheet')


@pytest.fixture
def button(mock_qpushbutton):
    return QRoundPushbutton('parent')


def test_init(button):
    QPushButton.__init__.assert_called_once_with(parent='parent')
    button.setFixedSize.assert_called_once_with(40, 40)
    button.setFlat.assert_called_once_with(True)
    button.setAttribute.assert_called_once_with(QtCore.Qt.WA_TranslucentBackground)
    assert (255, 37, 51) == button.color
    assert button.image.endswith('/CherryTomato/media/play.png')
    button.setStyleSheet.assert_called()


def test_setColor(button):
    mapplyStyleSheet = Mock()
    button.applyStyleSheet = mapplyStyleSheet

    button.setColor((101, 102, 103))

    assert (101, 102, 103) == button.color
    mapplyStyleSheet.assert_called_once_with()


def test_setImage(button):
    mapplyStyleSheet = Mock()
    button.applyStyleSheet = mapplyStyleSheet

    button.setImage('button.png')

    assert button.image.endswith('/CherryTomato/media/button.png')
    mapplyStyleSheet.assert_called_once_with()


def test_setImage_called_twice(button):
    mapplyStyleSheet = Mock()
    button.applyStyleSheet = mapplyStyleSheet

    button.setImage('button.png')
    button.setImage('button.png')

    assert button.image.endswith('/CherryTomato/media/button.png')
    mapplyStyleSheet.assert_called_once_with()


def test_applyStyleSheet(button):
    button.color = (101, 102, 103)
    button.image = 'button.png'

    button.setStyleSheet.reset_mock()
    button.applyStyleSheet()

    button.setStyleSheet.assert_called_once_with('''
        background-color: rgb(101, 102, 103);
        background-image: url("button.png");
        border: 1px solid rgb(101, 102, 103);
        border-radius: 20px;
        ''')
