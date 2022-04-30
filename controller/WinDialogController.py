from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ui.WinDialogUI import Ui_WinDialog as WinDialogUI


class WinDialogController(QDialog, WinDialogUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.close_win)

    def close_win(self):
        self.close()
        self.parent().close()
