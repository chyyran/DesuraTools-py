#coding=utf-8
import subprocess
import os
import ctypes

import win32api
import win32gui
import win32ui
import win32con
import win32com.shell.shell
import win32com.shell.shellcon

from PIL import Image
__author__ = 'ron975'
"""
This file contains all the methods that require windows.
"""


def data_dir():
    appdata = os.getenv('APPDATA')
    if not os.path.exists(os.path.join(appdata, "desuratools")):
        os.mkdir(os.path.join(appdata, "desuratools"))
    return os.path.join(appdata, "desuratools")


def init_icon():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Ron975.DesuraTools")


def get_icon(exe):
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
    large, small = win32gui.ExtractIconEx(exe, 0)
    if len(small) == 0:
        return False
    win32gui.DestroyIcon(large[0])
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    icon_bmp = win32ui.CreateBitmap()
    icon_bmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(icon_bmp)
    hdc.DrawIcon((0, 0), small[0])  # draw the icon before getting bits
    icon_info = icon_bmp.GetInfo()
    icon_buffer = icon_bmp.GetBitmapBits(True)
    icon = Image.frombuffer('RGB', (icon_info['bmWidth'], icon_info['bmHeight']), icon_buffer, 'raw', 'BGRX', 0, 1)
    win32gui.DestroyIcon(small[0])
    return icon


def steam_running():
    try:
        if win32ui.FindWindow(None, "Steam"):
            return True
    except win32ui.error:
        return False


def get_desura_path():
    start_menu = win32com.shell.shell.SHGetSpecialFolderPath(0, win32com.shell.shellcon.CSIDL_COMMON_STARTMENU)
    return os.path.join(start_menu, "Programs", "Desura", "Desura.lnk")


def desura_running(username):
    try:
        if win32ui.FindWindow(None, "Desura Windows: {0}".format(username)):
            return True
    except win32ui.error:
        return False


def start_desura():
    subprocess.Popen('start /B "" "{0}"'.format(get_desura_path()), shell=True)


def close_steam():
    subprocess.call("taskkill /im steam.exe /f /t")
