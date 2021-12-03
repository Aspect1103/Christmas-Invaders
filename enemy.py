# Builtin
from typing import TYPE_CHECKING
# Pip
import pygame

if TYPE_CHECKING:
    from game import Game


class Enemy:
    def __init__(self, game, x: float, y: float) -> None:
        self._game: Game = game
        self._x: float = x
        self._y: float = y
        pygame.draw.circle(game._displaySurface, color=pygame.Color(255, 0, 0), center=(self._x, self._y), radius=50)

    def __repr__(self) -> str:
        return f"<Enemy (X Position={self._x}) (Y Position={self._y})>"
