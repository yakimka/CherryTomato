"""Easy to use, flexible PyQt5 Pomodoro Technique timer."""

import os

__author__ = 'yakimka'
__maintainer__ = __author__
__email__ = 'ss.yakim@gmail.com'
__license__ = 'GPL-3.0'
__version__ = '1.1.0'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
APP_ICON = os.path.join(MEDIA_DIR, 'icon.png')

ORGANIZATION_NAME = __author__
APPLICATION_NAME = 'CherryTomato'

__all__ = (
    '__author__',
    '__email__',
    '__license__',
    '__maintainer__',
    '__version__',
    'BASE_DIR',
    'MEDIA_DIR',
    'APP_ICON',
    'ORGANIZATION_NAME',
    'APPLICATION_NAME',
)
