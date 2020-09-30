import pytest


def test_notifyOnStateChange(tomato, qtbot):
    with qtbot.waitSignal(tomato.onStateChange, timeout=64):
        tomato.notifyOnStateChange()


def test_notifyOnStop(tomato, qtbot):
    with qtbot.waitSignal(tomato.onStop, timeout=64):
        tomato.notifyOnStop()


def test_tick_once(tomato, qtbot):
    with qtbot.waitSignal(tomato.onChange, timeout=64):
        tomato.start()

    check_is_ticked_when_tomato(tomato)


def check_is_ticked_when_tomato(tomato):
    __tracebackhide__ = True

    assert tomato.running is True
    assert tomato.seconds == 100 - 0.064
    assert tomato.isTomato()


def test_tick_tomatos_count(tomato, qtbot):
    tomato._seconds = 0.2
    with qtbot.waitSignal(tomato.finished, timeout=1000):
        tomato.start()

    assert tomato.tomatoes == 1


def test_tick_tomatos_count_from_break(tomato_on_break, qtbot):
    tomato_on_break._seconds = 0.2
    with qtbot.waitSignal(tomato_on_break.finished, timeout=1000):
        tomato_on_break.start()

    assert tomato_on_break.tomatoes == 0


@pytest.mark.parametrize('is_tomato,flag,auto_stop', [
    (True, True, True),
    (True, False, False),
    (False, True, True),
    (False, False, False),
])
def test_tick_auto_stop(tomato, qtbot, mock_stop, is_tomato, flag, auto_stop):
    tomato.settings.autoStopTomato = flag
    tomato.settings.autoStopBreak = flag
    if not is_tomato:
        tomato.changeState()

    tomato._seconds = 0.2
    with qtbot.waitSignal(tomato.finished, timeout=1000):
        tomato.start()

    assert tomato.stop.called is auto_stop


def test_notify_about_any_change(tomato, qtbot):
    with qtbot.waitSignal(tomato.onChange, timeout=64):
        tomato.notifyAboutAnyChange()


def test_notify_timer_is_over(tomato, qtbot):
    with qtbot.waitSignal(tomato.finished, timeout=64):
        tomato.notifyTimerIsOver()


def test_notify_any_change_in_abort(tomato, qtbot):
    with qtbot.waitSignal(tomato.onChange, timeout=64):
        tomato.start()
