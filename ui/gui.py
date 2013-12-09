#coding=utf-8
from ui.guihelpers import *

__author__ = 'ron975'
__version__ = '1.0'
import sys
import webbrowser
import urllib
import socket
import httplib
import json
import os

from PySide.QtGui import QMainWindow, QApplication, QListWidgetItem, QAbstractItemView, QPixmap, QMenu
from PySide.QtGui import QAction, QMessageBox, QCursor
from PySide.QtCore import Qt

import icons
import steamutils
import installedgames
import gameslist
import windows

from generatehtml import DesuraReport
from ui.ui_mainform import Ui_MainWindow

from steamshortcut import steam_user_manager, steam_shortcut_manager


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = app
        self.current_username = ""
        self.setupUi(self)
        self.logger = get_logger('desuratools', 'desuratools.log')
        self.logger.info('Logger Created')
        boldfont = QApplication.font()
        boldfont.setBold(True)
        self.addToSteam_action = self.action_factory("Add to Steam", self.add_to_steam)
        self.addToSteam_action.setFont(boldfont)

        self.installGame_action = self.action_factory("Install", self.install_game)
        self.installGame_action.setFont(boldfont)

        self.desuraPage_action = self.action_factory("View Profile", self.open_desura_page)
        self.uninstallGame_action = self.action_factory("Uninstall", self.uninstall_game)
        self.verifyGame_action = self.action_factory("Verify", self.verify_game)

        self.ownedGames_menu = QMenu(self)
        self.ownedGames_menu.addActions([
            self.installGame_action,
            self.desuraPage_action
        ])

        self.installedGames_menu = QMenu(self)
        self.installedGames_menu.addActions([
            self.addToSteam_action,
            self.desuraPage_action,
            self.uninstallGame_action,
            self.verifyGame_action
        ])

        self.selectAllButton.clicked.connect(self.select_all_games)
        self.desuraAccountName_verify.clicked.connect(self.populate_owned_games)
        self.installButton.clicked.connect(self.process_install_button)
        self.generateDesuraReport_action.activated.connect(self.generate_report)
        self.tabWidget.currentChanged.connect(self.swap_tabs)
        self.ownedGames_list.itemSelectionChanged.connect(self.update_gameinfo)
        self.installedGames_list.itemSelectionChanged.connect(self.update_gameinfo)
        self.refreshButton.clicked.connect(self.refresh_list)
        self.refreshLists_action.activated.connect(self.refresh_all)

        self.installedGames_list.customContextMenuRequested.connect(self.show_game_context)
        self.installedGames_list.doubleClicked.connect(self.add_to_steam)

        self.installedGames_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ownedGames_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.steamID_input.addItems(steamutils.get_customurls_on_machine())
        self.ownedGames_list.addItem("Verify your Desura username to see your owned games")

        self.app.processEvents()
        self.loading_dialog = ProgressBarDialog()
        self.loading_dialog.show()
        self.app.processEvents()
        self.populate_installed_games()
        self.load_data()
        self.loading_dialog.close()
        self.raise_()

    def verify_user(self, username=None):
        if username is None:
            username=self.current_username
        if len(username) == 0:
            return False
        if windows.desura_running(username):
            return True
        verify_dialog = QMessageBox()
        verify_dialog.setText("<b>Verify your identity</b><br />Sign in to Desura to continue with account <b>{0}</b> to confirm your identity".format(username))
        verify_dialog.setInformativeText("<i>Waiting for Desura sign-in...</i>")
        verify_dialog.setWindowTitle("Sign into Desura to continue")
        verify_dialog.setStandardButtons(0)
        verify_dialog.setIcon(QMessageBox.Information)
        verify_dialog.addButton("Cancel", QMessageBox.RejectRole)
        verify_dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        desurawaiter = DesuraWaiter(username)
        desurawaiter.finished.connect(verify_dialog.close)
        desurawaiter.start()
        result = verify_dialog.exec_()
        if result == 0:
            desurawaiter.terminate()
            return False
        return True

    def load_data(self):
        try:
            with open(os.path.join(windows.data_dir(), 'desuratools.json'), 'r') as savefile:
                data = json.loads(savefile.read())
                if data['desuraname'] != "":
                    self.desuraAccountName_input.setText(data['desuraname'])
                    self.populate_owned_games()
                steamid = self.steamID_input.findText(data['steamname'])
                self.steamID_input.setCurrentIndex(steamid)
        except IOError:
            pass

    def closeEvent(self, *args, **kwargs):
        self.logger.info("Saving to file")
        savefile = open(os.path.join(windows.data_dir(), 'desuratools.json'), 'w')
        savefile.write(
                json.dumps({
                'desuraname': self.current_username,
                'steamname': self.steamID_input.currentText()
                })
        )
        savefile.close()

    def populate_qlistwidget(self, game, qlistwidget, iconurls=False):
           if iconurls:
               itemicon = self.qpixmap_from_url(game.icon)
               self.app.processEvents()
           else:
               itemicon = QPixmap(game.icon)
               self.app.processEvents()
           item = QListWidgetItem(itemicon, game.name, qlistwidget)
           item.setData(Qt.UserRole, game)
           qlistwidget.addItem(item)

    def populate_owned_games(self):
        self.statusBar.showMessage("Waiting for Desura... Please Wait")
        try:
            if not self.set_current_account():
                self.statusBar.showMessage("")
                return
            self.ownedGames_list.clear()
            self.loading_dialog.setAccount(self.current_username)
            self.app.processEvents()
            self.loading_dialog.setMaximum(len(gameslist.GamesList(self.current_username).get_games()))
            self.app.processEvents()
            for game in gameslist.GamesList(self.current_username).get_games():
                self.populate_qlistwidget(game, self.ownedGames_list, True)
                self.app.processEvents()
                self.loading_dialog.increment(1, game.name)
                self.app.processEvents()
                self.logger.info("Added Game {0}".format(game.name))
                self.statusBar.showMessage("Added Game {0}".format(game.name))
        except gameslist.PrivateProfileError:
            self.logger.error("Failed to load games -  Private Desura Profile")
            self.statusBar.showMessage("Failed to load games - Private Desura Profiles not supported")

            error_message(
                "The Desura Profile {0} is set to Private. <br/>DesuraTools works only with public Desura Profiles."
                .format(self.current_username)
            ).exec_()
            return

        except gameslist.NoSuchProfileError:
            self.logger.error("Failed to load games - Desura account not found")
            self.statusBar.showMessage("Failed to load games - Desura account not found")
            return
        except gameslist.InvalidDesuraProfileError:
            self.logger.error("Failed to load games - Desura account invalid")

        self.ownedGames_list.customContextMenuRequested.connect(self.show_game_context)
        self.ownedGames_list.doubleClicked.connect(self.install_game)
        self.logger.info("All owned Desura games loaded for account {0}".format(self.current_username))
        self.statusBar.showMessage("All owned Desura games loaded for account {0}".format(self.current_username))

    def set_current_account(self, username=None):
        if username is None:
            username = self.desuraAccountName_input.text()
        if not self.verify_user(username):
            return False
        try:
            gameslist.GamesList(username)
        except gameslist.InvalidDesuraProfileError:
            raise
        self.current_username = username
        self.logger.info("Set current username to {0}".format(self.current_username))
        self.setWindowTitle("DesuraTools - {0}".format(self.current_username))
        return True

    def populate_installed_games(self):
        for game in installedgames.get_games():
            self.populate_qlistwidget(game, self.installedGames_list)

    def swap_tabs(self):
        gamelist = self.get_current_list()
        if gamelist[1] == 0:
            self.installButton.setText("Add Selected to Steam")
        if gamelist[1] == 1:
            self.installButton.setText("Install Selected")
        self.gameIcon_label.clear()
        self.gameName_label.clear()
        self.gameShortName_label.clear()

    def show_game_context(self):
        gamelist = self.get_current_list()
        if gamelist[0].itemAt(gamelist[0].mapFromGlobal(QCursor.pos())) is gamelist[0].currentItem():
                if gamelist[1] == 0:
                    self.installedGames_menu.exec_(QCursor.pos())
                else:
                    self.ownedGames_menu.exec_(QCursor.pos())

    def process_install_button(self):
        gamelist = self.get_current_list()
        if gamelist[1] == 1:
            self.install_game()
        if gamelist[1] == 0:
            self.add_to_steam()
            self.get_steam_manager().save()

    def install_game(self):
        self.statusBar.showMessage("Sign into Desura to install")
        if not self.verify_user():
            self.statusBar.showMessage("Failed to verify user")
            return
        gamelist = self.get_current_list()
        if gamelist[1] == 1:
            for item in gamelist[0].selectedItems():
                game = item.data(Qt.UserRole)
                self.logger.info(' '.join(["Installing", game.name]))
                self.statusBar.showMessage(' '.join(["Installing", game.name]))
                game.install()

    def uninstall_game(self):
        self.statusBar.showMessage("Sign into Desura to uninstall")
        if not self.verify_user():
            self.statusBar.showMessage("Failed to verify user")
            return
        gamelist = self.get_current_list()
        if gamelist[1] == 0:
            if len(gamelist[0].selectedItems()) > 1:
                confirm_uninstall = user_choice(
                    "Are you sure you want to uninstall {0} games?".format(len(gamelist[0].selectedItems())),
                    "Confirm batch uninstallation",
                    QMessageBox.Information,
                    acceptbutton="Uninstall"
                )
                result = confirm_uninstall.exec_()
                if result is not QMessageBox.AcceptRole:
                    self.logger.info("Uninstall {0} games canceled".format(len(gamelist[0].selectedItems())))
                    self.statusBar.showMessage("Uninstall {0} games canceled".format(len(gamelist[0].selectedItems())))
                    return
            for item in gamelist[0].selectedItems():
                game = item.data(Qt.UserRole)
                self.logger.info(' '.join(["Uninstalling", game.name]))
                self.statusBar.showMessage(' '.join(["Uninstalling", game.name]))
                game.uninstall()

    def verify_game(self):
        self.statusBar.showMessage("Sign into Desura to verify")
        if not self.verify_user():
            self.statusBar.showMessage("Failed to verify user")
            return
        gamelist = self.get_current_list()
        if gamelist[1] == 0:
            for item in gamelist[0].selectedItems():
                game = item.data(Qt.UserRole)
                self.logger.info(' '.join(["Verifying", game.name]))
                self.statusBar.showMessage(' '.join(["Verifying", game.name]))
                game.verify()

    def add_to_steam(self):
        if not self.check_if_steam_running():
            return
        gamelist = self.get_current_list()
        if gamelist[1] == 0:
            for item in gamelist[0].selectedItems():
                game = item.data(Qt.UserRole)
                steamid = steam_user_manager.communityid64_from_name(self.steamID_input.currentText())
                self.app.processEvents()
                if not steamutils.check_steam_version(steamid, game.name):
                    if not steamutils.shortcut_exists(self.get_steam_manager(), game.name):
                        steamutils.insert_shortcut(self.get_steam_manager(), game.name, game.exe, icons.choose_icon(game))
                        self.statusBar.showMessage("Added {0} to the Steam library".format(game.name))
                        self.app.processEvents()
                    else:
                        self.statusBar.showMessage("{0} already exists in the Steam library".format(game.name))
                        self.app.processEvents()
                else:
                    self.statusBar.showMessage("You already own the Steam version of {0}".format(game.name))
                    self.app.processEvents()

    def get_steam_manager(self):
        steamid = steam_user_manager.communityid32_from_name(self.steamID_input.currentText())
        vdf = steam_user_manager.shortcuts_file_for_user_id(steamid)
        return steam_shortcut_manager.SteamShortcutManager(vdf)

    def update_gameinfo(self):
        gamelist = self.get_current_list()
        if len(gamelist[0].selectedItems()) == 1:
            game = gamelist[0].currentItem().data(Qt.UserRole)
            self.gameName_label.setText(game.name)
            self.gameShortName_label.setText(game.shortname)

            if gamelist[1] == 0:
                self.gameIcon_label.setPixmap(QPixmap(game.icon))
            if gamelist[1] == 1:
                self.gameIcon_label.setPixmap(self.qpixmap_from_url(game.icon))
        else:
            self.gameName_label.setText("{0} Items Selected".format(str(len(gamelist[0].selectedItems()))))
            self.gameIcon_label.clear()
            self.gameShortName_label.clear()

    def refresh_list(self):
        gamelist = self.get_current_list()
        gamelist[0].clear()
        if gamelist[1] == 0:
            self.populate_installed_games()
        if gamelist[1] == 1:
            self.populate_owned_games()

    def refresh_all(self):
        self.installedGames_list.clear()
        self.ownedGames_list.clear()
        self.populate_installed_games()
        self.populate_owned_games()

    def select_all_games(self):
        self.get_current_list()[0].selectAll()

    def open_desura_page(self):
        gamelist = self.get_current_list()
        for item in gamelist[0].selectedItems():
            game = item.data(Qt.UserRole)
            game.storepage()

    def get_current_list(self):
        if self.tabWidget.currentIndex() == 0:
            return self.installedGames_list, 0
        if self.tabWidget.currentIndex() == 1:
            return self.ownedGames_list, 1

    def check_if_steam_running(self):
        if windows.steam_running():
            self.statusBar.showMessage("Steam is currently running")

            ask_close_steam = user_choice(
                "<b>Steam is currently running</b><br />Please close Steam before adding a game",
                "Close Steam before continuing",
                QMessageBox.Warning,
                acceptbutton="Close Steam"
                )
            result = ask_close_steam.exec_()

            if result == QMessageBox.AcceptRole:
                self.logger.info("Waiting for Steam to close")
                self.statusBar.showMessage("Waiting for Steam to close")
                windows.close_steam()
                return True
            else:
                self.logger.error("Could not add game to Steam - Steam still running")
                self.statusBar.showMessage("Add to Steam cancelled")
                return False
        else:
            return True

    def generate_report(self):
        if len(self.current_username) == 0:
            self.statusBar.showMessage("Please enter your Desura username")
            return
        self.logger.info("Generating Report")
        self.statusBar.showMessage("Generating Report")
        webbrowser.open(str(DesuraReport(self.current_username)))

    def action_factory(self, text, connect):
        action = QAction(text, self)
        action.activated.connect(connect)
        return action

    @staticmethod
    def qpixmap_from_url(url):
            img_data = urllib.urlopen(url).read()
            itemicon = QPixmap()
            itemicon.loadFromData(img_data)
            return itemicon

def run():
    windows.init_icon()
    windows.data_dir()
    app = QApplication(sys.argv)
    try:
        frame = MainWindow(app)
        frame.show()
        app.exec_()
    except (socket.gaierror, httplib.BadStatusLine):
        error_message("An internet connection is required to use DesuraTools").exec_()
        raise
    except Exception, e:
        error_message("An error occured when starting DesuraTools<br /><i>{0}</i>".format(e)).exec_()
        raise

if __name__ == '__main__':
    print "Please run from desuratools.py"
