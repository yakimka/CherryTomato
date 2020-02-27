class CommandExecutor:
    def __init__(self, settings):
        self.settings = settings

    def onStart(self):
        print(self.settings.afterStartCommand)

    def onStop(self):
        print(self.settings.afterStopCommand)
