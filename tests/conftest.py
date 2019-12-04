import pytest

from CherryTomato.tomato_timer import TomatoTimer


@pytest.fixture
def tomato(monkeypatch):
    monkeypatch.setattr(TomatoTimer, 'TICK_TIME', 64)
    monkeypatch.setattr(TomatoTimer.STATE_TOMATO, 'time', 100)
    monkeypatch.setattr(TomatoTimer.STATE_BREAK, 'time', 25)
    monkeypatch.setattr(TomatoTimer.STATE_LONG_BREAK, 'time', 50)

    monkeypatch.setattr(TomatoTimer, 'TOMATOS_BEFORE_LONG_BREAK', 4)
    monkeypatch.setattr(TomatoTimer, 'AUTO_STOP_TOMATO', False)
    monkeypatch.setattr(TomatoTimer, 'AUTO_STOP_BREAK', False)
    monkeypatch.setattr(TomatoTimer, 'SWITCH_TO_TOMATO_ON_ABORT', True)

    tomato = TomatoTimer()

    return tomato


@pytest.fixture
def tomato_on_break(tomato):
    tomato.changeState()
    return tomato


@pytest.fixture
def mock_stop(mocker):
    return mocker.patch('CherryTomato.tomato_timer.TomatoTimer.stop')
