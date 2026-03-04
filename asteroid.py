import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return "small"
        else:
            log_event("asteroid_split")
            a_velocity = self.velocity.rotate(random.uniform(20, 50))
            b_velocity = -self.velocity.rotate(random.uniform(-20, -50))
            radius = self.radius - ASTEROID_MIN_RADIUS
            x, y = self.position
            a = Asteroid(x, y, radius)
            b = Asteroid(x, y, radius)
            a.velocity = a_velocity * random.uniform(0.8, 1.2)
            b.velocity = b_velocity * random.uniform(0.8, 1.2)

    def draw(self, surface):
        pygame.draw.circle(surface, "red", self.position, self.radius, width=LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
