from pydoc import text

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import FONT_SIZE, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from power_shield import Power_Shield
from power_up import Power_Up
from shield_pulse import Shield_Pulse
from shot import Shot


def screen_text(player, screen, font, font_i):
    if player.dead:
        text_to_render(font, screen, "GAME OVER!", 0, 0)
        text_to_render(font, screen, f"YOU SCORED: {player.kill_counter} POINTS", 0, 50)
        text_to_render(font_i, screen, "Press any key to close", 0, 85)

    text_surface = font.render(f"SCORE: {str(player.kill_counter)}", True, "white")
    screen.blit(text_surface, (25, SCREEN_HEIGHT - 50))


def text_to_render(font, screen, text, off_w, off_h):
    text_surface = font.render(text, True, "white")
    t_w, t_h = font.size(text)
    screen.blit(
        text_surface,
        (
            SCREEN_WIDTH // 2 - (t_w // 2) + off_w,
            SCREEN_HEIGHT // 2 - (t_h // 2) + off_h,
        ),
    )


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BUBBLE FIGHTER")
    font = pygame.font.SysFont("arial", FONT_SIZE)
    font_i = pygame.font.SysFont("arial", FONT_SIZE // 2)
    font_i.italic = True

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
    Power_Shield.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    # GAME LOOP
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        screen_text(player, screen, font, font_i)

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
                    if hasattr(s, "done"):
                        continue
                    s.kill()

            for p in pulse:
                if p.collides_with(a):
                    a.kill()

        for u in power_ups:
            if u.collides_with(player):
                player.gain_power_up(u.power_type)
                u.kill()
            for p in pulse:
                if p.collides_with(u):
                    u.kill()

        pygame.display.flip()


if __name__ == "__main__":
    main()
