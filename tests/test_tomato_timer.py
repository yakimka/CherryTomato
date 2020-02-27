from itertools import cycle

import pytest

from CherryTomato.tomato_timer import State

STATE_BREAK = State('break', 25)
STATE_LONG_BREAK = State('long_break', 50)


def test_instance(tomato):
    assert tomato.state == 'stateTomato'
    assert tomato.seconds == 100
    assert tomato.running is False


def test_init(tomato):
    assert tomato.running is False
    assert tomato.state == 'stateTomato'
    assert tomato.seconds == 100


@pytest.fixture
def mock_qt_timer(mocker):
    return mocker.patch('CherryTomato.tomato_timer.Qt.QTimer')


def test_running(mock_qt_timer, tomato):
    tomato.running
    tomato.timer.isActive.assert_called_once()


@pytest.mark.parametrize('seconds,expected', [
    (62, 62),
    (-5, 0),
])
def test_seconds_setter(tomato, seconds, expected):
    tomato.seconds = seconds
    assert tomato.seconds == expected


@pytest.mark.parametrize('seconds,progress', [
    (14, 86),
    (1, 99),
    (22.12, 77),
    (99.99, 0),
    (0, 100),
])
def test_progress(tomato, seconds, progress):
    tomato._seconds = seconds
    assert tomato.progress == progress


def test_start(mock_qt_timer, tomato):
    tomato.start()
    tomato.timer.start.assert_called_once()


def test_stop(mock_qt_timer, tomato):
    tomato.stop()
    tomato.timer.stop.assert_called_once()


@pytest.fixture
def mock_reset_time(mocker):
    return mocker.patch('CherryTomato.tomato_timer.TomatoTimer.resetTime')


@pytest.fixture
def mock_for_abort(mock_stop, mock_reset_time):
    pass


def test_abort(mock_for_abort, tomato):
    tomato.abort()

    tomato.stop.assert_called_once()
    tomato.resetTime.assert_called_once()
    assert tomato.isTomato()


@pytest.mark.parametrize('flag_value,changed', [
    (True, True),
    (False, False)
])
def test_abort_with_switch_to_tomato_flag(
        mock_for_abort,
        tomato_on_break,
        flag_value,
        changed
):
    tomato_on_break.settings.switchToTomatoOnAbort = flag_value

    tomato_on_break.abort()

    assert ('stateBreak' != tomato_on_break.state) is changed


def test_create_timer(mock_qt_timer, tomato):
    assert mock_qt_timer.return_value == tomato.timer


@pytest.mark.parametrize('state,expected', [
    ('stateTomato', True),
    ('stateBreak', False),
    ('stateLongBreak', False),
])
def test_is_tomato(tomato, state, expected):
    tomato.stateName = state
    assert tomato.isTomato() is expected


def test_change_state(tomato):
    for i, params in enumerate(cycle([('stateTomato', 100), ('stateBreak', 25)])):
        state, time = params

        assert tomato.state == state
        assert tomato.seconds == time
        tomato.changeState()
        if i == 10:
            break


@pytest.mark.parametrize('tomatoes,const_value,expected', [
    (0, 4, 'stateBreak'),
    (3, 4, 'stateBreak'),
    (5, 4, 'stateBreak'),
    (1, 10, 'stateBreak'),
    (4, 4, 'stateLongBreak'),
    (12, 1, 'stateLongBreak'),
    (20, 10, 'stateLongBreak'),
    (100, 10, 'stateLongBreak'),

])
def test_change_state_to_long_break(tomato, tomatoes, const_value, expected):
    tomato.settings.repeat = const_value
    tomato.tomatoes = tomatoes

    tomato.changeState()

    assert tomato.state == expected


def test_reset_time(tomato):
    tomato.applyTick()

    tomato.resetTime()

    assert tomato.seconds == 100
