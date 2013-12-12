"""
Used for building an SFX archive and creating a single executable during build
"""
import os

sfxpath = os.path.dirname(os.path.realpath(__file__))
sfxconfig = os.path.join(sfxpath, "sfxconfig")
sfxheader = os.path.join(sfxpath, "7zsd.sfx")
archiver = os.path.join(sfxpath, "7za.exe")