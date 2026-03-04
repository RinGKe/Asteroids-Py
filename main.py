import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # SPRITE GROUPS
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    # GAME LOOP
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        dt = clock.tick(FPS) / 1000

        updatable.update(dt)
        for i in drawable:
            i.draw(screen)
        for a in asteroids:
            if a.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    a.split()
                    s.kill()

        pygame.display.flip()


if __name__ == "__main__":
    main()
