#coding=utf-8
__author__ = 'ron975'
import webbrowser


class DesuraGame:
    def __init__(self, shortname, name, icon):
        """
        Represents a game on Desura.com
        :param shortname: Short name of the game
        :param name: Full name of the game
        :param icon: Icon URL of the game
        """
        self.shortname = shortname
        self.name = name
        self.icon = icon

    def install(self):
        print "Installing", self.shortname
        webbrowser.open("desura://install/games/{0}/".format(self.shortname))

    def uninstall(self):
        print "Uninstalling", self.shortname
        webbrowser.open("desura://uninstall/games/{0}/".format(self.shortname))

    def verify(self):
        print "Verifying", self.shortname
        webbrowser.open("desura://verify/games/{0}/".format(self.shortname))

    def storepage(self):
        webbrowser.open("http://desura.com/games/{0}".format(self.shortname))

class InstalledGame(DesuraGame):
    def __init__(self, shortname, name, exe, icon):
        """
        Represents a Desura game that is installed locally on the system.
        This does not include mods.
        :param shortname: Short name of the game
        :param name: Full name of the game
        :param exe: EXE path of the game
        :param icon: Icon path of the game
        """
        self.shortname = shortname
        self.name = name
        self.exe = exe
        self.icon = icon

    def install(self):
        raise NotImplementedError()