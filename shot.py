import pygame

from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius / 2)

    def update(self, dt):
        self.position += self.velocity * dt
