from unittest.mock import Mock

import pytest

from CherryTomato.settings import (Option, MinutesOption, CherryTomatoSettings)


class TestOption:
    class_ = Option

    def setup_method(self):
        self.option = self.class_(
            'onoffer',
            True,
            type=bool,
            deleter=True,
            ui=True
        )

    def test_init(self):
        assert 'onoffer' == self.option.name
        assert self.option.default is True
        assert bool == self.option.type
        assert self.option.deleter is True
        assert self.option.ui is True

    def test_str(self):
        assert 'onoffer' == str(self.option)

    def test_toRepresentation(self):
        assert 1234 == self.class_.toRepresentation(1234)

    def test_toInternalValue(self):
        assert 'hello' == self.class_.toInternalValue('hello')

    @pytest.mark.parametrize('type_,expected', [
        (None, {}),
        (int, {'type': int}),
        (Exception, {'type': Exception}),
    ])
    def test_getTypeKwarg(self, type_, expected):
        option = self.class_('name', 10, type=type_)

        assert expected == option.getTypeKwarg()


class TestMinutesOption(TestOption):
    class_ = MinutesOption

    def test_toRepresentation(self):
        assert 10 == self.class_.toRepresentation(600)

    def test_toInternalValue(self):
        assert 1380 == self.class_.toInternalValue(23)


@pytest.fixture
def settings_moptions(settings):
    settings.options = [
        Option('opt1', 1, deleter=True),
        Option('opt2', 2),
        Option('opt3', 3, type=int),
    ]
    msettingsBackend = Mock()
    settings.settingsBackend = msettingsBackend
    return settings


class TestCherryTomatoSettings:
    def test_init(self, settings, mock_settings_backend):
        assert mock_settings_backend == settings.settingsBackend

    def test_createQT(self, mocker):
        mock_qsettings = mocker.patch('CherryTomato.settings.QSettings')

        settings = CherryTomatoSettings.createQT()

        assert mock_qsettings() == settings.settingsBackend

    def test__findOption(self, settings_moptions):
        assert 'opt2' == settings_moptions._findOption('opt2').name

    def test__findOption_not_existed(self, settings_moptions):
        assert settings_moptions._findOption('not_existed') is None

    def test_dunder_getattr(self, settings_moptions):
        result = settings_moptions.opt3
        mvalue = settings_moptions.settingsBackend.value

        mvalue.assert_called_once_with('opt3', 3, type=int)
        assert mvalue() == result

    def test_dunder_getattr_not_existed(self, settings_moptions):
        with pytest.raises(AttributeError,
                           match="'CherryTomatoSettings' object has no attribute 'not_existed'"):
            settings_moptions.not_existed

    def test_dunder_setattr(self, settings_moptions):
        msetValue = settings_moptions.settingsBackend.setValue
        settings_moptions.opt3 = 42

        msetValue.assert_called_once_with('opt3', 42)

    def test_dunder_setattr_not_existed(self, settings_moptions):
        msetValue = settings_moptions.settingsBackend.setValue
        settings_moptions.not_existed = 42

        msetValue.assert_not_called()
        assert 42 == settings_moptions.not_existed

    def test_dunder_delattr(self, settings_moptions):
        mremove = settings_moptions.settingsBackend.remove
        del settings_moptions.opt1

        mremove.assert_called_once_with('opt1')

    def test_dunder_delattr_deleter_false(self, settings_moptions):
        with pytest.raises(AttributeError):
            del settings_moptions.opt2

    def test_dunder_delattr_not_existed(self, settings_moptions):
        with pytest.raises(AttributeError):
            del settings_moptions.not_existed
