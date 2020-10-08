import pytest

from CherryTomato import main

pytestmark = pytest.mark.usefixtures('mock_objects')


@pytest.fixture
def mock_objects(mocker):
    mocker.patch.object(main, 'QIcon')
    mocker.patch.object(main, 'QSystemTrayIcon')
    mocker.patch.object(main, 'QMenu')
    mocker.patch.object(main, 'QAction')
    mocker.patch.object(main, 'QCoreApplication')
    mocker.patch.object(main, 'Qt')
    mocker.patch.object(main, 'CherryTomatoSettings')
    mocker.patch.object(main, 'addCustomFont')
    mocker.patch.object(main, 'TomatoTimer')
    mocker.patch.object(main, 'TomatoTimerProxy')
    mocker.patch.object(main, 'CommandExecutor')
    mocker.patch.object(main, 'CherryTomatoMainWindow')


def test_set_tray_icon():
    main.main()

    main.QSystemTrayIcon.assert_called()


def test_not_set_tray_icon():
    main.CherryTomatoSettings.createQT().showTrayIcon = False

    main.main()

    main.QSystemTrayIcon.assert_not_called()


def test_use_system_font():
    main.CherryTomatoSettings.createQT().useSystemFont = True

    main.main()

    main.addCustomFont.assert_not_called()


def test_not_use_system_font():
    main.CherryTomatoSettings.createQT().useSystemFont = False

    main.main()

    main.addCustomFont.assert_called()
