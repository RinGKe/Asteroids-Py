from this import s

import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH


class Power_Shield(CircleShape):
    def __init__(self, x, y, radius, player):
        super().__init__(x, y, (radius * 2))
        self.done = False
        self.life_timer = 0
        self.player_ref = player

    def draw(self, surface):
        pygame.draw.circle(
            surface, "purple", self.position, self.radius, width=LINE_WIDTH
        )

    def update(self, dt):
        self.position = self.player_ref.position
        if self.done:
            self.radius += 1500 * dt
            self.life_timer += dt
            if self.life_timer >= 0.2:
                self.kill()
