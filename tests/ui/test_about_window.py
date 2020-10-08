from unittest import mock

import pytest
from PyQt5 import QtCore

from CherryTomato import __version__
from CherryTomato.about_window import About


@pytest.fixture
def about_window(qtbot):
    window = About()
    window.show()
    qtbot.addWidget(window)
    return window


def test_close_on_esc_press(about_window, qtbot):
    with mock.patch.object(about_window, 'close'):
        qtbot.keyClick(about_window, QtCore.Qt.Key_Escape)

        about_window.close.assert_called_once_with()


@pytest.mark.parametrize('key', [
    QtCore.Qt.Key_Space,
    QtCore.Qt.Key_Q,
    QtCore.Qt.Key_Backspace,
])
def test_not_close_on_other_keys(about_window, qtbot, key):
    with mock.patch.object(about_window, 'close'):
        qtbot.keyClick(about_window, key)

        about_window.close.assert_not_called()


def test_version(about_window):
    assert f'CherryTomato {__version__}' == about_window.labelTitle.text()


def test_icon(about_window):
    assert not about_window.windowIcon().isNull()
