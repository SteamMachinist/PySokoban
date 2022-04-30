from __future__ import annotations

from gamemodel.cell import *


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    DEFAULT = (0, 0)


class Game:
    def __init__(self, level: str):
        self.gamefield, self.sokoban_cell, self.target_cells = self.setup_level(level)
        self.steps_number = 0
        self.steps_list = []

    @staticmethod
    def setup_level(level: str) -> ([], FloorCell, []):
        gamefield = []
        sokoban_cell = None
        target_cells = []
        y = 0
        for line in level.split("\n"):
            x = 0
            gamefield.append([])
            for char in line:
                cell = Game.get_cell_for_char(char, x, y)
                if isinstance(cell, FloorCell):
                    if cell.is_target:
                        target_cells.append(cell)
                    if cell.content == CellContent.SOKOBAN:
                        sokoban_cell = cell
                gamefield[y].append(cell)
                x += 1
            y += 1
        return gamefield, sokoban_cell, target_cells

    @staticmethod
    def get_cell_for_char(char: str, x: int, y: int) -> Cell:
        if char == "0":
            return NoneCell(x, y)
        if char == "#":
            return WallCell(x, y)

        cell = FloorCell(x, y, False, CellContent.EMPTY)
        if char == "%":
            cell.content = CellContent.BOX
        if char == "@":
            cell.is_target = True
        if char == "&":
            cell.is_target = True
            cell.content = CellContent.BOX
        if char == "S":
            cell.content = CellContent.SOKOBAN
        if char == "$":
            cell.is_target = True
            cell.content = CellContent.SOKOBAN
        return cell

    def step(self, direction: Direction) -> bool:
        if self._move_(self.sokoban_cell, direction, True):
            self.steps_number += 1
        return self.check_win()

    def _move_(self, cell: FloorCell, direction: Direction, sokoban_move: bool) -> bool:
        next_cell = self.gamefield[cell.y + direction.value[1]][cell.x + direction.value[0]]
        if isinstance(next_cell, FloorCell):
            if next_cell.content == CellContent.EMPTY:
                self._do_move_(cell, next_cell, sokoban_move)
                return True
            else:
                result = sokoban_move and self._move_(next_cell, direction, False)
                if result:
                    self._do_move_(cell, next_cell, True)
                return result
        else:
            return False

    def _do_move_(self, cell: FloorCell, next_cell: FloorCell, sokoban: bool):
        self.steps_list.append((cell, next_cell, sokoban))
        self._change_content_(cell, next_cell, sokoban)

    def _change_content_(self, cell: FloorCell, next_cell: FloorCell, sokoban: bool):
        next_cell.content = cell.content
        cell.content = CellContent.EMPTY
        if sokoban:
            self.sokoban_cell = next_cell

    def check_win(self) -> bool:
        return all([cell.is_completed() for cell in self.target_cells])

    def back(self):
        if self.steps_number <= 0:
            return
        last_step = self.steps_list.pop()
        self._change_content_(last_step[1], last_step[0], last_step[2])
        if last_step[2] and len(self.steps_list) > 0:
            last_step = self.steps_list[-1]
            if not last_step[2]:
                self.steps_list.pop()
                self._change_content_(last_step[1], last_step[0], last_step[2])
        self.steps_number -= 1
