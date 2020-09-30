from itertools import cycle

import pytest

from CherryTomato.settings import STATE_TOMATO, STATE_BREAK, STATE_LONG_BREAK


def test_instance(tomato):
    assert tomato.state == 'stateTomato'
    assert tomato.seconds == 100
    assert tomato.running is False


def test_init(tomato):
    assert tomato.running is False
    assert tomato.state == 'stateTomato'
    assert tomato.seconds == 100


def test_create_timer(mock_qt_timer, tomato):
    assert mock_qt_timer.return_value == tomato.timer


def test_getStatus(tomato):
    assert (0, 'stateTomato') == tomato.getStatus()


def test_reset(tomato, mocker):
    mcreateTimer = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.createTimer')
    mchangeState = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.changeState')
    mnotifyAboutAnyChange = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.notifyAboutAnyChange'
    )

    tomato.tomatoes = 12
    tomato.stateName = 'dummy'
    tomato.maxSeconds = 123

    tomato.reset()

    assert 0 == tomato.tomatoes
    assert tomato.stateName is None
    assert tomato.maxSeconds is None
    mcreateTimer.assert_called_once_with()
    mchangeState.assert_called_once_with()
    mnotifyAboutAnyChange.assert_called_once_with()


def test_createTimer(tomato, mocker):
    mQTimer = mocker.patch('CherryTomato.tomato_timer.Qt.QTimer')
    mtick = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.tick')
    tomato.tickTime = 100500

    tomato.createTimer()

    assert mQTimer() == tomato.timer
    mQTimer().setInterval.assert_called_once_with(100500)
    mQTimer().timeout.connect.assert_called_once_with(mtick)
    mQTimer().timeout.disconnect.assert_not_called()


def test_createTimer_if_exists(tomato, mocker):
    mQTimer = mocker.patch('CherryTomato.tomato_timer.Qt.QTimer')
    mocker.patch('CherryTomato.tomato_timer.TomatoTimer.tick')

    tomato.createTimer()
    tomato.createTimer()

    mQTimer().timeout.disconnect.assert_called_once_with()


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


@pytest.mark.parametrize('state,expected_time', [
    (STATE_TOMATO, 100),
    (STATE_BREAK, 25),
    (STATE_LONG_BREAK, 50),
])
def test_state(state, expected_time, tomato):
    tomato.stateName = state

    assert state == tomato.state
    assert expected_time == tomato.state.time


def test_state_not_set(tomato):
    tomato.stateName = None

    assert tomato.state is None


def test__statesGen(tomato, mocker):
    m_isTimeForLongBreak = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer._isTimeForLongBreak',
        return_value=False
    )

    state_gen = tomato._statesGen()

    assert STATE_TOMATO == next(state_gen)
    assert STATE_BREAK == next(state_gen)
    assert STATE_TOMATO == next(state_gen)
    assert STATE_BREAK == next(state_gen)
    assert 2 == m_isTimeForLongBreak.call_count


def test__statesGen_long_break(tomato, mocker):
    m_isTimeForLongBreak = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer._isTimeForLongBreak',
        return_value=True
    )

    state_gen = tomato._statesGen()

    assert STATE_TOMATO == next(state_gen)
    assert STATE_LONG_BREAK == next(state_gen)
    assert STATE_TOMATO == next(state_gen)
    assert STATE_LONG_BREAK == next(state_gen)
    assert 2 == m_isTimeForLongBreak.call_count


@pytest.mark.parametrize('tomatoes,expected', [
    (0, False),
    (1, False),
    (2, False),
    (3, True),
    (4, False),
    (5, False),
    (6, True),
    (7, False),
])
def test__isTimeForLongBreak(tomato, mocker, tomatoes, expected):
    misTomato = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.isTomato', return_value=True)
    tomato.settings.repeat = 3
    tomato.tomatoes = tomatoes

    assert tomato._isTimeForLongBreak() is expected
    if tomatoes:
        misTomato.assert_called_once_with()


