![DesuraTools](https://raw.github.com/ron975/DesuraTools/master/icons/desuratools_banner.png)
==============
DesuraTools is a utility that allows you to manage your Desura library of games.

Features
--------
-  User friendly interface
-  Batch processing of games - install/uninstall/verify multiple games at once
-  Generate an HTML report of all your games on Desura
-  **Easily add installed Desura games to Steam as a non-Steam game**
-  Open source and licensed under GPL v3 - https://github.com/ron975/DesuraTools/

Usage
-----
Simply start DesuraTools. All Desura games that are currently installed will be listed under 'Installed Desura Games'. The games you own on Desura will be loaded from your profile when you verify your Desura account. 

DesuraTools requires Desura to be installed, and logged in at least once. To access Steam-related functions, Steam must also be installed.

###Batch install games from Desura
Simply input your Desura Profile ID [<sup>1</sup>](#1) in the text box, and click "Load Games".  DesuraTools will start Desura automatically and you must log into Desura to continue. After DesuraTools has confirmed you have been logged in[<sup>2</sup>](#2), it will start loading your games from your Desura profile[<sup>3</sup>](#3). They will be listed under the 'Owned Desura Games' tab. You can select one or more games and click "Install Selected" to install all the games you have selected. **Warning:** Installing too many games may crash Desura or your computer. 

###Adding games to Steam/Batch uninstalling/verifying games
All Desura games you have installed currently will be listed under 'Installed Desura Games'. The Steam IDs that have been logged on at least once will be displayed in t he dropdown box[<sup>4</sup>](#4), ensure the correct one is selected. Simply select one or more games from the list, and click "Add Selected to Steam", DesuraTools will automatically add the selected games to Steam, as a non-Steam game[<sup>5</sup>](#5). DesuraTools will check for duplicates: if the game already exists in the library as a Non-Steam Game, or if the Steam version of the game is owned, DesuraTools will skip over it.

###Generating an HTML report
Simply go into the File menu, and click "Generate Desura Report". Note that the icons under the "Owned Games" section will only be valid on the host computer as it makes use of file:// URLs. This feature is experimental.

###Usage Notes
######1
Your profile ID is not your Desura username. It can be found and changed under 'Profile ID' under 'Edit Profile'. It is 'the URL to access your profile (eg. http://www.desura.com/members/YOUR_URL)', and if you have not changed it, by default it is identical to your username. If you have set it to nothing, it starts with 'na'. If you have set it to something different than your username, enter that instead.

######2
DesuraTools does not require, can not access your Desura password. Desura for Windows sets its window title as "Desura Windows: username", where username is your Desura username, and DesuraTools listens for that window to open to detect whether Desura is running, and that you own the Desura account.

######3
Due to a lack of a proper API for Desura, DesuraTools scrapes your owned games from http://www.desura.com/members/profileid/games, where profileid is your Desura profileid. Thus, DesuraTools only works with profiles that are accessible to the public, i.e. 'Everyone can see my profile', or 'Everyone can see my profile, but my comment history is hidden', will work fine as well. You can temporarily set your profile to public while using DesuraTools.

######4
Any Steam ID that does not have a custom URL set will be displayed as "ID64:SteamID64", where SteamID64 is the SteamID64 for the account. It is recommended that a custom URL is set.

######5
DesuraTools makes use of various algorithms to determine the icon that will be set when adding to the Steam library. If the icon of the game executable is similar to the icon provided to Desura, it will opt to use the game's in-built icon, as then the icon will show properly on the jumplist. However, if the game executable icon is different than the icon on the game's Desura page, DesuraTools will add the icon provided to Desura rather than from the game executable. This is to accomodate games that do not have a proper icon set on their executable for various reasons, such as some small indie games using the unlicensed version of UDK.

***

Building
--------
Ensure that the [required dependencies](#dependencies) are installed. Simply run build_win.py to build the program. 
By default, it will also package the app into a single executable using 7zsd.sfx (LZMA compression)

You may use [Resource Hacker](http://www.angusj.com/resourcehacker/) to insert the correct resources located in the `resources_win` folder: icons (`icons.res`) and version information (`version.res`). Note that you will have to manually update the correct version number, the included compiled resource has it's `FileVersion` and `ProductVersion` set at 1.0.0.39.

Dependencies
------------
DesuraTools requires Python 2.7, PyInstaller, PIL, PySide, Qt4.8, requests, and pywin32 to build.

- [Python 2.7](http://www.python.org/ftp/python/2.7/python-2.7.msi)
- [Qt 4.8.5 (VS2008)](http://download.qt-project.org/official_releases/qt/4.8/4.8.5/qt-win-opensource-4.8.5-vs2008.exe)
- [Python Imaging Library 1.1.7 for Python 2.7](http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe)
- [pywin32 build 218](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py2.7.exe/download)


For PySide, requests and PyInstaller, it is recommended you install these libraries with pip. pip should be installed to the Scripts directory of your Python installation. pip can be installed from [here](https://bitbucket.org/pcarbonn/pipwin/downloads/pip-Win_1.6.exe).

Install PySide, PyInstaller and requests with `pip install pyside`, `pip install pyinstaller` and `pip install requests` respectively.

Porting
-------
DesuraTools has been designed so that porting to OSX or Linux is extremely easy. Simply remove or replace any windows specific functions, most of which are located in windows.py. Unfortunatley, I do not own an OSX or Linux machine, so I can not port the program myself. If you are interested, please feel free to fork DesuraTools.

***

Legal
-----
###Desura
>Desura, Desurium, the Desura logo are trademarks of Linden Research, Inc. All other trademarks are property of their respective owners

###Valve

>© 2013 Valve Corporation. Valve, the Valve logo, Half-Life, the Half-Life logo, the Lambda logo, Steam, the Steam logo, Team Fortress, the Team Fortress logo, Opposing Force, Day of Defeat, the Day of Defeat logo, Counter-Strike, the Counter-Strike logo, Source, the Source logo, Counter-Strike: Condition Zero, Portal, the Portal logo, Dota, the Dota 2 logo, and Defense of the Ancients are trademarks and/or registered trademarks of Valve Corporation.

_All other trademarks are property of their respective owners_

Licensing
---------
_DesuraTools is licensed under GNU GPL v3, and the source code is available at GitHub_

>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
>
>You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
