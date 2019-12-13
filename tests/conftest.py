import pytest

from CherryTomato.settings import CherryTomatoSettings
from CherryTomato.tomato_timer import TomatoTimer


class MockQSettings:
    def value(self, key, default, type=None):
        return default


@pytest.fixture
def settings(monkeypatch, mocker):
    monkeypatch.setattr(CherryTomatoSettings, 'TOMATO_DEFAULT', 100)
    monkeypatch.setattr(CherryTomatoSettings, 'BREAK_DEFAULT', 25)
    monkeypatch.setattr(CherryTomatoSettings, 'LONG_BREAK_DEFAULT', 50)
    monkeypatch.setattr(CherryTomatoSettings, 'REPEAT_DEFAULT', 4)
    monkeypatch.setattr(CherryTomatoSettings, 'AUTO_STOP_TOMATO_DEFAULT', False)
    monkeypatch.setattr(CherryTomatoSettings, 'AUTO_STOP_BREAK_DEFAULT', False)
    monkeypatch.setattr(CherryTomatoSettings, 'SWITCH_TO_TOMATO_ON_ABORT_DEFAULT', True)

    mocker.patch('CherryTomato.settings.QSettings', MockQSettings)
    settings = CherryTomatoSettings()

    return settings


@pytest.fixture
def tomato(settings, monkeypatch, mocker):
    monkeypatch.setattr(TomatoTimer, 'TICK_TIME', 64)
    mocker.patch('CherryTomato.tomato_timer.settings', settings)
    tomato = TomatoTimer()

    return tomato


@pytest.fixture
def tomato_on_break(tomato):
    tomato.changeState()
    return tomato


@pytest.fixture
def mock_stop(mocker):
    return mocker.patch('CherryTomato.tomato_timer.TomatoTimer.stop')
