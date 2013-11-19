#coding=utf-8
__author__ = 'ron975'
import webbrowser

from generatehtml import DesuraReport
import icons
import installedgames
import steam

class TextUI:
    def __init__(self):
        print "Options: report, steam"
        options = raw_input()
        if options == "report":
            print "What is your Desura username?"
            username = raw_input()
            try:
                print "Generating report"
                webbrowser.open(str(DesuraReport(username)))
            except Exception, e:
                print "Invalid Desura Username", e.message, e.args
        if options == "steam":
            print "Adding games to steam"
            print "Which is your Steam Account?"
            manager = steam.choose_userdata_folder()
            for game in installedgames.get_games():
                game.icon = icons.choose_icon(game)
                steam.insert_shortcut(manager, game.name, game.exe, icon=game.icon)
            manager.save()
            for shortcut in manager.shortcuts:
                print shortcut.appname


def run():
    TextUI()

if __name__ == "__main__":
    run()

