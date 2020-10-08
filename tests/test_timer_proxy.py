from unittest.mock import Mock

import pytest

from CherryTomato.timer_proxy import AbstractTimerProxy, TomatoTimerProxy


class InitMixin:
    class_ = None

    def test_init(self):
        mtimer = Mock()
        proxy = self.class_(mtimer)

        assert mtimer == proxy.timer
        assert mtimer.onStop == proxy.onStop
        assert mtimer.onStateChange == proxy.onStateChange
        assert mtimer.onChange == proxy.onChange
        assert mtimer.finished == proxy.finished


class TestAbstractTimerProxy(InitMixin):
    class_ = AbstractTimerProxy

    @pytest.mark.parametrize('method_name', [
        'isRunning',
        'getColorPalette',
        'getUpperText',
        'getBottomText',
        'getProgress',
        'onAction',
        'reset',
        'onSettingsChange',
    ])
    def test_not_implemented(self, method_name):
        with pytest.raises(NotImplementedError):
            getattr(self.class_(Mock()), method_name)()


@pytest.fixture
def tomato_timer_proxy():
    mtimer: Mock = Mock()
    return TomatoTimerProxy(mtimer)


class TestTomatoTimerProxy(InitMixin):
    class_ = TomatoTimerProxy

    def test_isRunning(self, tomato_timer_proxy):
        result = tomato_timer_proxy.isRunning()

        assert tomato_timer_proxy.timer.running == result

    def test_onAction_when_running(self, tomato_timer_proxy):
        tomato_timer_proxy.timer.running = True

        tomato_timer_proxy.onAction()

        tomato_timer_proxy.timer.abort.assert_called_once_with()
        tomato_timer_proxy.timer.start.assert_not_called()

    def test_onAction_when_not_running(self, tomato_timer_proxy):
        tomato_timer_proxy.timer.running = False

        tomato_timer_proxy.onAction()

        tomato_timer_proxy.timer.abort.assert_not_called()
        tomato_timer_proxy.timer.start.assert_called_once_with()

    def test_reset(self, tomato_timer_proxy):
        tomato_timer_proxy.reset()

        tomato_timer_proxy.timer.reset.assert_called_once_with()

    def test_onSettingsChange(self, tomato_timer_proxy):
        tomato_timer_proxy.onSettingsChange()

        tomato_timer_proxy.timer.onSettingsChange.assert_called_once_with()

    @pytest.mark.parametrize('seconds,expected', [
        (0, '00:00'),
        (1, '00:01'),
        (59, '00:59'),
        (61, '01:01'),
        (3549, '59:09'),
        (9999, '166:39'),
    ])
    def test_getUpperText(self, tomato_timer_proxy, seconds, expected):
        tomato_timer_proxy.timer.seconds = seconds

        assert expected == tomato_timer_proxy.getUpperText()

    def test_getBottomText(self, tomato_timer_proxy):
        tomato_timer_proxy.timer.tomatoes = 21

        assert '🍅x21' == tomato_timer_proxy.getBottomText()

    def test_getProgress(self, tomato_timer_proxy):
        assert tomato_timer_proxy.timer.progress == tomato_timer_proxy.getProgress()

    def test_getColorPalette_when_tomato(self, tomato_timer_proxy):
        tomato_timer_proxy.timer.isTomato.return_value = True

        assert ((249, 192, 191), (255, 37, 51)) == tomato_timer_proxy.getColorPalette()

    def test_getColorPalette_when_break(self, tomato_timer_proxy):
        tomato_timer_proxy.timer.isTomato.return_value = False

        assert ((176, 236, 193), (60, 187, 111)) == tomato_timer_proxy.getColorPalette()
