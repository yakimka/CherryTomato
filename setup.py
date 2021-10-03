import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

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


with open(os.path.join(module.BASE_DIR, '..', 'README.md')) as f:
    readme = f.read()

setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Desktop Environment :: K Desktop Environment (KDE)',
        'Topic :: Utilities',
    ],
    url='https://github.com/yakimka/CherryTomato',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.6',
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={'gui_scripts': ['cherry_tomato = {0}.main:main'.format(module_name)]},
    package_data={'': ['media/*.*'], },
)
