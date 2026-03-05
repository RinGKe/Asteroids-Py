from this import s

import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, SHIELD_PULSE_SPEED


class Shield_Pulse(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.life_timer = 0

    def draw(self, surface):
        pygame.draw.circle(
            surface, "white", self.position, self.radius, width=LINE_WIDTH
        )

    def update(self, dt):
        self.radius += SHIELD_PULSE_SPEED * dt
        self.life_timer += dt
        if self.life_timer >= 0.6:
            self.kill()