@pytest.mark.parametrize('tomatoes', [
    0, 1, 2, 3, 4, 5, 6, 7,
])
def test__isTimeForLongBreak_not_tomato(tomato, mocker, tomatoes):
    misTomato = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.isTomato', return_value=False)
    tomato.settings.repeat = 3
    tomato.tomatoes = tomatoes

    assert tomato._isTimeForLongBreak() is False
    if tomatoes:
        misTomato.assert_called_once_with()


@pytest.mark.parametrize('state,expected', [
    (STATE_TOMATO, True),
    (STATE_BREAK, False),
    (STATE_LONG_BREAK, False),
])
def test_isTomato(tomato, state, expected):
    tomato.stateName = state

    assert tomato.isTomato() is expected


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


def test_applyTick(tomato):
    tomato.seconds = 123

    tomato.applyTick()

    assert 123 == tomato.maxSeconds
    assert 122.936 == tomato.seconds


@pytest.mark.parametrize('isTomato,autoStopTomato,expected', [
    (True, True, True),
    (False, True, False),
    (True, False, False),
    (False, False, False),
])
def test__isNeedAutoStop_tomato(tomato, mocker, isTomato, autoStopTomato, expected):
    misTomato = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.isTomato',
        return_value=isTomato
    )
    tomato.settings.autoStopTomato = autoStopTomato
    tomato.settings.autoStopBreak = False

    assert tomato._isNeedAutoStop() is expected
    misTomato.assert_called()


@pytest.mark.parametrize('isTomato,autoStopBreak,expected', [
    (False, True, True),
    (True, True, False),
    (False, False, False),
    (True, False, False),
])
def test__isNeedAutoStop_break(tomato, mocker, isTomato, autoStopBreak, expected):
    misTomato = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.isTomato',
        return_value=isTomato
    )
    tomato.settings.autoStopBreak = autoStopBreak
    tomato.settings.autoStopTomato = False

    assert tomato._isNeedAutoStop() is expected
    misTomato.assert_called()


def test_stop(mock_qt_timer, tomato, mocker):
    mnotifyOnStop = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.notifyOnStop')

    tomato.stop()
    tomato.timer.stop.assert_called_once()
    mnotifyOnStop.assert_called_once_with()


def test_start(mock_qt_timer, tomato, mocker):
    mnotifyOnStart = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.notifyOnStart')

    tomato.start()
    tomato.timer.start.assert_called_once()
    mnotifyOnStart.assert_called_once_with()


@pytest.fixture
def mock_reset_time(mocker):
    return mocker.patch('CherryTomato.tomato_timer.TomatoTimer.resetTime')


@pytest.fixture
def mock_for_abort(mock_stop, mock_reset_time):
    pass


def test_abort(mock_for_abort, tomato, mocker):
    mnotifyAboutAnyChange = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.notifyAboutAnyChange'
    )
    mchangeState = mocker.patch('CherryTomato.tomato_timer.TomatoTimer.changeState')

    tomato.abort()

    tomato.stop.assert_called_once()
    tomato.resetTime.assert_called_once()
    assert tomato.isTomato()
    mnotifyAboutAnyChange.assert_called_once_with()
    mchangeState.assert_not_called()


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


def test_onSettingsChange_running(tomato, mock_reset_time, mocker):
    mnotifyAboutAnyChange = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.notifyAboutAnyChange'
    )

    tomato.maxSeconds = 1000

    tomato.onSettingsChange()

    mock_reset_time.assert_called_once_with()
    mnotifyAboutAnyChange.assert_called_once_with()


def test_onSettingsChange_stopped(tomato, mock_reset_time, mocker):
    mnotifyAboutAnyChange = mocker.patch(
        'CherryTomato.tomato_timer.TomatoTimer.notifyAboutAnyChange'
    )

    tomato.onSettingsChange()

    mock_reset_time.assert_not_called()
    mnotifyAboutAnyChange.assert_not_called()


def test_reset_time(tomato):
    tomato.applyTick()

    tomato.resetTime()

    assert tomato.seconds == 100
