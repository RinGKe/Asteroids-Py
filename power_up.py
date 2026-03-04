import pygame

from circleshape import CircleShape


class Power_Up(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0

    def triangle(self):
        radius = float(self.radius)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        back_a = pygame.Vector2(0, 1).rotate(self.rotation + 60) * radius / 1
        back_b = pygame.Vector2(0, 1).rotate(self.rotation - 60) * radius / 1
        a = self.position + forward * radius
        b = self.position - forward * radius * 1 + back_a
        c = self.position - forward * radius * 1 + back_b
        return [a, b, c]

    def draw(self, surface):
        pygame.draw.polygon(surface, "gold", self.triangle())

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += dt * 666
        if self.rotation % 360 == 0:
            self.rotation = 0
