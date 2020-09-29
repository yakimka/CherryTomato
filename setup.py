import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages
from setuptools import setup

module_name = 'CherryTomato'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    url='https://github.com/yakimka/CherryTomato',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.6',
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={'gui_scripts': ['cherry_tomato = {0}.main:main'.format(module_name)]},
    package_data={'': ['media/*.*'], },
)
