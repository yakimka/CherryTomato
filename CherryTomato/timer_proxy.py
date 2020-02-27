from collections import namedtuple

ColorPalette = namedtuple('ColorPalette', 'base highlight')


class AbstractTimerProxy:
    def __init__(self, timer):
        self.timer = timer
        self.onStart = self.timer.onStart
        self.onStop = self.timer.onStop
        self.onStateChange = self.timer.onStateChange
        self.onChange = self.timer.onChange
        self.finished = self.timer.finished

    def isRunning(self) -> bool:
        raise NotImplementedError

    def getColorPalette(self) -> ColorPalette:
        raise NotImplementedError

    def getUpperText(self) -> str:
        raise NotImplementedError

    def getBottomText(self) -> str:
        raise NotImplementedError

    def getProgress(self) -> int:
        raise NotImplementedError

    def onAction(self) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    def onSettingsChange(self) -> None:
        raise NotImplementedError


class TomatoTimerProxy(AbstractTimerProxy):
    def isRunning(self) -> bool:
        return self.timer.running

    def onAction(self) -> None:
        if not self.timer.running:
            self.timer.start()
        else:
            self.timer.abort()

    def reset(self) -> None:
        self.timer.reset()

    def onSettingsChange(self) -> None:
        self.timer.onSettingsChange()

    def getUpperText(self) -> str:
        minutes, seconds = int(self.timer.seconds // 60), int(self.timer.seconds % 60)
        return f'{minutes:02d}:{seconds:02d}'

    def getBottomText(self) -> str:
        tomatoSign = '🍅'
        return f'{tomatoSign}x{self.timer.tomatoes}'

    def getProgress(self) -> int:
        return self.timer.progress

    def getColorPalette(self) -> ColorPalette:
        if self.timer.isTomato():
            return self._tomatoColor()
        else:
            return self._breakColor()

    def _tomatoColor(self) -> ColorPalette:
        # https://coolors.co/eff0f1-d11f2a-8da1b9-95adb6-fad0cf
        lightRed = (249, 192, 191)
        red = (255, 37, 51)
        return ColorPalette(lightRed, red)

    def _breakColor(self) -> ColorPalette:
        # https://coolors.co/b5ffe1-3cbb6f-b0ecc1-4e878c-00241b
        lightGreen = (176, 236, 193)
        green = (60, 187, 111)
        return ColorPalette(lightGreen, green)
