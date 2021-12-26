# Builtin
import random
from typing import Optional, Any
# Pip
import pygame
import pygame.freetype
import pygame_widgets
from pygame_widgets.button import Button


class Game:
    """Manages the game and updates the display."""
    def __init__(self) -> None:
        self.running: bool = False
        self.display: Optional[pygame.Surface] = None
        self.rect: Optional[pygame.Rect] = None
        self.player: Optional[Player] = None
        self.presents: pygame.sprite.Group = pygame.sprite.Group()
        self.rockets: pygame.sprite.Group = pygame.sprite.Group()
        self.allSprites: pygame.sprite.Group = pygame.sprite.Group()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.last: int = pygame.time.get_ticks()
        self.score: int = 0
        self.background: Optional[pygame.Surface] = None

    def doInitialisation(self) -> None:
        """Initialises pygame modules and sets up the game."""
        pygame.init()
        self.running = True
        self.display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.rect = self.display.get_rect()
        self.background = pygame.image.load("Images/background.png").convert()

    def startLoop(self) -> None:
        """Calls the initialisation and starts the game loop."""
        # Initialise pygame
        self.doInitialisation()
        self.running = True
        self.player = Player(self)
        self.player.rect.center = (self.display.get_width()/2, self.display.get_height()-100)
        self.allSprites.add(self.player)
        # Start the game loop
        while self.running:
            # Run core functionality
            self.checkEntityInsideRect()
            now = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.last >= 1000:
                # 1 second has passed so spawn enemy
                self.spawnEnemy()
                self.last = now
            self.eventListener()
            self.checkCollisions()
            self.updateBackground()
            self.updateUI()
            self.updateEntities()
            self.clock.tick(30)
            pygame.display.update()
        # Create exit menu
        while True:
            self.display.fill((0, 0, 0))
            font = pygame.font.SysFont("comicsansms", 70)
            endingText = font.render(f"Game Over! Score: {self.score}", True, (255, 255, 255))
            self.display.blit(endingText, (self.display.get_width()/2-300, self.display.get_height()/2-100))
            button = Button(self.display, int(self.display.get_width()/2-200), int(self.display.get_height()/2), 500, 150, text="Click To Exit", font=font, margin=20, onClick=lambda: self.exit())
            try:
                pygame_widgets.update(pygame.event.get())
                pygame.display.flip()
            except pygame.error:
                # This is thrown when the button is clicked so ignore it
                break

    def spawnEnemy(self) -> None:
        """Spawns an enemy at a random position at the top."""
        present = Present(self)
        possiblePos = (random.randint(50, self.display.get_width() - 150), 25)
        present.rect.x, present.rect.y = possiblePos
        self.presents.add(present)
        self.allSprites.add(present)

    def updateEntities(self) -> None:
        """Renders all entities and updates the display."""
        self.allSprites.update(pygame.key.get_pressed())
        self.allSprites.draw(self.display)

    def eventListener(self) -> None:
        """Listens and responds to events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rocket = Rocket(self)
                    rocket.rect.center = self.player.rect.midtop
                    self.rockets.add(rocket)
                    self.allSprites.add(rocket)

    def checkCollisions(self) -> None:
        """Checks for collisions against presents from rockets."""
        for _ in pygame.sprite.groupcollide(self.presents, self.rockets, True, True).keys():
            self.score += 1
        for _ in pygame.sprite.groupcollide(pygame.sprite.Group(self.player), self.presents, True, True).keys():
            self.running = False

    def checkEntityInsideRect(self) -> None:
        """Checks if an entity (present or rocket) is inside the screen."""
        for entity in self.allSprites.sprites():
            if entity.rect.y < 0 or entity.rect.y > self.display.get_height():
                # Entity is not longer on the screen
                entity.kill()

    def updateBackground(self) -> None:
        """Updates the background."""
        self.display.blit(self.background, (0, 0))

    def updateUI(self) -> None:
        """Updates the score displayed to the user and the background."""
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.display.blit(text, (0, 0))

    @staticmethod
    def exit() -> None:
        """Exits and cleanups the game."""
        pygame.quit()


class Present(pygame.sprite.Sprite):
    def __init__(self, gameTemp: Game) -> None:
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
    def __init__(self, gameTemp: Game) -> None:
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
    def __init__(self, gameTemp: Game) -> None:
        """Initialises a Rocket object."""
        pygame.sprite.Sprite.__init__(self)
        self.game: Game = game
        self.speed: int = 15
        self.image: pygame.Surface = pygame.transform.scale(pygame.image.load("Images/rocket.png").convert(), (15, 45))
        self.rect: pygame.Rect = self.image.get_rect()

    def update(self, keys, *args) -> None:
        """Updates the Rocket object on the display."""
        self.rect.y -= self.speed


# Runs the game
if __name__ == "__main__":
    game = Game()
    game.startLoop()
