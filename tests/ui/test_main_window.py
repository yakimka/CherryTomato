from unittest.mock import Mock

import pytest
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QPoint

from CherryTomato.main_window import CherryTomatoMainWindow
from CherryTomato.timer_proxy import TomatoTimerProxy


@pytest.fixture
def main_window_in_tomato(settings, qtbot, tomato):
    assert tomato.isTomato()

    timerProxy = TomatoTimerProxy(tomato)
    window = CherryTomatoMainWindow(timerProxy, settings)
    window.show()
    qtbot.addWidget(window)
    return window


@pytest.fixture
def main_window_in_break(main_window_in_tomato, tomato):
    tomato.changeState()
    return main_window_in_tomato


@pytest.fixture(params=['tomato', 'break'])
def main_window(request, main_window_in_tomato, main_window_in_break):
    if request.param == 'tomato':
        return main_window_in_tomato
    elif request.param == 'break':
        return main_window_in_break


def test_start_button_with_tomato(main_window, qtbot):
    qtbot.mouseClick(main_window.button, QtCore.Qt.LeftButton)

    assert main_window.timerProxy.isRunning()


def test_stop_button_with_tomato(main_window, qtbot):
    qtbot.mouseClick(main_window.button, QtCore.Qt.LeftButton)

    qtbot.mouseClick(main_window.button, QtCore.Qt.LeftButton)

    assert main_window.timerProxy.isRunning() is False


def test_icon(main_window_in_tomato):
    assert not main_window_in_tomato.windowIcon().isNull()


@pytest.fixture
def mock_resize(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'resize')


@pytest.fixture
def mock_move(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'move')


def test_setWindowSizeAndPosition(main_window_in_tomato, mock_resize, mock_move):
    main_window_in_tomato.setWindowSizeAndPosition()

    mock_resize.assert_called_once_with(QSize(400, 520))
    mock_move.assert_called_once_with(QPoint(50, 50))


def test_setWindowSizeAndPosition_fail_restore(main_window_in_tomato, mock_resize, caplog):
    mock_resize.side_effect = TypeError

    main_window_in_tomato.setWindowSizeAndPosition()

    assert mock_resize.call_count == 2
    assert "Can't read window size and position settings. Restore to defaults" in caplog.messages
    assert "Can't restore window settings" in caplog.messages


@pytest.fixture
def mock_saveWindowSizeAndPosition(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'saveWindowSizeAndPosition')


def test_closeEvent(main_window_in_tomato, mock_saveWindowSizeAndPosition):
    event = Mock()
    main_window_in_tomato.closeEvent(event)

    mock_saveWindowSizeAndPosition.assert_called_once_with()
    event.accept.assert_called_once_with()


@pytest.fixture
def mock_size_and_pos(mocker):
    mocker.patch.object(CherryTomatoMainWindow, 'size', return_value='100x100')
    mocker.patch.object(CherryTomatoMainWindow, 'pos', return_value='1x1')


def test_saveWindowSizeAndPosition(main_window_in_tomato, settings, mock_size_and_pos):
    main_window_in_tomato.saveWindowSizeAndPosition()

    assert settings.size == '100x100'
    assert settings.position == '1x1'


@pytest.fixture
def mock_getWindowCenterPoint(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'getWindowCenterPoint', return_value=(1, 2))


def test_showAboutWindow(main_window_in_tomato, mock_getWindowCenterPoint):
    mock_aboutWindow = Mock()
    main_window_in_tomato.aboutWindow = mock_aboutWindow

    main_window_in_tomato.actionAbout.trigger()

    mock_getWindowCenterPoint.assert_called_once_with(mock_aboutWindow)
    mock_aboutWindow.move.assert_called_once_with(1, 2)
    mock_aboutWindow.show.assert_called_once_with()


def test_showSettingsWindow(main_window_in_tomato, mock_getWindowCenterPoint):
    mock_showSettingsWindow = Mock()
    main_window_in_tomato.settingsWindow = mock_showSettingsWindow

    main_window_in_tomato.actionSettings.trigger()

    mock_getWindowCenterPoint.assert_called_once_with(mock_showSettingsWindow)
    mock_showSettingsWindow.move.assert_called_once_with(1, 2)
    mock_showSettingsWindow.show.assert_called_once_with()


@pytest.fixture
def mock_x_y_width_height(mocker):
    mocker.patch.object(CherryTomatoMainWindow, 'x', return_value=4)
    mocker.patch.object(CherryTomatoMainWindow, 'y', return_value=18)
    mocker.patch.object(CherryTomatoMainWindow, 'width', return_value=8)
    mocker.patch.object(CherryTomatoMainWindow, 'height', return_value=20)


@pytest.fixture
def mock_any_window():
    any_window = Mock()
    any_window.width.return_value = 102
    any_window.height.return_value = 21
    return any_window


