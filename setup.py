from setuptools import setup

setup(name='CherryTomato',
      author='yakimka',
      version='0.4.0',
      packages=['CherryTomato'],
      install_requires=['PyQt5', 'qroundprogressbar'],
      url='https://github.com/yakimka/CherryTomato',
      license='GPL',
      entry_points={'gui_scripts': ['cherry_tomato = CherryTomato.main']},
      package_data={
            '': ['media/*.*'],
      })
