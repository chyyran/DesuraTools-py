#coding=utf-8
__author__ = 'ron975'
__version__ = '1.0'
import sys
import webbrowser
import urllib
import socket
import httplib

from PySide.QtGui import QMainWindow, QApplication, QListWidgetItem, QAbstractItemView, QPixmap, QMenu
from PySide.QtGui import QAction, QMessageBox, QCursor
from PySide.QtCore import Qt

import icons
import steammanager
import installedgames
import gameslist

from generatehtml import DesuraReport
from qtui.ui_mainform import Ui_MainWindow
from steam import steam_user_manager, steam_shortcut_manager


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = app
        self.setupUi(self)
        boldfont = QApplication.font()
        boldfont.setBold(True)

        self.installAction_action = QAction("Add to Steam", self)
        self.installAction_action.setFont(boldfont)
        self.installAction_action.activated.connect(self.process_install_action)

        self.desuraPage_action = QAction("Open Desura Page", self)
        self.desuraPage_action.activated.connect(self.open_desura_page)

        self.gameContext_menu = QMenu(self)
        self.gameContext_menu.addAction(self.installAction_action)
        self.gameContext_menu.addAction(self.desuraPage_action)

        self.desuraAccountName_verify.clicked.connect(self.populate_owned_games)
        self.installButton.clicked.connect(self.process_install_button)
        self.generateDesuraReport_action.activated.connect(self.generate_report)
        self.tabWidget.currentChanged.connect(self.swap_tabs)
        self.ownedGames_list.currentItemChanged.connect(self.update_gameinfo)
        self.installedGames_list.currentItemChanged.connect(self.update_gameinfo)
        self.refreshButton.clicked.connect(self.refresh_lists)
        self.installedGames_list.customContextMenuRequested.connect(self.show_game_context)
        self.installedGames_list.doubleClicked.connect(self.process_install_action)

        self.installedGames_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ownedGames_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.steamID_input.addItems(steammanager.get_customurls_on_machine())
        self.ownedGames_list.addItem("Verify your Desura Account Name to see your owned games")

        self.populate_installed_games()

    def qpixmap_from_url(self, url):
            img_data = urllib.urlopen(url).read()
            itemicon = QPixmap()
            itemicon.loadFromData(img_data)
            return itemicon

    def generate_report(self):
        username = self.desuraAccountName_input.text()
        webbrowser.open(str(DesuraReport(username)))

    def populate_qlistwidget(self, game, qlistwidget, iconurls=False):
           if iconurls:
               itemicon = self.qpixmap_from_url(game.icon)
               self.app.processEvents()
           else:
               itemicon = QPixmap(game.icon)
           item = QListWidgetItem(itemicon, game.name, qlistwidget)
           item.setData(Qt.UserRole, game)
           qlistwidget.addItem(item)

    def populate_owned_games(self):
        username = self.desuraAccountName_input.text()
        self.ownedGames_list.clear()
        try:
            for game in gameslist.GamesList(username).get_games():
                self.populate_qlistwidget(game, self.ownedGames_list, True)
                self.statusBar.showMessage("Added Game {0}".format(game.name))
        except Exception:
            self.statusBar.showMessage("Invalid Desura Name")
        self.ownedGames_list.customContextMenuRequested.connect(self.show_game_context)
        self.ownedGames_list.doubleClicked.connect(self.process_install_action)

    def populate_installed_games(self):
        for game in installedgames.get_games():
            self.populate_qlistwidget(game, self.installedGames_list)

    def swap_tabs(self):
        gamelist = self.get_current_list()
        if gamelist[1] == 0:
            self.installButton.setText("Add Selected to Steam")
            self.installAction_action.setText("Add to Steam")
        if gamelist[1] == 1:
            self.installAction_action.setText("Install")
            self.installButton.setText("Install Selected")
        self.gameIcon_label.clear()
        self.gameName_label.clear()
        self.gameShortName_label.clear()

    def process_install_button(self):
        gamelist = self.get_current_list()
        if gamelist[1] == 1:
            for item in self.ownedGames_list.selectedItems():
                self.statusBar.showMessage(' '.join(["Installing", game.name]))
                game = item.data(Qt.UserRole)
                game.install()
        if gamelist[1] == 0:
            for item in self.installedGames_list.selectedItems():
                game = item.data(Qt.UserRole)
                game.icon = icons.choose_icon(game)[0]
                steammanager.insert_shortcut(self.get_steam_manager(), game.name, game.exe, game.icon)
                self.statusBar.showMessage(' '.join(["Added", game.name, 'to Steam']))
            self.get_steam_manager().save()

    def process_install_action(self):
        gamelist = self.get_current_list()
        game = gamelist[0].currentItem().data(Qt.UserRole)
        if gamelist[1] == 1:
            self.statusBar.showMessage(' '.join(["Installing", game.name]))
            game.install()
        if gamelist[1] == 0:
            game.icon = icons.choose_icon(game)[0]
            steammanager.insert_shortcut(self.get_steam_manager(), game.name, game.exe, game.icon)
            self.statusBar.showMessage(' '.join(["Added", game.name, 'to Steam']))
        self.get_steam_manager().save()
        self.statusBar.showMessage("Saved Steam Shortcut File")

    def get_steam_manager(self):
        steamid = steam_user_manager.steam_id_from_name(self.steamID_input.currentText())
        vdf = steam_user_manager.shortcuts_file_for_user_id(steamid)
        return steam_shortcut_manager.SteamShortcutManager(vdf)

    def update_gameinfo(self):
        gamelist = self.get_current_list()
        game = gamelist[0].currentItem().data(Qt.UserRole)
        self.gameName_label.setText(game.name)
        self.gameShortName_label.setText(game.shortname)

        if gamelist[1] == 0:
            self.gameIcon_label.setPixmap(QPixmap(game.icon))
        if gamelist[1] == 1:
            self.gameIcon_label.setPixmap(self.qpixmap_from_url(game.icon))

    def refresh_lists(self):
        gamelist = self.get_current_list()
        gamelist[0].clear()
        if gamelist[1] == 0:
            self.populate_installed_games()
        if gamelist[1] == 1:
            self.populate_owned_games()

    def open_desura_page(self):
        gamelist = self.get_current_list()[0]
        shortname = gamelist.currentItem().data(Qt.UserRole).shortname
        webbrowser.open("http://desura.com/games/{0}".format(shortname))

    def show_game_context(self):
        gamelist = self.get_current_list()[0]
        if gamelist.itemAt(gamelist.mapFromGlobal(QCursor.pos())) is gamelist.currentItem():
                self.gameContext_menu.exec_(QCursor.pos())

    def get_current_list(self):
        if self.tabWidget.currentIndex() == 0:
            return self.installedGames_list, 0
        if self.tabWidget.currentIndex() == 1:
            return self.ownedGames_list, 1


def run():
    app = QApplication(sys.argv)
    try:
        frame = MainWindow(app)
        frame.show()
        app.exec_()
    except (socket.gaierror, httplib.BadStatusLine):
        errorbox = QMessageBox()
        errorbox.setText("An internet connection is required to use DesuraTools")
        errorbox.setIcon(QMessageBox.Critical)
        errorbox.exec_()
    except Exception, e:
        errorbox = QMessageBox()
        errorbox.setText("An error occured when starting DesuraTools<br /><i>{0}</i>".format(e.message))
        errorbox.setIcon(QMessageBox.Critical)
        errorbox.exec_()
if __name__ == '__main__':
    run()
