from setuptools import setup

from CherryTomato import VERSION

setup(
    name='CherryTomato',
    author='yakimka',
    version=VERSION,
    packages=['CherryTomato'],
    python_requires='>=3.6',
    install_requires=['PyQt5', 'qroundprogressbar'],
    extras_require={
        'dev': [
            'pytest',
            'pytest-qt',
            'pytest-mock',
            'flake8',
        ]
    },
    url='https://github.com/yakimka/CherryTomato',
    license='GPL',
    entry_points={'gui_scripts': ['cherry_tomato = CherryTomato.main:main']},
    package_data={'': ['media/*.*'], },
)
