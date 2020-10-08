from unittest.mock import MagicMock

import pytest
from PyQt5.QtCore import QSize, QPoint

from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.tomato_timer import TomatoTimer


@pytest.fixture
def default_settings():
    return {
        'stateTomato': 100,
        'stateBreak': 25,
        'stateLongBreak': 50,

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
def mock_settings_backend(default_settings):
    class MockQSettings:
        settings = default_settings

        def value(self, key, default, type=None):
            return self.settings.get(key)

        def setValue(self, key, value):
            self.settings[key] = value

        remove = MagicMock()

    return MockQSettings()


@pytest.fixture
def settings(mock_settings_backend):
    return CherryTomatoSettings(mock_settings_backend)


@pytest.fixture
def tomato(settings):
    return TomatoTimer(settings)


@pytest.fixture
def tomato_on_break(tomato):
    tomato.changeState()
    return tomato


@pytest.fixture
def mock_stop(mocker):
    return mocker.patch('CherryTomato.tomato_timer.TomatoTimer.stop')
