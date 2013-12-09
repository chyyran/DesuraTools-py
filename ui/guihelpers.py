#coding=utf-8
import logging
import webbrowser

from PySide.QtCore import QThread, Qt, Signal
from PySide.QtGui import QDialog, QStyle, QMessageBox, QPixmap
from ui.ui_progressbar import Ui_ProgressBar
import windows

__author__ = 'ron975'


class DesuraWaiter(QThread):
    def __init__(self, username, parent = None):
        super(DesuraWaiter, self).__init__(parent)
        self.username = username

    def run(self):
        if len(self.username) == 0:
            return
        if not windows.desura_running(self.username):
            start_desura()
            while not windows.desura_running(self.username):
                self.msleep(100)
            return
        return

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

    def increment(self, increment, game):
        value = self.progressBar.value()
        self.progressBar.setValue(value+increment)
        self.currentGame.setText(game)


def user_choice(text, windowtitle, icon, acceptbutton="OK"):
    choice_dialog = QMessageBox()
    choice_dialog.setWindowIcon(QPixmap("../icons/desuratools_256.png"))
    choice_dialog.setText(text)
    choice_dialog.setIcon(icon)
    choice_dialog.setStandardButtons(QMessageBox.Cancel)
    choice_dialog.setWindowTitle(windowtitle)
    choice_dialog.addButton(acceptbutton, QMessageBox.AcceptRole)
    return choice_dialog


def error_message(text):
    errorbox = QMessageBox()
    errorbox.setWindowIcon(QPixmap("../icons/desuratools_256.png"))
    errorbox.setWindowTitle("Error")
    errorbox.setText(text)
    errorbox.setIcon(QMessageBox.Critical)
    return errorbox


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


def start_desura():
    try:
        windows.start_desura()
    except WindowsError:
        error_message("Desura has not been installed or is not installed correctly. <br />"
                        "Please install Desura before using DesuraTools").exec_()
        webbrowser.open("http://www.desura.com/install", 2)
    except Exception, e:
        error_message("Error occured when launching Desura <br /> {0}".format(e.message))