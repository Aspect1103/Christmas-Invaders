# Builtin
from typing import List, Optional
# Pip
import pygame
# Custom
from enemy import Enemy


class Game:
    """Manages the game and updates the display."""
    def __init__(self) -> None:
        self._running: bool = False
        self._width: int = 1280
        self._height: int = 720
        self._displaySurface: Optional[pygame.Surface] = None
        self._enemies: List[Enemy] = []

    def doInitialisation(self) -> None:
        """Initialises pygame modules and sets up the game."""
        pygame.init()
        self._running = True
        self._displaySurface = pygame.display.set_mode(size=(self._width, self._height), flags=pygame.RESIZABLE)

    @staticmethod
    def doCleanup() -> None:
        """Cleans up pygame and its modules."""
        pygame.quit()

    def startLoop(self) -> None:
        """Calls the initialisation and starts the game loop."""
        # Initialise pygame
        self.doInitialisation()
        self._running = True
        # Start the game loop
        while self._running:
            self.spawnEnemies()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            # Wait a second to slow down enemy generation
            pygame.time.wait(1000)
            # Update the display
            pygame.display.update()
        # Cleanup the game
        self.doCleanup()

    def spawnEnemies(self) -> None:
        """Spawns an enemy and stores it."""
        self._enemies.append(Enemy(self, 300, 100))


# Runs the game
if __name__ == "__main__":
    game = Game()
    game.startLoop()
