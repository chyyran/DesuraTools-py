import sys
import os
import subprocess
import imp
import site
import distutils.dir_util
import shutil


def build(args=['-y', '--onedir', '--clean', '--windowed', '--icon="icons/desuratools.ico"', '--noupx', '--version-file=versioninfo.txt']):
    pyinstaller = os.path.join(site.getsitepackages()[0], "Scripts", "pyinstaller-script.py")
    dependencies = ['PySide', 'PIL', 'win32api', 'win32gui', 'win32ui', 'win32con', 'requests']
    imageformats = os.path.join(site.getsitepackages()[1], "PySide", "plugins", "imageformats")
    args.insert(0, 'desuratools.py')
    args.insert(0, pyinstaller)
    args.insert(0, "python")


    if not os.path.exists(pyinstaller):
        raise IOError("PyInstaller is required to build for windows")
    print "PyInstaller check passed"
    for module in dependencies:
        try:
            imp.find_module(module)
        except ImportError:
           raise ImportError("Dependency {0} is required".format(module))
    print "Dependency check passed"
    print "Building DesuraTools"
    subprocess.call(' '.join(args))

    print "Copying imageformat plugins"
    imageformats_dist = os.path.join(os.getcwd(), "dist", "desuratools", "imageformats")
    distutils.dir_util.copy_tree(imageformats, imageformats_dist, verbose=1)

    print "Copying icon"
    images_dist = os.path.join(os.getcwd(), "dist", "desuratools", "desuratools_256.png")
    shutil.copyfile("desuratools_256.png", images_dist)

    print "Use an SFX Archiving Program to create a one-file executable"
if __name__ == '__main__':
    build()
