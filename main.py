import pygame

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # SPRITES
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # SPRITE GROUPS
    updatables = pygame.sprite.Group()
    updatables.add(player)
    drawables = pygame.sprite.Group()
    drawables.add(player)

    # GAME LOOP
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        dt = clock.tick(FPS) / 1000

        updatables.update(dt)
        for i in drawables:
            i.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
