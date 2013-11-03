#coding=utf-8
__author__ = 'ron975'
"""
This file is part of DesuraTools
"""
import shortcutmanager

manager = shortcutmanager.SteamShortcutManager("D:\Steam\userdata\81548059\config\shortcuts.vdf")


def insert_shortcut(name, exe):
    for shortcut in manager.shortcuts:
        if shortcut.appname == name:
            pass
    manager.add_shortcut(name, exe, os.path.dirname(exe))