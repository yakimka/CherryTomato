from unittest import mock
from unittest.mock import Mock

import pytest
from PyQt5.QtCore import QRectF

from CherryTomato.widget import QRoundProgressBar, QRoundProgressBar_


@pytest.fixture
def mock_qroundprogressbar_(mocker):
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.__init__')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setFormat')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setValue')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setBarStyle')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setOutlinePenWidth')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setDataPenWidth')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.setMaximumWidth')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.width')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.height')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.valueFormatChanged')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.rebuildDataBrushIfNeeded')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.drawBackground')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.drawBase')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.drawValue')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.drawInnerBackground')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.palette')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.calculateInnerRect')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.font')
    mocker.patch('CherryTomato.widget.QRoundProgressBar_.valueToText')


@pytest.fixture
def mock_qpainter(mocker):
    return mocker.patch('CherryTomato.widget.QPainter')


@pytest.fixture
def mock_qfontmetricsf(mocker):
    return mocker.patch('CherryTomato.widget.QFontMetricsF')


@pytest.fixture
def mock_qfont(mocker):
    return mocker.patch('CherryTomato.widget.QFont')


@pytest.fixture
def mock_qrectf(mocker):
    return mocker.patch('CherryTomato.widget.QRectF')


@pytest.fixture
def progressbar(mock_qroundprogressbar_, mock_qpainter):
    progressbar = QRoundProgressBar('parent')
    progressbar.m_value = 0
    progressbar.m_min = 0
    progressbar.m_max = 0
    return progressbar


def test_init(progressbar):
    QRoundProgressBar_.__init__.assert_called_once_with('parent')
    assert progressbar.useSystemFont is True
    assert '' == progressbar.m_second_format
    progressbar.setFormat.assert_called_once_with('')
    progressbar.setValue.assert_called_once_with(0)
    progressbar.setBarStyle.assert_called_once_with(QRoundProgressBar.BarStyle.LINE)
    progressbar.setOutlinePenWidth.assert_called_once_with(4)
    progressbar.setDataPenWidth.assert_called_once_with(4)


def test_resizeEvent(progressbar):
    progressbar.resizeEvent(Mock())

    progressbar.height.assert_called_once_with()
    progressbar.setMaximumWidth.assert_called_once_with(progressbar.height())


def test_setSecondFormat(progressbar):
    progressbar.setSecondFormat('new_format')

    assert 'new_format' == progressbar.m_second_format
    progressbar.valueFormatChanged.assert_called_once_with()


def test_setSecondFormat_same_value(progressbar):
    progressbar.m_second_format = 'new_format'
    progressbar.setSecondFormat('new_format')

    progressbar.valueFormatChanged.assert_not_called()


@pytest.fixture
def mock_for_paintEvent(mocker, progressbar):
    progressbar.width.return_value = 100
    progressbar.height.return_value = 200
    mocker.patch('CherryTomato.widget.QRoundProgressBar.drawTwoTexts')
    mocker.patch('CherryTomato.widget.QRoundProgressBar.calculateInnerRect',
                 return_value=('firstInnerRect', 'secondInnerRect', 'innerRadius'))


@pytest.mark.parametrize('width,height', [
    (100, 200),
    (200, 100),
])
def test_paintEvent(progressbar, mock_for_paintEvent, width, height):
    progressbar.width.return_value = width
    progressbar.height.return_value = height

    progressbar.paintEvent(Mock())

    progressbar.rebuildDataBrushIfNeeded.assert_called_once_with()
    progressbar.drawBackground.assert_called()
    progressbar.drawBase(mock.ANY, QRectF(1.0, 1.0, 98.0, 98.0))
    progressbar.drawValue.assert_called_once_with(mock.ANY, mock.ANY, 0, 0)
    assert 2 == progressbar.drawInnerBackground.call_count
    progressbar.drawInnerBackground.assert_any_call(mock.ANY, 'secondInnerRect')
    progressbar.drawInnerBackground.assert_any_call(mock.ANY, 'firstInnerRect')
    progressbar.drawTwoTexts.assert_called_once_with(
        mock.ANY,
        'firstInnerRect',
        'secondInnerRect',
        'innerRadius',
        0,
    )


@pytest.mark.parametrize('m_value,m_max,m_min,expected_delta', [
    (0, 100, 200, 0),
    (1, 100, 201, 0.505),
    (10, 500, 260, -0.96),
])
def test_paintEvent_delta(progressbar, mock_for_paintEvent, m_value, m_max, m_min, expected_delta):
    progressbar.m_value = m_value
    progressbar.m_max = m_max
    progressbar.m_min = m_min
    progressbar.paintEvent(Mock())

    progressbar.drawValue.assert_called_once_with(mock.ANY, mock.ANY, m_value, expected_delta)


def test_calculateInnerRect(progressbar):
    minnerRect = Mock()
    minnerRect.getRect.return_value = (100, 500, 200, 300)
    QRoundProgressBar_.calculateInnerRect.return_value = (minnerRect, 20)

    firstHeight = 300 * 0.7
    expected_first = QRectF(100, 500, 200, firstHeight)
    expected_second = QRectF(100, 500 + firstHeight, 200, 300 - firstHeight)
    assert (expected_first, expected_second, 20) == progressbar.calculateInnerRect(12.5)
    QRoundProgressBar_.calculateInnerRect.assert_called_once_with(12.5)


def test_drawTwoTexts_not_executed(progressbar, mock_qfont):
    progressbar.m_format = 0

    progressbar.drawTwoTexts(Mock(), Mock(), Mock(), 20, 21)

    mock_qfont().setPixelSize.assert_not_called()


@pytest.mark.parametrize('use_system_font,expected', [
    (True, 'SystemFont'),
    (False, 'Noto Sans'),
])
def test_drawTwoTexts_system_font(
        progressbar,
        mock_qfontmetricsf,
        mock_qrectf,
        mock_qfont,
        use_system_font,
        expected,
):
    progressbar.font = Mock(return_value='SystemFont')
    progressbar.m_format = 1
    progressbar.useSystemFont = use_system_font

    progressbar.drawTwoTexts(Mock(), Mock(), Mock(), 20, 21)

    mock_qfont.assert_called_once_with(expected)
    mock_qfont().setPixelSize.assert_called()
