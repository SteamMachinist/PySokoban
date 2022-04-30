from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ui.GameInfoDialogUI import Ui_GameInfoDialog as GameInfoDialogUI


class GameInfoDialogController(QDialog, GameInfoDialogUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        with open("ui/resources/info.html") as f:
            info = f.read()
        self.textBrowser.setText(info)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(lambda: self.close())
