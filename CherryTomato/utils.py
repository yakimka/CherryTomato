class CommandExecutor:
    def __init__(self, settings):
        self.settings = settings

    def onStart(self):
        print('start')

    def onStop(self):
        print('stop')
