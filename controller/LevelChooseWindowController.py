import os

from ui.LevelChooseWindowUI import Ui_LevelChooseWindow as LevelChooseWindowUI

from controller.GameInfoDialogController import GameInfoDialogController as GameInfoDialog
from controller.GamefieldWindowController import GamefieldWindowController as GamefieldWindow

from PyQt5.QtWidgets import QMainWindow


class LevelChooseWindowController(QMainWindow, LevelChooseWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.HelpButton.clicked.connect(lambda: GameInfoDialog(self).show())
        self.StartButton.clicked.connect(self.start_level)

        levels = [level_name.replace(".txt", "") for level_name in os.listdir("levels") if level_name != "guide.txt"]
        self.comboBoxLevel.addItems(levels)

    def start_level(self):
        with open("levels/" + self.comboBoxLevel.currentText() + ".txt") as f:
            level = f.read()
        gamefield_window = GamefieldWindow(self, level)
        self.hide()
        gamefield_window.show()
