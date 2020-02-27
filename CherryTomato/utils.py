import shlex
import subprocess

from CherryTomato.settings import STATE_TOMATO


class CommandExecutor:
    def __init__(self, settings):
        self.settings = settings

    def onStart(self, status):
        print('start', status)
        self._execute(self.settings.afterStartCommand)

    def onStop(self, status):
        print('stop', status)
        self._execute(self.settings.afterStopCommand)

    def onStateChange(self, status):
        print('state', status)
        if status.state == STATE_TOMATO:
            self._execute(self.settings.onTomatoCommand)
        else:
            self._execute(self.settings.onBreakCommand)

    def _execute(self, command):
        if command:
            try:
                subprocess.Popen(
                    shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
            except Exception as e:
                print(e)
