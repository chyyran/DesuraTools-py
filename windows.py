#coding=utf-8
import subprocess

import win32api
import win32gui
import win32ui
import win32con

from PIL import Image
__author__ = 'ron975'
"""
This file contains all the methods that require windows.
"""

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
    hdc.DrawIcon((0,0), small[0]) #draw the icon before getting bits
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


def close_steam():
    subprocess.call("taskkill /im steam.exe /f /t")
