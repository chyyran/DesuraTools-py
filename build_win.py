import sys
import os
import subprocess
import imp
import site
import distutils.dir_util
import shutil
import sfx_win


def build(buildargs=['-y', '-windowed', '--onedir', '--clean', '--icon="icons/desuratools.ico"', '--noupx', '--version-file=versioninfo.txt'], package=True):
    pyinstaller = os.path.join(site.getsitepackages()[0], "Scripts", "pyinstaller-script.py")
    dependencies = ['PySide', 'PIL', 'win32api', 'win32gui', 'win32ui', 'win32con', 'requests']
    imageformats = os.path.join(site.getsitepackages()[1], "PySide", "plugins", "imageformats")
    buildargs.insert(0, 'desuratools.py')
    buildargs.insert(0, pyinstaller)
    buildargs.insert(0, "python")
    dist_folder = os.path.join(os.getcwd(), "dist")
    output_folder = os.path.join(os.getcwd(), "dist", "desuratools")

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
    subprocess.call(' '.join(buildargs))

    print "Copying imageformat plugins"
    imageformats_dist = os.path.join(output_folder, "imageformats")
    distutils.dir_util.copy_tree(imageformats, imageformats_dist, verbose=1)

    print "Copying icon"
    images_dist = os.path.join(output_folder, "desuratools_256.png")
    shutil.copyfile("desuratools_256.png", images_dist)

    if package:
        package_app(dist_folder, output_folder)


def package_app(dist_folder, build_folder, output="DesuraTools"):
    output7z = os.path.join(dist_folder, output + ".7z")
    outputexe = os.path.join(dist_folder, output + ".exe")
    buildfiles = os.path.join(build_folder, "*")

    print "Building SFX Executable"
    print "Archiving built files"
    subprocess.call(' '.join([sfx_win.archiver, 'a', '-t7z', output7z, buildfiles]))

    print "Concatenating SFX header"
    output = open(outputexe, 'wb')
    shutil.copyfileobj(open(sfx_win.sfxheader, 'rb'), output)
    shutil.copyfileobj(open(sfx_win.sfxconfig, 'rb'), output)
    shutil.copyfileobj(open(output7z, 'rb'), output)
    output.close()

    print "Complete"
if __name__ == '__main__':
    build()
