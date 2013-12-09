import sys
import os
from distutils.core import setup

setup(
    name='DesuraTools',
    version='1.0',
    packages=['ui', 'steamshortcut'],
    url='http://github.com/ron975/DesuraTools',
    license='GNU GPL v3',
    author='ron975',
    author_email='ronny@punyman.com',
    description='Desura Library Management',
    platforms='Windows',
    requires=['PySide', 'pywin32', 'PIL'],
    windows=[{'script':'__main__.py'}]
)
