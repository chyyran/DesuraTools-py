#coding=utf-8
__author__ = 'ron975'
__version__ = '1.0'
import sys
import webbrowser
import urllib
import socket
import httplib
import json
import logging

from PySide.QtGui import QMainWindow, QApplication, QListWidgetItem, QAbstractItemView, QPixmap, QMenu, QStyle, QDialog
from PySide.QtGui import QAction, QMessageBox, QCursor, QIcon
from PySide.QtCore import Qt

import icons
import steamutils
import installedgames
import gameslist
import windows

from generatehtml import DesuraReport
from ui.ui_mainform import Ui_MainWindow
from ui.ui_progressbar import Ui_ProgressBar

from steam import steam_user_manager, steam_shortcut_manager


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = app
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

        self.loading_dialog = ProgressBarDialog()
        self.loading_dialog.show()
        self.app.processEvents()
        self.populate_installed_games()
        self.load_data()
        self.loading_dialog.setText("<b>Verify your identity</b>")
        self.loading_dialog.setInformativeText("Sign in to Desura to continue")
        self.loading_dialog.setWindowTitle("Sign into Desura to continue")
        self.loading_dialog.setAccount(self.desuraAccountName_input.text(), "with")
        self.app.processEvents()
        self.wait_for_desura()
        self.loading_dialog.close()
        self.raise_()

    def load_data(self):
        try:
            with open('../desuratools.json', 'r') as savefile:
                data = json.loads(savefile.read())
                if data['desuraname'] != "":
                    self.desuraAccountName_input.setText(data['desuraname'])
                    self.populate_owned_games()
                steamid = self.steamID_input.findText(data['steamname'])
                self.steamID_input.setCurrentIndex(steamid)
        except:
           pass

    def closeEvent(self, *args, **kwargs):
        self.logger.info("Saving to file")
        savefile = open('../desuratools.json', 'w')
        savefile.write(
                json.dumps({
                'desuraname': self.desuraAccountName_input.text(),
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
        username = self.desuraAccountName_input.text()
        self.ownedGames_list.clear()
        try:
            self.loading_dialog.setAccount(username)
            self.app.processEvents()
            self.loading_dialog.setMaximum(len(gameslist.GamesList(username).get_games()))
            self.app.processEvents()
            for game in gameslist.GamesList(username).get_games():
                self.populate_qlistwidget(game, self.ownedGames_list, True)
                self.loading_dialog.increment(1)
                self.app.processEvents()
                self.logger.info("Added Game {0}".format(game.name))
                self.statusBar.showMessage("Added Game {0}".format(game.name))
        except gameslist.PrivateProfileError:
            self.logger.error("Private Desura Profile")
            self.statusBar.showMessage("Private Desura Profile not supported")

            error_message(
                "The Desura Profile {0} is set to Private. <br/>DesuraTools works only with public Desura Profiles."
                .format(username)
            ).exec_()

        except Exception:
            self.logger.error("Invalid Desura Name")
            self.statusBar.showMessage("Invalid Desura Name")
        self.ownedGames_list.customContextMenuRequested.connect(self.show_game_context)
        self.ownedGames_list.doubleClicked.connect(self.install_game)
        self.logger.info("All owned Desura games loaded for account {0}".format(username))
        self.statusBar.showMessage("All owned Desura games loaded for account {0}".format(username))

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
        self.statusBar.showMessage("Waiting for Desura")
        self.wait_for_desura()
        gamelist = self.get_current_list()
        if gamelist[1] == 1:
            for item in gamelist[0].selectedItems():
                game = item.data(Qt.UserRole)
                self.logger.info(' '.join(["Installing", game.name]))
                self.statusBar.showMessage(' '.join(["Installing", game.name]))
                game.install()

    def uninstall_game(self):
        self.statusBar.showMessage("Waiting for Desura")
        self.wait_for_desura()
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
        self.statusBar.showMessage("Waiting for Desura")
        self.wait_for_desura()
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
                if not steamutils.shortcut_exists(self.get_steam_manager(), game.name):
                    steamutils.insert_shortcut(self.get_steam_manager(), game.name, game.exe, icons.choose_icon(game))
                    self.statusBar.showMessage("Added {0} to the Steam library".format(game.name))
                else:
                    self.statusBar.showMessage("{0} already exists in the Steam library".format(game.name))

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
                self.logger.info("Closing Steam")
                self.statusBar.showMessage("Closing Steam")
                windows.close_steam()
                return True
            else:
                self.logger.error("Could not add game to Steam - Steam still running")
                self.statusBar.showMessage("Add to Steam cancelled")
                return False
        else:
            return True

    @classmethod
    def start_desura(cls):
        try:
            windows.start_desura()
        except WindowsError:
            error_message("Desura has not been installed or is not installed correctly. <br />"
                            "Please install Desura before using DesuraTools").exec_()
            webbrowser.open("http://www.desura.com/install", 2)
        except Exception, e:
            error_message("Error occured when launching Desura <br /> {0}".format(e.message))

    def wait_for_desura(self, username=None):
        if username is None:
            username = self.desuraAccountName_input.text()
        if not windows.desura_running(username):
            self.start_desura()
            while not windows.desura_running(username):
                self.app.processEvents()

    def generate_report(self):
        self.logger.info("Generating Report")
        self.statusBar.showMessage("Generating Report")
        username = self.desuraAccountName_input.text()
        webbrowser.open(str(DesuraReport(username)))

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

class ProgressBarDialog(QDialog, Ui_ProgressBar):
    def __init__(self, parent=None):
        super(ProgressBarDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.iconLabel.setPixmap(QStyle.standardPixmap(self.style(), QStyle.SP_MessageBoxInformation))

    def setText(self, text):
        self.textLabel.setText(text)

    def setInformativeText(self, text):
        self.infoTextLabel.setText(text)

    def setMaximum(self, maximum):
        self.progressBar.setMaximum(maximum)

    def setAccount(self, account, adverb='by'):
        self.accountLabel.setText("{0} account {1}".format(adverb, account))

    def increment(self, increment):
        value = self.progressBar.value()
        self.progressBar.setValue(value+increment)


def get_logger(name, fh):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(fh)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def error_message(text):
    errorbox = QMessageBox()
    errorbox.setWindowIcon(QPixmap("../icons/desuratools_256.png"))
    errorbox.setWindowTitle("Error")
    errorbox.setText(text)
    errorbox.setIcon(QMessageBox.Critical)
    return errorbox


def user_choice(text, windowtitle, icon, acceptbutton="OK"):
    choice_dialog = QMessageBox()
    choice_dialog.setWindowIcon(QPixmap("../icons/desuratools_256.png"))
    choice_dialog.setText(text)
    choice_dialog.setIcon(icon)
    choice_dialog.setStandardButtons(QMessageBox.Cancel)
    choice_dialog.setWindowTitle(windowtitle)
    choice_dialog.addButton(acceptbutton, QMessageBox.AcceptRole)
    return choice_dialog

def run():
    app = QApplication(sys.argv)
    try:
        frame = MainWindow(app)
        frame.show()
        app.exec_()
    except (socket.gaierror, httplib.BadStatusLine):
        error_message("An internet connection is required to use DesuraTools").exec_()
    except Exception, e:
        error_message("An error occured when starting DesuraTools<br /><i>{0}</i>".format(e.message)).exec_()

if __name__ == '__main__':
    run()
