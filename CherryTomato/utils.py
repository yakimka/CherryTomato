import logging
import os
import shlex
import subprocess

from PyQt5 import QtGui

from CherryTomato import BASE_DIR
from CherryTomato.settings import STATE_TOMATO, STATE_BREAK, STATE_LONG_BREAK


class CompactFormatter(logging.Formatter):
    """Leave class name only
    """

    def format(self, record):
        record.name = record.name.rpartition('.')[-1]
        return super().format(record)


def makeLogger(name, *, handler, level):
    """Create the root logger
    """
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


def classLogger(path, classname):
    """Return logger for a class
    """
    return logging.getLogger(path).getChild(classname)


class CommandExecutor:
    def __init__(self, settings):
        self.logger = classLogger(__name__, self.__class__.__name__)
        self.settings = settings

    def onStart(self, status):
        self._execute(self.settings.afterStartCommand, status)

    def onStop(self, status):
        self._execute(self.settings.afterStopCommand, status)

    def onStateChange(self, status):
        # Don't execute commands on reset
        if not status.tomatoes:
            return

        if status.state == STATE_TOMATO:
            self._execute(self.settings.onTomatoCommand, status)
        else:
            self._execute(self.settings.onBreakCommand, status)

    def _execute(self, command, status=None):
        if command:
            cmd_with_macros = self._applyMacros(command, status)
            try:
                subprocess.Popen(
                    shlex.split(cmd_with_macros),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT
                )
            except Exception:
                self.logger.exception(f'Error while executing command "{command}"', exc_info=True)

    @classmethod
    def _applyMacros(cls, cmd, status=None):
        if status:
            macros = {
                '{tomatoes}': str(status.tomatoes),
                '{state}': cls._convertState(status.state),
            }
            for key, value in macros.items():
                cmd = cmd.replace(key, value)

        return cmd

    @staticmethod
    def _convertState(state):
        states = {
            STATE_TOMATO: 'tomato',
            STATE_BREAK: 'break',
            STATE_LONG_BREAK: 'long_break'
        }

        return states[state]


def addCustomFont():
    fontDB = QtGui.QFontDatabase()
    fontDB.addApplicationFont(os.path.join(BASE_DIR, 'media', 'NotoSans-Regular.ttf'))
