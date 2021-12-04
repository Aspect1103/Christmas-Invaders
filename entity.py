# Builtin
from typing import TYPE_CHECKING, Any
# Pip
import pygame

if TYPE_CHECKING:
    from game import Game


class Present(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        """Initialises a Present object."""
        pygame.sprite.Sprite.__init__(self)
        self.game: Game = game
        self.speed: int = 2
        self.image: pygame.Surface = pygame.transform.scale(pygame.image.load("Images/present.png").convert(), (96, 134))
        self.rect: pygame.Rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Updates the Present object on the display."""
        self.rect.y += self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        """Initialises a Player object."""
        pygame.sprite.Sprite.__init__(self)
        self.game: Game = game
        self.speed: int = 10
        self.image: pygame.Surface = pygame.transform.scale(pygame.image.load("Images/tree.png").convert(), (92, 160))
        self.rect: pygame.Rect = self.image.get_rect()

    def update(self, keys, *args) -> None:
        """Updates the Player object on the display."""
        if keys[pygame.K_LEFT] and self.rect.x > 50:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.x < self.game.display.get_width() - 150:
            self.rect.x += self.speed


class Rocket(pygame.sprite.Sprite):
    def __init__(self, game) -> None:
        """Initialises a Rocket object."""
        pygame.sprite.Sprite.__init__(self)
        self.game: Game = game
        self.speed: int = 15
        self.image: pygame.Surface = pygame.transform.scale(pygame.image.load("Images/rocket.png").convert(), (15, 45))
        self.rect: pygame.Rect = self.image.get_rect()

    def update(self, keys, *args) -> None:
        """Updates the Rocket object on the display."""
        self.rect.y -= self.speed
