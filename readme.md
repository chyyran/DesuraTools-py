![DesuraTools](https://raw.github.com/ron975/DesuraTools/master/icons/desuratools_banner.png)
==============
DesuraTools is a easy to use utility to help manage your Desura Library

Usage
-----
Simply run `desuratools.exe`. Ensure the `imageformats` folder containing dll libraries is in the same folder as `desuratools.exe`

[Desura](http://desura.com) must be installed for DesuraTools to work correctly. [Steam](http://store.steampowered.com/) must be instaled to be able to add games to Steam as a "Non-Steam Game"

Input your Desura username and press "Load Games". Ensure the correct Steam ID is selected. DesuraTools will automatically save your settings.
Note: **Private Desura profiles are unsupported. A Steam account must have been logged on at least once on your computer for it to show in the list**

You can select multiple games using CTRL, or the "Select All" button. Right-click on a game, or multipe games, for more options. 

Features
--------
  * Install/Uninstall/Verify multiple Desura games at once
  * Easily add your Desura games to your Steam library

Building
--------
Ensure that the [required dependencies](#Dependencies) are installed. Simply run build_win.py to build the program.

Dependencies
------------
DesuraTools requires Python 2.7, PyInstaller, PIL, PySide, Qt4.8, and pywin32 to build.
[list]
[*][Python 2.7](http://www.python.org/ftp/python/2.7/python-2.7.msi)
[*][Qt 4.8.5 (VS2008)](http://download.qt-project.org/official_releases/qt/4.8/4.8.5/qt-win-opensource-4.8.5-vs2008.exe)
[*][Python Imaging Library 1.1.7 for Python 2.7](http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe)
[*][pywin32 build 218](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py2.7.exe/download)
[/list]

For PySide and PyInstaller, it is recommended you install these libraries with pip. pip should be installed to the Scripts directory of your Python installation. pip can be installed from [here](https://bitbucket.org/pcarbonn/pipwin/downloads/pip-Win_1.6.exe).

Install PySide and PyInstaller with `pip install pyside` and `pip install pyinstaller` respectively.

Porting
-------
DesuraTools has been designed so that porting to OSX or Linux is extremely easy. Unfortunatley, I do not own an OSX or Linux machine, so I can not port the program myself. If you are interested, please feel free to fork DesuraTools.

Legal
-----
DesuraTools is licensed under GNU GPL v3.
Desura, Desurium, the Desura logo are trademarks of Linden Research, Inc. All other trademarks are property of their respective owners
