import pytest
from PyQt5 import QtCore

from CherryTomato.main_window import CherryTomatoMainWindow
from CherryTomato.timer_proxy import TomatoTimerProxy


@pytest.fixture(params=['tomato', 'break'])
def mock_main_window(request, settings, qtbot, tomato):
    timerProxy = TomatoTimerProxy(tomato)
    window = CherryTomatoMainWindow(timerProxy, settings)

    if request.param == 'break':
        tomato.changeState()
    window.show()
    qtbot.addWidget(window)
    return window


def test_start_button_with_tomato(mock_main_window, qtbot):
    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    assert mock_main_window.timerProxy.isRunning()


def test_stop_button_with_tomato(mock_main_window, qtbot):
    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    assert mock_main_window.timerProxy.isRunning() is False
