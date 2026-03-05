import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, POWER_UP_CHANCE
from logger import log_event
from power_up import Power_Up


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self, player):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            player.add_kill_count()
            return 0
        else:
            log_event("asteroid_split")
            a_velocity = self.velocity.rotate(random.uniform(20, 50))
            b_velocity = self.velocity.rotate(random.uniform(-20, -50))
            radius = self.radius - ASTEROID_MIN_RADIUS
            x, y = self.position
            a = Asteroid(x, y, radius)
            b = Asteroid(x, y, radius)
            a.velocity = a_velocity * random.uniform(1, 1.5)
            b.velocity = b_velocity * random.uniform(1, 1.5)
            self.spawn_power_up()

    def spawn_power_up(self):
        if random.uniform(0, 1) <= POWER_UP_CHANCE:
            x, y = self.position
            power_up = Power_Up(x, y, 15)
            power_up.velocity = self.velocity * random.uniform(0.2, 0.8)

    def draw(self, surface):
        pygame.draw.circle(
            surface, "blue", self.position, self.radius, width=LINE_WIDTH
        )

    def update(self, dt):
        self.position += self.velocity * dt
        x, y = self.position
        if x > 2500 or y > 2500:
            self.kill()
