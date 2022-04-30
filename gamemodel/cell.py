from __future__ import annotations

from enum import Enum


class CellContent(Enum):
    EMPTY = 0
    BOX = 1
    SOKOBAN = 2


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return type(self).__name__ + " " + str(self.x) + " " + str(self.y)


class WallCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class NoneCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class FloorCell(Cell):
    def __init__(self, x: int, y: int, is_target: bool, content: CellContent):
        super().__init__(x, y)
        self.is_target = is_target
        self.content = content

    def __str__(self):
        return super().__str__() + " " + str(self.is_target) + " " + str(self.content)

    def is_completed(self) -> bool | None:
        if not self.is_target:
            return None
        else:
            return self.content == CellContent.BOX


class CellToChar(Enum):
    pass
