import os

from PyQt5 import QtSvg, QtCore
from PyQt5.QtCore import QTimer, QTime, QModelIndex, QRectF
from PyQt5.QtGui import QPainter, QStandardItemModel, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QHeaderView, QStyleOptionViewItem

from controller.GameInfoDialogController import GameInfoDialogController as GameInfoDialog
from controller.WinDialogController import WinDialogController as WinDialog
from gamemodel.game import *
from ui.GamefieldWindowUI import Ui_GamefieldWindow as GamefieldWindowUI


class GamefieldWindowController(QMainWindow, GamefieldWindowUI):
    def __init__(self, parent, level: str):
        super().__init__(parent)
        self.setupUi(self)
        self.level = level

        self.tableGamefield.mousePressEvent = lambda x: None

        images_dir = os.path.join("ui/resources/", 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self.closeEvent = self.close_and_show_parent
        self.actionChoose_level.triggered.connect(self.closeEvent)
        self.actionHelp.triggered.connect(lambda: GameInfoDialog(self).show())
        self.game = Game(level)
        self.actionBack.triggered.connect(self.back_action)
        self.backButton.clicked.connect(self.actionBack.trigger)
        self.actionReset_level.triggered.connect(self.reset_action)
        self.resetButton.clicked.connect(self.actionReset_level.trigger)

        self.textTime.setFontPointSize(11)
        self.textSteps.setFontPointSize(11)

        self.level_time = None
        self.timer = None
        self.setup_timer()

        self.setup_gamefield()
        self.game_resize(self.game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.tableGamefield.setItemDelegate(MyDelegate(self))
        self.update_view()

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(len(game.gamefield), len(game.gamefield[0]))
        self.tableGamefield.setModel(model)
        self.update_view()

    def update_view(self):
        self.tableGamefield.viewport().update()
        self.textSteps.setText(str(self.game.steps_number))

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        cell = self.game.gamefield[e.row()][e.column()]
        img = None
        if isinstance(cell, NoneCell):
            img = self._images['i7']
        if isinstance(cell, WallCell):
            img = self._images['i2']
        if isinstance(cell, FloorCell):
            if cell.content == CellContent.EMPTY:
                if cell.is_target:
                    img = self._images['i1']
                else:
                    img = self._images['i0']

            if cell.content == CellContent.BOX:
                if cell.is_target:
                    img = self._images['i4']
                else:
                    img = self._images['i3']

            if cell.content == CellContent.SOKOBAN:
                if cell.is_target:
                    img = self._images['i6']
                else:
                    img = self._images['i5']
        img.render(painter, QRectF(option.rect))

    def setup_gamefield(self):
        self.tableGamefield.horizontalHeader().setVisible(False)
        self.tableGamefield.horizontalHeader().setCascadingSectionResizes(False)
        self.tableGamefield.horizontalHeader().setDefaultSectionSize(50)
        self.tableGamefield.verticalHeader().setVisible(False)
        self.tableGamefield.verticalHeader().setCascadingSectionResizes(False)
        self.tableGamefield.verticalHeader().setDefaultSectionSize(50)
        self.tableGamefield.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableGamefield.horizontalHeader().setMinimumSectionSize(24)
        self.tableGamefield.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableGamefield.setFocusPolicy(QtCore.Qt.NoFocus)

        #self.tableGamefield.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def keyPressEvent(self, event):
        direction = Direction.DEFAULT
        if event.key() == QtCore.Qt.Key_W:
            direction = Direction.UP
        elif event.key() == QtCore.Qt.Key_A:
            direction = Direction.LEFT
        elif event.key() == QtCore.Qt.Key_S:
            direction = Direction.DOWN
        elif event.key() == QtCore.Qt.Key_D:
            direction = Direction.RIGHT
        if self.game.step(direction):
            WinDialog(self).show()
        self.update_view()
        event.accept()

    def setup_timer(self):
        self.level_time = QTime(00, 00)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_text)
        self.timer.start(1000)

    def update_time_text(self):
        self.level_time = self.level_time.addSecs(1)
        self.textTime.setText(self.level_time.toString("hh:ss"))

    def close_and_show_parent(self, qce: QCloseEvent):
        self.close()
        self.parent().show()

    def back_action(self):
        self.game.back()
        self.update_view()

    def reset_action(self):
        self.game = Game(self.level)
        self.setup_timer()
        self.update_view()
