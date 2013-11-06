#coding=utf-8
__author__ = 'ron975'
__version__ = '1.0'
import sys
import webbrowser
import urllib

import PySide
from PySide.QtGui import QMainWindow, QApplication, QListWidgetItem, QAbstractItemView, QPixmap
from PySide.QtCore import Qt, QSize
import icons
import steammanager
import installedgames
import gameslist
import thread

from testui.generatehtml import TestReport
from qtui.ui_mainform import Ui_MainWindow
from steam import steam_user_manager

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = app
        self.setupUi(self)

        self.desuraAccountName_verify.clicked.connect(self.populate_owned_games)
        self.installButton.clicked.connect(self.process_install_button)
        self.generateDesuraReport_action.activated.connect(self.generate_report)
        self.tabWidget.currentChanged.connect(self.swap_install_button)

        self.addToSteam_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.installGames_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.steamID_input.addItems(steammanager.get_customurls_on_machine())
        self.installGames_list.addItem("Verify your Desura Account Name to see your owned games")

        for game in installedgames.get_games():
            self.populate_qlistwidget(game, self.addToSteam_list)

    def populate_qlistwidget(self, game, qlistwidget, iconurls=False):
        if iconurls:
            img_data = urllib.urlopen(game.icon).read()
            itemicon = QPixmap()
            itemicon.loadFromData(img_data)
            self.app.processEvents()
        else:
            itemicon = QPixmap(game.icon)
        item = QListWidgetItem(itemicon, game.name, qlistwidget)
        item.setData(Qt.UserRole, game)
        qlistwidget.addItem(item)

    def generate_report(self):
        username = self.desuraAccountName_input.text()
        webbrowser.open(str(TestReport(username)))

    def get_steam_folder(self):
        customurl = self.steamID_input.currentText()
        print steam_user_manager.userdata_directory_for_name(customurl)

    def populate_owned_games(self):
        username = self.desuraAccountName_input.text()
        self.installGames_list.clear()
        for game in gameslist.GamesList(username).get_games():
            self.populate_qlistwidget(game, self.installGames_list, True)

    def swap_install_button(self):
        if self.tabWidget.currentIndex() == 0:
            self.installButton.setText("Install")
        if self.tabWidget.currentIndex() == 1:
            self.installButton.setText("Add to Steam")

    def process_install_button(self):
        if self.tabWidget.currentIndex() == 0:
            for item in self.installGames_list.selectedItems():
                game = item.data(Qt.UserRole)
                game.install()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow(app)
    frame.show()
    app.exec_()