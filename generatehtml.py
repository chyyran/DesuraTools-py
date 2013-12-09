#coding=utf-8
__author__ = 'ron975'

import installedgames
import gameslist
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class DesuraReport:
    def __init__(self, desuraname):
        self.desuraname = desuraname
        self.localgames = installedgames.get_games()
        self.ownedgames = gameslist.GamesList(desuraname).get_games()

    def table_local_games(self):
        tr = []
        tr_head = "<tr><th>#</th><th>Icon</th><th>Name</th><th>Short Name</th><th>EXE</th><th>Play</th><th>Desura Page</th></tr>"
        for  listindex, game in enumerate(self.localgames):
            listindex += 1
            index = "<td>{0}</td>".format(listindex)
            icon = "<td><img src='file:///{0}'></td>".format(game.icon)
            name = "<td>{0}</td>".format(game.name)
            shortname = "<td>{0}</td>".format(game.shortname)
            exe = "<td>{0}</td>".format(game.exe)
            play = "<td><a class='btn btn-success' href='desura://launch/games/{0}/'>Play</a></td>".format(game.shortname)
            desura = "<td><a class='btn btn-info' href='http://www.desura.com/games/{0}/'>Desura Page</a></td>".format(game.shortname)
            tr.append(''.join(['<tr>',index, icon, name, shortname, exe, play, desura, '</tr>']))

        return ''.join(["<table class='table table-striped table-hover table-condensed'>", tr_head, ''.join(tr), '<table>']), len(tr)

    def table_owned_games(self):
        tr = []
        tr_head = "<tr><th>#</th><th>Icon</th><th>Name</th><th>Short Name</th><th>Install</th><th>Desura Page</th></tr>"
        for listindex, game in enumerate(self.ownedgames):
            listindex += 1
            index = "<td>{0}</td>".format(listindex)
            icon = "<td><img src='{0}'></td>".format(game.icon)
            name = "<td>{0}</td>".format(game.name)
            shortname = "<td>{0}</td>".format(game.shortname)

            install = "<td><a class='btn btn-primary' href='desura://install/games/{0}/'>Install</a></td>".format(game.shortname)
            desura = "<td><a class='btn btn-info' href='http://www.desura.com/games/{0}/'>Desura Page</a></td>".format(game.shortname)
            tr.append(''.join(['<tr>',index, icon, name, shortname, install, desura, '</tr>']))

        return ''.join(["<table class='table table-striped table-hover table-condensed'>", tr_head, ''.join(tr), '<table>']), len(tr)

    def generate_html(self):
        desurareport = open("desurareport_{0}.html".format(id_generator()), "w")
        desurareport.write("<!DOCTYPE HTML><html>")
        desurareport.write('<head>')
        #bootstrap css
        desurareport.write('<link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.1/css/bootstrap.min.css" rel="stylesheet">')
        desurareport.write('<script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.1/js/bootstrap.min.js"></script>')
        desurareport.write("<link href='http://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'>")
        desurareport.write("<style type='text/css'>*{font-family: 'Roboto', sans-serif;}</style>")
        desurareport.write('<base target="_blank">')
        desurareport.write('</head><body>')
        desurareport.write("<h1>DesuraTools Report</h1>")
        desurareport.write("<b>Account: </b><a href='http://www.desura.com/members/{0}'>{0}</a>".format(self.desuraname))
        desurareport.write("<br/>")
        desurareport.write("<h2>Installed Games</h2>")
        desurareport.write("<b>Total Installed: </b>{0}".format(self.table_local_games()[1]))
        desurareport.write(self.table_local_games()[0])
        desurareport.write("<br/>")
        desurareport.write("<h2>Owned Games</h2>")
        desurareport.write("<b>Total Owned: </b>{0}".format(self.table_owned_games()[1]))
        desurareport.write(self.table_owned_games()[0])
        desurareport.write("</body></html>")
        desurareport.close()
        return desurareport.name

    def __repr__(self):
        return self.generate_html()


