import shlex
import subprocess

from CherryTomato.settings import STATE_TOMATO, STATE_BREAK, STATE_LONG_BREAK


class CommandExecutor:
    def __init__(self, settings):
        self.settings = settings

    def onStart(self, status):
        self._execute(self.settings.afterStartCommand, status)

    def onStop(self, status):
        self._execute(self.settings.afterStopCommand, status)

    def onStateChange(self, status):
        if status.state == STATE_TOMATO:
            self._execute(self.settings.onTomatoCommand, status)
        else:
            self._execute(self.settings.onBreakCommand, status)

    def _execute(self, command, status=None):
        if command:
            command = self._applyMacros(command, status)
            try:
                subprocess.Popen(
                    shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
            except Exception as e:
                print(e)

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
