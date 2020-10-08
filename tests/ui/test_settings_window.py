from unittest import mock
from unittest.mock import Mock

import pytest
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QPoint

from CherryTomato import settings_window as ct_settings_window
from CherryTomato.settings import CherryTomatoSettings


@pytest.fixture
def default_settings():
    return {
        'stateTomato': 23 * 60,
        'stateBreak': 3 * 60,
        'stateLongBreak': 6 * 60,

        'size': QSize(400, 520),
        'position': QPoint(50, 50),

        'useSystemFont': True,
        'showTrayIcon': True,
        'notification': True,
        'interrupt': True,
        'repeat': 4,
        'autoStopTomato': False,
        'autoStopBreak': False,
        'switchToTomatoOnAbort': True,

        'afterStartCommand': 'echo after_start',
        'afterStopCommand': 'echo after_stop',
        'onTomatoCommand': 'echo on_tomato',
        'onBreakCommand': 'echo on_break',
    }


@pytest.fixture
def settings_window(qtbot, monkeypatch, settings):
    mcreateQT = Mock()
    mcreateQT.return_value = settings
    monkeypatch.setattr(ct_settings_window.CherryTomatoSettings, 'createQT', mcreateQT)

    window = ct_settings_window.Settings()
    window.show()
    qtbot.addWidget(window)
    return window


def test_icon(settings_window):
    assert not settings_window.windowIcon().isNull()


def test_close_on_esc_press(settings_window, qtbot):
    with mock.patch.object(settings_window, 'close'):
        qtbot.keyClick(settings_window, QtCore.Qt.Key_Escape)

        settings_window.close.assert_called_once_with()


@pytest.mark.parametrize('key', [
    QtCore.Qt.Key_Space,
    QtCore.Qt.Key_Q,
    QtCore.Qt.Key_Backspace,
])
def test_not_close_on_other_keys(settings_window, qtbot, key):
    with mock.patch.object(settings_window, 'close'):
        qtbot.keyClick(settings_window, key)

        settings_window.close.assert_not_called()


text_value_params = [
    ('stateTomato', '23', 23 * 60),
    ('stateBreak', '3', 3 * 60),
    ('stateLongBreak', '6', 6 * 60),
    ('repeat', '4', 4),
    ('afterStartCommand', 'echo after_start', 'echo after_start'),
    ('afterStopCommand', 'echo after_stop', 'echo after_stop'),
    ('onTomatoCommand', 'echo on_tomato', 'echo on_tomato'),
    ('onBreakCommand', 'echo on_break', 'echo on_break'),
]

bool_value_params = [
    ('useSystemFont', True),
    ('showTrayIcon', True),
    ('notification', True),
    ('interrupt', True),
    ('autoStopTomato', False),
    ('autoStopBreak', False),
    ('switchToTomatoOnAbort', True),
]

value_params = text_value_params + bool_value_params


def test_values_is_actual():
    expected = {item[0] for item in value_params}
    actual = {item.name for item in CherryTomatoSettings.options if item.ui}
    assert expected == actual, 'Update value_params according to CherryTomatoSettings options'


@pytest.mark.parametrize('option_name,expected,_', text_value_params)
def test_text_values(settings_window, qtbot, option_name, expected, _):
    field = getattr(settings_window, option_name)

    assert expected == field.text()


@pytest.mark.parametrize('option_name,expected', bool_value_params)
def test_bool_values(settings_window, qtbot, option_name, expected):
    field = getattr(settings_window, option_name)

    assert field.isChecked() is expected


def test_close_event(settings_window, qtbot):
    event = Mock()
    mupdateSettings = Mock()
    settings_window.updateSettings = mupdateSettings

    with qtbot.waitSignal(settings_window.closing, timeout=64):
        settings_window.closeEvent(event)

    event.accept.assert_called_once_with()
    mupdateSettings.assert_called_once_with()


@pytest.fixture
def empty_settings(settings):
    settings_store = settings.settingsBackend.settings
    for key, value in settings_store.items():
        if isinstance(value, bool):
            settings_store[key] = False
        elif isinstance(value, int):
            settings_store[key] = 0
        elif isinstance(value, str):
            settings_store[key] = ''
    return settings


@pytest.fixture
def settings_window_empty_settings(qtbot, monkeypatch, empty_settings):
    mcreateQT = Mock()
    mcreateQT.return_value = empty_settings
    monkeypatch.setattr(ct_settings_window.CherryTomatoSettings, 'createQT', mcreateQT)

    window = ct_settings_window.Settings()
    window.show()
    qtbot.addWidget(window)
    return window


@pytest.mark.parametrize('option_name,value,expected', text_value_params)
def test_updateSettings_text(settings_window_empty_settings, qtbot, option_name, value, expected):
    field = getattr(settings_window_empty_settings, option_name)
    qtbot.keyClick(field, QtCore.Qt.Key_Delete)
    qtbot.keyClicks(field, value)

    settings_window_empty_settings.close()

    settings_store = settings_window_empty_settings.settings.settingsBackend.settings
    assert expected == settings_store[option_name]


@pytest.mark.parametrize('option_name,_', bool_value_params)
def test_updateSettings_bool(settings_window_empty_settings, qtbot, option_name, _):
    field = getattr(settings_window_empty_settings, option_name)
    qtbot.keyClick(field, QtCore.Qt.Key_Space)

    settings_window_empty_settings.close()

    settings_store = settings_window_empty_settings.settings.settingsBackend.settings
    assert settings_store[option_name] is True
