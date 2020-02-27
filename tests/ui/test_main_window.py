import pytest
from PyQt5 import QtCore

from CherryTomato.main_window import CherryTomatoMainWindow


@pytest.fixture(params=['tomato', 'break'])
def mock_main_window(request, settings, qtbot, tomato, monkeypatch):
    window = CherryTomatoMainWindow(settings)
    if request.param == 'break':
        tomato.changeState()
    monkeypatch.setattr(window, 'tomatoTimer', tomato)
    window.show()
    qtbot.addWidget(window)
    return window


def test_start_button_with_tomato(mock_main_window, qtbot):
    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    assert mock_main_window.tomatoTimer.running


def test_stop_button_with_tomato(mock_main_window, qtbot):
    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    qtbot.mouseClick(mock_main_window.button, QtCore.Qt.LeftButton)

    assert mock_main_window.tomatoTimer.running is False