def test_getWindowCenterPoint(main_window_in_tomato, mock_x_y_width_height, mock_any_window):
    result = main_window_in_tomato.getWindowCenterPoint(mock_any_window)

    assert (-43, 17) == result


@pytest.fixture
def mock_changeButtonState(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'changeButtonState')


@pytest.fixture
def mock_setColor(mocker):
    return mocker.patch.object(CherryTomatoMainWindow, 'setColor')


def test_display(main_window_in_tomato, mock_changeButtonState, mock_setColor):
    mprogress = Mock()
    main_window_in_tomato.progress = mprogress
    mtimerProxy = Mock()
    mtimerProxy.getColorPalette.return_value = [1, 2, 3]
    main_window_in_tomato.timerProxy = mtimerProxy
    main_window_in_tomato.settings.useSystemFont = 'use'

    main_window_in_tomato.display()

    assert 'use' == main_window_in_tomato.progress.useSystemFont
    mprogress.setFormat.assert_called_once_with(mtimerProxy.getUpperText())
    mprogress.setSecondFormat.assert_called_once_with(mtimerProxy.getBottomText())
    mprogress.setValue.assert_called_once_with(mtimerProxy.getProgress())
    mock_changeButtonState.assert_called_once_with()
    mock_setColor.assert_called_once_with(1, 2, 3)


@pytest.mark.parametrize('is_running,expected', [
    (True, 'stop.png'),
    (False, 'play.png'),
])
def test_changeButtonState(main_window_in_tomato, is_running, expected):
    mtimerProxy = Mock()
    mtimerProxy.isRunning.return_value = is_running
    main_window_in_tomato.timerProxy = mtimerProxy
    mbutton = Mock()
    main_window_in_tomato.button = mbutton

    main_window_in_tomato.changeButtonState()

    main_window_in_tomato.button.setImage.assert_called_once_with(expected)


def test_setColor(main_window_in_tomato):
    mprogress = Mock()
    main_window_in_tomato.progress = mprogress
    mbutton = Mock()
    main_window_in_tomato.button = mbutton

    main_window_in_tomato.setColor((1, 2, 3), (4, 5, 6))

    mprogress.setPalette.assert_called()
    mbutton.setColor.assert_called_once_with((4, 5, 6))


def test_setFocusOnWindow(main_window_in_tomato):
    main_window_in_tomato.show = Mock()
    main_window_in_tomato.activateWindow = Mock()
    main_window_in_tomato.raise_ = Mock()

    main_window_in_tomato.setFocusOnWindow()

    main_window_in_tomato.show.assert_called_once_with()
    main_window_in_tomato.activateWindow.assert_called_once_with()
    main_window_in_tomato.raise_.assert_called_once_with()


@pytest.fixture
def mock_for_set_focus(main_window_in_tomato):
    main_window_in_tomato.setFocusOnWindow = Mock()
    main_window_in_tomato.setWindowState = Mock()
    main_window_in_tomato.windowState = Mock()


def test_setFocusOnWindowAndPlayNotification_not_interrupt(main_window_in_tomato,
                                                           mock_for_set_focus):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.interrupt = False
    main_window_in_tomato.settings.notification = False

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    main_window_in_tomato.setFocusOnWindow.assert_not_called()
    main_window_in_tomato.setWindowState.assert_not_called()


def test_setFocusOnWindowAndPlayNotification_interrupt(main_window_in_tomato, mock_for_set_focus):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.interrupt = True
    main_window_in_tomato.settings.notification = False

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    main_window_in_tomato.setFocusOnWindow.assert_called_once_with()


def test_setFocusOnWindowAndPlayNotification_not_minimized(
        main_window_in_tomato,
        mock_for_set_focus
):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.interrupt = True
    main_window_in_tomato.settings.notification = False

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    main_window_in_tomato.setWindowState.assert_not_called()


def test_setFocusOnWindowAndPlayNotification_minimized(main_window_in_tomato, mock_for_set_focus):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.interrupt = True
    main_window_in_tomato.settings.notification = False
    main_window_in_tomato.windowState.return_value = QtCore.Qt.WindowMinimized

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    main_window_in_tomato.setWindowState.assert_called_once_with(QtCore.Qt.WindowNoState)


@pytest.fixture
def mock_QSound(mocker):
    return mocker.patch('CherryTomato.main_window.QSound')


def test_setFocusOnWindowAndPlayNotification_minimized_not_notificate(
        main_window_in_tomato,
        mock_QSound,
        mock_for_set_focus
):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.notification = False

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    mock_QSound.play.assert_not_called()


def test_setFocusOnWindowAndPlayNotification_minimized_notificate(
        main_window_in_tomato,
        mock_QSound,
        mock_for_set_focus
):
    main_window_in_tomato.settings = Mock()
    main_window_in_tomato.settings.notification = True

    main_window_in_tomato.setFocusOnWindowAndPlayNotification()

    mock_QSound.play.assert_called_once()
