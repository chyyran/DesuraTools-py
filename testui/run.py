#coding=utf-8
__author__ = 'ron975'
import webbrowser
from PIL import Image
from generatehtml import TestReport

import installedgames, steammanager

print "Options: report, steam"
options = raw_input()
if options == "report":
    print "What is your Desura username?"
    username = raw_input()
    try:
        print "Generating report"
        webbrowser.open(str(TestReport(username)))
    except Exception, e:
        print "Invalid Desura Username", e.message, e.args
if options == "steam":
    print "Adding games to steam"
    print "Which is your Steam Account?"
    manager = steammanager.choose_userdata_folder()
    for game in installedgames.get_games():
        if game.icon.lower().endswith("jpeg") or game.icon.lower().endswith("jpg"):
            Image.open(game.icon).save(game.icon+".png")
            game.icon += ".png"
        steammanager.insert_shortcut(manager, game.name, game.exe, icon=game.icon)
    manager.save()
    for shortcut in manager.shortcuts:
        print shortcut.appname