import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from power_up import Power_Up
from shield_pulse import Shield_Pulse
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
    pulse = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shots)
    Shield_Pulse.containers = (updatable, drawable, pulse)
    Power_Up.containers = (updatable, drawable, power_ups)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

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
                if player.shield:
                    player.destroy_shield()
                    field.add_spawn_multi()
                else:
                    player.death()

            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    a.split(player)
                    s.kill()

            for p in pulse:
                if p.collides_with(a):
                    a.kill()

        for p in power_ups:
            if p.collides_with(player):
                player.gain_power_up()
                p.kill()

        pygame.display.flip()


if __name__ == "__main__":
    main()
