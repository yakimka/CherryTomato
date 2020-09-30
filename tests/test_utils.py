import os
from unittest import mock
from unittest.mock import Mock

import pytest

from CherryTomato import BASE_DIR
from CherryTomato.settings import STATE_TOMATO, STATE_LONG_BREAK, STATE_BREAK
from CherryTomato.utils import (CommandExecutor, addCustomFont, CompactFormatter, makeLogger,
                                classLogger)


@pytest.fixture
def mock__execute(monkeypatch):
    m_execute = Mock()
    monkeypatch.setattr(CommandExecutor, '_execute', m_execute)
    return m_execute


@pytest.fixture
def executor(settings):
    settings.afterStartCommand = 'after_start'
    settings.afterStopCommand = 'after_stop'
    settings.onTomatoCommand = 'on_tomato'
    settings.onBreakCommand = 'on_break'
    return CommandExecutor(settings)


@pytest.fixture
def mstatus():
    status = Mock()
    status.tomatoes = 1
    status.state = STATE_TOMATO
    return status


@pytest.fixture
def mock_subprocess(monkeypatch):
    msubprocess = Mock()
    monkeypatch.setattr('CherryTomato.utils.subprocess', msubprocess)
    return msubprocess


class TestCommandExecutor:
    def test_init(self, executor, settings):
        assert settings == executor.settings

    def test_onStart(self, executor, mock__execute, mstatus):
        executor.onStart(mstatus)

        mock__execute.assert_called_once_with('after_start', mstatus)

    def test_onStop(self, executor, mock__execute, mstatus):
        executor.onStop(mstatus)

        mock__execute.assert_called_once_with('after_stop', mstatus)

    def test_onStateChange_tomato(self, executor, mock__execute, mstatus):
        mstatus.state = STATE_TOMATO
        executor.onStateChange(mstatus)

        mock__execute.assert_called_once_with('on_tomato', mstatus)

    @pytest.mark.parametrize('break_state', [STATE_BREAK, STATE_LONG_BREAK, 'else_state'])
    def test_onStateChange_break(self, break_state, executor, mock__execute, mstatus):
        mstatus.state = break_state
        executor.onStateChange(mstatus)

        mock__execute.assert_called_once_with('on_break', mstatus)

    def test_onStateChange_zero_tomatoes(self, executor, mock__execute, mstatus):
        mstatus.tomatoes = 0
        executor.onStateChange(mstatus)

        mock__execute.assert_not_called()

    def test__execute(self, executor, mock_subprocess):
        executor._execute('my_cmd')

        mock_subprocess.Popen.assert_called_once_with(
            ['my_cmd'],
            stdout=mock_subprocess.DEVNULL,
            stderr=mock_subprocess.STDOUT
        )

    def test__execute_empty_command(self, executor, mock_subprocess):
        executor._execute('')

        mock_subprocess.Popen.assert_not_called()

    def test__execute_fail(self, executor, mock_subprocess, caplog):
        mock_subprocess.Popen.side_effect = ValueError('Some exception message')

        executor._execute('fail_cmd')
        record = caplog.records[0]

        assert ValueError == record.exc_info[0]
        assert 'Some exception message' == str(record.exc_info[1])
        assert 'Error while executing command "fail_cmd"' == record.msg

    @pytest.mark.parametrize('command,expected', [
        ('tomatoes={tomatoes}', ['tomatoes=1']),
        ('state={state}', ['state=tomato']),
        ('state={state} tomatoes={tomatoes}', ['state=tomato', 'tomatoes=1']),
    ])
    def test__execute_with_macros(self, executor, mock_subprocess, mstatus, command, expected):
        executor._execute(command, mstatus)

        mock_subprocess.Popen.assert_called_once_with(
            expected,
            stdout=mock.ANY,
            stderr=mock.ANY
        )

    @pytest.mark.parametrize('state,expected', [
        (STATE_TOMATO, 'tomato'),
        (STATE_LONG_BREAK, 'long_break'),
        (STATE_BREAK, 'break'),
    ])
    def test_convertState(self, state, expected):
        assert expected == CommandExecutor._convertState(state)


def test_addCustomFont(monkeypatch):
    mqt_gui = Mock()
    monkeypatch.setattr('CherryTomato.utils.QtGui', mqt_gui)

    addCustomFont()

    addApplicationFont = mqt_gui.QFontDatabase().addApplicationFont
    addApplicationFont.assert_called_once_with(
        os.path.join(BASE_DIR, 'media', 'NotoSans-Regular.ttf')
    )


def test_CompactFormatter(monkeypatch):
    mformat = Mock()
    monkeypatch.setattr('CherryTomato.utils.logging.Formatter.format', mformat)
    mrecord = Mock()
    mrecord.name = 'first.second.third'

    CompactFormatter().format(mrecord)

    mformat.assert_called_once_with(mrecord)
    assert 'third' == mrecord.name


@pytest.fixture
def mgetLogger(monkeypatch):
    mlogger = Mock()
    monkeypatch.setattr('CherryTomato.utils.logging.getLogger', mlogger)
    return mlogger


def test_makeLogger(mgetLogger):
    result = makeLogger('dummy', handler='my_handler', level='MY_INFO')

    assert mgetLogger() == result
    mgetLogger().addHandler.assert_called_with('my_handler')
    mgetLogger().setLevel.assert_called_with('MY_INFO')
    assert False is mgetLogger().propagate


def test_classLogger(mgetLogger):
    result = classLogger('my_path', 'my_class')

    mgetLogger.assert_called_with('my_path')
    mgetLogger().getChild.assert_called_with('my_class')
    assert mgetLogger().getChild() == result
